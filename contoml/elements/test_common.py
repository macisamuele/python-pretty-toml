from contoml import tokens
from contoml.elements.atomic import AtomicElement
from contoml.elements.metadata import NewlineElement, PunctuationElement, WhitespaceElement, CommentElement

atomic_token_types = (
    tokens.TYPE_INTEGER,
    tokens.TYPE_FLOAT,
    tokens.TYPE_BARE_STRING,
    tokens.TYPE_STRING,
    tokens.TYPE_LITERAL_STRING,
    tokens.TYPE_MULTILINE_STRING,
    tokens.TYPE_MULTILINE_LITERAL_STRING,
)

punctuation_token_types = (
    tokens.TYPE_OPT_DOT,
    tokens.TYPE_OP_CURLY_LEFT_BRACKET,
    tokens.TYPE_OP_SQUARE_LEFT_BRACKET,
    tokens.TYPE_OP_DOUBLE_SQUARE_LEFT_BRACKET,
    tokens.TYPE_OP_SQUARE_RIGHT_BRACKET,
    tokens.TYPE_OP_CURLY_RIGHT_BRACKET,
    tokens.TYPE_OP_DOUBLE_SQUARE_RIGHT_BRACKET,
    tokens.TYPE_OP_ASSIGNMENT,
)

def primitive_token_to_primitive_element(token):
    if token.type == tokens.TYPE_NEWLINE:
        return NewlineElement((token,))
    elif token.type in atomic_token_types:
        return AtomicElement((token,))
    elif token.type == tokens.TYPE_NEWLINE:
        return NewlineElement((token,))
    elif token.type in punctuation_token_types:
        return PunctuationElement((token,))
    elif token.type == tokens.TYPE_WHITESPACE:
        return WhitespaceElement((token,))
    elif token.type == tokens.TYPE_COMMENT:
        return CommentElement((token,))
    else:
        raise RuntimeError("{} has no mapped primitive element".format(token))
