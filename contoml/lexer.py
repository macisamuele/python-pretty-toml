
import re

# Priority is encoded as the first two characters of each token type. The lower the sort order, the
# higher the priority.
TOKEN_TYPE_STRING = '99-string'
TOKEN_TYPE_MULTILINE_STRING = '99-multiline_string'
TOKEN_TYPE_LITERAL_STRING = '99-literal_string'
TOKEN_TYPE_MULTILINE_LITERAL_STRING = '99-multiline_literal_string'
TOKEN_TYPE_WHITESPACE = '99-whitespace'
TOKEN_TYPE_INTEGER = '00-int'
TOKEN_TYPE_FLOAT = '01-float'
TOKEN_TYPE_BOOLEAN = '00-bool'
TOKEN_TYPE_OP_SQUARE_LEFT_BRACKET = '00-square_left_bracket'
TOKEN_TYPE_OP_SQUARE_RIGHT_BRACKET = '00-square_right_bracket'
TOKEN_TYPE_OP_CURLY_LEFT_BRACKET = '00-curly_left_bracket'
TOKEN_TYPE_OP_CURLY_RIGHT_BRACKET = '00-curly_right_bracket'
TOKEN_TYPE_OP_ASSIGNMENT = '00-assign'
TOKEN_TYPE_OP_COMMA = '00-comma'


# Pairs of TOKEN_TYPE and Token spec in RegExp.
_LEXICAL_SPECS = (
    (TOKEN_TYPE_STRING, re.compile(r'^("(([^"]|\\")+?[^\\]|)")')),                       # Single line only
    (TOKEN_TYPE_MULTILINE_STRING, re.compile(r'^(""".*?""")', re.DOTALL)),
    (TOKEN_TYPE_LITERAL_STRING, re.compile(r"^('.*?')")),
    (TOKEN_TYPE_MULTILINE_LITERAL_STRING, re.compile(r"^('''.*?''')", re.DOTALL)),
    (TOKEN_TYPE_WHITESPACE, re.compile('^(\s+)', re.DOTALL)),                       # Can span multiple lines
    (TOKEN_TYPE_INTEGER, re.compile(r'^(((\+|-)[0-9_]+)|([1-9][0-9_]*))')),
    (TOKEN_TYPE_FLOAT, re.compile(r'^((((\+|-)[0-9_]+)|([1-9][0-9_]*))*(.[0-9_]+)?([eE](\+|-)?[1-9_]+)?)')),
    (TOKEN_TYPE_BOOLEAN, re.compile(r'^(true|false)')),
    (TOKEN_TYPE_OP_SQUARE_LEFT_BRACKET, re.compile(r'^(\[)')),
    (TOKEN_TYPE_OP_SQUARE_RIGHT_BRACKET, re.compile(r'^(\])')),
    (TOKEN_TYPE_OP_CURLY_LEFT_BRACKET, re.compile(r'^(\{)')),
    (TOKEN_TYPE_OP_CURLY_RIGHT_BRACKET, re.compile(r'^(\})')),
    (TOKEN_TYPE_OP_ASSIGNMENT, re.compile(r'^(=)')),
    (TOKEN_TYPE_OP_COMMA, re.compile(r'^(,)')),
)

def consume_token(source):
    """
    Returns a (TOKEN_TYPE, matched_text) pair if could match a token at the beginning of the
    given source text, or None if no token type could be matched.
    """
    matches = []

    for token_type, token_spec in _LEXICAL_SPECS:
        match = token_spec.search(source)
        if match:
            matches.append((token_type, match.group(1)))

    if len(matches) == 1:
        return matches[0]

    elif len(matches) > 1:
        # Return the maximal-munch
        maximal_munch_length = max(len(matched_text) for _, matched_text in matches)
        maximal_munches = [match for match in matches if len(match[1]) == maximal_munch_length]

        return sorted(maximal_munches, key=lambda x: x[0])[0]   # Return the first in sorting by priority
