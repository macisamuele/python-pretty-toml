
"""
    A Recursive Descent implementation of a parser for TOML.

    Grammar:
    --------

    Newline -> NEWLINE
    Comment -> COMMENT Newline
    LineTerminator -> Comment | Newline
    Space -> WHITESPACE Space | WHITESPACE | EMPTY
    TableHeader -> Space [ Space TableHeaderName Space ] Space LineTerminator
    TableHeaderName -> STRING Space '.' Space TableHeaderName | STRING
    Atomic -> STRING | INTEGER | FLOAT | DATE | BOOLEAN

    Array -> '[' Space ArrayInternal Space ']'
    ArrayInternal -> Atomic Space ',' Space LineTerminator Space ArrayInternal |
        Atomic Space ',' Space ArrayInternal | Atomic | EMPTY

    InlineTable -> '{' Space InlineTableInternal '}'
    InlineTableInternal -> Atomic Space ',' Space InlineTableInternal | Atomic | Empty

    Value -> Atomic | InlineTable | Array
    KeyValuePair -> STRING Space '=' Space Value Space LineTerminator

    TableBody -> KeyValuePair TableBody | KeyValuePair

    Output -> Space LineTerminator Output | TableHeader Output | TableBody Output | Empty
"""
from contoml import tokens
from contoml.elements.array import ArrayElement
from contoml.elements.atomic import AtomicElement
from contoml.elements.metadata import NewlineElement, CommentElement, WhitespaceElement, PunctuationElement
from contoml.elements.tableheader import TableHeaderElement

from contoml.parser.dsl import capture_from
from contoml.parser.errors import ParsingError

"""
    Non-terminals are represented as functions which return (RESULT, pending_token_stream), or raise ParsingError.
"""


def token(token_type):
    def factory(ts):
        t = ts.head
        if t.type != token_type:
            raise ParsingError('Expected a token of type {}'.format(token_type))
        return t, ts.tail
    return factory


def newline_element(token_stream):
    """
    Returns NewlineElement, pending_token_stream or raises ParsingError.
    """
    captured = capture_from(token_stream).extract(token(tokens.TYPE_NEWLINE))
    return NewlineElement(captured.value()), captured.pending_tokens


def comment_element(token_stream):
    """
    Returns CommentElement, pending_token_stream or raises ParsingError.
    """
    captured = capture_from(token_stream).extract(token(tokens.TYPE_COMMENT)).and_extract(token(tokens.TYPE_NEWLINE))
    return CommentElement(captured.value()), captured.pending_tokens


def line_terminator(token_stream):
    """
    Returns either (NewlineElement or CommentElement), and pending_token_stream.
    """
    captured = capture_from(token_stream).extract(comment_element).or_extract(newline_element)
    return captured.value('Expected a comment or a newline')[0], captured.pending_tokens


def zero_or_more_tokens(token_type):

    def factory(token_stream):
        def more(ts):
            c = capture_from(ts).extract(token(token_type)).and_extract(zero_or_more_tokens(token_type))
            return c.value(), c.pending_tokens

        def two(ts):
            c = capture_from(ts).extract(token(tokens.TYPE_WHITESPACE))
            return c.value(), c.pending

        def zero(ts):
            return tuple(), ts

        captured = capture_from(token_stream).extract(more).or_extract(two).or_extract(zero)
        return captured.value(), captured.pending_tokens

    return factory


def space_element(token_stream):
    captured = capture_from(token_stream).extract(zero_or_more_tokens(tokens.TYPE_WHITESPACE))
    return WhitespaceElement([t for t in captured.value() if t]), captured.pending_tokens


def string_token(token_stream):
    captured = capture_from(token_stream).\
        extract(token(tokens.TYPE_BARE_STRING)).\
        or_extract(token(tokens.TYPE_STRING)).\
        or_extract(token(tokens.TYPE_LITERAL_STRING)).\
        or_extract(token(tokens.TYPE_MULTILINE_STRING)).\
        or_extract(token(tokens.TYPE_MULTILINE_LITERAL_STRING))

    return captured.value('Expected a string'), captured.pending_tokens


def table_header_name_tokens(token_stream):

    def one(ts):
        c = capture_from(ts).\
            extract(string_token).\
            and_extract(zero_or_more_tokens(tokens.TYPE_WHITESPACE)).\
            and_extract(token(tokens.TYPE_OPT_DOT)).\
            and_extract(zero_or_more_tokens(tokens.TYPE_WHITESPACE)).\
            and_extract(table_header_name_tokens)
        return c.value(), c.pending_tokens

    captured = capture_from(token_stream).extract(one).or_extract(string_token)
    return captured.value(), captured.pending_tokens

def table_header_element(token_stream):
    captured = capture_from(token_stream).\
        extract(zero_or_more_tokens(tokens.TYPE_WHITESPACE)).\
        and_extract(token(tokens.TYPE_OP_SQUARE_LEFT_BRACKET)).\
        and_extract(zero_or_more_tokens(tokens.TYPE_WHITESPACE)).\
        and_extract(table_header_name_tokens).\
        and_extract(zero_or_more_tokens(tokens.TYPE_WHITESPACE)).\
        and_extract(token(tokens.TYPE_OP_SQUARE_RIGHT_BRACKET)).\
        and_extract(zero_or_more_tokens(tokens.TYPE_WHITESPACE)).\
        and_extract(token(tokens.TYPE_NEWLINE))

    return TableHeaderElement(captured.value()), captured.pending_tokens


def atomic_element(token_stream):
    captured = capture_from(token_stream).\
        extract(string_token).\
        or_extract(token(tokens.TYPE_INTEGER)).\
        or_extract(token(tokens.TYPE_FLOAT)).\
        or_extract(token(tokens.TYPE_DATE)).\
        or_extract(token(tokens.TYPE_BOOLEAN))
    return AtomicElement(captured.value('Expected an atomic primitive value')), captured.pending_tokens


def punctuation_element(token_type):
    def factory(ts):
        c = capture_from(ts).extract(token(token_type))
        return PunctuationElement(c.value('Expected the punctuation element: {}'.format(token_type))), c.pending_tokens
    return factory

def array_element(token_stream):

    # Array -> '[' Space ArrayInternal Space ']'
    # ArrayInternal -> Atomic Space ',' Space LineTerminator Space ArrayInternal |
    #     Atomic Space ',' Space ArrayInternal | Atomic | EMPTY

    def internal(ts):

        def one(ts1):
            c = capture_from(ts1).\
                extract(atomic_element).\
                and_extract(space_element).\
                and_extract(punctuation_element(tokens.TYPE_OP_COMMA)).\
                and_extract(space_element).\
                and_extract(line_terminator).\
                and_extract(space_element).\
                and_extract(internal)
            return c.value(), c.pending_tokens

        def two(ts2):
            c = capture_from(ts2).\
                extract(atomic_element).\
                and_extract(space_element).\
                and_extract(punctuation_element(tokens.TYPE_OP_COMMA)).\
                and_extract(space_element).\
                and_extract(internal)
            return c.value(), c.pending_tokens

        captured = capture_from(ts).extract(one).or_extract(two).or_extract(atomic_element).or_empty()
        return captured.value(), captured.pending_tokens

    ca = capture_from(token_stream).\
        extract(punctuation_element(tokens.TYPE_OP_SQUARE_LEFT_BRACKET)).\
        and_extract(space_element).\
        and_extract(internal).\
        and_extract(space_element).\
        and_extract(punctuation_element(tokens.TYPE_OP_SQUARE_RIGHT_BRACKET))
    return ArrayElement(ca.value()), ca.pending_tokens
