from contoml import py2toml, tokens
from contoml.elements.atomic import AtomicElement
from contoml.elements.metadata import PunctuationElement, WhitespaceElement


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
    }

    ts = (tokens.Token(operator_type_map[operator], operator),)
    return PunctuationElement(ts)

    raise NotImplementedError   # TODO


def create_whitespace_element(length=1):
    """
    Creates and returns a WhitespaceElement containing spaces.
    """
    ts = (tokens.Token(tokens.TYPE_WHITESPACE, ' ' * length),)
    return WhitespaceElement(ts)

