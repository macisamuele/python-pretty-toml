#! /usr/bin/python


def test_json_to_python(test_json_str):
    """
    Parses a string containing a JSON object encoded according to the format specified on
    https://github.com/BurntSushi/toml-test into a Python value.
    """
    import json
    import iso8601

    def convert(value):
        if isinstance(value, dict):
            if 'type' in value and 'value' in value:
                value_type, value_raw = value['type'], value['value']
                if value_type == 'string':
                    return value_raw
                elif value_type == 'integer':
                    return int(value_raw)
                elif value_type == 'float':
                    return float(value_raw)
                elif value_type == 'datetime':
                    return iso8601.parse_date(value_raw)
                elif value_type == 'bool':
                    return {'true': True, 'false': False}[value_raw]    # Let it crash
                elif value_type == 'array':
                    return convert(value_raw)
            else:
                return {k: convert(v) for (k, v) in value.items()}
        elif isinstance(value, (tuple, list)):
            return [convert(child) for child in value]
        else:
            raise RuntimeError('Invalid input')

    return convert(json.loads(test_json_str))


def encode(python_value):
    """
    Encodes a Python value into a TOML string.
    """
    import contoml
    return contoml.dumps(python_value)


def main():
    import sys
    print(encode(test_json_to_python(sys.stdin.read())))


main()



