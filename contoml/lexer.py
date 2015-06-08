import re

# Priority is encoded as the first two characters of each token type. The lower the sort order, the
# higher the priority.
TOKEN_TYPE_BOOLEAN = '00-bool'
TOKEN_TYPE_INTEGER = '00-int'
TOKEN_TYPE_OP_COMMA = '00-comma'
TOKEN_TYPE_OP_SQUARE_LEFT_BRACKET = '00-square_left_bracket'
TOKEN_TYPE_OP_SQUARE_RIGHT_BRACKET = '00-square_right_bracket'
TOKEN_TYPE_OP_CURLY_LEFT_BRACKET = '00-curly_left_bracket'
TOKEN_TYPE_OP_CURLY_RIGHT_BRACKET = '00-curly_right_bracket'
TOKEN_TYPE_OP_ASSIGNMENT = '00-assign'
TOKEN_TYPE_DOUBLE_SQUARE_LEFT_BRACKET = '00-double_square_left_bracket'
TOKEN_TYPE_DOUBLE_SQUARE_RIGHT_BRACKET = '00-double_square_right_bracket'
TOKEN_TYPE_FLOAT = '01-float'
TOKEN_TYPE_DATE = '40-date'
TOKEN_TYPE_OPT_DOT = '40-op_dot'
TOKEN_TYPE_BARE_STRING = '50-bare_string'
TOKEN_TYPE_STRING = '90-string'
TOKEN_TYPE_MULTILINE_STRING = '90-multiline_string'
TOKEN_TYPE_LITERAL_STRING = '90-literal_string'
TOKEN_TYPE_MULTILINE_LITERAL_STRING = '90-multiline_literal_string'
TOKEN_TYPE_WHITESPACE = '90-whitespace'
TOKEN_TYPE_COMMENT = '95-comment'


# Pairs of TOKEN_TYPE and Token spec in RegExp.
_LEXICAL_SPECS = (
    (TOKEN_TYPE_COMMENT, re.compile(r'^(#.*)\n')),
    (TOKEN_TYPE_STRING, re.compile(r'^("(([^"]|\\")+?[^\\]|)")')),                       # Single line only
    (TOKEN_TYPE_MULTILINE_STRING, re.compile(r'^(""".*?""")', re.DOTALL)),
    (TOKEN_TYPE_LITERAL_STRING, re.compile(r"^('.*?')")),
    (TOKEN_TYPE_MULTILINE_LITERAL_STRING, re.compile(r"^('''.*?''')", re.DOTALL)),
    (TOKEN_TYPE_BARE_STRING, re.compile(r'^([A-Za-z0-9_-]+)')),
    (TOKEN_TYPE_DATE, re.compile(
        r'^([0-9]{4}-[0-9]{2}-[0-9]{2}(T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]*)?)?(([zZ])|((\+|-)[0-9]{2}:[0-9]{2}))?)')),
    (TOKEN_TYPE_WHITESPACE, re.compile('^(\s+)', re.DOTALL)),                       # Can span multiple lines
    (TOKEN_TYPE_INTEGER, re.compile(r'^(((\+|-)[0-9_]+)|([1-9][0-9_]*))')),
    (TOKEN_TYPE_FLOAT, re.compile(r'^((((\+|-)[0-9_]+)|([1-9][0-9_]*))(.[0-9_]+)?([eE](\+|-)?[1-9_]+)?)')),
    (TOKEN_TYPE_BOOLEAN, re.compile(r'^(true|false)')),
    (TOKEN_TYPE_OP_SQUARE_LEFT_BRACKET, re.compile(r'^(\[)')),
    (TOKEN_TYPE_OP_SQUARE_RIGHT_BRACKET, re.compile(r'^(\])')),
    (TOKEN_TYPE_OP_CURLY_LEFT_BRACKET, re.compile(r'^(\{)')),
    (TOKEN_TYPE_OP_CURLY_RIGHT_BRACKET, re.compile(r'^(\})')),
    (TOKEN_TYPE_OP_ASSIGNMENT, re.compile(r'^(=)')),
    (TOKEN_TYPE_OP_COMMA, re.compile(r'^(,)')),
    (TOKEN_TYPE_DOUBLE_SQUARE_LEFT_BRACKET, re.compile(r'^(\[\[)')),
    (TOKEN_TYPE_DOUBLE_SQUARE_RIGHT_BRACKET, re.compile(r'^(\]\])')),
    (TOKEN_TYPE_OPT_DOT, re.compile(r'^(\.)')),
)


class Token:
    """
    A token/lexeme in a TOML source file.
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

    def __repr__(self):
        return "{}: {}".format(self.type, self.source_substring)


def _next_token(source):
    """
    Returns a single Token instance if could recognize one at the beginning of the
    given source text, or None if no token type could be recognized.
    """
    matches = []

    for token_type, token_spec in _LEXICAL_SPECS:
        match = token_spec.search(source)
        if match:
            matches.append(Token(token_type, match.group(1)))

    if len(matches) == 1:
        return matches[0]

    elif len(matches) > 1:
        # Return the maximal-munch
        maximal_munch_length = max(len(token.source_substring) for token in matches)
        maximal_munches = [token for token in matches if len(token.source_substring) == maximal_munch_length]

        return sorted(maximal_munches, key=lambda x: x.type)[0]   # Return the first in sorting by priority


class LexerError:

    def __init__(self, message):
        self._message = message

    def __repr__(self):
        return "{}".format(self._message)


def tokenize(source):
    """
    Tokenizes the input TOML source into a stream of tokens.

    Raises a LexerError when it fails recognize another token while not at the end of the source.
    """

    source = source.replace('\r\n', '\n')

    next_row = 1
    next_col = 1
    next_index = 0

    while next_index < len(source):

        new_token = _next_token(source[next_index:])

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

