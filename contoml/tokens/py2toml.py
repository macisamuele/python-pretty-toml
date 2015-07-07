
"""
A converter of python values to TOML Token instances.
"""
import codecs
import datetime
import six
import strict_rfc3339
import timestamp
from contoml import tokens
import re
from contoml.elements.metadata import NewlineElement
from contoml.errors import TOMLError


class NotPrimitiveError(TOMLError):
    pass


_operator_tokens_by_type = {
    tokens.TYPE_OP_SQUARE_LEFT_BRACKET: tokens.Token(tokens.TYPE_OP_SQUARE_LEFT_BRACKET, '['),
    tokens.TYPE_OP_SQUARE_RIGHT_BRACKET: tokens.Token(tokens.TYPE_OP_SQUARE_RIGHT_BRACKET, ']'),
    tokens.TYPE_OP_DOUBLE_SQUARE_LEFT_BRACKET: tokens.Token(tokens.TYPE_OP_DOUBLE_SQUARE_LEFT_BRACKET, '[['),
    tokens.TYPE_OP_DOUBLE_SQUARE_RIGHT_BRACKET: tokens.Token(tokens.TYPE_OP_DOUBLE_SQUARE_RIGHT_BRACKET, ']]'),
    tokens.TYPE_OP_COMMA: tokens.Token(tokens.TYPE_OP_COMMA, ','),
    tokens.TYPE_NEWLINE: tokens.Token(tokens.TYPE_NEWLINE, '\n'),
}


def operator_token(token_type):
    return _operator_tokens_by_type[token_type]


_newline = NewlineElement([operator_token(tokens.TYPE_NEWLINE)])


def newline_element():
    return _newline


def create_primitive_token(value):
    """
    Creates and returns a single token for the given primitive atomic value.

    Raises NotPrimitiveError when the given value is not a primitive atomic value
    """
    if isinstance(value, bool):
        return tokens.Token(tokens.TYPE_BOOLEAN, 'true' if value else 'false')
    elif isinstance(value, int):
        return tokens.Token(tokens.TYPE_INTEGER, '{}'.format(value))
    elif isinstance(value, float):
        return tokens.Token(tokens.TYPE_FLOAT, '{}'.format(value))
    elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        ts = timestamp(value) // 1000
        return tokens.Token(tokens.TYPE_DATE, strict_rfc3339.timestamp_to_rfc3339_utcoffset(ts))
    elif isinstance(value, six.string_types):
        return _create_string_token(value)

    raise NotPrimitiveError("{} of type {}".format(value, type(value)))


_bare_string_regex = re.compile('^[a-zA-Z0-9]*$')

def _create_string_token(text):
    if _bare_string_regex.match(text):
        return tokens.Token(tokens.TYPE_BARE_STRING, text)
    else:
        return tokens.Token(tokens.TYPE_STRING, '"{}"'.format(_escape_string(text)))

def _escape_string(text):
    if six.PY2:
        return text.encode('unicode-escape').encode('string-escape').replace('"', '\\"').replace("\\'", "'")
    else:
        return codecs.encode(text, 'unicode-escape').decode().replace('"', '\\"')


