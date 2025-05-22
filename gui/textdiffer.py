"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import inspect
import functools
import difflib
import settings
import functions
import qt
import data
import constants
import components.actionfilter
import components.internals

from .customeditor import *

"""
----------------------------------------------------------------------------
Object for displaying text difference between two files
----------------------------------------------------------------------------
"""
class TextDiffer(qt.QWidget):
    """A widget that holds two PlainEditors for displaying text difference"""
    #Class variables
    _parent                 = None
    main_form               = None
    name                    = ""
    savable                 = constants.CanSave.NO
    current_icon            = None
    internals        = None
    focused_editor          = None
    text_1                  = None
    text_2                  = None
    text_1_name             = None
    text_2_name             = None
    #Class constants
    DEFAULT_FONT            = qt.QFont(data.current_font_name, data.current_font_size)
    MARGIN_STYLE            = qt.QsciScintilla.STYLE_LINENUMBER
    INDICATOR_UNIQUE_1          = 1
    Indicator_Unique_1_Color    = qt.QColor(0x72, 0x9f, 0xcf, 80)
    INDICATOR_UNIQUE_2          = 2
    Indicator_Unique_2_Color    = qt.QColor(0xad, 0x7f, 0xa8, 80)
    INDICATOR_SIMILAR           = 3
    Indicator_Similar_Color     = qt.QColor(0x8a, 0xe2, 0x34, 80)
    GET_X_OFFSET    = qt.QsciScintillaBase.SCI_GETXOFFSET
    SET_X_OFFSET    = qt.QsciScintillaBase.SCI_SETXOFFSET
    UPDATE_H_SCROLL = qt.QsciScintillaBase.SC_UPDATE_H_SCROLL
    UPDATE_V_SCROLL = qt.QsciScintillaBase.SC_UPDATE_V_SCROLL
    #Diff icons
    icon_unique_1   = None
    icon_unique_2   = None
    icon_similar    = None
    #Marker references
    marker_unique_1         = None
    marker_unique_2         = None
    marker_unique_symbol_1  = None
    marker_unique_symbol_2  = None
    marker_similar_1        = None
    marker_similar_2        = None
    marker_similar_symbol_1 = None
    marker_similar_symbol_2 = None
    #Child widgets
    splitter    = None
    editor_1    = None
    editor_2    = None
    layout      = None


    def __del__(self):
        try:
            self.editor_1.mousePressEvent = None
            self.editor_1.wheelEvent = None
            self.editor_2.mousePressEvent = None
            self.editor_2.wheelEvent = None
            self.editor_1.actual_parent = None
            self.editor_2.actual_parent = None
            self.editor_1.__del__()
            self.editor_2.__del__()
            self.editor_1 = None
            self.editor_2 = None
            self.focused_editor = None
            self.splitter.setParent(None)
            self.splitter = None
            self.layout = None
            self._parent = None
            self.main_form = None
            self.internals = None
            # Clean up self
            self.setParent(None)
            self.deleteLater()
            """
            The actual clean up will occur when the next garbage collection
            cycle is executed, probably because of the nested functions and
            the focus decorator.
            """
        except:
            pass

    def __init__(self,
                 parent,
                 main_form,
                 text_1=None,
                 text_2=None,
                 text_1_name="",
                 text_2_name=""):
        """Initialization"""
        # Initialize the superclass
        super().__init__(parent)
        # Initialize components
        self.internals = components.internals.Internals(self, parent)
        # Initialize colors according to theme
        self.Indicator_Unique_1_Color = qt.QColor(data.theme["textdiffercolors"]["indicator-unique-1-color"])
        self.Indicator_Unique_2_Color = qt.QColor(data.theme["textdiffercolors"]["indicator-unique-2-color"])
        self.Indicator_Similar_Color = qt.QColor(data.theme["textdiffercolors"]["indicator-similar-color"])
        # Store the reference to the parent
        self._parent = parent
        # Store the reference to the main form
        self.main_form = main_form
        # Set the differ icon
        self.current_icon = functions.create_icon('tango_icons/compare-text.png')
        #Set the name of the differ widget
        if text_1_name != None and text_2_name != None:
            self.name = "Text difference: {:s} / {:s}".format(text_1_name, text_2_name)
            self.text_1_name = text_1_name
            self.text_2_name = text_2_name
        else:
            self.name = "Text difference"
            self.text_1_name = "TEXT 1"
            self.text_2_name = "TEXT 2"
        # Initialize diff icons
        self.icon_unique_1  = functions.create_icon("tango_icons/diff-unique-1.png")
        self.icon_unique_2  = functions.create_icon("tango_icons/diff-unique-2.png")
        self.icon_similar   = functions.create_icon("tango_icons/diff-similar.png")
        # Create the horizontal splitter and two editor widgets
        self.splitter = qt.QSplitter(qt.Qt.Orientation.Horizontal, self)
        self.editor_1 = CustomEditor(self, main_form)
        self.init_editor(self.editor_1)
        self.editor_2 = CustomEditor(self, main_form)
        self.init_editor(self.editor_2)
        self.editor_1.choose_lexer("text")
        self.editor_2.choose_lexer("text")
        self.splitter.addWidget(self.editor_1)
        self.splitter.addWidget(self.editor_2)
        self.layout = qt.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.splitter)
        # Set the layout
        self.setLayout(self.layout)
        # Connect the necessary signals
        self.editor_1.SCN_UPDATEUI.connect(self._scn_updateui_1)
        self.editor_2.SCN_UPDATEUI.connect(self._scn_updateui_2)
        self.editor_1.cursorPositionChanged.connect(self._cursor_change_1)
        self.editor_2.cursorPositionChanged.connect(self._cursor_change_2)
        # Overwrite the CustomEditor parent widgets to point to the TextDiffers' PARENT
        self.editor_1._parent = self._parent
        self.editor_2._parent = self._parent
        # Add a new attribute to the CustomEditor that will hold the TextDiffer reference
        self.editor_1.actual_parent = self
        self.editor_2.actual_parent = self
        # Set the embedded flag
        self.editor_1.embedded = True
        self.editor_2.embedded = True
        # Add decorators to each editors mouse clicks and mouse wheel scrolls
        def focus_decorator(function_to_decorate, focused_editor):
            def decorated_function(*args, **kwargs):
                self.focused_editor = focused_editor
                function_to_decorate(*args, **kwargs)
            return decorated_function
        self.editor_1.mousePressEvent = focus_decorator(
            self.editor_1.mousePressEvent,
            self.editor_1
        )
        self.editor_1.wheelEvent = focus_decorator(
            self.editor_1.wheelEvent,
            self.editor_1
        )
        self.editor_2.mousePressEvent = focus_decorator(
            self.editor_2.mousePressEvent,
            self.editor_2
        )
        self.editor_2.wheelEvent = focus_decorator(
            self.editor_2.wheelEvent,
            self.editor_2
        )
        # Add corner buttons
        self.add_corner_buttons()
        # Focus the first editor on initialization
        self.focused_editor = self.editor_1
        self.focused_editor.setFocus()
        # Initialize markers
        self.init_markers()
        # Set the theme
        self.set_theme(data.theme)
        # Set editor functions that have to be propagated from the TextDiffer
        # to the child editor
        self._init_editor_functions()
        # Check the text validity
        if text_1 == None or text_2 == None:
            #One of the texts is unspecified
            return
        # Create the diff
        self.compare(text_1, text_2)

    def _scn_updateui_1(self, sc_update):
        """Function connected to the SCN_UPDATEUI signal for scroll detection"""
        if self.focused_editor == self.editor_1:
            #Scroll the opposite editor
            if sc_update == self.UPDATE_H_SCROLL:
                current_x_offset = self.editor_1.SendScintilla(self.GET_X_OFFSET)
                self.editor_2.SendScintilla(self.SET_X_OFFSET, current_x_offset)
            elif sc_update == self.UPDATE_V_SCROLL:
                current_top_line = self.editor_1.firstVisibleLine()
                self.editor_2.setFirstVisibleLine(current_top_line)

    def _scn_updateui_2(self, sc_update):
        """Function connected to the SCN_UPDATEUI signal for scroll detection"""
        if self.focused_editor == self.editor_2:
            #Scroll the opposite editor
            if sc_update == self.UPDATE_H_SCROLL:
                current_x_offset = self.editor_2.SendScintilla(self.GET_X_OFFSET)
                self.editor_1.SendScintilla(self.SET_X_OFFSET, current_x_offset)
            elif sc_update == self.UPDATE_V_SCROLL:
                current_top_line = self.editor_2.firstVisibleLine()
                self.editor_1.setFirstVisibleLine(current_top_line)

    def _cursor_change_1(self, line, index):
        """
        Function connected to the cursorPositionChanged signal for
        cursor position change detection
        """
        if self.focused_editor == self.editor_1:
            #Update the cursor position on the opposite editor
            cursor_line, cursor_index = self.editor_1.getCursorPosition()
            #Check if the opposite editor line is long enough
            if self.editor_2.lineLength(cursor_line) > cursor_index:
                self.editor_2.setCursorPosition(cursor_line, cursor_index)
            else:
                self.editor_2.setCursorPosition(cursor_line, 0)
            #Update the first visible line, so that the views in both differs match
            current_top_line = self.editor_1.firstVisibleLine()
            self.editor_2.setFirstVisibleLine(current_top_line)

    def _cursor_change_2(self, line, index):
        """
        Function connected to the cursorPositionChanged signal for
        cursor position change detection
        """
        if self.focused_editor == self.editor_2:
            #Update the cursor position on the opposite editor
            cursor_line, cursor_index = self.editor_2.getCursorPosition()
            #Check if the opposite editor line is long enough
            if self.editor_1.lineLength(cursor_line) > cursor_index:
                self.editor_1.setCursorPosition(cursor_line, cursor_index)
            else:
                self.editor_1.setCursorPosition(cursor_line, 0)
            #Update the first visible line, so that the views in both differs match
            current_top_line = self.editor_2.firstVisibleLine()
            self.editor_1.setFirstVisibleLine(current_top_line)

    def _update_margins(self):
        """Update the text margin width"""
        self.editor_1.setMarginWidth(0, "0" * len(str(self.editor_1.lines())))
        self.editor_2.setMarginWidth(0, "0" * len(str(self.editor_2.lines())))

    def _signal_editor_cursor_change(self, cursor_line=None, cursor_column=None):
        """Signal that fires when cursor position changes in one of the editors"""
        self.main_form.display.update_cursor_position(cursor_line, cursor_column)

    def _init_editor_functions(self):
        """
        Initialize the editor functions that are called on the TextDiffer widget,
        but need to be executed on one of the editors
        """
        #Find text function propagated to the focused editor
        def enabled_function(*args, **kwargs):
            #Get the function
            function = getattr(self.focused_editor, args[0])
            #Call the function˘, leaving out the "function name" argument
            function(*args[1:], **kwargs)
        #Unimplemented functions
        def uniplemented_function(*args, **kwargs):
            self.main_form.display.repl_display_message(
                "Function '{:s}' is not implemented by the TextDiffer!".format(args[0]),
                message_type=constants.MessageType.ERROR
            )
        all_editor_functions = inspect.getmembers(
            CustomEditor,
            predicate=inspect.isfunction
        )
        skip_functions = [
            "set_theme",
            "__del__",
        ]
        enabled_functions = [
            "find_text",
        ]
        disabled_functions = [
            "__init__",
            "__setattr__",
            "_filter_keypress",
            "_filter_keyrelease",
            "_init_special_functions",
            "_set_indicator",
            "find_text",
            "keyPressEvent",
            "keyReleaseEvent",
            "mousePressEvent",
            "setFocus",
            "wheelEvent",
        ]
        #Check methods
        for function in all_editor_functions:
            if function[0] in skip_functions:
                #Use the TextDiffer implementation of this function
                continue
            if function[0] in enabled_functions:
                #Find text is enabled
                setattr(
                    self,
                    function[0],
                    functools.partial(enabled_function, function[0])
                )
            elif function[0] in disabled_functions:
                #Disabled functions should be skipped, they are probably already
                #implemented by the TextDiffer
                continue
            else:
                #Unimplemented functions should display an error message
                setattr(
                    self,
                    function[0],
                    functools.partial(uniplemented_function, function[0])
                )

    def mousePressEvent(self, event):
        """Overloaded mouse click event"""
        #Execute the superclass mouse click event
        super().mousePressEvent(event)
        #Set focus to the clicked editor
        self.setFocus()
        #Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self._parent
        #Hide the function wheel if it is shown
        self.main_form.view.hide_all_overlay_widgets()
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()

    def setFocus(self):
        """Overridden focus event"""
        #Execute the superclass focus function
        super().setFocus()
        #Check indication
        self.main_form.view.indication_check()
        #Focus the last focused editor
        self.focused_editor.setFocus()

    def init_margin(self,
                    editor,
                    marker_unique,
                    marker_unique_symbol,
                    marker_similar,
                    marker_similar_symbol):
        """Initialize margin for coloring lines showing diff symbols"""
        editor.setMarginWidth(0, "0")
        #Setting the margin width to 0 makes the marker colour the entire line
        #to the marker background color
        editor.setMarginWidth(1, "00")
        editor.setMarginWidth(2, 0)
        editor.setMarginType(0, qt.QsciScintilla.MarginType.TextMargin)
        editor.setMarginType(1, qt.QsciScintilla.MarginType.SymbolMargin)
        editor.setMarginType(2, qt.QsciScintilla.MarginType.SymbolMargin)
        #I DON'T KNOW THE ENTIRE LOGIC BEHIND MARKERS AND MARGINS! If you set
        #something wrong in the margin mask, the markers on a different margin don't appear!
        #http://www.scintilla.org/ScintillaDoc.html#SCI_SETMARGINMASKN
        editor.setMarginMarkerMask(
            1,
            ~qt.QsciScintillaBase.SC_MASK_FOLDERS
        )
        editor.setMarginMarkerMask(
            2,
            0x0
        )

    def init_markers(self):
        """Initialize all markers for showing diff symbols"""
        #Set the images
        image_scale_size = functions.create_size(16, 16)
        image_unique_1  = functions.create_pixmap('tango_icons/diff-unique-1.png')
        image_unique_2  = functions.create_pixmap('tango_icons/diff-unique-2.png')
        image_similar   = functions.create_pixmap('tango_icons/diff-similar.png')
        #Scale the images to a smaller size
        image_unique_1  = image_unique_1.scaled(image_scale_size)
        image_unique_2  = image_unique_2.scaled(image_scale_size)
        image_similar   = image_similar.scaled(image_scale_size)
        #Markers for editor 1
        self.marker_unique_1            = self.editor_1.markerDefine(qt.QsciScintilla.MarkerSymbol.Background, 0)
        self.marker_unique_symbol_1     = self.editor_1.markerDefine(image_unique_1, 1)
        self.marker_similar_1           = self.editor_1.markerDefine(qt.QsciScintilla.MarkerSymbol.Background, 2)
        self.marker_similar_symbol_1    = self.editor_1.markerDefine(image_similar, 3)
        #Set background colors only for the background markers
        self.editor_1.setMarkerBackgroundColor(self.Indicator_Unique_1_Color, self.marker_unique_1)
        self.editor_1.setMarkerBackgroundColor(self.Indicator_Similar_Color, self.marker_similar_1)
        #Margins for editor 1
        self.init_margin(
            self.editor_1,
            self.marker_unique_1,
            self.marker_unique_symbol_1,
            self.marker_similar_1,
            self.marker_similar_symbol_1
        )
        #Markers for editor 2
        self.marker_unique_2            = self.editor_2.markerDefine(qt.QsciScintilla.MarkerSymbol.Background, 0)
        self.marker_unique_symbol_2     = self.editor_2.markerDefine(image_unique_2, 1)
        self.marker_similar_2           = self.editor_2.markerDefine(qt.QsciScintilla.MarkerSymbol.Background, 2)
        self.marker_similar_symbol_2    = self.editor_2.markerDefine(image_similar, 3)
        #Set background colors only for the background markers
        self.editor_2.setMarkerBackgroundColor(self.Indicator_Unique_2_Color, self.marker_unique_2)
        self.editor_2.setMarkerBackgroundColor(self.Indicator_Similar_Color, self.marker_similar_2)
        #Margins for editor 2
        self.init_margin(
            self.editor_2,
            self.marker_unique_2,
            self.marker_unique_symbol_2,
            self.marker_similar_2,
            self.marker_similar_symbol_2
        )

    def init_indicator(self,
                       editor,
                       indicator,
                       color):
        """
        Set the indicator settings
        """
        editor.indicatorDefine(
            qt.QsciScintillaBase.INDIC_ROUNDBOX,
            indicator
        )
        editor.setIndicatorForegroundColor(
            color,
            indicator
        )
        editor.SendScintilla(
            qt.QsciScintillaBase.SCI_SETINDICATORCURRENT,
            indicator
        )

    def init_editor(self, editor):
        """Initialize all of the PlainEditor settings for difference displaying"""
        editor.setLexer(None)
        editor.setUtf8(True)
        editor.setIndentationsUseTabs(False)
        editor.setFont(self.DEFAULT_FONT)
        editor.setBraceMatching(qt.QsciScintilla.BraceMatch.SloppyBraceMatch)
        editor.setMatchedBraceBackgroundColor(qt.QColor(255, 153, 0))
        editor.setAcceptDrops(False)
        editor.setEolMode(qt.QsciScintilla.EolMode(settings.editor['end_of_line_mode']))
        editor.setReadOnly(True)
        editor.savable = constants.CanSave.NO

    def set_margin_text(self, editor, line, text):
        """Set the editor's margin text at the selected line"""
        editor.setMarginText(line, text, self.MARGIN_STYLE)

    def set_line_indicator(self, editor, line, indicator_index):
        """Set the editor's selected line color"""
        #Set the indicator
        if indicator_index == self.INDICATOR_UNIQUE_1:
            self.init_indicator(
                editor,
                self.INDICATOR_UNIQUE_1,
                self.Indicator_Unique_1_Color
            )
        elif indicator_index == self.INDICATOR_UNIQUE_2:
            self.init_indicator(
                editor,
                self.INDICATOR_UNIQUE_2,
                self.Indicator_Unique_2_Color
            )
        elif indicator_index == self.INDICATOR_SIMILAR:
            self.init_indicator(
                editor,
                self.INDICATOR_SIMILAR,
                self.Indicator_Similar_Color
            )
        #Color the line background
        scintilla_command = qt.QsciScintillaBase.SCI_INDICATORFILLRANGE
        start   = editor.positionFromLineIndex(line, 0)
        length  = editor.lineLength(line)
        editor.SendScintilla(
            scintilla_command,
            start,
            length
        )

    def compare(self, text_1, text_2):
        """
        Compare two text strings and display the difference
        !! This function uses Python's difflib which is not 100% accurate !!
        """
        #Store the original text
        self.text_1 = text_1
        self.text_2 = text_2
        text_1_list = text_1.split("\n")
        text_2_list = text_2.split("\n")
        #Create the difference
        differer = difflib.Differ()
        list_sum = list(differer.compare(text_1_list, text_2_list))
        #Assemble the two lists of strings that will be displayed in each editor
        list_1              = []
        line_counter_1      = 1
        line_numbering_1    = []
        line_styling_1      = []
        list_2              = []
        line_counter_2      = 1
        line_numbering_2    = []
        line_styling_2      = []
        #Flow control flags
        skip_next     = False
        store_next    = False
        for i, line in enumerate(list_sum):
            if store_next == True:
                store_next = False
                list_2.append(line[2:])
                line_numbering_2.append(str(line_counter_2))
                line_counter_2 += 1
                line_styling_2.append(self.INDICATOR_SIMILAR)
            elif skip_next == False:
                if line.startswith("  "):
                    #The line is the same in both texts
                    list_1.append(line[2:])
                    line_numbering_1.append(str(line_counter_1))
                    line_counter_1 += 1
                    line_styling_1.append(None)
                    list_2.append(line[2:])
                    line_numbering_2.append(str(line_counter_2))
                    line_counter_2 += 1
                    line_styling_2.append(None)
                elif line.startswith("- "):
                    #The line is unique to text 1
                    list_1.append(line[2:])
                    line_numbering_1.append(str(line_counter_1))
                    line_counter_1 += 1
                    line_styling_1.append(self.INDICATOR_UNIQUE_1)
                    list_2.append("")
                    line_numbering_2.append("")
                    line_styling_2.append(None)
                elif line.startswith("+ "):
                    #The line is unique to text 2
                    list_1.append("")
                    line_numbering_1.append("")
                    line_styling_1.append(None)
                    list_2.append(line[2:])
                    line_numbering_2.append(str(line_counter_2))
                    line_counter_2 += 1
                    line_styling_2.append(self.INDICATOR_UNIQUE_2)
                elif line.startswith("? "):
                    #The line is similar
                    if (list_sum[i-1].startswith("- ") and
                        len(list_sum) > (i+1) and
                        list_sum[i+1].startswith("+ ") and
                        len(list_sum) > (i+2) and
                        list_sum[i+2].startswith("? ")):
                        """
                        Line order:
                            - ...
                            ? ...
                            + ...
                            ? ...
                        """
                        #Lines have only a few character difference, skip the
                        #first '?' and handle the next '?' as a "'- '/'+ '/'? '" sequence
                        pass
                    elif list_sum[i-1].startswith("- "):
                        #Line in text 1 has something added
                        """
                        Line order:
                            - ...
                            ? ...
                            + ...
                        """
                        line_styling_1[len(line_numbering_1) - 1] = self.INDICATOR_SIMILAR

                        list_2.pop()
                        line_numbering_2.pop()
                        line_styling_2.pop()
                        store_next = True
                    elif list_sum[i-1].startswith("+ "):
                        #Line in text 2 has something added
                        """
                        Line order:
                            - ...
                            + ...
                            ? ...
                        """
                        list_1.pop()
                        line_numbering_1.pop()
                        line_styling_1.pop()
                        line_styling_1[len(line_numbering_1) - 1] = self.INDICATOR_SIMILAR

                        pop_index_2 = (len(line_numbering_2) - 1) - 1
                        list_2.pop(pop_index_2)
                        line_numbering_2.pop(pop_index_2)
                        line_styling_2.pop()
                        line_styling_2.pop()
                        line_styling_2.append(self.INDICATOR_SIMILAR)
            else:
                skip_next = False
        #Display the results
        self.editor_1.setText("\n".join(list_1))
        self.editor_2.setText("\n".join(list_2))
        #Set margins and style for both editors
        for i, line in enumerate(line_numbering_1):
            self.set_margin_text(self.editor_1, i, line)
            line_styling = line_styling_1[i]
            if line_styling != None:
                if line_styling == self.INDICATOR_SIMILAR:
                    self.editor_1.markerAdd(i, self.marker_similar_1)
                    self.editor_1.markerAdd(i, self.marker_similar_symbol_1)
                else:
                    self.editor_1.markerAdd(i, self.marker_unique_1)
                    self.editor_1.markerAdd(i, self.marker_unique_symbol_1)
        for i, line in enumerate(line_numbering_2):
            self.set_margin_text(self.editor_2, i, line)
            line_styling = line_styling_2[i]
            if line_styling != None:
                if line_styling == self.INDICATOR_SIMILAR:
                    self.editor_2.markerAdd(i, self.marker_similar_2)
                    self.editor_2.markerAdd(i, self.marker_similar_symbol_2)
                else:
                    self.editor_2.markerAdd(i, self.marker_unique_2)
                    self.editor_2.markerAdd(i, self.marker_unique_symbol_2)
        #Check if there were any differences
        if (any(line_styling_1) == False and any(line_styling_2) == False):
            self.main_form.display.repl_display_message(
                "No differences between texts.",
                message_type=constants.MessageType.SUCCESS
            )
        else:
            #Count the number of differences
            difference_counter_1 = 0
            #Similar line count is the same in both editor line stylings
            similarity_counter = 0
            for diff in line_styling_1:
                if diff != None:
                    if diff == self.INDICATOR_SIMILAR:
                        similarity_counter += 1
                    else:
                        difference_counter_1 += 1
            difference_counter_2 = 0
            for diff in line_styling_2:
                if diff != None:
                    if diff == self.INDICATOR_SIMILAR:
                        #Skip the similar line, which were already counter above
                        continue
                    else:
                        difference_counter_2 += 1
            #Display the differences/similarities messages
            self.main_form.display.repl_display_message(
                "{:d} differences found in '{:s}'!".format(difference_counter_1, self.text_1_name),
                message_type=constants.MessageType.DIFF_UNIQUE_1
            )
            self.main_form.display.repl_display_message(
                "{:d} differences found in '{:s}'!".format(difference_counter_2, self.text_2_name),
                message_type=constants.MessageType.DIFF_UNIQUE_2
            )
            self.main_form.display.repl_display_message(
                "{:d} similarities found between documents!".format(similarity_counter, self.text_2_name),
                message_type=constants.MessageType.DIFF_SIMILAR
            )
        self._update_margins()

    def find_next_unique_1(self):
        """Find and scroll to the first unique 1 difference"""
        self.focused_editor         = self.editor_1
        cursor_line, cursor_index   = self.editor_1.getCursorPosition()
        next_unique_diff_line = self.editor_1.markerFindNext(cursor_line+1, 0b0011)
        #Correct the line numbering to the 1..line_count display
        next_unique_diff_line += 1
        self.editor_1.goto_line(next_unique_diff_line, skip_repl_focus=False)
        self.editor_2.goto_line(next_unique_diff_line, skip_repl_focus=False)
        #Check if we are back at the start of the document
        if next_unique_diff_line == 0:
            self.main_form.display.repl_display_message(
                "Scrolled back to the start of the document!",
                message_type=constants.MessageType.DIFF_UNIQUE_1
            )
            self.main_form.display.write_to_statusbar(
                "Scrolled back to the start of the document!"
            )

    def find_next_unique_2(self):
        """Find and scroll to the first unique 2 difference"""
        self.focused_editor         = self.editor_2
        cursor_line, cursor_index   = self.editor_2.getCursorPosition()
        next_unique_diff_line = self.editor_2.markerFindNext(cursor_line+1, 0b0011)
        #Correct the line numbering to the 1..line_count display
        next_unique_diff_line += 1
        self.editor_1.goto_line(next_unique_diff_line, skip_repl_focus=False)
        self.editor_2.goto_line(next_unique_diff_line, skip_repl_focus=False)
        #Check if we are back at the start of the document
        if next_unique_diff_line == 0:
            self.main_form.display.repl_display_message(
                "Scrolled back to the start of the document!",
                message_type=constants.MessageType.DIFF_UNIQUE_2
            )
            self.main_form.display.write_to_statusbar(
                "Scrolled back to the start of the document!"
            )

    def find_next_similar(self):
        """Find and scroll to the first similar line"""
        self.focused_editor         = self.editor_1
        cursor_line, cursor_index   = self.editor_1.getCursorPosition()
        next_unique_diff_line = self.editor_1.markerFindNext(cursor_line+1, 0b1100)
        #Correct the line numbering to the 1..line_count display
        next_unique_diff_line += 1
        self.editor_1.goto_line(next_unique_diff_line, skip_repl_focus=False)
        self.editor_2.goto_line(next_unique_diff_line, skip_repl_focus=False)
        #Check if we are back at the start of the document
        if next_unique_diff_line == 0:
            self.main_form.display.repl_display_message(
                "Scrolled back to the start of the document!",
                message_type=constants.MessageType.DIFF_SIMILAR
            )
            self.main_form.display.write_to_statusbar(
                "Scrolled back to the start of the document!"
            )

    def add_corner_buttons(self):
        # Unique 1 button
        self.internals.add_corner_button(
            functions.create_icon("tango_icons/diff-unique-1.png"),
            "Scroll to next unique line\nin document: '{:s}'".format(
                self.text_1_name
            ),
            self.find_next_unique_1
        )
        # Unique 2 button
        self.internals.add_corner_button(
            functions.create_icon("tango_icons/diff-unique-2.png"),
            "Scroll to next unique line\nin document: '{:s}'".format(
                self.text_2_name
            ),
            self.find_next_unique_2
        )
        # Similar button
        self.internals.add_corner_button(
            functions.create_icon("tango_icons/diff-similar.png"),
            "Scroll to next similar line\nin both documents",
            self.find_next_similar
        )

    def set_theme(self, theme):
        def set_editor_theme(editor):
            if theme["name"] == "Air":
                editor.resetFoldMarginColors()
            elif theme["name"] == "Earth":
                editor.setFoldMarginColors(
                    qt.QColor(theme["foldmargin"]["foreground"]),
                    qt.QColor(theme["foldmargin"]["background"])
                )
            editor.setMarginsForegroundColor(qt.QColor(theme["linemargin"]["foreground"]))
            editor.setMarginsBackgroundColor(qt.QColor(theme["linemargin"]["background"]))
            editor.SendScintilla(
                qt.QsciScintillaBase.SCI_STYLESETBACK,
                qt.QsciScintillaBase.STYLE_DEFAULT,
                qt.QColor(theme["fonts"]["default"]["color"])
            )
            editor.SendScintilla(
                qt.QsciScintillaBase.SCI_STYLESETBACK,
                qt.QsciScintillaBase.STYLE_LINENUMBER,
                qt.QColor(theme["linemargin"]["background"])
            )
            editor.SendScintilla(
                qt.QsciScintillaBase.SCI_SETCARETFORE,
                qt.QColor(theme["cursor"])
            )
            editor.choose_lexer("text")
        set_editor_theme(self.editor_1)
        set_editor_theme(self.editor_2)
