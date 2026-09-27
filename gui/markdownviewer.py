"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Read-only Markdown viewer tab widget. Renders markdown documents
##      with Qt's built-in QTextDocument::setMarkdown (zero dependencies)
##      and offers a "render in browser" full-GFM escape hatch.

import os
import re
import subprocess
import tempfile
import traceback
from typing import Any, Optional

import components.internals
import components.markdownhtml
import components.pathwatcher
import constants
import data
import functions
import qt
import settings

from gui.menu import Menu


def _is_word_char(character: str) -> bool:
    """Whether a character is part of a word rather than a separator"""
    return character.isalnum() or character == "_"


class MarkdownViewer(qt.QTextBrowser):
    # Class variables
    name: str
    _parent: Any = None
    main_form: Any = None
    current_icon: Any = None
    internals: components.internals.Internals
    savable = constants.CanSave.NO
    save_path: str
    # True until the first successful read, so the cursor is parked correctly
    _first_load: bool = True
    # Raw text line to show on the first load, cleared once applied
    _initial_line: Optional[int] = None
    # True once the widget has been shown, i.e. it has a layout to scroll
    _shown_once: bool = False
    # A line needs at least this many words before its position is trusted
    # enough to anchor the search of the lines around it.
    _MIN_ANCHOR_WORDS = 3

    def __init__(
        self, file_path: str, parent: Any, main_form: Any, line: Optional[int] = None
    ) -> None:
        super().__init__(parent)
        self.name = os.path.basename(file_path)
        self.save_path = file_path
        self._parent = parent
        self.main_form = main_form
        # Raw text line to show on the first load, if any
        self._initial_line = line

        self.current_icon = functions.create_icon("tango_icons/markdown.png")
        self.internals = components.internals.Internals(parent=self, tab_widget=parent)
        self.internals.update_icon(self)

        # Watch state (only remove what we added)
        self._added_watch = False
        self._reload_timer: Optional[qt.QTimer] = None

        # Store the modification time for change detection
        modification_time: Optional[float] = None
        try:
            modification_time = os.path.getmtime(file_path)
        except OSError:
            pass
        self.modification_time = modification_time

        # Initialize the widget
        self.setReadOnly(True)
        self.setUndoRedoEnabled(False)
        self.setLineWrapMode(qt.QTextEdit.LineWrapMode.WidgetWidth)
        # External links via the system browser; internal links via Ex.Co.
        self.setOpenExternalLinks(False)
        self.setOpenLinks(False)
        # Resolve relative image/link paths against the document directory
        document_dir = os.path.dirname(self.save_path) or "."
        self.document().setBaseUrl(  # type: ignore[union-attr]
            qt.QUrl.fromLocalFile(document_dir)
        )
        # Theme styling
        self.set_theme(settings.get_theme())

        # Corner buttons: browser preview and back-to-editor switch
        self.add_corner_buttons()

        # Link handling
        self.anchorClicked.connect(self._anchor_clicked)

        # Auto-reload via the shared file system watcher
        self.main_form.tools.path_watcher.file_changed.connect(self._on_file_event)
        if not self._file_is_monitored(self.save_path):
            self.main_form.tools.pathwatcher_add(self.save_path)
            self._added_watch = True

        # Show the file
        self.reload_from_disk()

    def _file_is_monitored(self, file_path: str) -> bool:
        normalized = functions.normalize_path(file_path)
        for monitored in self.main_form.tools.path_watcher.get_monitored_files():
            if functions.normalize_path(monitored) == normalized:
                return True
        return False

    def set_theme(self, theme: dict) -> None:
        color = theme["fonts"]["default"]["color"]
        background = theme["fonts"]["default"]["background"]
        self.setStyleSheet(
            "QTextEdit {{ color: {0}; background-color: {1}; }}".format(
                color, background
            )
        )
        self.setFont(settings.get_current_font())
        self.document().setDefaultFont(  # type: ignore[union-attr]
            settings.get_current_font()
        )

    def add_corner_buttons(self) -> None:
        """Add the corner buttons of the markdown viewer tab"""

        def back_to_editor() -> None:
            index = self._parent.indexOf(self)
            self._parent.switch_to_editor_view(index)

        self.internals.add_corner_button(
            "tango_icons/gnome-web-browser.png",
            "Open rendered preview in browser",
            self.open_preview_in_browser,
        )
        self.internals.add_corner_button(
            "tango_icons/accessories-text-editor.png",
            "Back to editor view",
            back_to_editor,
        )

    """
    Events
    """

    def keyPressEvent(self, event: Any) -> None:
        super().keyPressEvent(event)
        self.main_form.view.indication_check()

    def mousePressEvent(self, event: Any) -> None:
        super().mousePressEvent(event)
        self.main_form.view.indication_check()
        self.main_form.last_focused_widget = self._parent

    def contextMenuEvent(self, event: Any) -> None:
        menu = Menu(self)
        standard_menu = self.createStandardContextMenu()
        menu.addActions(standard_menu.actions())  # type: ignore[union-attr]
        menu.addSeparator()
        preview_action = menu.addAction(
            functions.create_icon("tango_icons/gnome-web-browser.png"),
            "Open rendered preview in browser",
        )
        preview_action.triggered.connect(  # type: ignore[union-attr]
            self.open_preview_in_browser
        )
        menu.popup(qt.QCursor.pos())

    def _anchor_clicked(self, url: qt.QUrl) -> None:
        url_string = url.toString()
        if url.isLocalFile() or url_string.startswith("file://"):
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                self.main_form.open_file(file_path)
                return
        functions.open_url(url_string)

    """
    Reloading
    """

    def reload_from_disk(self) -> None:
        try:
            scroll_bar: qt.QScrollBar = self.verticalScrollBar()  # type: ignore[assignment]
            scroll_position = scroll_bar.value()
            first_load = self._first_load
            text = functions.read_file_to_string(self.save_path)
            self.setText("")
            self.document().setMarkdown(text)  # type: ignore[union-attr]
            if first_load:
                # setMarkdown leaves the cursor at the very end of the
                # document, and Qt issues an ensureCursorVisible() as soon as
                # the widget is shown and laid out, which would drag the view
                # to the bottom. Park the cursor at the start instead; the
                # requested line, if any, is applied by _apply_initial_line.
                cursor = self.textCursor()
                cursor.movePosition(qt.QTextCursor.MoveOperation.Start)
                self.setTextCursor(cursor)
            self._first_load = False
            scroll_bar.setValue(scroll_position)
            self.modification_time = os.path.getmtime(self.save_path)
            # A pending line may have been scheduled before this document
            # existed; re-arm now that there is something to scroll to.
            if self._initial_line is not None and self._shown_once:
                qt.QTimer.singleShot(0, self._apply_initial_line)
        except Exception:
            self.main_form.display.repl_display_error(
                "Error re-reading file '{}'!\n{}".format(
                    self.save_path, traceback.format_exc()
                )
            )

    def _on_file_event(
        self,
        event_type: object,
        source: str,
        destination: Optional[str],
        modification_time: Optional[float],
    ) -> None:
        if functions.normalize_path(source) != functions.normalize_path(self.save_path):
            return
        if event_type not in (
            components.pathwatcher.FileEvent.MODIFIED,
            components.pathwatcher.FileEvent.CREATED,
        ):
            return
        if self._reload_timer is None:
            self._reload_timer = qt.QTimer(self)
            self._reload_timer.setSingleShot(True)
            self._reload_timer.timeout.connect(self.reload_from_disk)
        self._reload_timer.start(200)

    """
    Positioning
    """

    @staticmethod
    def _plain(text: str) -> str:
        """Strip markdown markup so a source line can be found when rendered

        A rendered block carries none of the source markup, so the source has
        to be reduced the same way before the two can be compared: list and
        heading markers, emphasis, code span delimiters, links, images and
        inline HTML all have to go, otherwise a line such as
        ``- **Mercurial** (`.hg/`)`` can never be found in the plain text it
        renders to. Underscores are deliberately left alone, since snake_case
        identifiers inside code spans survive rendering unchanged and are far
        more common here than underscore emphasis.
        """
        text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r" \1 ", text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"^[\s>]*(?:[-*+]|\d+[.)])[ \t]+", "", text)
        text = re.sub(r"^[ \t]*#{1,6}[ \t]*", "", text)
        text = text.replace("`", "").replace("*", "").replace("|", " ")
        return " ".join(text.split()).lower()

    def showEvent(self, event):
        super().showEvent(event)
        self._shown_once = True
        # The view only has a real geometry once it is shown and laid out, so
        # the requested line is applied from here rather than at load time.
        if self._initial_line is not None:
            qt.QTimer.singleShot(0, self._apply_initial_line)

    def _apply_initial_line(self) -> None:
        """Show the line the raw text editor was displaying, once it sticks

        The line stays pending until the widget has been shown at least once
        and the document is loaded, because until then there is no layout to
        scroll and no rendered blocks to scroll to.
        """
        if self._initial_line is None:
            return
        if not self._shown_once:
            return
        if self.document().isEmpty():  # type: ignore[union-attr]
            return
        line = self._initial_line
        self.scroll_to_source_line(line)
        self._initial_line = None

    def _find_clean(self, needle: str, origin: int, plain_lower: str) -> Any:
        """Find *needle* at or after *origin*, but only on word boundaries

        ``QTextDocument.find`` matches anywhere, so a short needle such as
        "run" would happily match inside "runtime" or "runs" and put a heading
        on an unrelated word. The characters flanking each hit are checked to
        keep the hit word-aligned. Returns None when nothing matches.
        """
        document: Any = self.document()
        # Qt's find is case-insensitive unless asked otherwise, which suits
        # the lowercased needles built by _plain.
        position = origin
        while True:
            cursor = document.find(needle, position)
            if cursor.isNull():
                return None
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            before = plain_lower[start - 1] if start > 0 else " "
            after = plain_lower[end] if end < len(plain_lower) else " "
            if not _is_word_char(before) and not _is_word_char(after):
                return cursor
            position = end

    @classmethod
    def _searchable(cls, line: str) -> list[str]:
        """The words of a source line, ready to be searched for

        Returns an empty list for a line with nothing to look for, such as a
        bare rule or a table separator, which have no counterpart in the
        rendered document at all and would otherwise match stray punctuation.
        """
        words = cls._plain(line).split()
        if not any(word.isalnum() for word in words):
            return []
        return words

    def _search_words(
        self, words: list[str], origin: int, plain_lower: str, min_words: int
    ) -> Any:
        """Find the longest run of leading words at or after *origin*

        Only runs of at least *min_words* words are accepted, so a caller can
        insist on a match distinctive enough to trust. Returns None when no
        such run is present.
        """
        for count in range(len(words), min_words - 1, -1):
            cursor = self._find_clean(" ".join(words[:count]), origin, plain_lower)
            if cursor is not None:
                return cursor
        return None

    def _anchors(
        self,
        source_lines: list[str],
        offsets: list[int],
        plain_lower: str,
    ) -> list[tuple[int, int, int]]:
        """Build a monotonic chain of confidently located source lines.

        Only lines with at least ``_MIN_ANCHOR_WORDS`` words become anchors,
        and only when that many leading words are actually found: a long
        phrase is distinctive enough to trust, whereas one or two words match
        far too easily. That matters for text the renderer drops outright --
        YAML frontmatter, for instance, produces no blocks at all -- where a
        weak match would anchor the chain to an arbitrary common word and
        drag every later line with it.

        Anchors are searched strictly forwards from the previous hit, so the
        chain can neither run backwards nor collapse onto an early block.
        Lines that cannot be placed confidently are simply absent from it.

        Returns ``(source offset, block number, position in the plain text)``
        tuples in increasing source order.
        """
        anchors: list[tuple[int, int, int]] = []
        search_from = 0
        for index, line in enumerate(source_lines):
            words = self._searchable(line)
            if len(words) < self._MIN_ANCHOR_WORDS:
                continue
            cursor = self._search_words(
                words, search_from, plain_lower, self._MIN_ANCHOR_WORDS
            )
            if cursor is not None:
                anchors.append(
                    (offsets[index], cursor.blockNumber(), cursor.selectionStart())
                )
                search_from = cursor.selectionEnd()
        return anchors

    def _source_line_block(self, line_number: int) -> int:
        """Return the rendered block number that shows a raw text line.

        Rendering does not preserve line numbers, and no line-to-block
        correspondence can be assumed: a run of source lines collapses into
        one paragraph, a table row becomes one block *per cell*, headings lose
        their hashes and fenced code becomes a single preformatted block.
        Pairing the two streams up structurally would need a special case for
        every construct, so the line is located in the rendered text instead
        and the block Qt reports is used. The search starts just after the
        nearest confidently located line before this one, so a phrase that
        occurs several times cannot drag the view to an earlier occurrence.
        """
        document: qt.QTextDocument = self.document()  # type: ignore[assignment]
        source_lines = functions.read_file_to_string(self.save_path).split("\n")
        if not source_lines:
            return -1
        target = min(max(line_number - 1, 0), len(source_lines) - 1)
        offsets = [0] * (len(source_lines) + 1)
        for index, line in enumerate(source_lines):
            offsets[index + 1] = offsets[index] + len(line) + 1

        plain_lower = document.toPlainText().lower()
        anchors = self._anchors(source_lines, offsets, plain_lower)

        origin = 0
        for offset, _block, position in anchors:
            if offset < offsets[target]:
                origin = position + 1

        words = self._searchable(source_lines[target])
        if not words:
            return self._interpolated_block(offsets[target], anchors)
        # Only a run of several words is distinctive enough to place the line
        # by outright; a shorter one matches too easily.
        cursor = self._search_words(words, origin, plain_lower, self._MIN_ANCHOR_WORDS)
        if cursor is None:
            # The line may sit before the nearest anchor, which happens when
            # earlier text was dropped by the renderer; retry from the top.
            cursor = self._search_words(words, 0, plain_lower, self._MIN_ANCHOR_WORDS)
        if cursor is not None:
            return cursor.blockNumber()
        # A short heading has too few words to be trusted, yet it is exactly
        # what the weak search is good for, so it is accepted only when it
        # lands next to where interpolation expects it. That keeps headings
        # like "## Testing" placeable while stopping a line the renderer
        # dropped from landing on some unrelated occurrence far away.
        estimate = self._interpolated_block(offsets[target], anchors)
        if estimate >= 0:
            tolerance = max(2, document.blockCount() // 40)
            cursor = self._search_words(words, origin, plain_lower, 1)
            if cursor is not None and abs(cursor.blockNumber() - estimate) <= tolerance:
                return cursor.blockNumber()
        return estimate

    @staticmethod
    def _interpolated_block(offset: int, anchors: list[tuple[int, int, int]]) -> int:
        """Estimate a block for a line no anchor could locate"""
        if not anchors:
            return -1
        before = [anchor for anchor in anchors if anchor[0] < offset]
        after = [anchor for anchor in anchors if anchor[0] > offset]
        low = before[-1] if before else None
        high = after[0] if after else None
        if low is None:
            return high[1] if high is not None else -1
        if high is None:
            return low[1]
        span = high[0] - low[0]
        if span <= 0:
            return low[1]
        ratio = (offset - low[0]) / span
        return round(low[1] + ratio * (high[1] - low[1]))

    def _proportional_block(self, line_number: int) -> int:
        """Estimate a block from a line's share of the source text

        The last resort, for a document too featureless to anchor at all: a
        line of bare punctuation with no anchors on either side of it.
        """
        document: qt.QTextDocument = self.document()  # type: ignore[assignment]
        text = functions.read_file_to_string(self.save_path)
        if not text:
            return 0
        lines = text.split("\n")
        index = min(max(line_number - 1, 0), len(lines) - 1)
        offset = sum(len(line) + 1 for line in lines[:index])
        block_count = document.blockCount()
        return min(block_count - 1, max(0, round(offset / len(text) * block_count)))

    def scroll_to_source_line(self, line_number: int) -> bool:
        """Place a 1-based raw text line at the top of the view

        Returns True when a rendered block was found and positioned. A block
        near the end of the document cannot reach the top of the view, since
        there is not enough content left to scroll; it is left at the bottom
        of the viewport instead.
        """
        block_number = self._source_line_block(line_number)
        if block_number < 0:
            block_number = self._proportional_block(line_number)
        if block_number < 0:
            return False
        document: qt.QTextDocument = self.document()  # type: ignore[assignment]
        block = document.findBlockByNumber(block_number)
        if not block.isValid():
            return False
        cursor = qt.QTextCursor(block)
        cursor.movePosition(qt.QTextCursor.MoveOperation.StartOfBlock)
        self.setTextCursor(cursor)
        # cursorRect is in viewport coordinates, so shifting by the current
        # scroll offset puts the block flush with the top of the view.
        scroll_bar: qt.QScrollBar = self.verticalScrollBar()  # type: ignore[assignment]
        scroll_bar.setValue(scroll_bar.value() + self.cursorRect(cursor).top())
        return True

    """
    General
    """

    def open_preview_in_browser(self) -> None:
        try:
            import components.markdownhtml

            text = functions.read_file_to_string(self.save_path)
            html_text = components.markdownhtml.render(text, title=self.name)
            html_text = components.markdownhtml.absolutize_links(
                html_text, os.path.dirname(self.save_path)
            )
            # Deterministic temp output path
            preview_dir = os.path.join(tempfile.gettempdir(), "exco", "markdown")
            os.makedirs(preview_dir, exist_ok=True)
            html_path = os.path.join(preview_dir, "{}.html".format(self.name))
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_text)
            if data.on_windows:
                os.startfile(html_path)
            else:
                subprocess.call(["xdg-open", html_path])
        except Exception:
            self.main_form.display.repl_display_error(
                "Error rendering Markdown preview!\n{}".format(traceback.format_exc())
            )

    def shutdown(self) -> None:
        try:
            self.main_form.tools.path_watcher.file_changed.disconnect(
                self._on_file_event
            )
        except Exception:
            pass
        if self._reload_timer is not None:
            self._reload_timer.stop()
        if self._added_watch:
            self.main_form.tools.pathwatcher_remove(self.save_path)
