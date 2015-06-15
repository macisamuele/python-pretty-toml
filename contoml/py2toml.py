
"""
A converter of python values to TOML Token instances.
"""
from contoml import tokens


def serialize(value, to_token_type):
    """
    Serializes the given value to a tokens.Token instance based on to_token_type.
    """
    if to_token_type == tokens.TYPE_INTEGER:
        return tokens.Token(tokens.TYPE_INTEGER, '{}'.format(value))

    raise NotImplementedError
