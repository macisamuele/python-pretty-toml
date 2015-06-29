from contoml import parser, lexer
from contoml.file import entries
from contoml.file.entries import AnonymousTableEntry
from contoml.parser.tokenstream import TokenStream


def test_entry_extraction():
    text = open('sample.toml').read()
    elements = parser.parse(TokenStream(lexer.tokenize(text))).elements

    e = tuple(entries.extract(elements))

    assert len(e) == 13
    assert isinstance(e[0], AnonymousTableEntry)
