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
    element, pending_ts = parser.line_terminator_element(ts)

    assert isinstance(element, CommentElement)
    assert pending_ts.offset == 2
    assert ts.offset == 0

def test_line_terminator_2():
    tokens = tokenize('\n')
    ts = TokenStream(tokens)
    element, pending_ts = parser.line_terminator_element(ts)

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

def test_array_2():

    text = """[
  "alpha",
  "omega"
]"""

    array_element, pending_ts = parser.array_element(TokenStream(tokenize(text)))

    assert array_element[0] == 'alpha'
    assert array_element[1] == 'omega'

def test_inline_table():
    inline_table, pending_ts = parser.inline_table_element(TokenStream(tokenize('{ "id"= 42,test = name} vroom')))

    assert set(inline_table.keys()) == {'id', 'test'}
    assert len(pending_ts) == 2
    assert inline_table['id'] == 42
    assert inline_table['test'] == 'name'

def test_table_body():
    table_body, pending_ts = parser.table_body_element(TokenStream(tokenize(' name= "test" # No way man!\nid =42\n vvv')))
    assert set(table_body.keys()) == {'name', 'id'}
    assert len(pending_ts) == 2
    assert table_body['name'] == 'test'
    assert table_body['id'] == 42


def test_key_value_pair():
    text = """hosts = [
  "alpha",
  "omega"
]
"""

    parsed, pending_ts = parser.key_value_pair(TokenStream(tokenize(text)))

    assert isinstance(parsed[1], AtomicElement)
    assert isinstance(parsed[5], ArrayElement)

def test_table_body_2():

    text = """
data = [ ["gamma", "delta"], [1, 2] ]

# Line breaks are OK when inside arrays
hosts = [
  "alpha",
  "omega"
]

str_multiline = wohoo
"""

    table_body, pending_Ts = parser.table_body_element(TokenStream(tokenize(text)))

    print(table_body)


def test_toml_file():
    ts = TokenStream(tokenize("""

    # My awesome TOML sample

    name =    amr
    id= 42

    [section1]
        sec1name =3.14
        sec11 =  false
    [section2]
    sec2name= 2.16

    [[person]]  # array of tables
    name =Amr

[[person]]
name= fawzy
"""))

    toml_file = parser.toml_file(ts)

    assert toml_file['']['name'] == 'amr'
    assert toml_file['']['id'] == 42

    assert toml_file['section1']['sec1name'] == 3.14
    assert toml_file['section1']['sec11'] == False
    assert toml_file['section2']['sec2name'] == 2.16

    assert toml_file['person'][0]['name'] == 'Amr'
    assert toml_file['person'][1]['name'] == 'fawzy'
