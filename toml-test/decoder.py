#! /usr/bin/python

import six


def python_to_test_json(python_value):
    """
    Converts a Python value to a JSON dump of the value according to the spec on
    https://github.com/BurntSushi/toml-test.
    """
    import json
    import datetime
    import strict_rfc3339

    TYPE = 'type'
    VALUE = 'value'

    def convert(value):
        if isinstance(value, dict):
            return {k: convert(v) for (k, v) in value.items()}
        elif isinstance(value, (list, tuple)):
            return {TYPE: 'array', VALUE: [convert(v) for v in value]}
        elif isinstance(value, datetime.datetime):
            return {TYPE: 'datetime', VALUE: strict_rfc3339.timestamp_to_rfc3339_utcoffset(int(value.timestamp()))}
        elif isinstance(value, six.string_types):
            return {TYPE: 'string', VALUE: value}
        elif isinstance(value, bool):
            return {TYPE: 'bool', VALUE: 'true' if value else 'false'}
        elif isinstance(value, six.integer_types):
            return {TYPE: 'integer', VALUE: str(value)}
        elif isinstance(value, float):
            return {TYPE: 'float', VALUE: str(value)}
        else:
            raise RuntimeError('Unexpected type')

    return json.dumps(convert(python_value))


def decode(toml_text):
    """
    Decodes a TOML file text into the corresponding Python value.
    """
    import contoml
    return contoml.loads(toml_text).primitive


def main():
    import sys
    print(python_to_test_json(decode(sys.stdin.read())))


main()
