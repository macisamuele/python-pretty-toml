from contoml import lexer
from contoml.elements import AtomicElement, WhitespaceElement, NewlineElement, CommentElement, PunctuationElement, \
    ArrayElement


def test_atomic_element():
    element = AtomicElement(tuple(lexer.tokenize(' \t 42 ')))
    assert element.value == 42
    element.set(23)
    assert element.serialized() == ' \t 23 '


def test_whitespace_element():
    element = WhitespaceElement(tuple(lexer.tokenize(' \t   ')))
    assert element.serialized() == ' \t   '


def test_newline_element():
    element = NewlineElement(tuple(lexer.tokenize('\n\n\n')))
    assert element.serialized() == '\n\n\n'


def test_comment_element():
    element = CommentElement(tuple(lexer.tokenize('# This is my insightful remark\n')))
    assert element.serialized() == '# This is my insightful remark\n'


def test_punctuation_element():
    PunctuationElement(tuple(lexer.tokenize('[')))
    PunctuationElement(tuple(lexer.tokenize('[[')))
    PunctuationElement(tuple(lexer.tokenize('.')))
    PunctuationElement(tuple(lexer.tokenize(']')))
    PunctuationElement(tuple(lexer.tokenize(']]')))


def test_array_element():
    tokens = tuple(lexer.tokenize('[4, 8, [42, 23], 15]'))
    assert len(tokens) == 17
    sub_elements = (
        PunctuationElement(tokens[:1]),

        AtomicElement(tokens[1:2]),
        PunctuationElement(tokens[2:3]),
        WhitespaceElement(tokens[3:4]),

        AtomicElement(tokens[4:5]),
        PunctuationElement(tokens[5:6]),
        WhitespaceElement(tokens[6:7]),

        ArrayElement((
            PunctuationElement(tokens[7:8]),

            AtomicElement(tokens[8:9]),
            PunctuationElement(tokens[9:10]),
            WhitespaceElement(tokens[10:11]),

            AtomicElement(tokens[11:12]),
            PunctuationElement(tokens[12:13]),
        )),

        PunctuationElement(tokens[13:14]),
        WhitespaceElement(tokens[14:15]),
        AtomicElement(tokens[15:16]),
        PunctuationElement(tokens[16:17])
    )

    array_element = ArrayElement(sub_elements)

    assert len(array_element) == 4

    assert array_element[0] == 4
    assert array_element[1] == 8
    assert array_element[2][0] == 42
    assert array_element[2][1] == 23
    assert array_element[-1] == 15
