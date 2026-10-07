"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.

For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import struct
from typing import Any, Sequence

import data
import qt


DROP_EFFECT_FORMAT: str = "Preferred DropEffect"
DROP_EFFECT_COPY: int = 1
DROP_EFFECT_MOVE: int = 2
# The 'Preferred DropEffect' of the file managers is a native clipboard
# format, which Qt hands out as a mime type named after it; setting that
# mime type publishes the format itself, which is what makes a cut in Ex.Co
# move the items when they are pasted in the OS file manager. Without it the
# file manager pastes a copy, since plain 'setUrls' provides no way to say
# which of the two is meant.
QT_NATIVE_DROP_EFFECT: str = 'application/x-qt-windows-mime;value="{}"'.format(
    DROP_EFFECT_FORMAT
)
# Nautilus and Files mark a cut with this mime type, holding the verb
# followed by the uris, one per line.
GNOME_COPIED_FILES: str = "x-special/gnome-copied-files"


def set_files(paths: Sequence[str], move: bool) -> None:
    """Publish the paths on the system clipboard as files, so that the OS
    file manager can paste them. A cut is published as a move, which also
    makes the sources disappear from there."""
    mime: qt.QMimeData = qt.QMimeData()
    mime.setUrls([qt.QUrl.fromLocalFile(path) for path in paths])
    if data.on_windows:
        mime.setData(
            QT_NATIVE_DROP_EFFECT,
            struct.pack("<I", DROP_EFFECT_MOVE if move else DROP_EFFECT_COPY),
        )
    else:
        mime.setData(
            GNOME_COPIED_FILES,
            ("{}\n{}".format("cut" if move else "copy", _uri_list(paths))).encode(
                "utf-8"
            ),
        )
    clipboard().setMimeData(mime)


def get_files() -> tuple[list[str], bool] | None:
    """Return the paths held by the system clipboard together with whether
    they are to be moved, or None when it holds no files at all (a copied
    text, for instance, is not a file)."""
    mime: qt.QMimeData | None = _mime_data()
    if mime is None or not mime.hasUrls():
        return None
    paths: list[str] = [url.toLocalFile() for url in mime.urls() if url.isLocalFile()]
    if len(paths) == 0:
        return None
    return (paths, _is_move(mime))


def clear_files() -> None:
    """Release the files on the system clipboard.

    Used once a cut has consumed its sources, the way the OS file manager
    empties the clipboard after it moved them."""
    clipboard().clear()


def clipboard() -> qt.QClipboard:
    """The clipboard of the running application."""
    application: Any = data.application
    if application is None:
        raise RuntimeError("Cannot reach the clipboard without an application!")
    return application.clipboard()


def _mime_data() -> qt.QMimeData | None:
    """The mime data of the system clipboard, or None when it is empty."""
    mime: qt.QMimeData | None = clipboard().mimeData()
    if mime is None:
        return None
    if not _has_payload(mime) or not mime.hasUrls():
        return None
    return mime


def _has_payload(mime: qt.QMimeData) -> bool:
    """Whether the clipboard's mime data carries anything.

    An empty mime data object still reports its formats, so a clipboard
    that was emptied would otherwise look like a copied text."""
    formats: list[str] = mime.formats()
    if not formats:
        return False
    for format in formats:
        payload: Any = mime.data(format)
        if len(bytes(payload)) > 0:
            return True
    return False


def _is_move(mime: qt.QMimeData) -> bool:
    """Whether the file manager marked the files as cut rather than copied."""
    if data.on_windows:
        effect: Any = mime.data(QT_NATIVE_DROP_EFFECT)
        if len(effect) < 4:
            return False
        return struct.unpack("<I", bytes(effect[:4]))[0] == DROP_EFFECT_MOVE
    gnome: Any = mime.data(GNOME_COPIED_FILES)
    verb: str = bytes(gnome).decode("utf-8", "replace")
    return verb.splitlines()[0].strip().lower() == "cut" if verb else False


def _uri_list(paths: Sequence[str]) -> str:
    return "\n".join([qt.QUrl.fromLocalFile(path).toString() for path in paths])
