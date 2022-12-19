# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2022 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

"""
Sessions
"""
session_structures = {
    "mark-1": {
        "name": str,
        "chain": str,
        "main-window-files": list,
        "upper-window-files": list,
        "lower-window-files": list,
    },
    "mark-2": {
        "name": str,
        "layout": str
    },
}


"""
Settings tables
"""
# Editor settings
editor = {
    "default": {
        'autocompletion': True,
        'brace_color': "#80ff9900",
        'cursor_line_visible': False,
        'edge_marker_color': "#ffb4b4b4",
        'edge_marker_column': 90,
        'edge_marker_visible': False,
        'end_of_line_mode': 2,
        'end_of_line_visibility': False,
        'maximum_highlights': 300,
        'overwrite_mode': False,
        'tab_width': 4,
        'word_wrap': False,
        'zoom_factor': 0,
    },
}

# Keyboard shortcuts
keyboard_shortcuts = {
    "default": {
        "general": {
            'bookmark_goto': [
                'Alt+0',
                'Alt+1',
                'Alt+2',
                'Alt+3',
                'Alt+4',
                'Alt+5',
                'Alt+6',
                'Alt+7',
                'Alt+8',
                'Alt+9'
            ],
            'bookmark_store': [
                'Alt+Shift+0',
                'Alt+Shift+1',
                'Alt+Shift+2',
                'Alt+Shift+3',
                'Alt+Shift+4',
                'Alt+Shift+5',
                'Alt+Shift+6',
                'Alt+Shift+7',
                'Alt+Shift+8',
                'Alt+Shift+9'
            ],
            'bookmark_toggle': 'Ctrl+B',
            'clear_highlights': 'Ctrl+Shift+G',
            'close_tab': 'Ctrl+W',
            'cwd_tree': 'F7',
            'cwd_explorer': 'Alt+F7',
            'new_cwd_tree': 'Ctrl+F7',
            'find': 'Ctrl+F',
            'find_and_replace': 'Ctrl+Shift+F',
            'find_brace': 'Ctrl+J',
            'find_files': 'Ctrl+F1',
            'find_in_documents': 'Ctrl+F4',
            'find_in_files': 'Ctrl+F2',
            'find_replace_in_documents': 'Ctrl+F5',
            'goto_line': 'Ctrl+M',
            'highlight': 'Ctrl+G',
            'indent_to_cursor': 'Ctrl+I',
            'lower_focus': 'Ctrl+3',
            'main_focus': 'Ctrl+1',
            'maximize_window': 'F11',
            'move_tab_left': 'Ctrl+,',
            'move_tab_right': 'Ctrl+.',
            'new_file': 'Ctrl+N',
            'node_tree': 'F8',
            'open_file': 'Ctrl+O',
            'regex_find': 'Alt+F',
            'regex_find_and_replace': 'Alt+Shift+F',
            'regex_highlight': 'Alt+G',
            'regex_replace_all': 'Alt+Shift+H',
            'regex_replace_selection': 'Alt+H',
            'reload_file': 'F9',
            'repeat_eval': 'F3',
            'repl_focus_multi': 'Ctrl+5',
            'repl_focus_single_1': 'Ctrl+R',
            'repl_focus_single_2': 'Ctrl+4',
            'replace_all': 'Ctrl+Shift+H',
            'replace_all_in_documents': 'Ctrl+F6',
            'replace_in_files': 'Ctrl+F3',
            'replace_selection': 'Ctrl+H',
            'reset_zoom': 'Alt+Z',
            'save_file': 'Ctrl+S',
            'saveas_file': 'Ctrl+Shift+S',
            'spin_clockwise': 'Ctrl+PgDown',
            'spin_counterclockwise': 'Ctrl+PgUp',
            'system_tabs_toggle': 'F1',
            'to_lowercase': 'Alt+L',
            'to_uppercase': 'Alt+U',
            'toggle_autocompletion': 'Ctrl+K',
            'toggle_comment': 'Ctrl+Shift+C',
            'toggle_edge': 'Ctrl+E',
            'toggle_log': 'F10',
            'toggle_messages': 'F7',
            'toggle_mode': 'F5',
            'toggle_wrap': 'Ctrl+P',
            'upper_focus': 'Ctrl+2',
            'function_wheel_toggle': 'F1',
            'select_tab_left': 'Ctrl+,',
            'select_tab_right': 'Ctrl+.',
            'toggle_main_window_side': 'F6',
    
        },
        "editor": {
            'cancel': 'Escape',
            'charleft': 'Left',
            'charleftextend': 'Left+Shift',
            'charleftrectextend': 'Left+Alt+Shift',
            'charright': 'Right',
            'charrightextend': 'Right+Shift',
            'charrightrectextend': 'Right+Alt+Shift',
            'clear': 'Delete',
            'copy': 'Ctrl+C',
            'cut': 'Ctrl+X',
            'delete_end_of_line': 'Ctrl+Shift+Delete',
            'delete_end_of_word': 'Ctrl+Delete',
            'delete_start_of_line': 'Ctrl+Shift+BackSpace',
            'delete_start_of_word': 'Ctrl+BackSpace',
            'deleteback': 'Backspace',
            'deleteback_word': 'Backspace+Shift',
            'edittoggleovertype': 'Insert',
            'go_to_end': 'Ctrl+End',
            'go_to_start': 'Ctrl+Home',
            'homedisplay': 'Home+Alt',
            'indent': 'Tab',
            'line_copy': 'Ctrl+Shift+T',
            'line_cut': 'Ctrl+L',
            'line_delete': 'Ctrl+Shift+L',
            'line_selection_duplicate': 'Ctrl+D',
            'line_transpose': 'Ctrl+T',
            'linedown': 'Down',
            'linedownextend': 'Down+Shift',
            'linedownrectextend': 'Down+Alt+Shift',
            'lineend': 'End',
            'lineenddisplay': 'End+Alt',
            'lineendextend': 'End+Shift',
            'lineendrectextend': 'End+Alt+Shift',
            'linescrolldown': 'Down+Ctrl',
            'linescrollup': 'Up+Ctrl',
            'lineup': 'Up',
            'lineupextend': 'Up+Shift',
            'lineuprectextend': 'Up+Alt+Shift',
            'lowercase': 'U+Ctrl',
            'newline': 'Return',
            'newline2': 'Return+Shift',
            'pagedownrectextend': 'PageDown+Alt+Shift',
            'pageuprectextend': 'PageUp+Alt+Shift',
            'paradown': ']+Ctrl',
            'paradownextend': ']+Ctrl+Shift',
            'paraup': '[+Ctrl',
            'paraupextend': '[+Ctrl+Shift',
            'paste': 'Ctrl+V',
            'redo': 'Ctrl+Y',
            'scroll_down': 'PageDown',
            'scroll_up': 'PageUp',
            'select_all': 'Ctrl+A',
            'select_page_down': 'Shift+PageDown',
            'select_page_up': 'Shift+PageUp',
            'select_to_end': 'Ctrl+Shift+End',
            'select_to_start': 'Ctrl+Shift+Home',
            'setzoom': 'Divide+Ctrl',
            'undo': 'Ctrl+Z',
            'unindent': 'Shift+Tab',
            'uppercase': 'U+Ctrl+Shift',
            'vchome': 'Home',
            'vchomeextend': 'Home+Shift',
            'vchomerectextend': 'Home+Alt+Shift',
            'wordleft': 'Left+Ctrl',
            'wordleftextend': 'Left+Shift+Ctrl',
            'wordpartleft': '/+Ctrl',
            'wordpartleftextend': '/+Ctrl+Shift',
            'wordpartright': '\\+Ctrl',
            'wordpartrightextend': '\\+Ctrl+Shift',
            'wordright': 'Right+Ctrl',
            'wordrightextend': 'Right+Shift+Ctrl',
            'zoomin': 'Ctrl++',
            'zoomout': 'Ctrl+-',
        },
    }
}

# Default layout
default_layout = """
{
    "WINDOW-SIZE": [
        1000,
        600
    ],
    "BOXES": {
        "0": {
            "BOX-H": {
                "0": {
                    "BOX-V": {
                        "0": {
                            "TABS": {
                                "CURRENT-INDEX": -1
                            }
                        }
                    },
                    "SIZES": [
                        600
                    ]
                },
                "1": {
                    "BOX-V": {
                        "0": {
                            "BOX-H": {
                                "0": {
                                    "TABS": {
                                        "CURRENT-INDEX": -1
                                    }
                                }
                            },
                            "SIZES": [
                                300
                            ]
                        },
                        "1": {
                            "BOX-H": {
                                "0": {
                                    "TABS": {
                                        "CURRENT-INDEX": -1
                                    }
                                }
                            },
                            "SIZES": [
                                300
                            ]
                        }
                    },
                    "SIZES": [
                        300,
                        300
                    ]
                }
            },
            "SIZES": [
                600,
                400
            ]
        }
    }
}
"""

# One-window layout
one_window_layout = """
{{
    "WINDOW-SIZE": [
        {0},
        {1}
    ],
    "BOXES": {{
        "0": {{
            "BOX-V": {{
                "0": {{
                    "TABS": {{
                        "CURRENT-INDEX": -1
                    }}
                }}
            }},
            "SIZES": [
                {1}
            ]
        }}
    }}
}}
"""