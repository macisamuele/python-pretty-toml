
"""
A regular expression based Lexer for TOML.
"""


from collections import namedtuple
import re

# A TokenKind is the abstract type of token, represented by one of the following enumerated values.
from contoml import TOMLError

TOKEN_KIND_STRING = 'token-kind-string'
TOKEN_KIND_INTEGER = 'token-kind-integer'
TOKEN_KIND_FLOAT = 'token-kind-float'
TOKEN_KIND_BOOLEAN = 'token-kind-bool'
TOKEN_KIND_OPERATOR = 'token-kind-operator'
TOKEN_KIND_WHITESPACE = 'token-kind-whitespace'
TOKEN_KIND_DATE = 'token-kind-date'

class TokenType:
    """
    A TokenType is a concrete type of a source token along with a defined priority and a higher-order kind.

    The priority will be used in determining the tokenization behaviour of the lexer in the following manner:
    whenever more than one token is recognizable as the next possible token and they are all of equal source
    length, this priority is going to be used to break the tie by favoring the token type of the lowest priority
    value. A TokenType instance is naturally ordered by its priority.
    """

    def __init__(self, priority, kind):
        self._priority = priority
        self._kind = kind

    @property
    def kind(self):
        return self._kind

    @property
    def priority(self):
        return self._priority

    def __repr__(self):
        return "{}-{}".format(self.priority, self._kind)

    def __lt__(self, other):
        return isinstance(other, TokenType) and self._priority < other.priority

# Possible types of tokens
TOKEN_TYPE_BOOLEAN = TokenType(0, TOKEN_KIND_BOOLEAN)
TOKEN_TYPE_INTEGER = TokenType(0, TOKEN_KIND_INTEGER)
TOKEN_TYPE_OP_COMMA = TokenType(0, TOKEN_KIND_OPERATOR)
TOKEN_TYPE_OP_SQUARE_LEFT_BRACKET = TokenType(0, TOKEN_KIND_OPERATOR)
TOKEN_TYPE_OP_SQUARE_RIGHT_BRACKET = TokenType(0, TOKEN_KIND_OPERATOR)
TOKEN_TYPE_OP_CURLY_LEFT_BRACKET = TokenType(0, TOKEN_KIND_OPERATOR)
TOKEN_TYPE_OP_CURLY_RIGHT_BRACKET = TokenType(0, TOKEN_KIND_OPERATOR)
TOKEN_TYPE_OP_ASSIGNMENT = TokenType(0, TOKEN_KIND_OPERATOR)
TOKEN_TYPE_DOUBLE_SQUARE_LEFT_BRACKET = TokenType(0, TOKEN_KIND_OPERATOR)
TOKEN_TYPE_DOUBLE_SQUARE_RIGHT_BRACKET = TokenType(0, TOKEN_KIND_OPERATOR)
TOKEN_TYPE_FLOAT = TokenType(1, TOKEN_KIND_FLOAT)
TOKEN_TYPE_DATE = TokenType(40, TOKEN_KIND_DATE)
TOKEN_TYPE_OPT_DOT = TokenType(40, TOKEN_KIND_OPERATOR)
TOKEN_TYPE_BARE_STRING = TokenType(50, TOKEN_KIND_STRING)
TOKEN_TYPE_STRING = TokenType(90, TOKEN_KIND_STRING)
TOKEN_TYPE_MULTILINE_STRING = TokenType(90, TOKEN_KIND_STRING)
TOKEN_TYPE_LITERAL_STRING = TokenType(90, TOKEN_KIND_STRING)
TOKEN_TYPE_MULTILINE_LITERAL_STRING = TokenType(90, TOKEN_KIND_STRING)
TOKEN_TYPE_WHITESPACE = TokenType(90, TOKEN_KIND_WHITESPACE)
TOKEN_TYPE_COMMENT = TokenType(95, TOKEN_KIND_WHITESPACE)


TokenSpec = namedtuple('TokenSpec', ('type', 're'))


# Specs of all the valid tokens
_LEXICAL_SPECS = (
    TokenSpec(TOKEN_TYPE_COMMENT, re.compile(r'^(#.*)\n')),
    TokenSpec(TOKEN_TYPE_STRING, re.compile(r'^("(([^"]|\\")+?[^\\]|)")')),                       # Single line only
    TokenSpec(TOKEN_TYPE_MULTILINE_STRING, re.compile(r'^(""".*?""")', re.DOTALL)),
    TokenSpec(TOKEN_TYPE_LITERAL_STRING, re.compile(r"^('.*?')")),
    TokenSpec(TOKEN_TYPE_MULTILINE_LITERAL_STRING, re.compile(r"^('''.*?''')", re.DOTALL)),
    TokenSpec(TOKEN_TYPE_BARE_STRING, re.compile(r'^([A-Za-z0-9_-]+)')),
    TokenSpec(TOKEN_TYPE_DATE, re.compile(
        r'^([0-9]{4}-[0-9]{2}-[0-9]{2}(T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]*)?)?(([zZ])|((\+|-)[0-9]{2}:[0-9]{2}))?)')),
    TokenSpec(TOKEN_TYPE_WHITESPACE, re.compile('^(\s+)', re.DOTALL)),                       # Can span multiple lines
    TokenSpec(TOKEN_TYPE_INTEGER, re.compile(r'^(((\+|-)[0-9_]+)|([1-9][0-9_]*))')),
    TokenSpec(TOKEN_TYPE_FLOAT, re.compile(r'^((((\+|-)[0-9_]+)|([1-9][0-9_]*))(.[0-9_]+)?([eE](\+|-)?[1-9_]+)?)')),
    TokenSpec(TOKEN_TYPE_BOOLEAN, re.compile(r'^(true|false)')),
    TokenSpec(TOKEN_TYPE_OP_SQUARE_LEFT_BRACKET, re.compile(r'^(\[)')),
    TokenSpec(TOKEN_TYPE_OP_SQUARE_RIGHT_BRACKET, re.compile(r'^(\])')),
    TokenSpec(TOKEN_TYPE_OP_CURLY_LEFT_BRACKET, re.compile(r'^(\{)')),
    TokenSpec(TOKEN_TYPE_OP_CURLY_RIGHT_BRACKET, re.compile(r'^(\})')),
    TokenSpec(TOKEN_TYPE_OP_ASSIGNMENT, re.compile(r'^(=)')),
    TokenSpec(TOKEN_TYPE_OP_COMMA, re.compile(r'^(,)')),
    TokenSpec(TOKEN_TYPE_DOUBLE_SQUARE_LEFT_BRACKET, re.compile(r'^(\[\[)')),
    TokenSpec(TOKEN_TYPE_DOUBLE_SQUARE_RIGHT_BRACKET, re.compile(r'^(\]\])')),
    TokenSpec(TOKEN_TYPE_OPT_DOT, re.compile(r'^(\.)')),
)


class Token:
    """
    A token/lexeme in a TOML source file.

    A Token instance is naturally ordered by its type.
    """

    def __init__(self, _type, source_substring, col=None, row=None):
        self._source_substring = source_substring
        self._type = _type
        self._col = col
        self._row = row

    @property
    def col(self):
        """
        Column number (1-indexed).
        """
        return self._col

    @property
    def row(self):
        """
        Row number (1-indexed).
        """
        return self._row

    @property
    def type(self):
        """
        One of of the TOKEN_TYPE_* constants.
        """
        return self._type

    @property
    def source_substring(self):
        """
        The substring of the initial source file containing this token.
        """
        return self._source_substring

    def __lt__(self, other):
        return isinstance(other, Token) and self.type < other.type

    def __repr__(self):
        return "{}: {}".format(self.type, self.source_substring)


def _next_token_candidates(source):
    matches = []
    for token_spec in _LEXICAL_SPECS:
        match = token_spec.re.search(source)
        if match:
            matches.append(Token(token_spec.type, match.group(1)))
    return matches

def _choose_from_next_token_candidates(candidates):

    if len(candidates) == 1:
        return candidates[0]
    elif len(candidates) > 1:
        # Return the maximal-munch with ties broken by natural order of token type.
        maximal_munch_length = max(len(token.source_substring) for token in candidates)
        maximal_munches = [token for token in candidates if len(token.source_substring) == maximal_munch_length]
        return sorted(maximal_munches)[0]   # Return the first in sorting by priority


def _munch_a_token(source):
    """
    Munches a single Token instance if it could recognize one at the beginning of the
    given source text, or None if no token type could be recognized.
    """
    candidates = _next_token_candidates(source)
    return _choose_from_next_token_candidates(candidates)


class LexerError(TOMLError):

    def __init__(self, message):
        self._message = message

    def __repr__(self):
        return "{}".format(self._message)


def tokenize(source):
    """
    Tokenizes the input TOML source into a stream of tokens.

    Raises a LexerError when it fails recognize another token while not at the end of the source.
    """

    # Newlines are going to be normalized to UNIX newlines.
    source = source.replace('\r\n', '\n')

    next_row = 1
    next_col = 1
    next_index = 0

    while next_index < len(source):

        new_token = _munch_a_token(source[next_index:])

        if not new_token:
            raise LexerError("failed to read the next token at ({}, {}): {}".format(
                next_row, next_col, source[next_index:]))

        # Set the col and row on the new token
        new_token = Token(new_token.type, new_token.source_substring, next_col, next_row)

        # Advance the index, row and col count
        next_index += len(new_token.source_substring)
        for c in new_token.source_substring:
            if c == '\n':
                next_row += 1
                next_col = 1
            else:
                next_col += 1

        yield new_token

