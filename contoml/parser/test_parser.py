from contoml.elements.array import ArrayElement
from contoml.elements.atomic import AtomicElement
from contoml.elements.metadata import CommentElement, NewlineElement, WhitespaceElement
from contoml.elements.tableheader import TableHeaderElement
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
    ts = TokenStream(tokenize(" [ namez    . namey . namex ] \n other things"))
    table_header_element, pending_tokens = parser.table_header_element(ts)

    assert isinstance(table_header_element, TableHeaderElement)
    assert len(pending_tokens) == 4


def test_atomic_element():
    e1, p1 = parser.atomic_element(TokenStream(tokenize('42 not')))
    assert isinstance(e1, AtomicElement) and e1.value == 42
    assert len(p1) == 2

    e2, p2 = parser.atomic_element(TokenStream(tokenize('not 42')))
    assert isinstance(e2, AtomicElement) and e2.value == 'not'
    assert len(p2) == 2


def test_array():
    array_element, pending_ts = parser.array_element(TokenStream(tokenize('[ 3, 4, 5,6,7] ')))

    assert isinstance(array_element, ArrayElement)
    assert len(array_element) == 5
    assert len(pending_ts) == 1


def test_inline_table():
    inline_table, pending_ts = parser.inline_table_element(TokenStream(tokenize('{ "id"= 42,test = name} vroom')))

    assert set(inline_table.keys()) == {'id', 'test'}
    assert len(pending_ts) == 2
    assert inline_table['id'] == 42
    assert inline_table['test'] == 'name'
