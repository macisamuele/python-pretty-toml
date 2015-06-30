from contoml import lexer, parser
from contoml.file import entries, elementsanitizer
from contoml.file.entries import EntryName
from contoml.file.structurer import superdict, structure
from contoml.parser.tokenstream import TokenStream
from contoml.file.cascadedict import CascadeDict


def test_superdict():

    d = superdict()

    d[EntryName(('super', 'sub1', 'sub2', 'sub3'))] = 12
    d[EntryName(('super', 'sub1', 'sub2', 'sub4'))] = 42

    assert d[EntryName(('super', 'sub1', 'sub2', 'sub3'))] == 12
    assert isinstance(d[EntryName(('super', 'sub1', 'sub2'))], CascadeDict)
    assert d[EntryName(('super', 'sub1', 'sub2', 'sub4'))] == 42


def test_structure():
    tokens = TokenStream(lexer.tokenize(open('sample.toml').read()))
    elements = elementsanitizer.sanitize(parser.parse(tokens))
    entries_ = tuple(entries.extract(elements))

    navigable_struct = structure(entries_)

    print(navigable_struct)
