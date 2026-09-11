"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

View/layout management (windows, trees, zoom, focus, tabs).

Controls window splitting, tab navigation, zoom level, focus
cycling, and the function-wheel overlay. Namespace class attached
to the MainWindow instance.
"""

import json
import os
import traceback
from typing import Any, Dict, Optional, Tuple

import constants
import data
import functions
import gui.stylesheets
import qt
import settings
import settings.constants
from gui.custombuttons import CustomButton
from gui.stylesheets import (
    StyleSheetButton,
    StyleSheetMenu,
    StyleSheetMenuBar,
    StyleSheetScrollbar,
    StyleSheetTable,
    StyleSheetTabWidget,
    StyleSheetTooltip,
    StyleSheetTreeWidget,
)
from gui.customeditor import CustomEditor
from gui.dialogs import YesNoDialog
from gui.excoinfo import ExCoInfo
from gui.functionwheel import FunctionWheel
from gui.hexview import HexView
from gui.menu import Menu
from gui.plaineditor import PlainEditor
from gui.settingsguimanipulator import SettingsGuiManipulator
from gui.tabwidget import TabWidget
from gui.templates import create_groupbox_with_layout
from gui.textdiffer import TextDiffer
from gui.thebox import TheBox
from gui.treedisplays import TreeDisplay, TreeExplorer


class View:
    """
    Functions for manipulating the application appearance
    (namespace/nested class to MainWindow)
    """

    # Class varibles
    _parent = None
    __stored_layout_standard = None
    __stored_layout_one_window = None
    # Default widths and heights of the windows
    vertical_width_1 = 2 / 3
    vertical_width_2 = 1 / 3
    horizontal_width_1 = 2 / 3
    horizontal_width_2 = 1 / 3
    main_relation = 55
    # Overlay helper widget that will be displayed on top of the main groupbox
    function_wheel_overlay = None
    # Last executed functions text on the function wheel
    last_executed_function_text = None
    # Function wheel overlay minimum size
    # Stored REPL single/multi line state
    repl_state = None
    # Lock used when spinning widgets, so the layout does not get saved mid-spin
    layout_save_block = False

    def __init__(self, parent: "MainWindow") -> None:
        """Initialization of the View object instance"""
        # Get the reference to the MainWindow parent object instance
        self._parent = parent
        # Initialize the REPL state to unknown, so it will force
        # the form layout to refresh it
        self.repl_state = None

    def layout_init(self, show_overlay: bool = False) -> None:
        """
        Create the basic layout
        """
        # Create QSplitters
        main_splitter = qt.QSplitter(qt.Qt.Orientation.Vertical)
        main_splitter.setObjectName("MainSplitter")
        # Create the boxes
        boxes_groupbox = create_groupbox_with_layout(
            name="MainGroupBox",
            borderless=True,
        )
        # Main box
        main_box = TheBox(
            "", "Main", qt.Qt.Orientation.Horizontal, self._parent, self._parent
        )
        boxes_groupbox.layout().addWidget(main_box)

        # Vertically split edit fields with the REPL
        main_splitter.addWidget(boxes_groupbox)
        main_splitter.addWidget(self._parent.repl_box)
        # Set the sizes for the main splitter
        main_splitter.setStretchFactor(0, 1)
        # Initialize the main groupbox
        main_groupbox = qt.QGroupBox(self._parent)
        main_groupbox_layout = qt.QVBoxLayout(main_groupbox)
        main_groupbox_layout.addWidget(main_splitter)
        main_groupbox_layout.setContentsMargins(2, 2, 2, 2)
        main_groupbox_layout.setSpacing(0)
        main_groupbox.setLayout(main_groupbox_layout)
        main_groupbox.setObjectName("Main_Groupbox")
        # Add the splitters combined in the groupbox to the main form
        self._parent.setCentralWidget(main_groupbox)
        # Save references to the MainWindow
        self._parent.boxes_groupbox = boxes_groupbox
        self._parent.main_box = main_box
        self._parent.main_splitter = main_splitter
        self._parent.main_groupbox = main_groupbox
        self._parent.main_groupbox_layout = main_groupbox_layout
        # Initialize the function wheel overlay over the QMainWindows central widget, if needed
        self.function_wheel_overlay = FunctionWheel(
            parent=self._parent.main_groupbox,
            main_form=self._parent,
        )
        self.function_wheel_overlay.setObjectName("Function_Wheel")
        if show_overlay == True:
            self._parent.view.show_function_wheel()
        else:
            self._parent.view.hide_function_wheel()
        # Settings GUI Manipulator
        if self._parent.settings.gui_manipulator is not None:
            self._parent.settings.gui_manipulator.__del__()
            self._parent.settings.gui_manipulator = None

        self.layout_restore(settings.constants.default_layout)
        self.check_all_close_buttons()

        functions.process_events()

    def show_about(self) -> None:
        """Show ExCo information"""
        about = ExCoInfo(
            self._parent,
            app_dir=settings.get("application-directory"),
        )
        # The exec_() function shows the dialog in MODAL mode (the parent is unclickable while the dialog is shown)
        about.exec()

    def set_window_focus(self, window: TabWidget) -> None:
        """
        Set focus to one of the editing windows
        """
        try:
            # If the window does not have focus, set focus to it
            window.currentWidget().setFocus()
            # Update the Save/SaveAs buttons in the menubar
            window._set_save_status()
            # Check is the widget is a scintilla custom editor
            if isinstance(window.currentWidget(), CustomEditor):
                # Update the cursor position
                cw = window.currentWidget()
                line = cw.getCursorPosition()[0]
                column = cw.getCursorPosition()[1]
                index = cw.positionFromLineIndex(line, column)
                self._parent.display.update_cursor_position(line, column, index)
            else:
                # Clear the cursor position
                self._parent.display.update_cursor_position()
        except:
            window.setFocus()
            self._parent.display.write_to_statusbar(
                "Empty window '" + window.name + "' focused!", 1000
            )
            # Clear the cursor position
            self._parent.display.update_cursor_position()
        finally:
            # Store the last focused widget
            self._parent.last_focused_widget = window

    def set_repl_type(self, _type: constants.ReplType) -> None:
        """
        Set REPL input as a one line ReplLineEdit or a multiline ReplHelper
        """
        # Check if the REPL type needs to be updated
        if (
            _type == constants.ReplType.SINGLE_LINE
            and self.repl_state == constants.ReplType.SINGLE_LINE
        ):
            self._parent.main_splitter.setSizes([10, 1])
            return
        elif (
            _type == constants.ReplType.MULTI_LINE
            and self.repl_state == constants.ReplType.MULTI_LINE
        ):
            return
        self.repl_state = _type
        # Reinitialize the groupbox that holds the REPL
        self._parent.repl_box.set_repl(_type, self._parent.repl.get_language())
        self._parent.main_splitter.setSizes([10, 1])

    def toggle_window_size(self) -> None:
        """
        Maximize the main application window
        """
        if self._parent.isMaximized() == True:
            self._parent.showNormal()
        else:
            self._parent.showMaximized()

    def toggle_one_window_mode(self) -> None:
        """
        Toggle between one-window mode and a stored layout
        """
        windows = self._parent.get_all_windows()
        if len(windows) > 1:
            # Store layout and change to one-window
            self.__stored_layout_standard = self.layout_generate()
            json_layout = json.loads(self.__stored_layout_standard)
            window_size = json_layout["WINDOW-SIZE"]

            # Remove the widget from current layout
            widgets = []
            for w in windows:
                for i in reversed(range(w.count())):
                    widget = w.widget(i)
                    widgets.append((widget, w.tabText(i)))
                    w.removeTab(i)
                    widget.setParent(None)
                w.setParent(None)
                w.deleteLater()

            # Set one-window layout
            if self.__stored_layout_one_window is not None:
                one_window_layout = self.__stored_layout_one_window
            else:
                if isinstance(window_size, tuple) or isinstance(window_size, list):
                    one_window_layout = settings.constants.one_window_layout.format(
                        "[{}, {}]".format(*window_size), window_size[1]
                    )
                elif window_size == "MAXIMIZED":
                    one_window_layout = settings.constants.one_window_layout.format(
                        '"{}"'.format(window_size), 9999
                    )
                else:
                    raise Exception("Unknown window size: '{}'".format(window_size))
            self.layout_restore(one_window_layout)
            # Put all widgets back into the one
            largest_window = self._parent.get_largest_window()
            widgets.sort(
                key=lambda x: isinstance(x, CustomEditor) or isinstance(x, PlainEditor)
            )
            for w in reversed(widgets):
                widget, tab_text = w
                if tab_text == constants.SpecialTabNames.Messages.value:
                    continue
                largest_window.addTab(widget, tab_text)
                if hasattr(widget, "_parent"):
                    widget._parent = largest_window
                elif hasattr(widget, "parent") and not callable(widget.parent):
                    widget.parent = largest_window
                widget.internals.update_tab_widget(largest_window)
                widget.internals.update_icon(widget)
                widget.internals.update_corner_widget(widget)
            # Update the icons of the tabs
            for i in range(largest_window.count()):
                largest_window.update_tab_icon(largest_window.widget(i))

        else:
            # Remove the widget from current layout
            widgets = {}
            for w in windows:
                for i in reversed(range(w.count())):
                    widget = w.widget(i)
                    widgets[widget.internals.get_id()] = {
                        "widget": widget,
                        "tab-text": w.tabText(i),
                    }
                    w.removeTab(i)
                    widget.setParent(None)
                w.setParent(None)
                w.deleteLater()

            # Restore stored layout
            self.layout_restore(
                self.__stored_layout_standard, pre_stored_widgets=widgets
            )

    def hide_all_overlay_widgets(self) -> None:
        """
        Hide every overlay widget: function wheel, settings gui manipulator, ...
        """
        self.hide_function_wheel()
        self.hide_settings_manipulator()

    def toggle_function_wheel(self) -> None:
        """
        Show/hide the function wheel overlay
        """
        if self.function_wheel_overlay.isVisible() == True:
            self.hide_function_wheel()
        else:
            self.show_function_wheel()

    def hide_function_wheel(self) -> None:
        """
        Hide the function wheel overlay
        """
        if self.function_wheel_overlay is not None:
            self.function_wheel_overlay.hide()

    def show_function_wheel(self) -> None:
        """
        Show the function wheel overlay
        """
        self.hide_all_overlay_widgets()
        # Check the windows size before displaying the overlay
        if (
            self._parent.width() < self.function_wheel_overlay.width()
            or self._parent.height() < self.function_wheel_overlay.height()
        ):
            new_size = functions.create_size(
                int(
                    self.function_wheel_overlay.width()
                    + self.function_wheel_overlay.width() / 5
                ),
                int(
                    self.function_wheel_overlay.height()
                    + self.function_wheel_overlay.height() / 5
                ),
            )
            self._parent.resize(new_size)
        # Check if the function wheel overlay is initialized
        if self.function_wheel_overlay is not None:
            # Save the currently focused widget
            focused_widget = self._parent.get_window_by_child_tab()
            if focused_widget is None:
                focused_widget = self._parent.get_window_by_focus()
            # Store the last focused widget and tab
            self._parent.last_focused_widget = focused_widget
            # Show the function wheel overlay
            self.function_wheel_overlay.show()

    def toggle_settings_manipulator(self) -> None:
        """
        Show/hide the settings manipulator
        """
        if (
            self._parent.settings.gui_manipulator is not None
            and self._parent.settings.gui_manipulator.isVisible() == True
        ):
            self.hide_settings_manipulator()
        else:
            self.show_settings_manipulator()

    def show_settings_manipulator(self) -> None:
        self.hide_all_overlay_widgets()
        # Initialize the settings GUI manipulator if needed
        if self._parent.settings.gui_manipulator is None:
            compare_size = SettingsGuiManipulator.DEFAULT_SIZE
            if (
                self._parent.width() < compare_size[0]
                or self._parent.height() < compare_size[1]
            ):
                new_size = functions.create_size(
                    int(compare_size[0] + compare_size[0] / 5),
                    int(compare_size[1] + compare_size[1] / 5),
                )
                self._parent.resize(new_size)
            self._parent.settings.gui_manipulator = SettingsGuiManipulator(
                parent=self._parent.main_groupbox,
                main_form=self._parent,
            )
        elif self._parent.settings.gui_manipulator.isVisible():
            return
        # Show the gui manipulator
        self._parent.settings.gui_manipulator.show()

    def hide_settings_manipulator(self) -> None:
        if self._parent.settings.gui_manipulator is not None:
            self._parent.settings.gui_manipulator.hide()

    def init_style_sheet(self) -> str:
        style_sheet = """
#Form {{
    background-color: {};
    border: 0px;
}}
#Main_Groupbox {{
    border: 0px;
}}
QSplitter {{
    margin: 0px;
    padding: 0px;
    width: 4px;
}}
QSplitter::handle {{
    background: {};
}}
{}
{}
{}
{}
{}
{}
{}
{}
        """.format(
            settings.get_theme()["form"],
            settings.get_theme()["form"],
            StyleSheetScrollbar.full(),
            StyleSheetButton.standard(),
            StyleSheetMenu.standard(),
            StyleSheetMenuBar.standard(),
            StyleSheetTooltip.standard(),
            StyleSheetTable.standard(),
            StyleSheetTabWidget.standard(),
            StyleSheetTreeWidget.standard(),
        )
        return style_sheet

    def reset_entire_style_sheet(self) -> None:
        style_sheet = self.init_style_sheet()
        self._parent.setStyleSheet(style_sheet)
        self._parent.menubar.update_style()
        Menu.update_styles()
        self.indication_check()

    def indicate_window(self) -> None:
        # Windows
        windows = self._parent.get_all_windows()
        for w in windows:
            w.style().unpolish(w)
            w.style().polish(w)
            w.repaint()
            functions.process_events()

        data.signal_dispatcher.update_title.emit()

    def indication_check(self) -> None:
        if hasattr(self, "indication_timer"):
            self.indication_timer.stop()
        else:
            self.indication_timer = qt.QTimer(self._parent)
            self.indication_timer.setInterval(50)
            self.indication_timer.setSingleShot(True)
            self.indication_timer.timeout.connect(self.__indication_check)
        self.indication_timer.start(50)

    __indication_state = None

    def __indication_check(self) -> None:
        """
        Check if any of the main windows or the REPL is focused
        and indicate the focused widget if needed
        """
        windows = self._parent.get_all_windows()
        if len(windows) == 0 or self._parent.repl is None:
            self.__indication_state = None
            return
        Menu.update_styles()

        # Check the REPL focus
        if (
            self._parent.repl.hasFocus() == True
            or self._parent.repl_helper.hasFocus() == True
        ):
            self._parent.repl_box.indication_set()
            return
        else:
            self._parent.repl_box.indication_reset()

        # Check the focus for all of the windows
        window_indicated_flag = False
        indication_list = {}
        for window in windows:
            #                window.setProperty("indicated", False)
            indication_list[window] = False
        for window in windows:
            if window.count() == 0:
                if window.hasFocus() == True:
                    indication_list[window] = True
                    window_indicated_flag = True
                else:
                    indication_list[window] = False
            else:
                window.indicated = False
                for i in range(window.count()):
                    if isinstance(window.widget(i), TextDiffer) == True:
                        if (
                            window.widget(i).hasFocus() == True
                            or window.widget(i).editor_1.hasFocus() == True
                            or window.widget(i).editor_2.hasFocus() == True
                        ):
                            indication_list[window] = True
                            window_indicated_flag = True
                    else:
                        w = window.widget(i)
                        if w.hasFocus() == True:
                            indication_list[window] = True
                            window_indicated_flag = True

        if window_indicated_flag:
            for k, v in indication_list.items():
                k.setProperty("indicated", v)
            self.indicate_window()
            self.__indication_state = "window-indicated"
            return

    def refresh_theme(self) -> None:
        windows = self._parent.get_all_windows()
        for window in windows:
            window.customize_tab_bar()
            for i in range(window.count()):
                if hasattr(window.widget(i), "refresh_lexer") == True:
                    window.widget(i).refresh_lexer()
                elif hasattr(window.widget(i), "set_theme") == True:
                    window.widget(i).set_theme(settings.get_theme())
        self._parent.repl_helper.refresh_lexer()
        self.reset_entire_style_sheet()
        self._parent.statusbar.setStyleSheet(
            gui.stylesheets.StyleSheetStatusbar.standard()
        )
        # Update the taskbar menu
        self._parent.display.update_theme_taskbar_icon()

        # Update the function wheel
        self.function_wheel_overlay.update_style()

        # Reset the button styled images
        CustomButton.stored_hex = None

    def create_recent_file_list_menu(self) -> Menu:
        self._parent.recent_files_menu = Menu("Recent Files", self._parent.menubar)
        temp_icon = functions.create_icon("tango_icons/file-recent-files.png")
        self._parent.recent_files_menu.setIcon(temp_icon)
        return self._parent.recent_files_menu

    def delete_recent_file_list_menu(self) -> None:
        self._parent.recent_files_menu.setParent(None)
        self._parent.recent_files_menu = None

    def clear_recent_file_list(self) -> None:
        warning = "Are you sure you wish to delete\n" + "the recent files list?"
        reply = YesNoDialog.warning(warning)
        if reply == constants.DialogResult.No.value:
            return
        self._parent.settings.clear_recent_list()
        self._parent.settings.update_recent_list()
        self._parent.display.repl_display_success("Recent file list cleared.")

    """
    Layout
    """

    def check_all_close_buttons(self) -> None:
        for w in self._parent.get_all_windows():
            w.check_close_button()

    def get_layout_classes(self) -> Tuple[Dict[str, Any], Dict[Any, str]]:
        from gui.terminal import Terminal

        # Class name storage
        classes = {
            "CustomEditor": CustomEditor,
            "PlainEditor": PlainEditor,
            constants.SpecialTabNames.Messages.value: PlainEditor,
            "TreeDisplay": TreeDisplay,
            "TreeExplorer": TreeExplorer,
            "HexView": HexView,
            "Terminal": Terminal,
        }
        inverted_classes = {v: k for k, v in classes.items()}
        return classes, inverted_classes

    def reindex_all_windows(self) -> None:
        # Adjust indexes if needed
        for box in self._parent.get_all_boxes():
            index = 0
            box.update_orientations()
            for i in range(box.count()):
                tab_widget = box.widget(i)
                if isinstance(tab_widget, TabWidget):
                    name = tab_widget.objectName()
                    base_name = functions.remove_tabs_from_name(name)
                    box_name = box.objectName()
                    if base_name != box_name:
                        name = box_name + ".Tabs0"
                    new_name = "{}{}".format(
                        functions.remove_tab_number_from_name(name), index
                    )
                    tab_widget.setObjectName(new_name)
                    index += 1
        # Adjust unnecessary box duplications in names and
        # more than one box at one position
        boxes = self._parent.get_all_boxes()
        for b in boxes:
            if (
                b.count() == 1
                and isinstance(b.widget(0), TheBox)
                and b.objectName() != "Main"
            ):
                # Remove the unnecessary box (OLD)
                #                        b.parent().addWidget(b.widget(0))
                # Remove the unnecessary box
                index = b.parent().indexOf(b)
                b.parent().insertWidget(index, b.widget(0))

                b.setParent(None)
                b.deleteLater()
            elif b.count() == 0:
                pass

        def rename(box: Any) -> None:
            for i in range(box.count()):
                widget = box.widget(i)
                if isinstance(widget, TheBox):
                    if widget.orientation() == qt.Qt.Orientation.Vertical:
                        widget.setObjectName(box.objectName() + f".V{i}")
                    else:
                        widget.setObjectName(box.objectName() + f".H{i}")
                    rename(widget)
                else:
                    tabs_name = widget.objectName().split(".")[-1]
                    widget.setObjectName(widget.parent().objectName() + f".{tabs_name}")

        main_box = self._parent.findChild(TheBox, "Main")
        rename(main_box)

        # Check close buttons
        self.check_all_close_buttons()

        # Save the layout
        qt.QTimer.singleShot(10, self._parent.view.layout_save)

    def layout_generate(self) -> str:
        main = self._parent.findChild(TheBox, "Main")
        children = main.get_child_boxes()
        window_size = self._parent.size()
        window_size = (window_size.width(), window_size.height())
        if self._parent.isMaximized():
            window_size = "MAXIMIZED"
        layout = {"WINDOW-SIZE": window_size, "BOXES": children}

        json_layout = json.dumps(layout, ensure_ascii=False)
        return json_layout

    def layout_restore(
        self, json_layout: Any, pre_stored_widgets: Optional[Dict] = None
    ) -> None:
        main_form = self._parent
        main_form.display.repl_suppress()
        # Class name storage
        classes, inverted_classes = self.get_layout_classes()

        # First load the JSON layout, to see if it's valid
        if isinstance(json_layout, str):
            layout = json.loads(json_layout)
        else:
            layout = json_layout

        # Restore size
        window_size = layout["WINDOW-SIZE"]
        screen_size = functions.get_screen_size()
        if window_size == "MAXIMIZED":
            self._parent.showMaximized()
        elif isinstance(window_size, tuple) or isinstance(window_size, list):
            w, h = window_size
            if w > screen_size[0] or h > screen_size[1]:
                self._parent.showMaximized()
            else:
                self._parent.resize(qt.QSize(int(w), int(h)))
                functions.center_to_current_screen(self._parent)

        main_box = self._parent.main_box
        main_box.clear_all()

        def create_box(parent: Any, box: Dict[str, Any]) -> None:
            for k, v in sorted(box.items()):
                if k.startswith("BOX"):
                    orientation = qt.Qt.Orientation.Horizontal
                    if k[-1] == "V":
                        orientation = qt.Qt.Orientation.Vertical
                    new_box = parent.add_box(orientation, add_tabs=False)
                    new_box.show()
                    for _k, _v in v.items():
                        create_box(new_box, _v)
                elif k == "SIZES":
                    new_box.setSizes(v)
                elif k.startswith("TABS"):
                    new_tabs = parent.add_tabs()
                    new_tabs.check_close_button()

                    if pre_stored_widgets:
                        for key, class_string in v.items():
                            if isinstance(class_string, tuple) or isinstance(
                                class_string, list
                            ):
                                cls, tab_index, widget_data = class_string
                                number = widget_data[-1]
                                if number in pre_stored_widgets.keys():
                                    wd = pre_stored_widgets[number]
                                    w = wd["widget"]
                                    new_tabs.addTab(w, wd["tab-text"])
                                    if hasattr(w, "_parent"):
                                        w._parent = new_tabs
                                    elif hasattr(w, "parent") and not callable(
                                        w.parent
                                    ):
                                        w.parent = new_tabs
                                    w.internals.update_tab_widget(new_tabs)
                                    w.internals.update_icon(w)
                                    w.internals.update_corner_widget(w)
                        continue

                    current_index = None
                    tab_index = None
                    widget_data = None
                    for key, class_string in v.items():
                        if key == "CURRENT-INDEX":
                            current_index = class_string
                            continue
                        elif isinstance(class_string, str):
                            cls = class_string
                        elif isinstance(class_string, tuple) or isinstance(
                            class_string, list
                        ):
                            cls, tab_index, widget_data = class_string
                        else:
                            self._parent.display.repl_display_error(
                                f"[LAYOUT] Unknown item 'class_string': {class_string.__class__}"
                            )
                            continue

                        if cls in classes.keys():
                            if cls == "CustomEditor":
                                file = key
                                if isinstance(class_string, tuple) or isinstance(
                                    class_string, list
                                ):
                                    line, index, first_visible_line = widget_data[:3]
                                widget = self._parent.open_file(file, new_tabs, False)
                                if tab_index is not None:
                                    widget = new_tabs.widget(tab_index)
                                    if widget is not None:
                                        widget.setCursorPosition(line, index)
                                        widget.setFirstVisibleLine(first_visible_line)

                            elif cls == "TreeExplorer":
                                directory_path = widget_data[0]
                                if os.path.isdir(directory_path):
                                    file_explorer = new_tabs.tree_add_tab(
                                        constants.SpecialTabNames.FileExplorer.value,
                                        TreeExplorer,
                                    )
                                    file_explorer.display_directory(directory_path)
                                    file_explorer.open_file_signal.connect(
                                        self._parent.open_file
                                    )
                                    file_explorer.open_file_hex_signal.connect(
                                        self._parent.open_file_hex
                                    )
                                    file_explorer.internals.update_icon(file_explorer)

                            elif cls == "HexView":
                                file_path = widget_data[0]
                                if os.path.isfile(file_path):
                                    new_tabs.hexview_add(file_path)

                            elif cls == "Terminal":
                                working_path = widget_data[0]
                                # Newer layouts persist the shell; fall back to
                                # the default when restoring older ones.
                                shell = widget_data[1] if len(widget_data) > 2 else None
                                new_terminal = new_tabs.terminal_add(shell=shell)
                                if working_path is not None and os.path.isdir(
                                    working_path
                                ):
                                    new_terminal.set_cwd(working_path)

                            elif cls == constants.SpecialTabNames.Messages.value:
                                self._parent.repl_messages_tab = (
                                    new_tabs.plain_add_document(
                                        constants.SpecialTabNames.Messages.value
                                    )
                                )
                                rmt = self._parent.repl_messages_tab
                                rmt.internals.set_icon(
                                    rmt, self._parent.display.repl_messages_icon
                                )
                        else:
                            self._parent.display.repl_display_error(
                                f"Unknown tab type: {v}"
                            )
                    if current_index is not None:
                        new_tabs.setCurrentIndex(current_index)
                else:
                    self._parent.display.repl_display_error(
                        "Unknown box child type: {}".format(k)
                    )

        # Open the permanent items
        for k, v in sorted(layout["BOXES"].items()):
            create_box(main_box, v)

        main_form.display.repl_unsuppress()

    def layout_save(self, *args: Any, _async: bool = True) -> None:
        def save(*args: Any, **kwargs: Any) -> None:
            try:
                if _async:
                    self.layout_save_timer.stop()
                self.layout_generate()
            except:
                self._parent.display.repl_display_error(traceback.format_exc())

        if _async:
            if not hasattr(self, "layout_save_timer"):
                # Create the layout save timer if it doesn't exist yet
                self.layout_save_timer = qt.QTimer(self._parent)
                self.layout_save_timer.setInterval(500)
                self.layout_save_timer.setSingleShot(True)
                self.layout_save_timer.timeout.connect(save)
            timer = self.layout_save_timer
            if timer.isActive():
                timer.stop()
            timer.start()
        else:
            save()

    def check_layout_timer(self):
        if hasattr(self, "layout_save_timer"):
            timer = self.layout_save_timer
            return timer.isActive()
        else:
            return False
