from contoml.elements.metadata import CommentElement, NewlineElement, WhitespaceElement
from contoml.lexer import tokenize
from contoml.parser import parser
from contoml.parser.tokenstream import TokenStream


def test_line_terminator_1():
    tokens = tokenize('# Sup\n')
    ts = TokenStream(tokens)
    element, pending_ts = parser.line_terminator(ts)

    assert isinstance(element, CommentElement)
    assert pending_ts.offset == 2
    assert ts.offset == 0

def test_line_terminator_2():
    tokens = tokenize('\n')
    ts = TokenStream(tokens)
    element, pending_ts = parser.line_terminator(ts)

    assert isinstance(element, NewlineElement)
    assert pending_ts.offset == 1
    assert ts.offset == 0

def test_space_1():
    ts = TokenStream(tokenize('  noo'))
    space_element, pending_ts = parser.space_element(ts)

    assert isinstance(space_element, WhitespaceElement)
    assert len(space_element.tokens) == 2
    assert pending_ts.offset == 2
    assert ts.offset == 0

def test_space_2():
    ts = TokenStream(tokenize(' noo'))
    space_element, pending_ts = parser.space_element(ts)

    assert isinstance(space_element, WhitespaceElement)
    assert len(space_element.tokens) == 1
    assert pending_ts.offset == 1
    assert ts.offset == 0

def test_space_3():
    ts = TokenStream(tokenize('noo'))
    space_element, pending_ts = parser.space_element(ts)

    assert isinstance(space_element, WhitespaceElement)
    assert len(space_element.tokens) == 0
    assert pending_ts.offset == 0
    assert ts.offset == 0


def test_table_header():
    ts = TokenStream(tokenize(" [ namez    . namey . namex ] \n"))
    a, b = parser.table_header(ts)

    print(a, b)
