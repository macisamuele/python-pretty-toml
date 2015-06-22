import datetime
import strict_rfc3339
from contoml import py2toml, tokens


def test_string():
    assert py2toml.create_primitive_token('fawzy') == tokens.Token(tokens.TYPE_BARE_STRING, 'fawzy')
    assert py2toml.create_primitive_token('I am a "cr\'azy" sentence.') == \
           tokens.Token(tokens.TYPE_STRING, '"I am a \\"cr\'azy\\" sentence."')

def test_int():
    assert py2toml.create_primitive_token(42) == tokens.Token(tokens.TYPE_INTEGER, '42')

def test_float():
    assert py2toml.create_primitive_token(4.2) == tokens.Token(tokens.TYPE_FLOAT, '4.2')

def test_bool():
    assert py2toml.create_primitive_token(False) == tokens.Token(tokens.TYPE_BOOLEAN, 'false')
    assert py2toml.create_primitive_token(True) == tokens.Token(tokens.TYPE_BOOLEAN, 'true')

def test_date():
    ts = strict_rfc3339.rfc3339_to_timestamp('1979-05-27T00:32:00-07:00')
    dt = datetime.datetime.fromtimestamp(ts)
    assert py2toml.create_primitive_token(dt) == tokens.Token(tokens.TYPE_DATE, '1979-05-27T07:32:00Z')
