from contoml.errors import InvalidValueError


def new():
    from contoml.file.file import TOMLFile
    return TOMLFile([])


def loads(text):
    """
    Parses TOML text into a dict-like object and returns it.
    """
    from .parser import parse_token_stream
    from .lexer import tokenize as lexer
    from .parser.tokenstream import TokenStream
    from .file import TOMLFile

    tokens = lexer(text)
    elements = parse_token_stream(TokenStream(tokens))
    return TOMLFile(elements)


def load(file_path):
    return loads(open(file_path).read())


def dumps(value):

    if not isinstance(value, dict):
        raise InvalidValueError('Input must be a dict of dicts, or just a dict!')

    f = new()

    if all(isinstance(child, dict) for child in value.values()):
        for k, v in value.items():
            f[k] = v
    else:
        f[''] = value

    return f.dumps()


def dump(obj, file_path):
    with open(file_path, 'w') as fp:
        fp.write(dumps(obj))
