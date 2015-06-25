
from contoml.errors import TOMLError, InvalidTOMLFileError


def loads(text):
    """
    Parses TOML text into a dict-like object and returns it.
    """
    from .parser.parser import toml_file as parser
    from .lexer import tokenize as lexer
    from .parser.tokenstream import TokenStream

    tokens = lexer(text)
    return parser(TokenStream(tokens))


def load(file_path):
    return loads(open(file_path).read())
