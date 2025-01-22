# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import qt
import data
import lexers


missing_themes = {}

class AVS(qt.QsciLexerAVS):
    styles = {
        "BlockComment" : 1,
        "ClipProperty" : 13,
        "Default" : 0,
        "Filter" : 10,
        "Function" : 12,
        "Identifier" : 6,
        "Keyword" : 9,
        "KeywordSet6" : 14,
        "LineComment" : 3,
        "NestedBlockComment" : 2,
        "Number" : 4,
        "Operator" : 5,
        "Plugin" : 11,
        "String" : 7,
        "TripleString" : 8,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['AVS'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['AVS']):
                   missing_themes['AVS'].append(style)
        if len(missing_themes['AVS']) != 0:
            print("Lexer 'AVS' missing themes:")
            for mt in missing_themes['AVS']:
                print('    - ' + mt)
            raise Exception("Lexer 'AVS' has missing themes!")

class Bash(qt.QsciLexerBash):
    styles = {
        "Backticks" : 11,
        "Comment" : 2,
        "Default" : 0,
        "DoubleQuotedString" : 5,
        "Error" : 1,
        "HereDocumentDelimiter" : 12,
        "Identifier" : 8,
        "Keyword" : 4,
        "Number" : 3,
        "Operator" : 7,
        "ParameterExpansion" : 10,
        "Scalar" : 9,
        "SingleQuotedHereDocument" : 13,
        "SingleQuotedString" : 6,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Bash'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Bash']):
                   missing_themes['Bash'].append(style)
        if len(missing_themes['Bash']) != 0:
            print("Lexer 'Bash' missing themes:")
            for mt in missing_themes['Bash']:
                print('    - ' + mt)
            raise Exception("Lexer 'Bash' has missing themes!")

class Batch(qt.QsciLexerBatch):
    styles = {
        "Comment" : 1,
        "Default" : 0,
        "ExternalCommand" : 5,
        "HideCommandChar" : 4,
        "Keyword" : 2,
        "Label" : 3,
        "Operator" : 7,
        "Variable" : 6,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Batch'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Batch']):
                   missing_themes['Batch'].append(style)
        if len(missing_themes['Batch']) != 0:
            print("Lexer 'Batch' missing themes:")
            for mt in missing_themes['Batch']:
                print('    - ' + mt)
            raise Exception("Lexer 'Batch' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Batch']):
                   missing_themes['Batch'].append(style)
        if len(missing_themes['Batch']) != 0:
            print("Lexer 'Batch' missing themes:")
            for mt in missing_themes['Batch']:
                print('    - ' + mt)
            raise Exception("Lexer 'Batch' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Batch']):
                   missing_themes['Batch'].append(style)
        if len(missing_themes['Batch']) != 0:
            print("Lexer 'Batch' missing themes:")
            for mt in missing_themes['Batch']:
                print('    - ' + mt)
            raise Exception("Lexer 'Batch' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Batch']):
                   missing_themes['Batch'].append(style)
        if len(missing_themes['Batch']) != 0:
            print("Lexer 'Batch' missing themes:")
            for mt in missing_themes['Batch']:
                print('    - ' + mt)
            raise Exception("Lexer 'Batch' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Batch']):
                   missing_themes['Batch'].append(style)
        if len(missing_themes['Batch']) != 0:
            print("Lexer 'Batch' missing themes:")
            for mt in missing_themes['Batch']:
                print('    - ' + mt)
            raise Exception("Lexer 'Batch' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Batch']):
                   missing_themes['Batch'].append(style)
        if len(missing_themes['Batch']) != 0:
            print("Lexer 'Batch' missing themes:")
            for mt in missing_themes['Batch']:
                print('    - ' + mt)
            raise Exception("Lexer 'Batch' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Batch']):
                   missing_themes['Batch'].append(style)
        if len(missing_themes['Batch']) != 0:
            print("Lexer 'Batch' missing themes:")
            for mt in missing_themes['Batch']:
                print('    - ' + mt)
            raise Exception("Lexer 'Batch' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Batch']):
                   missing_themes['Batch'].append(style)
        if len(missing_themes['Batch']) != 0:
            print("Lexer 'Batch' missing themes:")
            for mt in missing_themes['Batch']:
                print('    - ' + mt)
            raise Exception("Lexer 'Batch' has missing themes!")

class CMake(qt.QsciLexerCMake):
    styles = {
        "BlockForeach" : 10,
        "BlockIf" : 11,
        "BlockMacro" : 12,
        "BlockWhile" : 9,
        "Comment" : 1,
        "Default" : 0,
        "Function" : 5,
        "KeywordSet3" : 8,
        "Label" : 7,
        "Number" : 14,
        "String" : 2,
        "StringLeftQuote" : 3,
        "StringRightQuote" : 4,
        "StringVariable" : 13,
        "Variable" : 6,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['CMake'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CMake']):
                   missing_themes['CMake'].append(style)
        if len(missing_themes['CMake']) != 0:
            print("Lexer 'CMake' missing themes:")
            for mt in missing_themes['CMake']:
                print('    - ' + mt)
            raise Exception("Lexer 'CMake' has missing themes!")

class CPP(qt.QsciLexerCPP):
    styles = {
        "Comment" : 1,
        "CommentDoc" : 3,
        "CommentDocKeyword" : 17,
        "CommentDocKeywordError" : 18,
        "CommentLine" : 2,
        "CommentLineDoc" : 15,
        "Default" : 0,
        "DoubleQuotedString" : 6,
        "EscapeSequence" : 27,
        "GlobalClass" : 19,
        "HashQuotedString" : 22,
        "Identifier" : 11,
        "InactiveComment" : 65,
        "InactiveCommentDoc" : 67,
        "InactiveCommentDocKeyword" : 81,
        "InactiveCommentDocKeywordError" : 82,
        "InactiveCommentLine" : 66,
        "InactiveCommentLineDoc" : 79,
        "InactiveDefault" : 64,
        "InactiveDoubleQuotedString" : 70,
        "InactiveEscapeSequence" : 91,
        "InactiveGlobalClass" : 83,
        "InactiveHashQuotedString" : 86,
        "InactiveIdentifier" : 75,
        "InactiveKeyword" : 69,
        "InactiveKeywordSet2" : 80,
        "InactiveNumber" : 68,
        "InactiveOperator" : 74,
        "InactivePreProcessor" : 73,
        "InactivePreProcessorComment" : 87,
        "InactivePreProcessorCommentLineDoc" : 88,
        "InactiveRawString" : 84,
        "InactiveRegex" : 78,
        "InactiveSingleQuotedString" : 71,
        "InactiveTaskMarker" : 90,
        "InactiveTripleQuotedVerbatimString" : 85,
        "InactiveUUID" : 72,
        "InactiveUnclosedString" : 76,
        "InactiveUserLiteral" : 89,
        "InactiveVerbatimString" : 77,
        "Keyword" : 5,
        "KeywordSet2" : 16,
        "Number" : 4,
        "Operator" : 10,
        "PreProcessor" : 9,
        "PreProcessorComment" : 23,
        "PreProcessorCommentLineDoc" : 24,
        "RawString" : 20,
        "Regex" : 14,
        "SingleQuotedString" : 7,
        "TaskMarker" : 26,
        "TripleQuotedVerbatimString" : 21,
        "UUID" : 8,
        "UnclosedString" : 12,
        "UserLiteral" : 25,
        "VerbatimString" : 13,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['CPP'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CPP']):
                   missing_themes['CPP'].append(style)
        if len(missing_themes['CPP']) != 0:
            print("Lexer 'CPP' missing themes:")
            for mt in missing_themes['CPP']:
                print('    - ' + mt)
            raise Exception("Lexer 'CPP' has missing themes!")

class CSS(qt.QsciLexerCSS):
    styles = {
        "AtRule" : 12,
        "Attribute" : 16,
        "CSS1Property" : 6,
        "CSS2Property" : 15,
        "CSS3Property" : 17,
        "ClassSelector" : 2,
        "Comment" : 9,
        "Default" : 0,
        "DoubleQuotedString" : 13,
        "ExtendedCSSProperty" : 19,
        "ExtendedPseudoClass" : 20,
        "ExtendedPseudoElement" : 21,
        "IDSelector" : 10,
        "Important" : 11,
        "MediaRule" : 22,
        "Operator" : 5,
        "PseudoClass" : 3,
        "PseudoElement" : 18,
        "SingleQuotedString" : 14,
        "Tag" : 1,
        "UnknownProperty" : 7,
        "UnknownPseudoClass" : 4,
        "Value" : 8,
        "Variable" : 23,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['CSS'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSS']):
                   missing_themes['CSS'].append(style)
        if len(missing_themes['CSS']) != 0:
            print("Lexer 'CSS' missing themes:")
            for mt in missing_themes['CSS']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSS' has missing themes!")

class CSharp(qt.QsciLexerCSharp):
    styles = {
        "Comment" : 1,
        "CommentDoc" : 3,
        "CommentDocKeyword" : 17,
        "CommentDocKeywordError" : 18,
        "CommentLine" : 2,
        "CommentLineDoc" : 15,
        "Default" : 0,
        "DoubleQuotedString" : 6,
        "EscapeSequence" : 27,
        "GlobalClass" : 19,
        "HashQuotedString" : 22,
        "Identifier" : 11,
        "InactiveComment" : 65,
        "InactiveCommentDoc" : 67,
        "InactiveCommentDocKeyword" : 81,
        "InactiveCommentDocKeywordError" : 82,
        "InactiveCommentLine" : 66,
        "InactiveCommentLineDoc" : 79,
        "InactiveDefault" : 64,
        "InactiveDoubleQuotedString" : 70,
        "InactiveEscapeSequence" : 91,
        "InactiveGlobalClass" : 83,
        "InactiveHashQuotedString" : 86,
        "InactiveIdentifier" : 75,
        "InactiveKeyword" : 69,
        "InactiveKeywordSet2" : 80,
        "InactiveNumber" : 68,
        "InactiveOperator" : 74,
        "InactivePreProcessor" : 73,
        "InactivePreProcessorComment" : 87,
        "InactivePreProcessorCommentLineDoc" : 88,
        "InactiveRawString" : 84,
        "InactiveRegex" : 78,
        "InactiveSingleQuotedString" : 71,
        "InactiveTaskMarker" : 90,
        "InactiveTripleQuotedVerbatimString" : 85,
        "InactiveUUID" : 72,
        "InactiveUnclosedString" : 76,
        "InactiveUserLiteral" : 89,
        "InactiveVerbatimString" : 77,
        "Keyword" : 5,
        "KeywordSet2" : 16,
        "Number" : 4,
        "Operator" : 10,
        "PreProcessor" : 9,
        "PreProcessorComment" : 23,
        "PreProcessorCommentLineDoc" : 24,
        "RawString" : 20,
        "Regex" : 14,
        "SingleQuotedString" : 7,
        "TaskMarker" : 26,
        "TripleQuotedVerbatimString" : 21,
        "UUID" : 8,
        "UnclosedString" : 12,
        "UserLiteral" : 25,
        "VerbatimString" : 13,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['CSharp'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CSharp']):
                   missing_themes['CSharp'].append(style)
        if len(missing_themes['CSharp']) != 0:
            print("Lexer 'CSharp' missing themes:")
            for mt in missing_themes['CSharp']:
                print('    - ' + mt)
            raise Exception("Lexer 'CSharp' has missing themes!")

class CoffeeScript(qt.QsciLexerCoffeeScript):
    styles = {
        "BlockRegex" : 23,
        "BlockRegexComment" : 24,
        "Comment" : 1,
        "CommentBlock" : 22,
        "CommentDoc" : 3,
        "CommentDocKeyword" : 17,
        "CommentDocKeywordError" : 18,
        "CommentLine" : 2,
        "CommentLineDoc" : 15,
        "Default" : 0,
        "DoubleQuotedString" : 6,
        "GlobalClass" : 19,
        "Identifier" : 11,
        "InstanceProperty" : 25,
        "Keyword" : 5,
        "KeywordSet2" : 16,
        "Number" : 4,
        "Operator" : 10,
        "PreProcessor" : 9,
        "Regex" : 14,
        "SingleQuotedString" : 7,
        "UUID" : 8,
        "UnclosedString" : 12,
        "VerbatimString" : 13,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['CoffeeScript'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['CoffeeScript']):
                   missing_themes['CoffeeScript'].append(style)
        if len(missing_themes['CoffeeScript']) != 0:
            print("Lexer 'CoffeeScript' missing themes:")
            for mt in missing_themes['CoffeeScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'CoffeeScript' has missing themes!")

class Custom(qt.QsciLexerCustom):
    styles = {
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Custom'] = []

class D(qt.QsciLexerD):
    styles = {
        "BackquoteString" : 18,
        "Character" : 12,
        "Comment" : 1,
        "CommentDoc" : 3,
        "CommentDocKeyword" : 16,
        "CommentDocKeywordError" : 17,
        "CommentLine" : 2,
        "CommentLineDoc" : 15,
        "CommentNested" : 4,
        "Default" : 0,
        "Identifier" : 14,
        "Keyword" : 6,
        "KeywordDoc" : 8,
        "KeywordSecondary" : 7,
        "KeywordSet5" : 20,
        "KeywordSet6" : 21,
        "KeywordSet7" : 22,
        "Number" : 5,
        "Operator" : 13,
        "RawString" : 19,
        "String" : 10,
        "Typedefs" : 9,
        "UnclosedString" : 11,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['D'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['D']):
                   missing_themes['D'].append(style)
        if len(missing_themes['D']) != 0:
            print("Lexer 'D' missing themes:")
            for mt in missing_themes['D']:
                print('    - ' + mt)
            raise Exception("Lexer 'D' has missing themes!")

class Diff(qt.QsciLexerDiff):
    styles = {
        "AddingPatchAdded" : 8,
        "AddingPatchRemoved" : 10,
        "Command" : 2,
        "Comment" : 1,
        "Default" : 0,
        "Header" : 3,
        "LineAdded" : 6,
        "LineChanged" : 7,
        "LineRemoved" : 5,
        "Position" : 4,
        "RemovingPatchAdded" : 9,
        "RemovingPatchRemoved" : 11,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Diff'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Diff']):
                   missing_themes['Diff'].append(style)
        if len(missing_themes['Diff']) != 0:
            print("Lexer 'Diff' missing themes:")
            for mt in missing_themes['Diff']:
                print('    - ' + mt)
            raise Exception("Lexer 'Diff' has missing themes!")

class Fortran77(qt.QsciLexerFortran77):
    styles = {
        "Comment" : 1,
        "Continuation" : 14,
        "Default" : 0,
        "DottedOperator" : 12,
        "DoubleQuotedString" : 4,
        "ExtendedFunction" : 10,
        "Identifier" : 7,
        "IntrinsicFunction" : 9,
        "Keyword" : 8,
        "Label" : 13,
        "Number" : 2,
        "Operator" : 6,
        "PreProcessor" : 11,
        "SingleQuotedString" : 3,
        "UnclosedString" : 5,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Fortran77'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran77']):
                   missing_themes['Fortran77'].append(style)
        if len(missing_themes['Fortran77']) != 0:
            print("Lexer 'Fortran77' missing themes:")
            for mt in missing_themes['Fortran77']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran77' has missing themes!")

class Fortran(qt.QsciLexerFortran):
    styles = {
        "Comment" : 1,
        "Continuation" : 14,
        "Default" : 0,
        "DottedOperator" : 12,
        "DoubleQuotedString" : 4,
        "ExtendedFunction" : 10,
        "Identifier" : 7,
        "IntrinsicFunction" : 9,
        "Keyword" : 8,
        "Label" : 13,
        "Number" : 2,
        "Operator" : 6,
        "PreProcessor" : 11,
        "SingleQuotedString" : 3,
        "UnclosedString" : 5,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Fortran'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Fortran']):
                   missing_themes['Fortran'].append(style)
        if len(missing_themes['Fortran']) != 0:
            print("Lexer 'Fortran' missing themes:")
            for mt in missing_themes['Fortran']:
                print('    - ' + mt)
            raise Exception("Lexer 'Fortran' has missing themes!")

class HTML(qt.QsciLexerHTML):
    styles = {
        "ASPAtStart" : 15,
        "ASPJavaScriptComment" : 57,
        "ASPJavaScriptCommentDoc" : 59,
        "ASPJavaScriptCommentLine" : 58,
        "ASPJavaScriptDefault" : 56,
        "ASPJavaScriptDoubleQuotedString" : 63,
        "ASPJavaScriptKeyword" : 62,
        "ASPJavaScriptNumber" : 60,
        "ASPJavaScriptRegex" : 67,
        "ASPJavaScriptSingleQuotedString" : 64,
        "ASPJavaScriptStart" : 55,
        "ASPJavaScriptSymbol" : 65,
        "ASPJavaScriptUnclosedString" : 66,
        "ASPJavaScriptWord" : 61,
        "ASPPythonClassName" : 114,
        "ASPPythonComment" : 107,
        "ASPPythonDefault" : 106,
        "ASPPythonDoubleQuotedString" : 109,
        "ASPPythonFunctionMethodName" : 115,
        "ASPPythonIdentifier" : 117,
        "ASPPythonKeyword" : 111,
        "ASPPythonNumber" : 108,
        "ASPPythonOperator" : 116,
        "ASPPythonSingleQuotedString" : 110,
        "ASPPythonStart" : 105,
        "ASPPythonTripleDoubleQuotedString" : 113,
        "ASPPythonTripleSingleQuotedString" : 112,
        "ASPStart" : 16,
        "ASPVBScriptComment" : 82,
        "ASPVBScriptDefault" : 81,
        "ASPVBScriptIdentifier" : 86,
        "ASPVBScriptKeyword" : 84,
        "ASPVBScriptNumber" : 83,
        "ASPVBScriptStart" : 80,
        "ASPVBScriptString" : 85,
        "ASPVBScriptUnclosedString" : 87,
        "ASPXCComment" : 20,
        "Attribute" : 3,
        "CDATA" : 17,
        "Default" : 0,
        "Entity" : 10,
        "HTMLComment" : 9,
        "HTMLDoubleQuotedString" : 6,
        "HTMLNumber" : 5,
        "HTMLSingleQuotedString" : 7,
        "HTMLValue" : 19,
        "JavaScriptComment" : 42,
        "JavaScriptCommentDoc" : 44,
        "JavaScriptCommentLine" : 43,
        "JavaScriptDefault" : 41,
        "JavaScriptDoubleQuotedString" : 48,
        "JavaScriptKeyword" : 47,
        "JavaScriptNumber" : 45,
        "JavaScriptRegex" : 52,
        "JavaScriptSingleQuotedString" : 49,
        "JavaScriptStart" : 40,
        "JavaScriptSymbol" : 50,
        "JavaScriptUnclosedString" : 51,
        "JavaScriptWord" : 46,
        "OtherInTag" : 8,
        "PHPComment" : 124,
        "PHPCommentLine" : 125,
        "PHPDefault" : 118,
        "PHPDoubleQuotedString" : 119,
        "PHPDoubleQuotedVariable" : 126,
        "PHPKeyword" : 121,
        "PHPNumber" : 122,
        "PHPOperator" : 127,
        "PHPSingleQuotedString" : 120,
        "PHPStart" : 18,
        "PHPVariable" : 123,
        "PythonClassName" : 99,
        "PythonComment" : 92,
        "PythonDefault" : 91,
        "PythonDoubleQuotedString" : 94,
        "PythonFunctionMethodName" : 100,
        "PythonIdentifier" : 102,
        "PythonKeyword" : 96,
        "PythonNumber" : 93,
        "PythonOperator" : 101,
        "PythonSingleQuotedString" : 95,
        "PythonStart" : 90,
        "PythonTripleDoubleQuotedString" : 98,
        "PythonTripleSingleQuotedString" : 97,
        "SGMLBlockDefault" : 31,
        "SGMLCommand" : 22,
        "SGMLComment" : 29,
        "SGMLDefault" : 21,
        "SGMLDoubleQuotedString" : 24,
        "SGMLEntity" : 28,
        "SGMLError" : 26,
        "SGMLParameter" : 23,
        "SGMLParameterComment" : 30,
        "SGMLSingleQuotedString" : 25,
        "SGMLSpecial" : 27,
        "Script" : 14,
        "Tag" : 1,
        "UnknownAttribute" : 4,
        "UnknownTag" : 2,
        "VBScriptComment" : 72,
        "VBScriptDefault" : 71,
        "VBScriptIdentifier" : 76,
        "VBScriptKeyword" : 74,
        "VBScriptNumber" : 73,
        "VBScriptStart" : 70,
        "VBScriptString" : 75,
        "VBScriptUnclosedString" : 77,
        "XMLEnd" : 13,
        "XMLStart" : 12,
        "XMLTagEnd" : 11,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['HTML'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['HTML']):
                   missing_themes['HTML'].append(style)
        if len(missing_themes['HTML']) != 0:
            print("Lexer 'HTML' missing themes:")
            for mt in missing_themes['HTML']:
                print('    - ' + mt)
            raise Exception("Lexer 'HTML' has missing themes!")

class IDL(qt.QsciLexerIDL):
    styles = {
        "Comment" : 1,
        "CommentDoc" : 3,
        "CommentDocKeyword" : 17,
        "CommentDocKeywordError" : 18,
        "CommentLine" : 2,
        "CommentLineDoc" : 15,
        "Default" : 0,
        "DoubleQuotedString" : 6,
        "EscapeSequence" : 27,
        "GlobalClass" : 19,
        "HashQuotedString" : 22,
        "Identifier" : 11,
        "InactiveComment" : 65,
        "InactiveCommentDoc" : 67,
        "InactiveCommentDocKeyword" : 81,
        "InactiveCommentDocKeywordError" : 82,
        "InactiveCommentLine" : 66,
        "InactiveCommentLineDoc" : 79,
        "InactiveDefault" : 64,
        "InactiveDoubleQuotedString" : 70,
        "InactiveEscapeSequence" : 91,
        "InactiveGlobalClass" : 83,
        "InactiveHashQuotedString" : 86,
        "InactiveIdentifier" : 75,
        "InactiveKeyword" : 69,
        "InactiveKeywordSet2" : 80,
        "InactiveNumber" : 68,
        "InactiveOperator" : 74,
        "InactivePreProcessor" : 73,
        "InactivePreProcessorComment" : 87,
        "InactivePreProcessorCommentLineDoc" : 88,
        "InactiveRawString" : 84,
        "InactiveRegex" : 78,
        "InactiveSingleQuotedString" : 71,
        "InactiveTaskMarker" : 90,
        "InactiveTripleQuotedVerbatimString" : 85,
        "InactiveUUID" : 72,
        "InactiveUnclosedString" : 76,
        "InactiveUserLiteral" : 89,
        "InactiveVerbatimString" : 77,
        "Keyword" : 5,
        "KeywordSet2" : 16,
        "Number" : 4,
        "Operator" : 10,
        "PreProcessor" : 9,
        "PreProcessorComment" : 23,
        "PreProcessorCommentLineDoc" : 24,
        "RawString" : 20,
        "Regex" : 14,
        "SingleQuotedString" : 7,
        "TaskMarker" : 26,
        "TripleQuotedVerbatimString" : 21,
        "UUID" : 8,
        "UnclosedString" : 12,
        "UserLiteral" : 25,
        "VerbatimString" : 13,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['IDL'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['IDL']):
                   missing_themes['IDL'].append(style)
        if len(missing_themes['IDL']) != 0:
            print("Lexer 'IDL' missing themes:")
            for mt in missing_themes['IDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'IDL' has missing themes!")

class JSON(qt.QsciLexerJSON):
    styles = {
        "CommentBlock" : 7,
        "CommentLine" : 6,
        "Default" : 0,
        "Error" : 13,
        "EscapeSequence" : 5,
        "IRI" : 9,
        "IRICompact" : 10,
        "Keyword" : 11,
        "KeywordLD" : 12,
        "Number" : 1,
        "Operator" : 8,
        "Property" : 4,
        "String" : 2,
        "UnclosedString" : 3,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['JSON'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JSON']):
                   missing_themes['JSON'].append(style)
        if len(missing_themes['JSON']) != 0:
            print("Lexer 'JSON' missing themes:")
            for mt in missing_themes['JSON']:
                print('    - ' + mt)
            raise Exception("Lexer 'JSON' has missing themes!")

class Java(qt.QsciLexerJava):
    styles = {
        "Comment" : 1,
        "CommentDoc" : 3,
        "CommentDocKeyword" : 17,
        "CommentDocKeywordError" : 18,
        "CommentLine" : 2,
        "CommentLineDoc" : 15,
        "Default" : 0,
        "DoubleQuotedString" : 6,
        "EscapeSequence" : 27,
        "GlobalClass" : 19,
        "HashQuotedString" : 22,
        "Identifier" : 11,
        "InactiveComment" : 65,
        "InactiveCommentDoc" : 67,
        "InactiveCommentDocKeyword" : 81,
        "InactiveCommentDocKeywordError" : 82,
        "InactiveCommentLine" : 66,
        "InactiveCommentLineDoc" : 79,
        "InactiveDefault" : 64,
        "InactiveDoubleQuotedString" : 70,
        "InactiveEscapeSequence" : 91,
        "InactiveGlobalClass" : 83,
        "InactiveHashQuotedString" : 86,
        "InactiveIdentifier" : 75,
        "InactiveKeyword" : 69,
        "InactiveKeywordSet2" : 80,
        "InactiveNumber" : 68,
        "InactiveOperator" : 74,
        "InactivePreProcessor" : 73,
        "InactivePreProcessorComment" : 87,
        "InactivePreProcessorCommentLineDoc" : 88,
        "InactiveRawString" : 84,
        "InactiveRegex" : 78,
        "InactiveSingleQuotedString" : 71,
        "InactiveTaskMarker" : 90,
        "InactiveTripleQuotedVerbatimString" : 85,
        "InactiveUUID" : 72,
        "InactiveUnclosedString" : 76,
        "InactiveUserLiteral" : 89,
        "InactiveVerbatimString" : 77,
        "Keyword" : 5,
        "KeywordSet2" : 16,
        "Number" : 4,
        "Operator" : 10,
        "PreProcessor" : 9,
        "PreProcessorComment" : 23,
        "PreProcessorCommentLineDoc" : 24,
        "RawString" : 20,
        "Regex" : 14,
        "SingleQuotedString" : 7,
        "TaskMarker" : 26,
        "TripleQuotedVerbatimString" : 21,
        "UUID" : 8,
        "UnclosedString" : 12,
        "UserLiteral" : 25,
        "VerbatimString" : 13,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Java'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Java']):
                   missing_themes['Java'].append(style)
        if len(missing_themes['Java']) != 0:
            print("Lexer 'Java' missing themes:")
            for mt in missing_themes['Java']:
                print('    - ' + mt)
            raise Exception("Lexer 'Java' has missing themes!")

class JavaScript(qt.QsciLexerJavaScript):
    styles = {
        "Comment" : 1,
        "CommentDoc" : 3,
        "CommentDocKeyword" : 17,
        "CommentDocKeywordError" : 18,
        "CommentLine" : 2,
        "CommentLineDoc" : 15,
        "Default" : 0,
        "DoubleQuotedString" : 6,
        "EscapeSequence" : 27,
        "GlobalClass" : 19,
        "HashQuotedString" : 22,
        "Identifier" : 11,
        "InactiveComment" : 65,
        "InactiveCommentDoc" : 67,
        "InactiveCommentDocKeyword" : 81,
        "InactiveCommentDocKeywordError" : 82,
        "InactiveCommentLine" : 66,
        "InactiveCommentLineDoc" : 79,
        "InactiveDefault" : 64,
        "InactiveDoubleQuotedString" : 70,
        "InactiveEscapeSequence" : 91,
        "InactiveGlobalClass" : 83,
        "InactiveHashQuotedString" : 86,
        "InactiveIdentifier" : 75,
        "InactiveKeyword" : 69,
        "InactiveKeywordSet2" : 80,
        "InactiveNumber" : 68,
        "InactiveOperator" : 74,
        "InactivePreProcessor" : 73,
        "InactivePreProcessorComment" : 87,
        "InactivePreProcessorCommentLineDoc" : 88,
        "InactiveRawString" : 84,
        "InactiveRegex" : 78,
        "InactiveSingleQuotedString" : 71,
        "InactiveTaskMarker" : 90,
        "InactiveTripleQuotedVerbatimString" : 85,
        "InactiveUUID" : 72,
        "InactiveUnclosedString" : 76,
        "InactiveUserLiteral" : 89,
        "InactiveVerbatimString" : 77,
        "Keyword" : 5,
        "KeywordSet2" : 16,
        "Number" : 4,
        "Operator" : 10,
        "PreProcessor" : 9,
        "PreProcessorComment" : 23,
        "PreProcessorCommentLineDoc" : 24,
        "RawString" : 20,
        "Regex" : 14,
        "SingleQuotedString" : 7,
        "TaskMarker" : 26,
        "TripleQuotedVerbatimString" : 21,
        "UUID" : 8,
        "UnclosedString" : 12,
        "UserLiteral" : 25,
        "VerbatimString" : 13,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['JavaScript'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['JavaScript']):
                   missing_themes['JavaScript'].append(style)
        if len(missing_themes['JavaScript']) != 0:
            print("Lexer 'JavaScript' missing themes:")
            for mt in missing_themes['JavaScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'JavaScript' has missing themes!")

class Lua(qt.QsciLexerLua):
    styles = {
        "BasicFunctions" : 13,
        "Character" : 7,
        "Comment" : 1,
        "CoroutinesIOSystemFacilities" : 15,
        "Default" : 0,
        "Identifier" : 11,
        "Keyword" : 5,
        "KeywordSet5" : 16,
        "KeywordSet6" : 17,
        "KeywordSet7" : 18,
        "KeywordSet8" : 19,
        "Label" : 20,
        "LineComment" : 2,
        "LiteralString" : 8,
        "Number" : 4,
        "Operator" : 10,
        "Preprocessor" : 9,
        "String" : 6,
        "StringTableMathsFunctions" : 14,
        "UnclosedString" : 12,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Lua'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Lua']):
                   missing_themes['Lua'].append(style)
        if len(missing_themes['Lua']) != 0:
            print("Lexer 'Lua' missing themes:")
            for mt in missing_themes['Lua']:
                print('    - ' + mt)
            raise Exception("Lexer 'Lua' has missing themes!")

class Makefile(qt.QsciLexerMakefile):
    styles = {
        "Comment" : 1,
        "Default" : 0,
        "Error" : 9,
        "Operator" : 4,
        "Preprocessor" : 2,
        "Target" : 5,
        "Variable" : 3,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Makefile'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Makefile']):
                   missing_themes['Makefile'].append(style)
        if len(missing_themes['Makefile']) != 0:
            print("Lexer 'Makefile' missing themes:")
            for mt in missing_themes['Makefile']:
                print('    - ' + mt)
            raise Exception("Lexer 'Makefile' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Makefile']):
                   missing_themes['Makefile'].append(style)
        if len(missing_themes['Makefile']) != 0:
            print("Lexer 'Makefile' missing themes:")
            for mt in missing_themes['Makefile']:
                print('    - ' + mt)
            raise Exception("Lexer 'Makefile' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Makefile']):
                   missing_themes['Makefile'].append(style)
        if len(missing_themes['Makefile']) != 0:
            print("Lexer 'Makefile' missing themes:")
            for mt in missing_themes['Makefile']:
                print('    - ' + mt)
            raise Exception("Lexer 'Makefile' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Makefile']):
                   missing_themes['Makefile'].append(style)
        if len(missing_themes['Makefile']) != 0:
            print("Lexer 'Makefile' missing themes:")
            for mt in missing_themes['Makefile']:
                print('    - ' + mt)
            raise Exception("Lexer 'Makefile' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Makefile']):
                   missing_themes['Makefile'].append(style)
        if len(missing_themes['Makefile']) != 0:
            print("Lexer 'Makefile' missing themes:")
            for mt in missing_themes['Makefile']:
                print('    - ' + mt)
            raise Exception("Lexer 'Makefile' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Makefile']):
                   missing_themes['Makefile'].append(style)
        if len(missing_themes['Makefile']) != 0:
            print("Lexer 'Makefile' missing themes:")
            for mt in missing_themes['Makefile']:
                print('    - ' + mt)
            raise Exception("Lexer 'Makefile' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Makefile']):
                   missing_themes['Makefile'].append(style)
        if len(missing_themes['Makefile']) != 0:
            print("Lexer 'Makefile' missing themes:")
            for mt in missing_themes['Makefile']:
                print('    - ' + mt)
            raise Exception("Lexer 'Makefile' has missing themes!")

class Markdown(qt.QsciLexerMarkdown):
    styles = {
        "BlockQuote" : 15,
        "CodeBackticks" : 19,
        "CodeBlock" : 21,
        "CodeDoubleBackticks" : 20,
        "Default" : 0,
        "EmphasisAsterisks" : 4,
        "EmphasisUnderscores" : 5,
        "Header1" : 6,
        "Header2" : 7,
        "Header3" : 8,
        "Header4" : 9,
        "Header5" : 10,
        "Header6" : 11,
        "HorizontalRule" : 17,
        "Link" : 18,
        "OrderedListItem" : 14,
        "Prechar" : 12,
        "Special" : 1,
        "StrikeOut" : 16,
        "StrongEmphasisAsterisks" : 2,
        "StrongEmphasisUnderscores" : 3,
        "UnorderedListItem" : 13,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Markdown'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Markdown']):
                   missing_themes['Markdown'].append(style)
        if len(missing_themes['Markdown']) != 0:
            print("Lexer 'Markdown' missing themes:")
            for mt in missing_themes['Markdown']:
                print('    - ' + mt)
            raise Exception("Lexer 'Markdown' has missing themes!")

class Matlab(qt.QsciLexerMatlab):
    styles = {
        "Command" : 2,
        "Comment" : 1,
        "Default" : 0,
        "DoubleQuotedString" : 8,
        "Identifier" : 7,
        "Keyword" : 4,
        "Number" : 3,
        "Operator" : 6,
        "SingleQuotedString" : 5,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Matlab'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Matlab']):
                   missing_themes['Matlab'].append(style)
        if len(missing_themes['Matlab']) != 0:
            print("Lexer 'Matlab' missing themes:")
            for mt in missing_themes['Matlab']:
                print('    - ' + mt)
            raise Exception("Lexer 'Matlab' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Matlab']):
                   missing_themes['Matlab'].append(style)
        if len(missing_themes['Matlab']) != 0:
            print("Lexer 'Matlab' missing themes:")
            for mt in missing_themes['Matlab']:
                print('    - ' + mt)
            raise Exception("Lexer 'Matlab' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Matlab']):
                   missing_themes['Matlab'].append(style)
        if len(missing_themes['Matlab']) != 0:
            print("Lexer 'Matlab' missing themes:")
            for mt in missing_themes['Matlab']:
                print('    - ' + mt)
            raise Exception("Lexer 'Matlab' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Matlab']):
                   missing_themes['Matlab'].append(style)
        if len(missing_themes['Matlab']) != 0:
            print("Lexer 'Matlab' missing themes:")
            for mt in missing_themes['Matlab']:
                print('    - ' + mt)
            raise Exception("Lexer 'Matlab' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Matlab']):
                   missing_themes['Matlab'].append(style)
        if len(missing_themes['Matlab']) != 0:
            print("Lexer 'Matlab' missing themes:")
            for mt in missing_themes['Matlab']:
                print('    - ' + mt)
            raise Exception("Lexer 'Matlab' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Matlab']):
                   missing_themes['Matlab'].append(style)
        if len(missing_themes['Matlab']) != 0:
            print("Lexer 'Matlab' missing themes:")
            for mt in missing_themes['Matlab']:
                print('    - ' + mt)
            raise Exception("Lexer 'Matlab' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Matlab']):
                   missing_themes['Matlab'].append(style)
        if len(missing_themes['Matlab']) != 0:
            print("Lexer 'Matlab' missing themes:")
            for mt in missing_themes['Matlab']:
                print('    - ' + mt)
            raise Exception("Lexer 'Matlab' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Matlab']):
                   missing_themes['Matlab'].append(style)
        if len(missing_themes['Matlab']) != 0:
            print("Lexer 'Matlab' missing themes:")
            for mt in missing_themes['Matlab']:
                print('    - ' + mt)
            raise Exception("Lexer 'Matlab' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Matlab']):
                   missing_themes['Matlab'].append(style)
        if len(missing_themes['Matlab']) != 0:
            print("Lexer 'Matlab' missing themes:")
            for mt in missing_themes['Matlab']:
                print('    - ' + mt)
            raise Exception("Lexer 'Matlab' has missing themes!")

class Octave(qt.QsciLexerOctave):
    styles = {
        "Command" : 2,
        "Comment" : 1,
        "Default" : 0,
        "DoubleQuotedString" : 8,
        "Identifier" : 7,
        "Keyword" : 4,
        "Number" : 3,
        "Operator" : 6,
        "SingleQuotedString" : 5,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Octave'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Octave']):
                   missing_themes['Octave'].append(style)
        if len(missing_themes['Octave']) != 0:
            print("Lexer 'Octave' missing themes:")
            for mt in missing_themes['Octave']:
                print('    - ' + mt)
            raise Exception("Lexer 'Octave' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Octave']):
                   missing_themes['Octave'].append(style)
        if len(missing_themes['Octave']) != 0:
            print("Lexer 'Octave' missing themes:")
            for mt in missing_themes['Octave']:
                print('    - ' + mt)
            raise Exception("Lexer 'Octave' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Octave']):
                   missing_themes['Octave'].append(style)
        if len(missing_themes['Octave']) != 0:
            print("Lexer 'Octave' missing themes:")
            for mt in missing_themes['Octave']:
                print('    - ' + mt)
            raise Exception("Lexer 'Octave' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Octave']):
                   missing_themes['Octave'].append(style)
        if len(missing_themes['Octave']) != 0:
            print("Lexer 'Octave' missing themes:")
            for mt in missing_themes['Octave']:
                print('    - ' + mt)
            raise Exception("Lexer 'Octave' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Octave']):
                   missing_themes['Octave'].append(style)
        if len(missing_themes['Octave']) != 0:
            print("Lexer 'Octave' missing themes:")
            for mt in missing_themes['Octave']:
                print('    - ' + mt)
            raise Exception("Lexer 'Octave' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Octave']):
                   missing_themes['Octave'].append(style)
        if len(missing_themes['Octave']) != 0:
            print("Lexer 'Octave' missing themes:")
            for mt in missing_themes['Octave']:
                print('    - ' + mt)
            raise Exception("Lexer 'Octave' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Octave']):
                   missing_themes['Octave'].append(style)
        if len(missing_themes['Octave']) != 0:
            print("Lexer 'Octave' missing themes:")
            for mt in missing_themes['Octave']:
                print('    - ' + mt)
            raise Exception("Lexer 'Octave' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Octave']):
                   missing_themes['Octave'].append(style)
        if len(missing_themes['Octave']) != 0:
            print("Lexer 'Octave' missing themes:")
            for mt in missing_themes['Octave']:
                print('    - ' + mt)
            raise Exception("Lexer 'Octave' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Octave']):
                   missing_themes['Octave'].append(style)
        if len(missing_themes['Octave']) != 0:
            print("Lexer 'Octave' missing themes:")
            for mt in missing_themes['Octave']:
                print('    - ' + mt)
            raise Exception("Lexer 'Octave' has missing themes!")

class PO(qt.QsciLexerPO):
    styles = {
        "Comment" : 1,
        "Default" : 0,
        "Flags" : 11,
        "Fuzzy" : 8,
        "MessageContext" : 6,
        "MessageContextText" : 7,
        "MessageContextTextEOL" : 14,
        "MessageId" : 2,
        "MessageIdText" : 3,
        "MessageIdTextEOL" : 12,
        "MessageString" : 4,
        "MessageStringText" : 5,
        "MessageStringTextEOL" : 13,
        "ProgrammerComment" : 9,
        "Reference" : 10,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['PO'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PO']):
                   missing_themes['PO'].append(style)
        if len(missing_themes['PO']) != 0:
            print("Lexer 'PO' missing themes:")
            for mt in missing_themes['PO']:
                print('    - ' + mt)
            raise Exception("Lexer 'PO' has missing themes!")

class POV(qt.QsciLexerPOV):
    styles = {
        "BadDirective" : 9,
        "Comment" : 1,
        "CommentLine" : 2,
        "Default" : 0,
        "Directive" : 8,
        "Identifier" : 5,
        "KeywordSet6" : 14,
        "KeywordSet7" : 15,
        "KeywordSet8" : 16,
        "Number" : 3,
        "ObjectsCSGAppearance" : 10,
        "Operator" : 4,
        "PredefinedFunctions" : 13,
        "PredefinedIdentifiers" : 12,
        "String" : 6,
        "TypesModifiersItems" : 11,
        "UnclosedString" : 7,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['POV'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['POV']):
                   missing_themes['POV'].append(style)
        if len(missing_themes['POV']) != 0:
            print("Lexer 'POV' missing themes:")
            for mt in missing_themes['POV']:
                print('    - ' + mt)
            raise Exception("Lexer 'POV' has missing themes!")

class Pascal(qt.QsciLexerPascal):
    styles = {
        "Asm" : 14,
        "Character" : 12,
        "Comment" : 2,
        "CommentLine" : 4,
        "CommentParenthesis" : 3,
        "Default" : 0,
        "HexNumber" : 8,
        "Identifier" : 1,
        "Keyword" : 9,
        "Number" : 7,
        "Operator" : 13,
        "PreProcessor" : 5,
        "PreProcessorParenthesis" : 6,
        "SingleQuotedString" : 10,
        "UnclosedString" : 11,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Pascal'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Pascal']):
                   missing_themes['Pascal'].append(style)
        if len(missing_themes['Pascal']) != 0:
            print("Lexer 'Pascal' missing themes:")
            for mt in missing_themes['Pascal']:
                print('    - ' + mt)
            raise Exception("Lexer 'Pascal' has missing themes!")

class Perl(qt.QsciLexerPerl):
    styles = {
        "Array" : 13,
        "BacktickHereDocument" : 25,
        "BacktickHereDocumentVar" : 62,
        "Backticks" : 20,
        "BackticksVar" : 57,
        "Comment" : 2,
        "DataSection" : 21,
        "Default" : 0,
        "DoubleQuotedHereDocument" : 24,
        "DoubleQuotedHereDocumentVar" : 61,
        "DoubleQuotedString" : 6,
        "DoubleQuotedStringVar" : 43,
        "Error" : 1,
        "FormatBody" : 42,
        "FormatIdentifier" : 41,
        "Hash" : 14,
        "HereDocumentDelimiter" : 22,
        "Identifier" : 11,
        "Keyword" : 5,
        "Number" : 4,
        "Operator" : 10,
        "POD" : 3,
        "PODVerbatim" : 31,
        "QuotedStringQ" : 26,
        "QuotedStringQQ" : 27,
        "QuotedStringQQVar" : 64,
        "QuotedStringQR" : 29,
        "QuotedStringQRVar" : 66,
        "QuotedStringQW" : 30,
        "QuotedStringQX" : 28,
        "QuotedStringQXVar" : 65,
        "Regex" : 17,
        "RegexVar" : 54,
        "Scalar" : 12,
        "SingleQuotedHereDocument" : 23,
        "SingleQuotedString" : 7,
        "SubroutinePrototype" : 40,
        "Substitution" : 18,
        "SubstitutionVar" : 55,
        "SymbolTable" : 15,
        "Translation" : 44,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Perl'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Perl']):
                   missing_themes['Perl'].append(style)
        if len(missing_themes['Perl']) != 0:
            print("Lexer 'Perl' missing themes:")
            for mt in missing_themes['Perl']:
                print('    - ' + mt)
            raise Exception("Lexer 'Perl' has missing themes!")

class PostScript(qt.QsciLexerPostScript):
    styles = {
        "ArrayParenthesis" : 9,
        "BadStringCharacter" : 15,
        "Base85String" : 14,
        "Comment" : 1,
        "DSCComment" : 2,
        "DSCCommentValue" : 3,
        "Default" : 0,
        "DictionaryParenthesis" : 10,
        "HexString" : 13,
        "ImmediateEvalLiteral" : 8,
        "Keyword" : 6,
        "Literal" : 7,
        "Name" : 5,
        "Number" : 4,
        "ProcedureParenthesis" : 11,
        "Text" : 12,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['PostScript'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['PostScript']):
                   missing_themes['PostScript'].append(style)
        if len(missing_themes['PostScript']) != 0:
            print("Lexer 'PostScript' missing themes:")
            for mt in missing_themes['PostScript']:
                print('    - ' + mt)
            raise Exception("Lexer 'PostScript' has missing themes!")

class Properties(qt.QsciLexerProperties):
    styles = {
        "Assignment" : 3,
        "Comment" : 1,
        "Default" : 0,
        "DefaultValue" : 4,
        "Key" : 5,
        "Section" : 2,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Properties'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Properties']):
                   missing_themes['Properties'].append(style)
        if len(missing_themes['Properties']) != 0:
            print("Lexer 'Properties' missing themes:")
            for mt in missing_themes['Properties']:
                print('    - ' + mt)
            raise Exception("Lexer 'Properties' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Properties']):
                   missing_themes['Properties'].append(style)
        if len(missing_themes['Properties']) != 0:
            print("Lexer 'Properties' missing themes:")
            for mt in missing_themes['Properties']:
                print('    - ' + mt)
            raise Exception("Lexer 'Properties' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Properties']):
                   missing_themes['Properties'].append(style)
        if len(missing_themes['Properties']) != 0:
            print("Lexer 'Properties' missing themes:")
            for mt in missing_themes['Properties']:
                print('    - ' + mt)
            raise Exception("Lexer 'Properties' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Properties']):
                   missing_themes['Properties'].append(style)
        if len(missing_themes['Properties']) != 0:
            print("Lexer 'Properties' missing themes:")
            for mt in missing_themes['Properties']:
                print('    - ' + mt)
            raise Exception("Lexer 'Properties' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Properties']):
                   missing_themes['Properties'].append(style)
        if len(missing_themes['Properties']) != 0:
            print("Lexer 'Properties' missing themes:")
            for mt in missing_themes['Properties']:
                print('    - ' + mt)
            raise Exception("Lexer 'Properties' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Properties']):
                   missing_themes['Properties'].append(style)
        if len(missing_themes['Properties']) != 0:
            print("Lexer 'Properties' missing themes:")
            for mt in missing_themes['Properties']:
                print('    - ' + mt)
            raise Exception("Lexer 'Properties' has missing themes!")

class Ruby(qt.QsciLexerRuby):
    styles = {
        "Backticks" : 18,
        "ClassName" : 8,
        "ClassVariable" : 17,
        "Comment" : 2,
        "DataSection" : 19,
        "Default" : 0,
        "DemotedKeyword" : 29,
        "DoubleQuotedString" : 6,
        "Error" : 1,
        "FunctionMethodName" : 9,
        "Global" : 13,
        "HereDocument" : 21,
        "HereDocumentDelimiter" : 20,
        "Identifier" : 11,
        "InstanceVariable" : 16,
        "Keyword" : 5,
        "ModuleName" : 15,
        "Number" : 4,
        "Operator" : 10,
        "POD" : 3,
        "PercentStringQ" : 25,
        "PercentStringq" : 24,
        "PercentStringr" : 27,
        "PercentStringw" : 28,
        "PercentStringx" : 26,
        "Regex" : 12,
        "SingleQuotedString" : 7,
        "Stderr" : 40,
        "Stdin" : 30,
        "Stdout" : 31,
        "Symbol" : 14,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Ruby'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Ruby']):
                   missing_themes['Ruby'].append(style)
        if len(missing_themes['Ruby']) != 0:
            print("Lexer 'Ruby' missing themes:")
            for mt in missing_themes['Ruby']:
                print('    - ' + mt)
            raise Exception("Lexer 'Ruby' has missing themes!")

class SQL(qt.QsciLexerSQL):
    styles = {
        "Comment" : 1,
        "CommentDoc" : 3,
        "CommentDocKeyword" : 17,
        "CommentDocKeywordError" : 18,
        "CommentLine" : 2,
        "CommentLineHash" : 15,
        "Default" : 0,
        "DoubleQuotedString" : 6,
        "Identifier" : 11,
        "Keyword" : 5,
        "KeywordSet5" : 19,
        "KeywordSet6" : 20,
        "KeywordSet7" : 21,
        "KeywordSet8" : 22,
        "Number" : 4,
        "Operator" : 10,
        "PlusComment" : 13,
        "PlusKeyword" : 8,
        "PlusPrompt" : 9,
        "QuotedIdentifier" : 23,
        "QuotedOperator" : 24,
        "SingleQuotedString" : 7,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['SQL'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['SQL']):
                   missing_themes['SQL'].append(style)
        if len(missing_themes['SQL']) != 0:
            print("Lexer 'SQL' missing themes:")
            for mt in missing_themes['SQL']:
                print('    - ' + mt)
            raise Exception("Lexer 'SQL' has missing themes!")

class Spice(qt.QsciLexerSpice):
    styles = {
        "Command" : 2,
        "Comment" : 8,
        "Default" : 0,
        "Delimiter" : 6,
        "Function" : 3,
        "Identifier" : 1,
        "Number" : 5,
        "Parameter" : 4,
        "Value" : 7,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Spice'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Spice']):
                   missing_themes['Spice'].append(style)
        if len(missing_themes['Spice']) != 0:
            print("Lexer 'Spice' missing themes:")
            for mt in missing_themes['Spice']:
                print('    - ' + mt)
            raise Exception("Lexer 'Spice' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Spice']):
                   missing_themes['Spice'].append(style)
        if len(missing_themes['Spice']) != 0:
            print("Lexer 'Spice' missing themes:")
            for mt in missing_themes['Spice']:
                print('    - ' + mt)
            raise Exception("Lexer 'Spice' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Spice']):
                   missing_themes['Spice'].append(style)
        if len(missing_themes['Spice']) != 0:
            print("Lexer 'Spice' missing themes:")
            for mt in missing_themes['Spice']:
                print('    - ' + mt)
            raise Exception("Lexer 'Spice' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Spice']):
                   missing_themes['Spice'].append(style)
        if len(missing_themes['Spice']) != 0:
            print("Lexer 'Spice' missing themes:")
            for mt in missing_themes['Spice']:
                print('    - ' + mt)
            raise Exception("Lexer 'Spice' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Spice']):
                   missing_themes['Spice'].append(style)
        if len(missing_themes['Spice']) != 0:
            print("Lexer 'Spice' missing themes:")
            for mt in missing_themes['Spice']:
                print('    - ' + mt)
            raise Exception("Lexer 'Spice' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Spice']):
                   missing_themes['Spice'].append(style)
        if len(missing_themes['Spice']) != 0:
            print("Lexer 'Spice' missing themes:")
            for mt in missing_themes['Spice']:
                print('    - ' + mt)
            raise Exception("Lexer 'Spice' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Spice']):
                   missing_themes['Spice'].append(style)
        if len(missing_themes['Spice']) != 0:
            print("Lexer 'Spice' missing themes:")
            for mt in missing_themes['Spice']:
                print('    - ' + mt)
            raise Exception("Lexer 'Spice' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Spice']):
                   missing_themes['Spice'].append(style)
        if len(missing_themes['Spice']) != 0:
            print("Lexer 'Spice' missing themes:")
            for mt in missing_themes['Spice']:
                print('    - ' + mt)
            raise Exception("Lexer 'Spice' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Spice']):
                   missing_themes['Spice'].append(style)
        if len(missing_themes['Spice']) != 0:
            print("Lexer 'Spice' missing themes:")
            for mt in missing_themes['Spice']:
                print('    - ' + mt)
            raise Exception("Lexer 'Spice' has missing themes!")

class TCL(qt.QsciLexerTCL):
    styles = {
        "Comment" : 1,
        "CommentBlock" : 21,
        "CommentBox" : 20,
        "CommentLine" : 2,
        "Default" : 0,
        "ExpandKeyword" : 11,
        "ITCLKeyword" : 14,
        "Identifier" : 7,
        "KeywordSet6" : 16,
        "KeywordSet7" : 17,
        "KeywordSet8" : 18,
        "KeywordSet9" : 19,
        "Modifier" : 10,
        "Number" : 3,
        "Operator" : 6,
        "QuotedKeyword" : 4,
        "QuotedString" : 5,
        "Substitution" : 8,
        "SubstitutionBrace" : 9,
        "TCLKeyword" : 12,
        "TkCommand" : 15,
        "TkKeyword" : 13,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['TCL'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TCL']):
                   missing_themes['TCL'].append(style)
        if len(missing_themes['TCL']) != 0:
            print("Lexer 'TCL' missing themes:")
            for mt in missing_themes['TCL']:
                print('    - ' + mt)
            raise Exception("Lexer 'TCL' has missing themes!")

class TeX(qt.QsciLexerTeX):
    styles = {
        "Command" : 4,
        "Default" : 0,
        "Group" : 2,
        "Special" : 1,
        "Symbol" : 3,
        "Text" : 5,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['TeX'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TeX']):
                   missing_themes['TeX'].append(style)
        if len(missing_themes['TeX']) != 0:
            print("Lexer 'TeX' missing themes:")
            for mt in missing_themes['TeX']:
                print('    - ' + mt)
            raise Exception("Lexer 'TeX' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TeX']):
                   missing_themes['TeX'].append(style)
        if len(missing_themes['TeX']) != 0:
            print("Lexer 'TeX' missing themes:")
            for mt in missing_themes['TeX']:
                print('    - ' + mt)
            raise Exception("Lexer 'TeX' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TeX']):
                   missing_themes['TeX'].append(style)
        if len(missing_themes['TeX']) != 0:
            print("Lexer 'TeX' missing themes:")
            for mt in missing_themes['TeX']:
                print('    - ' + mt)
            raise Exception("Lexer 'TeX' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TeX']):
                   missing_themes['TeX'].append(style)
        if len(missing_themes['TeX']) != 0:
            print("Lexer 'TeX' missing themes:")
            for mt in missing_themes['TeX']:
                print('    - ' + mt)
            raise Exception("Lexer 'TeX' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TeX']):
                   missing_themes['TeX'].append(style)
        if len(missing_themes['TeX']) != 0:
            print("Lexer 'TeX' missing themes:")
            for mt in missing_themes['TeX']:
                print('    - ' + mt)
            raise Exception("Lexer 'TeX' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['TeX']):
                   missing_themes['TeX'].append(style)
        if len(missing_themes['TeX']) != 0:
            print("Lexer 'TeX' missing themes:")
            for mt in missing_themes['TeX']:
                print('    - ' + mt)
            raise Exception("Lexer 'TeX' has missing themes!")

class VHDL(qt.QsciLexerVHDL):
    styles = {
        "Attribute" : 10,
        "Comment" : 1,
        "CommentBlock" : 15,
        "CommentLine" : 2,
        "Default" : 0,
        "Identifier" : 6,
        "Keyword" : 8,
        "KeywordSet7" : 14,
        "Number" : 3,
        "Operator" : 5,
        "StandardFunction" : 11,
        "StandardOperator" : 9,
        "StandardPackage" : 12,
        "StandardType" : 13,
        "String" : 4,
        "UnclosedString" : 7,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['VHDL'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['VHDL']):
                   missing_themes['VHDL'].append(style)
        if len(missing_themes['VHDL']) != 0:
            print("Lexer 'VHDL' missing themes:")
            for mt in missing_themes['VHDL']:
                print('    - ' + mt)
            raise Exception("Lexer 'VHDL' has missing themes!")

class Verilog(qt.QsciLexerVerilog):
    styles = {
        "Comment" : 1,
        "CommentBang" : 3,
        "CommentKeyword" : 20,
        "CommentLine" : 2,
        "DeclareInputOutputPort" : 23,
        "DeclareInputPort" : 21,
        "DeclareOutputPort" : 22,
        "Default" : 0,
        "Identifier" : 11,
        "InactiveComment" : 65,
        "InactiveCommentBang" : 67,
        "InactiveCommentKeyword" : 84,
        "InactiveCommentLine" : 66,
        "InactiveDeclareInputOutputPort" : 87,
        "InactiveDeclareInputPort" : 85,
        "InactiveDeclareOutputPort" : 86,
        "InactiveDefault" : 64,
        "InactiveIdentifier" : 75,
        "InactiveKeyword" : 69,
        "InactiveKeywordSet2" : 71,
        "InactiveNumber" : 68,
        "InactiveOperator" : 74,
        "InactivePortConnection" : 88,
        "InactivePreprocessor" : 73,
        "InactiveString" : 70,
        "InactiveSystemTask" : 72,
        "InactiveUnclosedString" : 76,
        "InactiveUserKeywordSet" : 83,
        "Keyword" : 5,
        "KeywordSet2" : 7,
        "Number" : 4,
        "Operator" : 10,
        "PortConnection" : 24,
        "Preprocessor" : 9,
        "String" : 6,
        "SystemTask" : 8,
        "UnclosedString" : 12,
        "UserKeywordSet" : 19,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['Verilog'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['Verilog']):
                   missing_themes['Verilog'].append(style)
        if len(missing_themes['Verilog']) != 0:
            print("Lexer 'Verilog' missing themes:")
            for mt in missing_themes['Verilog']:
                print('    - ' + mt)
            raise Exception("Lexer 'Verilog' has missing themes!")

class XML(qt.QsciLexerXML):
    styles = {
        "ASPAtStart" : 15,
        "ASPJavaScriptComment" : 57,
        "ASPJavaScriptCommentDoc" : 59,
        "ASPJavaScriptCommentLine" : 58,
        "ASPJavaScriptDefault" : 56,
        "ASPJavaScriptDoubleQuotedString" : 63,
        "ASPJavaScriptKeyword" : 62,
        "ASPJavaScriptNumber" : 60,
        "ASPJavaScriptRegex" : 67,
        "ASPJavaScriptSingleQuotedString" : 64,
        "ASPJavaScriptStart" : 55,
        "ASPJavaScriptSymbol" : 65,
        "ASPJavaScriptUnclosedString" : 66,
        "ASPJavaScriptWord" : 61,
        "ASPPythonClassName" : 114,
        "ASPPythonComment" : 107,
        "ASPPythonDefault" : 106,
        "ASPPythonDoubleQuotedString" : 109,
        "ASPPythonFunctionMethodName" : 115,
        "ASPPythonIdentifier" : 117,
        "ASPPythonKeyword" : 111,
        "ASPPythonNumber" : 108,
        "ASPPythonOperator" : 116,
        "ASPPythonSingleQuotedString" : 110,
        "ASPPythonStart" : 105,
        "ASPPythonTripleDoubleQuotedString" : 113,
        "ASPPythonTripleSingleQuotedString" : 112,
        "ASPStart" : 16,
        "ASPVBScriptComment" : 82,
        "ASPVBScriptDefault" : 81,
        "ASPVBScriptIdentifier" : 86,
        "ASPVBScriptKeyword" : 84,
        "ASPVBScriptNumber" : 83,
        "ASPVBScriptStart" : 80,
        "ASPVBScriptString" : 85,
        "ASPVBScriptUnclosedString" : 87,
        "ASPXCComment" : 20,
        "Attribute" : 3,
        "CDATA" : 17,
        "Default" : 0,
        "Entity" : 10,
        "HTMLComment" : 9,
        "HTMLDoubleQuotedString" : 6,
        "HTMLNumber" : 5,
        "HTMLSingleQuotedString" : 7,
        "HTMLValue" : 19,
        "JavaScriptComment" : 42,
        "JavaScriptCommentDoc" : 44,
        "JavaScriptCommentLine" : 43,
        "JavaScriptDefault" : 41,
        "JavaScriptDoubleQuotedString" : 48,
        "JavaScriptKeyword" : 47,
        "JavaScriptNumber" : 45,
        "JavaScriptRegex" : 52,
        "JavaScriptSingleQuotedString" : 49,
        "JavaScriptStart" : 40,
        "JavaScriptSymbol" : 50,
        "JavaScriptUnclosedString" : 51,
        "JavaScriptWord" : 46,
        "OtherInTag" : 8,
        "PHPComment" : 124,
        "PHPCommentLine" : 125,
        "PHPDefault" : 118,
        "PHPDoubleQuotedString" : 119,
        "PHPDoubleQuotedVariable" : 126,
        "PHPKeyword" : 121,
        "PHPNumber" : 122,
        "PHPOperator" : 127,
        "PHPSingleQuotedString" : 120,
        "PHPStart" : 18,
        "PHPVariable" : 123,
        "PythonClassName" : 99,
        "PythonComment" : 92,
        "PythonDefault" : 91,
        "PythonDoubleQuotedString" : 94,
        "PythonFunctionMethodName" : 100,
        "PythonIdentifier" : 102,
        "PythonKeyword" : 96,
        "PythonNumber" : 93,
        "PythonOperator" : 101,
        "PythonSingleQuotedString" : 95,
        "PythonStart" : 90,
        "PythonTripleDoubleQuotedString" : 98,
        "PythonTripleSingleQuotedString" : 97,
        "SGMLBlockDefault" : 31,
        "SGMLCommand" : 22,
        "SGMLComment" : 29,
        "SGMLDefault" : 21,
        "SGMLDoubleQuotedString" : 24,
        "SGMLEntity" : 28,
        "SGMLError" : 26,
        "SGMLParameter" : 23,
        "SGMLParameterComment" : 30,
        "SGMLSingleQuotedString" : 25,
        "SGMLSpecial" : 27,
        "Script" : 14,
        "Tag" : 1,
        "UnknownAttribute" : 4,
        "UnknownTag" : 2,
        "VBScriptComment" : 72,
        "VBScriptDefault" : 71,
        "VBScriptIdentifier" : 76,
        "VBScriptKeyword" : 74,
        "VBScriptNumber" : 73,
        "VBScriptStart" : 70,
        "VBScriptString" : 75,
        "VBScriptUnclosedString" : 77,
        "XMLEnd" : 13,
        "XMLStart" : 12,
        "XMLTagEnd" : 11,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['XML'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['XML']):
                   missing_themes['XML'].append(style)
        if len(missing_themes['XML']) != 0:
            print("Lexer 'XML' missing themes:")
            for mt in missing_themes['XML']:
                print('    - ' + mt)
            raise Exception("Lexer 'XML' has missing themes!")

class YAML(qt.QsciLexerYAML):
    styles = {
        "Comment" : 1,
        "Default" : 0,
        "DocumentDelimiter" : 6,
        "Identifier" : 2,
        "Keyword" : 3,
        "Number" : 4,
        "Operator" : 9,
        "Reference" : 5,
        "SyntaxErrorMarker" : 8,
        "TextBlockMarker" : 7,
    }
    
    def __init__(self, parent=None):
        super().__init__()
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        missing_themes['YAML'] = []
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['YAML']):
                   missing_themes['YAML'].append(style)
        if len(missing_themes['YAML']) != 0:
            print("Lexer 'YAML' missing themes:")
            for mt in missing_themes['YAML']:
                print('    - ' + mt)
            raise Exception("Lexer 'YAML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['YAML']):
                   missing_themes['YAML'].append(style)
        if len(missing_themes['YAML']) != 0:
            print("Lexer 'YAML' missing themes:")
            for mt in missing_themes['YAML']:
                print('    - ' + mt)
            raise Exception("Lexer 'YAML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['YAML']):
                   missing_themes['YAML'].append(style)
        if len(missing_themes['YAML']) != 0:
            print("Lexer 'YAML' missing themes:")
            for mt in missing_themes['YAML']:
                print('    - ' + mt)
            raise Exception("Lexer 'YAML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['YAML']):
                   missing_themes['YAML'].append(style)
        if len(missing_themes['YAML']) != 0:
            print("Lexer 'YAML' missing themes:")
            for mt in missing_themes['YAML']:
                print('    - ' + mt)
            raise Exception("Lexer 'YAML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['YAML']):
                   missing_themes['YAML'].append(style)
        if len(missing_themes['YAML']) != 0:
            print("Lexer 'YAML' missing themes:")
            for mt in missing_themes['YAML']:
                print('    - ' + mt)
            raise Exception("Lexer 'YAML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['YAML']):
                   missing_themes['YAML'].append(style)
        if len(missing_themes['YAML']) != 0:
            print("Lexer 'YAML' missing themes:")
            for mt in missing_themes['YAML']:
                print('    - ' + mt)
            raise Exception("Lexer 'YAML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['YAML']):
                   missing_themes['YAML'].append(style)
        if len(missing_themes['YAML']) != 0:
            print("Lexer 'YAML' missing themes:")
            for mt in missing_themes['YAML']:
                print('    - ' + mt)
            raise Exception("Lexer 'YAML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['YAML']):
                   missing_themes['YAML'].append(style)
        if len(missing_themes['YAML']) != 0:
            print("Lexer 'YAML' missing themes:")
            for mt in missing_themes['YAML']:
                print('    - ' + mt)
            raise Exception("Lexer 'YAML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['YAML']):
                   missing_themes['YAML'].append(style)
        if len(missing_themes['YAML']) != 0:
            print("Lexer 'YAML' missing themes:")
            for mt in missing_themes['YAML']:
                print('    - ' + mt)
            raise Exception("Lexer 'YAML' has missing themes!")
        for style in self.styles.keys():
            try:
                self.setPaper(
                    qt.QColor(data.theme["fonts"][style.lower()]["background"]),
                    self.styles[style]
                )
                lexers.set_font(self, style, theme["fonts"][style.lower()])
            except:
               if not(style in missing_themes['YAML']):
                   missing_themes['YAML'].append(style)
        if len(missing_themes['YAML']) != 0:
            print("Lexer 'YAML' missing themes:")
            for mt in missing_themes['YAML']:
                print('    - ' + mt)
            raise Exception("Lexer 'YAML' has missing themes!")