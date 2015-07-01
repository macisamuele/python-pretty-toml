

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
