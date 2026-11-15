"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

Git / Mercurial working-copy state for the tree explorer.

Three layers, each usable without the ones above it:

* pure functions -- ``find_repo``, ``read_branch`` and the two status parsers
  work on paths and bytes only, so they are testable without Qt or a repo;
* ``StatusSnapshot`` -- the parsed answer, queried per path;
* ``VcsStatusProvider`` -- runs the (slow, ~250 ms) status command on a worker
  thread, caches the result and tells the GUI when it changes.

The repository root and the branch are found by reading the filesystem, never
by spawning a process.
"""

import dataclasses
import enum
import html
import os
import shutil
import subprocess
import threading
import time
from typing import Any, Callable

import qt


class VcsState(enum.Enum):
    """File states, declared in priority order (a directory shows the first)."""

    CONFLICT = "U"
    MODIFIED = "M"
    ADDED = "A"
    DELETED = "D"
    UNTRACKED = "?"
    IGNORED = "I"

    @property
    def letter(self) -> str:
        return str(self.value)

    @property
    def priority(self) -> int:
        return list(VcsState).index(self)


# Colours used when the theme has no "vcscolors" block.
DEFAULT_COLORS: dict[str, str] = {
    "conflict": "#cc0000",
    "modified": "#c4a000",
    "added": "#4e9a06",
    "deleted": "#a40000",
    "untracked": "#3465a4",
    "ignored": "#888a85",
}

STATUS_TIMEOUT_S: float = 10.0
METADATA_DEBOUNCE_MS: int = 300
# hg rewrites .hg/dirstate while it answers a status query; ignore the echo.
SELF_EVENT_QUIET_S: float = 0.5
# Most subdirectories checked for ignored files in one hg query.
MAX_HG_SUBDIRS: int = 200
# How often a visible explorer compares its directory's fingerprint, and the
# most files that fingerprint looks at.
POLL_INTERVAL_MS: int = 3000
MAX_FINGERPRINT_ENTRIES: int = 5000


def path_key(path: str) -> str:
    """A comparable form of *path* (case and separators normalised)."""
    return os.path.normcase(os.path.normpath(path))


@dataclasses.dataclass(frozen=True)
class RepoInfo:
    kind: str  # "git" or "hg"
    root: str
    meta_dir: str  # the directory holding HEAD/index or branch/dirstate


def _git_meta_dir(root: str, dot_git: str) -> str | None:
    """The real git directory: *dot_git* itself, or its ``gitdir:`` target."""
    if os.path.isdir(dot_git):
        return dot_git
    try:
        with open(dot_git, "r", encoding="utf-8", errors="replace") as handle:
            first: str = handle.readline().strip()
    except OSError:
        return None
    if not first.startswith("gitdir:"):
        return None
    target: str = first[len("gitdir:") :].strip()
    if not os.path.isabs(target):
        target = os.path.join(root, target)
    target = os.path.normpath(target)
    return target if os.path.isdir(target) else None


def find_repo(path: str) -> RepoInfo | None:
    """The nearest enclosing repository of *path*, or None. No subprocess.

    Deliberately uncached: it is a handful of stat calls, and a cached
    'not a repository' would outlive a later `git init`.
    """
    start: str = os.path.abspath(path)
    found: RepoInfo | None = None
    current: str = start
    while True:
        dot_git: str = os.path.join(current, ".git")
        if os.path.exists(dot_git):
            meta: str | None = _git_meta_dir(current, dot_git)
            if meta is not None:
                found = RepoInfo("git", current, meta)
                break
        dot_hg: str = os.path.join(current, ".hg")
        if os.path.isdir(dot_hg):
            found = RepoInfo("hg", current, dot_hg)
            break
        parent: str = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return found


def _read_first_line(path: str) -> str | None:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.readline().strip()
    except OSError:
        return None


def directory_fingerprint(
    directory: str, skip: Callable[[str], bool] | None = None
) -> int:
    """A cheap digest of the files directly in *directory* (name, mtime, size).

    It changes when a file there is edited, added or removed by *anyone*, which
    is what lets a poll notice an edit by another program without spawning a
    status process: `scandir` already carries each entry's stat. Directories
    are not looked into (an in-place edit does not touch a directory's mtime,
    so reading one would cost a scan per subdirectory and still see nothing),
    and *skip* lets the caller leave out files that do not matter -- the
    ignored ones, which a build may rewrite constantly. 0 when unreadable.
    """
    entries: list[tuple[str, int, int]] = []
    try:
        with os.scandir(directory) as scan:
            for entry in scan:
                if len(entries) >= MAX_FINGERPRINT_ENTRIES:
                    break
                try:
                    if entry.is_dir(follow_symlinks=False):
                        continue
                    if skip is not None and skip(entry.path):
                        continue
                    info: os.stat_result = entry.stat(follow_symlinks=False)
                except OSError:
                    continue
                entries.append((entry.name, info.st_mtime_ns, info.st_size))
    except OSError:
        return 0
    entries.sort()
    return hash(tuple(entries))


def read_branch(repo: RepoInfo) -> str:
    """The branch label of *repo*, read from the metadata files."""
    if repo.kind == "git":
        head: str | None = _read_first_line(os.path.join(repo.meta_dir, "HEAD"))
        if not head:
            return "?"
        if head.startswith("ref:"):
            ref: str = head[4:].strip()
            prefix: str = "refs/heads/"
            return ref[len(prefix) :] if ref.startswith(prefix) else ref
        return head[:8]  # detached HEAD: a short SHA
    branch: str = _read_first_line(os.path.join(repo.meta_dir, "branch")) or "default"
    bookmark: str | None = _read_first_line(
        os.path.join(repo.meta_dir, "bookmarks.current")
    )
    return f"{branch} @{bookmark}" if bookmark else branch


# --- parsers ----------------------------------------------------------------

_GIT_CONFLICTS: frozenset[str] = frozenset({"DD", "AU", "UD", "UA", "DU", "AA", "UU"})


def _git_state(code: str) -> VcsState:
    if code == "??":
        return VcsState.UNTRACKED
    if code == "!!":
        return VcsState.IGNORED
    if code in _GIT_CONFLICTS:
        return VcsState.CONFLICT
    if code[0] == "A":
        return VcsState.ADDED
    if "D" in code:
        return VcsState.DELETED
    return VcsState.MODIFIED  # M, T, R, C in either column


@dataclasses.dataclass(frozen=True)
class Tracking:
    """A git branch's upstream and how far the two have diverged."""

    upstream: str | None = None
    ahead: int = 0
    behind: int = 0
    gone: bool = False  # the upstream branch no longer exists

    def describe(self) -> str:
        """e.g. 'origin/main (ahead 2, behind 1)'; '' without an upstream."""
        if self.upstream is None:
            return ""
        if self.gone:
            return f"{self.upstream} (gone)"
        if not self.ahead and not self.behind:
            return f"{self.upstream} (up to date)"
        parts: list[str] = []
        if self.ahead:
            parts.append(f"ahead {self.ahead}")
        if self.behind:
            parts.append(f"behind {self.behind}")
        return f"{self.upstream} ({', '.join(parts)})"


def parse_git_tracking(output: bytes) -> Tracking | None:
    """Parse the '## main...origin/main [ahead 1, behind 2]' line of
    ``git status --branch -z`` (its first field), or None if it is missing."""
    first: str = output.decode("utf-8", errors="replace").split("\0", 1)[0]
    if not first.startswith("## "):
        return None
    line: str = first[3:]
    if "..." not in line:
        return Tracking()  # no upstream, an unborn branch, or a detached HEAD
    upstream, _, rest = line.partition("...")
    counts: str = ""
    if " [" in rest:
        rest, _, counts = rest.partition(" [")
        counts = counts.rstrip("]")
    upstream = rest or upstream
    if counts == "gone":
        return Tracking(upstream, gone=True)
    ahead: int = 0
    behind: int = 0
    for part in counts.split(","):
        words: list[str] = part.split()
        if len(words) == 2 and words[1].isdigit():
            if words[0] == "ahead":
                ahead = int(words[1])
            elif words[0] == "behind":
                behind = int(words[1])
    return Tracking(upstream, ahead, behind)


def parse_git_status(output: bytes) -> dict[str, VcsState]:
    """Parse ``git status --porcelain=v1 -z`` into {relative path: state}.

    A rename or copy entry is followed by a second NUL-separated field (the
    original path) that is not an entry of its own and must be skipped.
    A path ending in '/' is a whole untracked or ignored directory.
    """
    result: dict[str, VcsState] = {}
    fields: list[str] = output.decode("utf-8", errors="replace").split("\0")
    index: int = 0
    while index < len(fields):
        entry: str = fields[index]
        index += 1
        if len(entry) < 4 or entry.startswith("## "):
            continue  # too short, or the `--branch` header line
        code: str = entry[:2]
        if code[0] in "RC" or code[1] in "RC":
            index += 1
        result[entry[3:]] = _git_state(code)
    return result


_HG_LETTERS: dict[str, VcsState] = {
    "M": VcsState.MODIFIED,
    "A": VcsState.ADDED,
    "R": VcsState.DELETED,
    "!": VcsState.DELETED,
    "?": VcsState.UNTRACKED,
    "I": VcsState.IGNORED,
}


def parse_hg_status(output: bytes) -> dict[str, VcsState]:
    """Parse ``hg status -0`` ('<letter> <path>' NUL-terminated entries)."""
    result: dict[str, VcsState] = {}
    for entry in output.decode("utf-8", errors="replace").split("\0"):
        if len(entry) < 3 or entry[1] != " ":
            continue
        state: VcsState | None = _HG_LETTERS.get(entry[0])
        if state is not None:
            # hg prints the native separator; the rest of the module uses "/"
            path: str = entry[2:]
            result[path.replace(os.sep, "/") if os.sep == "\\" else path] = state
    return result


def parse_hg_resolve(output: bytes) -> dict[str, VcsState]:
    """Parse ``hg resolve -l``: unresolved ('U ') files are conflicts."""
    result: dict[str, VcsState] = {}
    for line in output.decode("utf-8", errors="replace").splitlines():
        if line.startswith("U "):
            result[line[2:]] = VcsState.CONFLICT
    return result


# --- current commit ---------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class HeadInfo:
    """The checked-out commit, for the repository row's tooltip."""

    commit: str
    author: str
    date: str
    subject: str
    tags: tuple[str, ...] = ()
    phase: str = ""  # hg only: public / draft / secret

    @property
    def short(self) -> str:
        return self.commit[:8]


def _git_common_dir(meta_dir: str) -> str:
    """Where a worktree keeps its refs (its own gitdir holds only HEAD)."""
    pointer: str | None = _read_first_line(os.path.join(meta_dir, "commondir"))
    if not pointer:
        return meta_dir
    return os.path.normpath(os.path.join(meta_dir, pointer))


def read_head_id(repo: RepoInfo) -> str | None:
    """The checked-out commit id, read from the metadata files (no process).

    git: HEAD itself, or the loose ref / `packed-refs` line it points at.
    hg: the first parent in `.hg/dirstate` (its first 20 bytes). None for a
    repository without commits.
    """
    if repo.kind == "hg":
        try:
            with open(os.path.join(repo.meta_dir, "dirstate"), "rb") as handle:
                node: bytes = handle.read(20)
        except OSError:
            return None
        if len(node) != 20 or node == b"\0" * 20:
            return None
        return node.hex()
    head: str | None = _read_first_line(os.path.join(repo.meta_dir, "HEAD"))
    if not head:
        return None
    if not head.startswith("ref:"):
        return head
    ref: str = head[4:].strip()
    common: str = _git_common_dir(repo.meta_dir)
    loose: str | None = _read_first_line(os.path.join(common, *ref.split("/")))
    if loose:
        return loose
    try:
        with open(os.path.join(common, "packed-refs"), "r", encoding="utf-8") as handle:
            for line in handle:
                parts: list[str] = line.split()
                if len(parts) == 2 and parts[1] == ref:
                    return parts[0]
    except OSError:
        pass
    return None


def parse_head_info(output: bytes, kind: str = "git") -> HeadInfo | None:
    """Parse the NUL-separated log output of the checked-out commit.

    Fields: commit, author, date, subject, then the refs of the commit. git
    sends its `%D` decoration ('HEAD -> main, tag: v1, origin/main', of which
    only the 'tag: ' entries are tags); hg sends its space-separated tags (minus
    the moving 'tip') and then the phase.
    """
    fields: list[str] = output.decode("utf-8", errors="replace").strip().split("\0")
    if len(fields) < 4 or not fields[0]:
        return None
    tags: tuple[str, ...] = ()
    phase: str = ""
    if len(fields) > 4:
        if kind == "git":
            tags = tuple(
                part[len("tag: ") :]
                for part in fields[4].split(", ")
                if part.startswith("tag: ")
            )
        else:
            tags = tuple(tag for tag in fields[4].split() if tag != "tip")
    if len(fields) > 5:
        phase = fields[5].strip()
    return HeadInfo(fields[0], fields[1], fields[2], fields[3], tags, phase)


# stamp -> details, so the log process runs once per commit, not per query
_head_cache: dict[str, tuple[str, HeadInfo]] = {}


def _mtime(path: str) -> int:
    try:
        return os.stat(path).st_mtime_ns
    except OSError:
        return 0


def _head_stamp(repo: RepoInfo, commit: str) -> str:
    """What the cached details are valid for: the commit and its tag files.

    Tagging an existing commit changes nothing about its id, so the stamp also
    carries the mtime of the places tags live (git: `packed-refs` and
    `refs/tags`; hg: `localtags`) -- cheap stats, no process.
    """
    if repo.kind == "git":
        common: str = _git_common_dir(repo.meta_dir)
        marks: list[int] = [
            _mtime(os.path.join(common, "packed-refs")),
            _mtime(os.path.join(common, "refs", "tags")),
        ]
    else:
        marks = [_mtime(os.path.join(repo.meta_dir, "localtags"))]
    return commit + "|" + "|".join(str(mark) for mark in marks)


def head_info(repo: RepoInfo) -> HeadInfo | None:
    """The details of the checked-out commit; one `log` process per new commit."""
    commit: str | None = read_head_id(repo)
    if commit is None:
        return None
    key: str = path_key(repo.root)
    stamp: str = _head_stamp(repo, commit)
    cached: tuple[str, HeadInfo] | None = _head_cache.get(key)
    if cached is not None and cached[0] == stamp:
        return cached[1]
    exe: str | None = _executable(repo.kind)
    if exe is None:
        return None
    env: dict[str, str] = dict(os.environ)
    command: list[str]
    if repo.kind == "git":
        command = [
            exe,
            "--no-optional-locks",
            "log",
            "-1",
            "--date=format:%Y-%m-%d %H:%M",
            "--format=%H%x00%an%x00%ad%x00%s%x00%D",
        ]
    else:
        env["HGPLAIN"] = "1"
        env["HGENCODING"] = "utf-8"
        command = [
            exe,
            "log",
            "-r",
            ".",
            "-T",
            "{node}\\0{author|person}\\0{date|isodate}\\0{desc|firstline}"
            "\\0{tags}\\0{phase}",
        ]
    try:
        result = _run(command, repo.root, env)
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    info: HeadInfo | None = parse_head_info(result.stdout, repo.kind)
    if info is not None:
        _head_cache[key] = (stamp, info)
    return info


# --- snapshot ---------------------------------------------------------------


@dataclasses.dataclass
class StatusSnapshot:
    kind: str = ""
    root: str = ""
    branch: str = ""
    files: dict[str, VcsState] = dataclasses.field(default_factory=dict)
    dirs: dict[str, VcsState] = dataclasses.field(default_factory=dict)
    counts: dict[VcsState, int] = dataclasses.field(default_factory=dict)
    error: str | None = None
    head: HeadInfo | None = None
    tracking: Tracking | None = None

    @classmethod
    def build(
        cls,
        repo: RepoInfo,
        branch: str,
        entries: dict[str, VcsState],
        error: str | None = None,
    ) -> "StatusSnapshot":
        """Index *entries* ({root-relative path: state}) by absolute path key."""
        snapshot = cls(kind=repo.kind, root=repo.root, branch=branch, error=error)
        root_key: str = path_key(repo.root)
        for relative, state in entries.items():
            absolute: str = path_key(os.path.join(repo.root, relative))
            snapshot.files[absolute] = state
            snapshot.counts[state] = snapshot.counts.get(state, 0) + 1
            if state == VcsState.IGNORED:
                continue  # an ignored entry never marks its parents
            parent: str = os.path.dirname(absolute)
            while len(parent) >= len(root_key) and parent != os.path.dirname(parent):
                known: VcsState | None = snapshot.dirs.get(parent)
                if known is None or state.priority < known.priority:
                    snapshot.dirs[parent] = state
                if parent == root_key:
                    break
                parent = os.path.dirname(parent)
        return snapshot

    def state_for(self, path: str) -> VcsState | None:
        """The state of a file or directory, or None when it is clean."""
        key: str = path_key(path)
        exact: VcsState | None = self.files.get(key)
        if exact is not None:
            return exact
        # inside a wholly untracked / ignored directory ('?? dir/')
        root_key: str = path_key(self.root)
        parent: str = os.path.dirname(key)
        while len(parent) >= len(root_key) and parent != os.path.dirname(parent):
            inherited: VcsState | None = self.files.get(parent)
            if inherited in (VcsState.UNTRACKED, VcsState.IGNORED):
                return inherited
            if parent == root_key:
                break
            parent = os.path.dirname(parent)
        return self.dirs.get(key)

    def describe_counts(self) -> str:
        """e.g. '2 modified, 1 added, 1 untracked', or 'clean'."""
        parts: list[str] = [
            f"{self.counts[state]} {state.name.lower()}"
            for state in VcsState
            if state != VcsState.IGNORED and self.counts.get(state)
        ]
        return ", ".join(parts) if parts else "clean"

    def _count_parts(self) -> list[str]:
        return [
            f"{self.counts[state]}{state.letter}"
            for state in VcsState
            if state != VcsState.IGNORED and self.counts.get(state)
        ]

    def summary(self) -> str:
        """e.g. 'git: main · 3M 1A 2?'."""
        text: str = f"{self.kind}: {self.branch}"
        parts: list[str] = self._count_parts()
        if parts:
            text += " · " + " ".join(parts)
        return text

    def summary_rich(self) -> str:
        """Rich text 'git: main · 7b05e612 · 3M 1A 2?' with one link.

        The tool name is the link (`vcs:menu`): the label turns a click on it
        into a popup menu of the values worth copying (`copy_entries`). Names
        are escaped, since a branch may hold '<' or '&'.
        """
        text: str = (
            f'<a href="vcs:menu">{html.escape(self.kind)}</a>: '
            f"{html.escape(self.branch)}"
        )
        if self.head is not None:
            text += f" · {html.escape(self.head.short)}"
        parts: list[str] = self._count_parts()
        if parts:
            text += " · " + " ".join(parts)
        return text

    @property
    def branch_name(self) -> str:
        """The branch alone: hg labels a bookmark as 'stable @bookmark'."""
        return self.branch.split(" @", 1)[0]

    def copy_entries(self) -> list[tuple[str, str, str] | None]:
        """What the repository menu offers: (menu text, value, what), or None
        for a separator.

        The value is what lands on the clipboard (the *full* commit id even
        though the label shows eight characters); *what* names it for the
        statusbar. Entries that do not apply -- no commit yet, no upstream, no
        tag, no bookmark -- are left out.
        """
        name: str = self.branch_name
        entries: list[tuple[str, str, str] | None] = [
            (f"Copy branch name ({name})", name, f"branch {name}")
        ]
        if " @" in self.branch:
            bookmark: str = self.branch.split(" @", 1)[1]
            entries.append(
                (f"Copy bookmark ({bookmark})", bookmark, f"bookmark {bookmark}")
            )
        if self.tracking is not None and self.tracking.upstream is not None:
            upstream: str = self.tracking.upstream
            entries.append(
                (f"Copy upstream ({upstream})", upstream, f"upstream {upstream}")
            )
        if self.head is not None:
            entries.append(None)
            what: str = f"commit {self.head.short}"
            entries.append(("Copy full commit hash", self.head.commit, what))
            entries.append(
                (f"Copy short commit hash ({self.head.short})", self.head.short, what)
            )
            if self.head.tags:
                entries.append(None)
                for tag in self.head.tags:
                    entries.append((f"Copy tag ({tag})", tag, f"tag {tag}"))
        entries.append(None)
        entries.append(("Copy repository path", self.root, "repository path"))
        return entries


# --- running the tools ------------------------------------------------------

_executables: dict[str, str | None] = {}


def _executable(name: str) -> str | None:
    if name not in _executables:
        _executables[name] = shutil.which(name)
    return _executables[name]


def _run(
    command: list[str], cwd: str, env: dict[str, str]
) -> subprocess.CompletedProcess[bytes]:
    flags: int = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0  # type: ignore[attr-defined]
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        timeout=STATUS_TIMEOUT_S,
        creationflags=flags,
    )


def query_status(repo: RepoInfo, listing_dir: str) -> StatusSnapshot:
    """Run the status command(s) for *repo*, plus the commit details. Never raises."""
    snapshot: StatusSnapshot = _query_status(repo, listing_dir)
    try:
        snapshot.head = head_info(repo)
    except Exception:  # a tooltip detail must never break the status
        snapshot.head = None
    return snapshot


def _query_status(repo: RepoInfo, listing_dir: str) -> StatusSnapshot:
    """Run the status command(s) for *repo*. Blocking; never raises."""
    branch: str = read_branch(repo)
    exe: str | None = _executable(repo.kind)
    if exe is None:
        return StatusSnapshot.build(
            repo, branch, {}, error=f"'{repo.kind}' executable not found"
        )
    env: dict[str, str] = dict(os.environ)
    try:
        if repo.kind == "git":
            result = _run(
                [
                    exe,
                    "--no-optional-locks",
                    "-c",
                    "core.quotepath=off",
                    "status",
                    "--porcelain=v1",
                    "--branch",
                    "-z",
                    "--ignored=matching",
                    "-unormal",
                ],
                repo.root,
                env,
            )
            if result.returncode != 0:
                return StatusSnapshot.build(repo, branch, {}, error=_error_text(result))
            snapshot = StatusSnapshot.build(
                repo, branch, parse_git_status(result.stdout)
            )
            snapshot.tracking = parse_git_tracking(result.stdout)
            return snapshot
        env["HGPLAIN"] = "1"
        env["HGENCODING"] = "utf-8"
        result = _run([exe, "status", "-mardu", "-0"], repo.root, env)
        if result.returncode != 0:
            return StatusSnapshot.build(repo, branch, {}, error=_error_text(result))
        entries: dict[str, VcsState] = parse_hg_status(result.stdout)
        entries.update(_hg_ignored(exe, repo, listing_dir, env))
        if os.path.exists(os.path.join(repo.meta_dir, "merge", "state")):
            resolve = _run([exe, "resolve", "-l"], repo.root, env)
            if resolve.returncode == 0:
                entries.update(parse_hg_resolve(resolve.stdout))
        return StatusSnapshot.build(repo, branch, entries)
    except (OSError, subprocess.SubprocessError) as error:
        return StatusSnapshot.build(repo, branch, {}, error=str(error))


def _hg_ignored(
    exe: str, repo: RepoInfo, listing_dir: str, env: dict[str, str]
) -> dict[str, VcsState]:
    """Ignored entries of *listing_dir*, files and (inferred) directories.

    hg reports ignored *files* only, and a repo-wide query would walk .venv and
    friends. So ask for the files directly in the listed directory and in each
    of its subdirectories with one `rootfilesin:` pattern apiece (one process,
    no recursion); a subdirectory holding an ignored file directly is reported
    as an ignored directory, which is how `venv/` or `__pycache__/` get tinted.
    A directory whose ignored files all sit deeper is not detected.
    """
    relative: str = os.path.relpath(listing_dir, repo.root).replace("\\", "/")
    if relative.startswith(".."):
        return {}
    prefix: str = "" if relative == "." else relative + "/"
    patterns: list[str] = [f"rootfilesin:{relative}"]
    try:
        with os.scandir(listing_dir) as scan:
            names: list[str] = sorted(
                entry.name
                for entry in scan
                if entry.is_dir(follow_symlinks=False) and entry.name != ".hg"
            )
    except OSError:
        names = []
    patterns += [f"rootfilesin:{prefix}{name}" for name in names[:MAX_HG_SUBDIRS]]
    result = _run([exe, "status", "-i", "-0", *patterns], repo.root, env)
    if result.returncode != 0:
        return {}
    entries: dict[str, VcsState] = parse_hg_status(result.stdout)
    for path in list(entries):
        below: str = path[len(prefix) :] if path.startswith(prefix) else ""
        if "/" in below:
            entries[prefix + below.split("/", 1)[0] + "/"] = VcsState.IGNORED
    return entries


def _error_text(result: subprocess.CompletedProcess[bytes]) -> str:
    text: str = result.stderr.decode("utf-8", errors="replace").strip()
    return text.splitlines()[0] if text else f"exit code {result.returncode}"


# --- provider ---------------------------------------------------------------


class VcsStatusProvider(qt.QObject):
    """Async, cached status shared by every explorer tab.

    A request is keyed by (repository root, listed directory): the root alone
    would let two tabs on different directories overwrite each other's hg
    'ignored' entries. At most one worker runs per key; a request that
    arrives meanwhile coalesces into one follow-up run. A result is applied
    only if no newer request was made since it started.
    """

    status_ready = qt.pyqtSignal(str, object)  # key, StatusSnapshot
    # A repository's metadata changed (commit, checkout, ...): the argument
    # is the repository root's path_key. Each explorer still showing that
    # repository re-requests its own directory; keys nobody displays any
    # more are left alone instead of costing a process each.
    metadata_changed = qt.pyqtSignal(str)
    _finished = qt.pyqtSignal(str, int, object)  # key, generation, snapshot

    def __init__(self, parent: qt.QObject | None = None) -> None:
        super().__init__(parent)
        self._cache: dict[str, StatusSnapshot] = {}
        self._repos: dict[str, tuple[RepoInfo, str]] = {}
        self._generation: dict[str, int] = {}
        self._running: set[str] = set()
        self._rerun: set[str] = set()
        self._quiet_until: dict[str, float] = {}
        self._finished.connect(self._on_finished)
        self._watcher = qt.QFileSystemWatcher(self)
        self._watcher.directoryChanged.connect(self._on_metadata_changed)
        self._watched: dict[str, str] = {}  # watched dir key -> repo root key
        self._debounce = qt.QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(METADATA_DEBOUNCE_MS)
        self._debounce.timeout.connect(self._refresh_changed)
        self._changed_roots: set[str] = set()

    @staticmethod
    def key_for(repo: RepoInfo, listing_dir: str) -> str:
        return path_key(repo.root) + "|" + path_key(listing_dir)

    def cached(self, key: str) -> StatusSnapshot | None:
        return self._cache.get(key)

    def request(self, listing_dir: str, repo: RepoInfo | None = None) -> str | None:
        """Ask for fresh status of the repo containing *listing_dir*.

        Returns the key the result will be announced under, or None when the
        directory is not inside a repository.
        """
        repo = repo or find_repo(listing_dir)
        if repo is None:
            return None
        key: str = self.key_for(repo, listing_dir)
        self._repos[key] = (repo, listing_dir)
        self._watch(repo)
        self._generation[key] = self._generation.get(key, 0) + 1
        if key in self._running:
            self._rerun.add(key)
        else:
            self._start(key)
        return key

    def _start(self, key: str) -> None:
        repo, listing_dir = self._repos[key]
        generation: int = self._generation[key]
        self._running.add(key)
        thread = threading.Thread(
            target=self._work, args=(key, generation, repo, listing_dir), daemon=True
        )
        thread.start()

    def _work(
        self, key: str, generation: int, repo: RepoInfo, listing_dir: str
    ) -> None:
        snapshot: StatusSnapshot = query_status(repo, listing_dir)
        try:
            self._finished.emit(key, generation, snapshot)
        except RuntimeError:
            pass  # the provider was destroyed during shutdown

    @qt.pyqtSlot(str, int, object)
    def _on_finished(self, key: str, generation: int, snapshot: Any) -> None:
        self._running.discard(key)
        repo, _listing = self._repos[key]
        self._quiet_until[path_key(repo.root)] = time.monotonic() + SELF_EVENT_QUIET_S
        if key in self._rerun:
            self._rerun.discard(key)
            self._start(key)
        if generation == self._generation.get(key):
            self._cache[key] = snapshot
            self.status_ready.emit(key, snapshot)

    def _watch(self, repo: RepoInfo) -> None:
        meta: str = repo.meta_dir
        if path_key(meta) not in self._watched and os.path.isdir(meta):
            self._watcher.addPath(meta)
            self._watched[path_key(meta)] = path_key(repo.root)

    @qt.pyqtSlot(str)
    def _on_metadata_changed(self, directory: str) -> None:
        root: str | None = self._watched.get(path_key(directory))
        if root is None:
            return
        busy: bool = any(k.startswith(root + "|") for k in self._running)
        if busy or time.monotonic() < self._quiet_until.get(root, 0.0):
            return  # our own status query touched the metadata
        self._changed_roots.add(root)
        self._debounce.start()

    def _refresh_changed(self) -> None:
        roots: set[str] = self._changed_roots
        self._changed_roots = set()
        for root in roots:
            self.metadata_changed.emit(root)


_provider: VcsStatusProvider | None = None


def provider() -> VcsStatusProvider:
    """The shared provider, created on first use (on the GUI thread)."""
    global _provider
    if _provider is None:
        _provider = VcsStatusProvider(qt.QApplication.instance())
    return _provider


def theme_color(theme: dict[str, Any], state: VcsState) -> str:
    """The colour of *state* from the theme's 'vcscolors', else the default."""
    block: dict[str, str] = theme.get("vcscolors", {}) or {}
    name: str = state.name.lower()
    return block.get(name, DEFAULT_COLORS[name])
