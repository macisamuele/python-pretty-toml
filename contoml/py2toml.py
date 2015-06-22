
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
from contoml.errors import TOMLError


class NotPrimitiveError(TOMLError):
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
    if isinstance(value, bool):
        return tokens.Token(tokens.TYPE_BOOLEAN, 'true' if value else 'false')
    elif isinstance(value, int):
        return tokens.Token(tokens.TYPE_INTEGER, '{}'.format(value))
    elif isinstance(value, float):
        return tokens.Token(tokens.TYPE_FLOAT, '{}'.format(value))
    elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        ts = timestamp(value) // 1000
        return tokens.Token(tokens.TYPE_DATE, strict_rfc3339.timestamp_to_rfc3339_utcoffset(ts))
    elif isinstance(value, str):
        return _create_string_token(value)

    raise NotPrimitiveError


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
