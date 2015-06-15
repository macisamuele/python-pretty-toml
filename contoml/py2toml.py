
"""
A converter of python values to TOML Token instances.
"""
from contoml import tokens


class NotPrimitiveError(Exception):
    pass


def create_operator_token(token_type):

    if token_type == tokens.TYPE_OP_COMMA:
        return tokens.Token(tokens.TYPE_OP_COMMA, ',')

    raise NotImplementedError   # TODO


def create_primitive_token(value):
    """
    Creates and returns a single token for the given primitive atomic value.

    Raises NotPrimitiveError when the given value is not a primitive atomic value
    """
    if isinstance(value, int):
        return tokens.Token(tokens.TYPE_INTEGER, '{}'.format(value))
    else:
        raise NotPrimitiveError

    raise NotImplementedError   # TODO



