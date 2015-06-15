
from .common import *
from contoml import tokens


class WhitespaceElement(TokenElement):
    """
    An element that contains tokens of whitespace
    """

    def __init__(self, _tokens):
        TokenElement.__init__(self, _tokens, TYPE_METADATA)
    
    def _validate_tokens(self, _tokens):
        for token in _tokens:
            assert token.type == tokens.TYPE_WHITESPACE


class NewlineElement(TokenElement):
    """
    An element containing newline tokens
    """

    def __init__(self, _tokens):
        TokenElement.__init__(self, _tokens, TYPE_METADATA)

    def _validate_tokens(self, _tokens):
        for token in _tokens:
            assert token.type == tokens.TYPE_NEWLINE


class CommentElement(TokenElement):
    """
    An element containing a single comment token followed by a newline token.
    """

    def __init__(self, _tokens):
        TokenElement.__init__(self, _tokens, TYPE_METADATA)

    def _validate_tokens(self, _tokens):
        assert len(_tokens) == 2
        assert _tokens[0].type == tokens.TYPE_COMMENT
        assert _tokens[1].type == tokens.TYPE_NEWLINE


class PunctuationElement(TokenElement):
    """
    An element containing a single punctuation token.
    """

    def __init__(self, _tokens):
        TokenElement.__init__(self, _tokens, TYPE_METADATA)

    @property
    def token(self):
        """
        Returns the token contained in this Element.
        """
        return self.tokens[0]

    def _validate_tokens(self, _tokens):
        assert _tokens
        assert tokens.is_operator(_tokens[0])
