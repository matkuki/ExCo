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


class MarkdownViewer(qt.QTextBrowser):
    # Class variables
    name: str
    _parent: Any = None
    main_form: Any = None
    current_icon: Any = None
    internals: components.internals.Internals
    savable = constants.CanSave.NO
    save_path: str

    def __init__(self, file_path: str, parent: Any, main_form: Any) -> None:
        super().__init__(parent)
        self.name = os.path.basename(file_path)
        self.save_path = file_path
        self._parent = parent
        self.main_form = main_form

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
            scroll_position = self.verticalScrollBar().value()  # type: ignore[union-attr]
            text = functions.read_file_to_string(self.save_path)
            self.setText("")
            self.document().setMarkdown(text)  # type: ignore[union-attr]
            self.verticalScrollBar().setValue(scroll_position)  # type: ignore[union-attr]
            self.modification_time = os.path.getmtime(self.save_path)
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
