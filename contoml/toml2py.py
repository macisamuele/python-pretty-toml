from contoml.tokens import TYPE_BOOLEAN, TYPE_INTEGER, TYPE_FLOAT, TYPE_DATE, \
    TYPE_MULTILINE_STRING, TYPE_BARE_STRING, TYPE_MULTILINE_LITERAL_STRING, TYPE_LITERAL_STRING, \
    TYPE_STRING


def deserialize(token):
    """
    Deserializes the value of a single tokens.Token instance based on its type.
    """
    
    if token.type == TYPE_BOOLEAN:
        return _to_boolean(token)
    elif token.type == TYPE_INTEGER:
        return _to_int(token)
    elif token.type == TYPE_FLOAT:
        return _to_float(token)
    elif token.type == TYPE_DATE:
        return _to_date(token)
    elif token.type in (TYPE_STRING, TYPE_MULTILINE_STRING, TYPE_BARE_STRING,
                        TYPE_LITERAL_STRING, TYPE_MULTILINE_LITERAL_STRING):
        return _to_string(token)
    else:
        raise Exception('This should never happen!')

def _to_string(token):
    raise NotImplementedError

def _to_int(token):
    return int(token.source_substring.replace('_', ''))

def _to_float(token):
    raise NotImplementedError

def _to_boolean(token):
    raise NotImplementedError

def _to_date(token):
    raise NotImplementedError
