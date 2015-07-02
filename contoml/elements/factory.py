from contoml import tokens
from contoml.tokens import py2toml
from contoml.elements.atomic import AtomicElement
from contoml.elements.metadata import PunctuationElement, WhitespaceElement, NewlineElement
from contoml.elements.tableheader import TableHeaderElement


def create_element(value):
    """
    Creates and returns the appropriate elements.Element instance from the given Python primitive, sequence-like,
    or dict-like value.
    """

    try:
        primitive_token = py2toml.create_primitive_token(value)
        return AtomicElement((primitive_token,))
    except py2toml.NotPrimitiveError:
        # TODO: Create a container element and return it
        pass

    raise NotImplementedError   # TODO


def create_operator_element(operator):
    """
    Creates a PunctuationElement instance containing an operator token of the specified type. The operator
    should be a TOML source str.
    """
    operator_type_map = {
        ',': tokens.TYPE_OP_COMMA,
        '=': tokens.TYPE_OP_ASSIGNMENT,
        '[': tokens.TYPE_OP_SQUARE_LEFT_BRACKET,
        ']': tokens.TYPE_OP_SQUARE_RIGHT_BRACKET,
        '[[': tokens.TYPE_OP_DOUBLE_SQUARE_LEFT_BRACKET,
        ']]': tokens.TYPE_OP_DOUBLE_SQUARE_RIGHT_BRACKET,
    }

    ts = (tokens.Token(operator_type_map[operator], operator),)
    return PunctuationElement(ts)


def create_newline_element():
    """
    Creates and returns a single NewlineElement.
    """
    ts = (tokens.Token(tokens.TYPE_NEWLINE, '\n'),)
    return NewlineElement(ts)


def create_whitespace_element(length=1):
    """
    Creates and returns a WhitespaceElement containing spaces.
    """
    ts = (tokens.Token(tokens.TYPE_WHITESPACE, ' ' * length),)
    return WhitespaceElement(ts)


def create_table_header_element(name):
    return TableHeaderElement((
        py2toml.operator_token(tokens.TYPE_OP_SQUARE_LEFT_BRACKET),
        py2toml.create_primitive_token(name),
        py2toml.operator_token(tokens.TYPE_OP_SQUARE_RIGHT_BRACKET),
        py2toml.operator_token(tokens.TYPE_NEWLINE),
    ))

def create_array_of_tables_header_element(name):
    return TableHeaderElement((
        py2toml.operator_token(tokens.TYPE_OP_DOUBLE_SQUARE_LEFT_BRACKET),
        py2toml.create_primitive_token(name),
        py2toml.operator_token(tokens.TYPE_OP_DOUBLE_SQUARE_RIGHT_BRACKET),
        py2toml.operator_token(tokens.TYPE_NEWLINE),
    ))
