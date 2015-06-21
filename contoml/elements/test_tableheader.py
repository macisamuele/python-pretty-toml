from contoml import lexer
from contoml.elements.tableheader import TableHeader


def test_tableheader():
    tokens = tuple(lexer.tokenize('\n\t [[personal. information.details]]'))
    element = TableHeader(tokens)

    assert element.is_array_of_tables
    assert ('personal', 'information', 'details') == element.names

    assert element.has_name_prefix(('personal', 'information'))
