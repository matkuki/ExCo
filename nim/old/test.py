import nimpy_lexers

class Lexer:
    def __init__(self):
        pass
    
    def SendScintilla(self):
        print("Inside SendScintilla")

class Editor:
    def text(self):
        return "Test STRing čćžđšpfdf!\n" * 10

nimpy_lexers.python_style_text(0,1,10,Lexer(),Editor())
