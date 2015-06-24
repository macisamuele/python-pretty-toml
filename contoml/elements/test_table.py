from contoml import lexer
from contoml.elements.atomic import AtomicElement
from contoml.elements.metadata import WhitespaceElement, PunctuationElement, NewlineElement, CommentElement
from contoml.elements.table import TableElement


def test_table():

    tokens = tuple(lexer.tokenize('name = first\nid=42 # My id\n\n\n'))

    elements = (
        AtomicElement(tokens[:1]),
        WhitespaceElement(tokens[1:2]),
        PunctuationElement(tokens[2:3]),
        WhitespaceElement(tokens[3:4]),
        AtomicElement(tokens[4:5]),
        NewlineElement(tokens[5:6]),

        AtomicElement(tokens[6:7]),
        PunctuationElement(tokens[7:8]),
        AtomicElement(tokens[8:9]),
        WhitespaceElement(tokens[9:10]),
        CommentElement(tokens[10:12]),

        NewlineElement(tokens[12:13]),
        NewlineElement(tokens[13:14]),
        NewlineElement(tokens[14:15]),
    )

    table = TableElement(elements)

    assert set(table.items()) == {('name', 'first'), ('id', 42)}

    assert table['name'] == 'first'
    assert table['id'] == 42

    table['relation'] = 'another'

    assert set(table.items()) == {('name', 'first'), ('id', 42), ('relation', 'another')}
    assert table.serialized() == 'name = first\nid=42 # My id\n\n\n\nrelation = another'

    table['name'] = 'fawzy'

    assert set(table.items()) == {('name', 'fawzy'), ('id', 42), ('relation', 'another')}
    assert table.serialized() == 'name = fawzy\nid=42 # My id\n\n\n\nrelation = another'


