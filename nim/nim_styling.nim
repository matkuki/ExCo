
import math
import python3
import tables
import strutils
import unicode
import future
import sequtils
import parseutils

type
    Sequence = object
        start*: seq[char]
        stop*: seq[char]
        stop_extra*: seq[char]
        negative_lookbehind*: seq[char]
        style*: int
    
    SeqActive = object
        active*: bool
        sequence*: Sequence

const SCI_GETSTYLEAT = 2010

var styles = {
    "Default" : 0,
    "Comment" : 1,
    "Number" : 2,
    "DoubleQuotedString" : 3,
    "SingleQuotedString" : 4,
    "Keyword" : 5,
    "TripleSingleQuotedString" : 6,
    "TripleDoubleQuotedString" : 7,
    "ClassName" : 8,
    "FunctionMethodName" : 9,
    "Operator" : 10,
    "Identifier" : 11,
    "CommentBlock" : 12,
    "UnclosedString" : 13,
    "HighlightedIdentifier" : 14,
    "Decorator" : 15,
    "CustomKeyword" : 16
}.toTable()

var 
    keywords = [
        "del", "open", "ascii", "bool", "DeprecationWarning", "ReferenceError", "Warning", "yield", "KeyboardInterrupt", "NotADirectoryError", 
        "str","FileNotFoundError", "OverflowError", "is", "FloatingPointError", "with", "repr", "sorted", "WindowsError", "property", 
        "set","FutureWarning", "TimeoutError", "ConnectionAbortedError", "BufferError", "LookupError", "ImportError", "assert", "vars", "complex", 
        "False","memoryview", "UnicodeWarning", "Ellipsis", "global", "zip", "hasattr", "setattr", "AssertionError", "sum", 
        "delattr","frozenset", "True", "TabError", "min", "reversed", "oct", "type", "IndexError", "RecursionError", 
        "hash","help", "SyntaxError", "divmod", "PendingDeprecationWarning", "ConnectionError", "ord", "super", "class", "FileExistsError", 
        "exec","__debug__", "range", "not", "elif", "copyright", "IndentationError", "print", "license", "as", 
        "GeneratorExit","def", "__package__", "hex", "import", "UnicodeTranslateError", "enumerate", "float", "InterruptedError", "and", 
        "ValueError","KeyError", "locals", "__spec__", "__loader__", "ArithmeticError", "raise", "map", "pass", "UnicodeEncodeError", 
        "EnvironmentError","from", "max", "__name__", "EOFError", "SystemError", "for", "IOError", "dir", "next", 
        "all","ConnectionResetError", "any", "staticmethod", "Exception", "eval", "iter", "UserWarning", "UnicodeDecodeError", "break", 
        "ProcessLookupError","StopAsyncIteration", "if", "BrokenPipeError", "None", "slice", "bin", "MemoryError", "finally", "callable", 
        "classmethod","input", "IsADirectoryError", "NameError", "credits", "BaseException", "quit", "getattr", "while", "compile", 
        "bytearray","SyntaxWarning", "TypeError", "or", "abs", "int", "continue", "BytesWarning", "return", "ChildProcessError", 
        "in","StopIteration", "tuple", "PermissionError", "format", "len", "object", "UnicodeError", "__doc__", "pow", 
        "isinstance","RuntimeWarning", "__build_class__", "AttributeError", "OSError", "exit", "globals", "issubclass", "filter", "chr", 
        "round","UnboundLocalError", "ResourceWarning", "id", "bytes", "BlockingIOError", "ImportWarning", "except", "nonlocal", "try", 
        "lambda","__import__", "NotImplemented", "ConnectionRefusedError", "ZeroDivisionError", "list", "SystemExit", "RuntimeError", "NotImplementedError", "dict", 
        "else"
    ]
    custom_keywords = [
        "self"
    ]
    separator_list = [
        ' ', '\t', '\c', '\r', '\l', '(', ')', '[', ']', '{', '}'
    ]
    operator_list = [
        '=', '+', '-', '*', '/', '<', '>', '$', '.',
        '~', '&', '%', '|', '!', '?', '^', '.', ':', ','
    ]
    extended_separators: array[len(separator_list) + len(operator_list), char]
    
extended_separators[0..separator_list.high] = separator_list
extended_separators[separator_list.high+1..len(extended_separators)-1] = operator_list

var
    sq = Sequence(
        start: @['"'], 
        stop: @['"'], 
        stop_extra: @['\l'], 
        negative_lookbehind: @['\\'],
        style: styles["SingleQuotedString"]
    )
    dq = Sequence(
        start: @['\''], 
        stop: @['\''], 
        stop_extra: @['\l'], 
        negative_lookbehind: @['\\'],
        style: styles["DoubleQuotedString"]
    )
    tqd = Sequence(
        start: @['\'','\'','\''], 
        stop: @['\'','\'','\''], 
        stop_extra: @[], 
        negative_lookbehind: @[],
        style: styles["TripleSingleQuotedString"]
    )
    tqs = Sequence(
        start: @['"','"','"'], 
        stop: @['"','"','"'], 
        stop_extra: @[], 
        negative_lookbehind: @[],
        style: styles["TripleDoubleQuotedString"]
    )
    comment = Sequence(
        start: @['#'], 
        stop: @['\l'], 
        stop_extra: @[], 
        negative_lookbehind: @[],
        style: styles["Comment"]
    )
    dcomment = Sequence(
        start: @['#', '#'], 
        stop: @['\l'], 
        stop_extra: @[], 
        negative_lookbehind: @[],
        style: styles["CommentBlock"]
    )
    decorator = Sequence(
        start: @['@'], 
        stop: @[' '], 
        stop_extra: @[], 
        negative_lookbehind: @[],
        style: styles["Decorator"]
    )
    sequence_lists = [
        tqd, tqs, dcomment, comment, decorator, sq, dq
    ]                           
    multiline_sequence_list = [tqd, tqs]
#    sequence_start_strings = lc[x.start | (x <- sequence_lists ), string]

proc python_style_text*(self, args: PyObjectPtr): PyObjectPtr {.exportc, cdecl.} =
    var
        result_object: PyObjectPtr
        value_start, value_end: cint
        lexer, editor: PyObjectPtr
        parse_result: cint
    
    parse_result = argParseTuple(
        args, 
        "iiOO", 
        addr(value_start),
        addr(value_end),
        addr(lexer),
        addr(editor),
    )    
    if parse_result == 0:
        echo "Napaka v pretvarjanju argumentov v funkcijo!"        
        returnNone()
    var
        text_method = objectGetAttr(editor, buildValue("s", cstring("text")))
        text_object = objectCallObject(text_method, tupleNew(0))
        string_object = unicodeAsEncodedString(text_object, "utf-8", nil)
        cstring_whole_text = bytesAsString(string_object)
        whole_text = $cstring_whole_text
        text = whole_text[int(value_start)..int(value_end-1)]
        text_length = len(text)
        current_token: string = ""
    # Prepare the objects that will be called as functions
    var
        start_styling_obj: PyObjectPtr
        start_args: PyObjectPtr
        set_styling_obj: PyObjectPtr
        set_args: PyObjectPtr
        send_scintilla_obj: PyObjectPtr
        send_args: PyObjectPtr
    start_styling_obj = objectGetAttr(lexer, buildValue("s", cstring("startStyling")))
    start_args = tupleNew(1)
    set_styling_obj = objectGetAttr(lexer, buildValue("s", cstring("setStyling")))
    set_args = tupleNew(2)
    send_scintilla_obj = objectGetAttr(editor, buildValue("s", cstring("SendScintilla")))
    send_args = tupleNew(2)
    
    # Template for final cleanup
    template clean_up() =
        xDecref(text_method)
        xDecref(text_object)
        xDecref(string_object)
        xDecref(args)
        xDecref(result_object)
        
        xDecref(start_styling_obj)
        xDecref(start_args)
        xDecref(set_styling_obj)
        xDecref(set_args)
        xDecref(send_scintilla_obj)
        xDecref(send_args)
    # Template for the lexers setStyling function
    template set_styling(length: int, style: int) =
        discard tupleSetItem(set_args, 0, buildValue("i", length))
        discard tupleSetItem(set_args, 1, buildValue("i", style))
        discard objectCallObject(set_styling_obj, set_args)
    # Procedure for getting previous style
    proc get_previous_style(): int =
        discard tupleSetItem(send_args, 0, buildValue("i", SCI_GETSTYLEAT))
        discard tupleSetItem(send_args, 1, buildValue("i", value_start - 1))
        result = longAsLong(objectCallObject(send_scintilla_obj, send_args))
        xDecref(send_args)
    # Template for starting styling
    template start_styling() =
        discard tupleSetItem(start_args, 0, buildValue("i", value_start))
        discard objectCallObject(start_styling_obj, start_args)
    # Safety
    if set_styling_obj == nil:
        raise newException(FieldError, "Lexer doesn't contain the 'setStyling' method!")
    elif start_styling_obj == nil:
        raise newException(FieldError, "Lexer doesn't contain the 'startStyling' method!")
    elif send_scintilla_obj == nil:
        raise newException(FieldError, "Editor doesn't contain the 'SendScintilla' method!")
    # Styling initialization
    start_styling()
    #------------------------------------------------------------------------------
    var 
        actseq = SeqActive(active: false)
        token_name: string = ""
        previous_token: string = ""
        token_start: int = 0
        token_length: int = 0
    # Check previous style
    if value_start != 0:
        var previous_style = get_previous_style()
        for i in multiline_sequence_list:
            if previous_style == i.style:
                actseq.sequence = i
                actseq.active = true
                break
    # Style the tokens accordingly
    proc check_start_sequence(pos: int, sequence: var SeqActive): bool =
        for s in sequence_lists:
            var found = true
            for i, ch in s.start.pairs:
                if text[pos+i] != ch:
                    found = false
                    break
            if found == false:
                continue
            sequence.sequence = s
            return true
        return false
    
    proc check_stop_sequence(pos: int, actseq: SeqActive): bool =
        if text[pos] in actseq.sequence.stop_extra:
            return true
        if (pos > 0 and (text[pos-1] in actseq.sequence.negative_lookbehind)) and
           (pos > 1 and not (text[pos-2] in actseq.sequence.negative_lookbehind)):
            return false
        for i, s in actseq.sequence.stop.pairs:
            if text[pos+i] != s:
                return false
        return true
    
    template style_token(token_name: string, token_length: int) =
        if token_length > 0:
            if token_name in keywords:
                set_styling(token_length, styles["Keyword"])
                previous_token = token_name
            elif token_name in custom_keywords:
                set_styling(token_length, styles["CustomKeyword"])
            elif token_name[0].isdigit() or (token_name[0] == '.' and token_name[1].isdigit()):
                set_styling(token_length, styles["Number"])
            elif previous_token == "class":
                set_styling(token_length, styles["ClassName"])
                previous_token = ""
            elif previous_token == "def":
                set_styling(token_length, styles["FunctionMethodName"])
                previous_token = ""
            else:
                set_styling(token_length, styles["Default"])
    
    var i = 0
    token_start = i
    while i < text_length:
        if actseq.active == true or check_start_sequence(i, actseq) == true:
            #[
                Multiline sequence already started in the previous line or
                a start sequence was found
            ]#
            if actseq.active == false:
                # Style the currently accumulated token
                token_name = text[token_start..i]
                token_length = i - token_start
                style_token(token_name, token_length)
            # Set the states and reset the flags
            token_start = i
            token_length = 0
            if actseq.active == false:
                i += len(actseq.sequence.start)
            while i < text_length:
                # Check for end of comment
                if check_stop_sequence(i, actseq) == true:
                    i += len(actseq.sequence.stop)
                    break
                i += 1
            # Style text
            token_length = i - token_start
            set_styling(token_length, actseq.sequence.style)
            # Style the separator tokens after the sequence, if any
            token_start = i
            while text[i] in extended_separators and i < text_length:
                i += 1
            token_length = i - token_start
            if token_length > 0:
                set_styling(token_length, styles["Default"])
            # Set the states and reset the flags
            token_start = i
            token_length = 0
            # Skip to the next iteration, because the index is already
            # at the position at the end of the string
            actseq.active = false
            continue
        elif text[i] in extended_separators:
            #[
                Separator found
            ]#
            token_name = text[token_start..i-1]
            token_length = len(token_name)
            if token_length > 0:
                style_token(token_name, token_length)
                token_start = i
                while text[i] in extended_separators and i < text_length:
                    i += 1
                token_length = i - token_start
                if token_length > 0:
                    set_styling(token_length, styles["Default"])
                # State reset
                token_start = i
                token_length = 0
                continue
            else:
                while text[i] in extended_separators and i < text_length:
                    i += 1
                token_length = i - token_start
                if token_length > 0:
                    set_styling(token_length, styles["Default"])
                # State reset
                token_start = i
                token_length = 0
                continue
        # Update loop variables
        inc(i)
        # Check for end of text
        if i >= text_length:
            # Style text
            token_name = text[token_start..i]
            token_length = i - token_start
            style_token(token_name, token_length)
    #------------------------------------------------------------------------------
    clean_up()
    returnNone()


echo "Nim lexers imported!"


