
from contoml.lexer import *

# A mapping from token types to a sequence of pairs of (source_text, expected_matched_text)
valid_tokens = {
    TOKEN_TYPE_STRING: (
        ('"a valid hug3 text" "some other string" = 42', '"a valid hug3 text"'),
        (
            r'"I\'m a string. \"You can quote me\". Name\tJos\u00E9\nLocation\tSF." "some other string" = 42',
            r'"I\'m a string. \"You can quote me\". Name\tJos\u00E9\nLocation\tSF."'
        ),
    ),
    TOKEN_TYPE_MULTILINE_STRING: (
        ('"""\nRoses are red\nViolets are blue""" """other text"""', '"""\nRoses are red\nViolets are blue"""'),
    ),
    TOKEN_TYPE_LITERAL_STRING: (
        (r"'This is \ \n a \\ literal string' 'another \ literal string'", r"'This is \ \n a \\ literal string'"),
    ),
    TOKEN_TYPE_MULTILINE_LITERAL_STRING: (
        (
            "'''\nThe first newline is\ntrimmed in raw strings.\n   All other whitespace\n   is preserved.\n''' '''some other\n\n\t string'''",
            "'''\nThe first newline is\ntrimmed in raw strings.\n   All other whitespace\n   is preserved.\n'''"
        ),
    ),
    TOKEN_TYPE_WHITESPACE: (
        (' \t\n \r  some_text', ' \t\n \r  '),
    ),
    TOKEN_TYPE_INTEGER: (
        ('+99 "number"', "+99"),
        ('42 fwfwef', "42"),
        ('-17 fh34g34g', "-17"),
        ('5_349_221 apples', "5_349_221"),
        ('-1_2_3_4_5 steps', '-1_2_3_4_5')
    ),
    TOKEN_TYPE_FLOAT: (
        ('1.0 fwef', '1.0'),
        ('3.1415 g4g', '3.1415'),
        ('-0.01 433re', '-0.01'),
        ('5e+2_2ersdvf', '5e+2_2'),
        ('1e6ewe23', '1e6'),
        ('-2E-2.23rf23', '-2E-2'),
        ('6.626e-34+234f', '6.626e-34'),
        ('9_224_617.445_991_228_313f1ewer 23f4h = nonesense', '9_224_617.445_991_228_313'),
        ('1e1_000 2346f,ef2!!', '1e1_000'),
    ),
    TOKEN_TYPE_BOOLEAN: (
        ('false business = true', 'false'),
        ('true true', 'true'),
    ),
    TOKEN_TYPE_OP_SQUARE_LEFT_BRACKET: (
        ('[table_name]', '['),
    ),
    TOKEN_TYPE_OP_SQUARE_RIGHT_BRACKET: (
        (']\nbusiness = awesome', ']'),
    ),
    TOKEN_TYPE_OP_CURLY_LEFT_BRACKET: (
        ('{item_exists = no}', '{'),
    ),
    TOKEN_TYPE_OP_CURLY_RIGHT_BRACKET: (
        ('} moving on', '}'),
    ),
    TOKEN_TYPE_OP_COMMA: (
        (',item2,item4', ','),
    ),
    TOKEN_TYPE_OP_ASSIGNMENT: (
        ('== 42', '='),
    )
}

# A mapping from a token type to a sequence of (source, matched_text) pairs that shouldn't result from consuming the
# source text.
invalid_tokens = {
    TOKEN_TYPE_INTEGER: (
        ('_234_423', ''),
        ('0446234234', ''),
    ),
    TOKEN_TYPE_STRING: (
        ('"""', '"""'),
    ),
    TOKEN_TYPE_BOOLEAN: (
        ('True', 'True'),
        ('True', 'true'),
    )
}

def test_valid_tokenizing():
    for token_type in valid_tokens:
        for (source, expected_match) in valid_tokens[token_type]:

            token_data = consume_token(source)
            assert token_data, "Failed to tokenize: {}\nExpected: {}\nOut of: {}\nGot nothing!".format(token_type, expected_match, source)

            recognized_type, matched_text = token_data
            assert recognized_type == token_type
            assert matched_text == expected_match


def test_invalid_tokenizing():
    for token_type in invalid_tokens:
        for source, expected_match in invalid_tokens[token_type]:
            token_data = consume_token(source)
            if token_data:
                assert token_data[0] != token_type or token_data[1] != expected_match
