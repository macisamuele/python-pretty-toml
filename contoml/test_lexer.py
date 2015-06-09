# -*- coding: utf-8 -*-

from .lexer import _next_token
from .lexer import *

# A mapping from token types to a sequence of pairs of (source_text, expected_matched_text)
valid_tokens = {
    TOKEN_TYPE_COMMENT: (
        (
            '# My very insightful comment about the state of the universe\n# And now for something completely different!',
            '# My very insightful comment about the state of the universe',
        ),
    ),
    TOKEN_TYPE_STRING: (
        ('"a valid hug3 text" "some other string" = 42', '"a valid hug3 text"'),
        (
            r'"I\'m a string. \"You can quote me\". Name\tJos\u00E9\nLocation\tSF." "some other string" = 42',
            r'"I\'m a string. \"You can quote me\". Name\tJos\u00E9\nLocation\tSF."'
        ),
        ('"ʎǝʞ" key', '"ʎǝʞ"'),
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
    TOKEN_TYPE_DATE: (
        ('1979-05-27 5345', '1979-05-27'),
        ('1979-05-27T07:32:00Z something', '1979-05-27T07:32:00Z'),
        ('1979-05-27T00:32:00-07:00 ommm', '1979-05-27T00:32:00-07:00'),
        ('1979-05-27T00:32:00.999999-07:00 2346', '1979-05-27T00:32:00.999999-07:00'),
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
        ('5e+2_2 ersdvf', '5e+2_2'),
        ('1e6 ewe23', '1e6'),
        ('-2E-2.2 3 rf23', '-2E-2'),
        ('6.626e-34 +234f', '6.626e-34'),
        ('9_224_617.445_991_228_313 f1ewer 23f4h = nonesense', '9_224_617.445_991_228_313'),
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
    ),
    TOKEN_TYPE_DOUBLE_SQUARE_LEFT_BRACKET: (
        ('[[array.of.tables]]', '[['),
    ),
    TOKEN_TYPE_DOUBLE_SQUARE_RIGHT_BRACKET: (
        (']] item=3', ']]'),
    ),
    TOKEN_TYPE_BARE_STRING: (
        ('key another', 'key'),
        ('bare_key 2fews', 'bare_key'),
        ('bare-key kfcw', 'bare-key'),
    ),
    TOKEN_TYPE_OPT_DOT: (
        ('."another key"', '.'),
        ('.subname', '.'),

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
    ),
    TOKEN_TYPE_FLOAT: (
        ('', ''),
    )
}

def test_valid_tokenizing():
    for token_type in valid_tokens:
        for (source, expected_match) in valid_tokens[token_type]:

            token = _next_token(source)
            assert token, "Failed to tokenize: {}\nExpected: {}\nOut of: {}\nGot nothing!".format(
                token_type, expected_match, source)

            assert token.type == token_type, \
                "Expected type: {}\nOut of: {}\nThat matched: {}\nOf type: {}".format(
                    token_type, source, token.source_substring, token.type)
            assert token.source_substring == expected_match


def test_invalid_tokenizing():
    for token_type in invalid_tokens:
        for source, expected_match in invalid_tokens[token_type]:
            token = _next_token(source)
            if token:
                assert not (token.type == token_type and token.source_substring == expected_match)


def test_tokenizing_sample_file():
    source = open('sample.toml').read()
    # Number of valid tokens was manually verified
    assert len(list(tokenize(source))) == 147
