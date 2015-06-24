
class TokenStream:
    """
    An immutable subset of a token sequence
    """

    class EndOfStream(Exception):
        pass

    Nothing = tuple()

    def __init__(self, _tokens, offset=0):
        if isinstance(_tokens, tuple):
            self._tokens = _tokens
        else:
            self._tokens = tuple(_tokens)
        self._head_index = offset

    @property
    def head(self):
        try:
            return self._tokens[self._head_index]
        except IndexError:
            raise TokenStream.EndOfStream

    @property
    def tail(self):
        return TokenStream(self._tokens, offset=self._head_index+1)

    @property
    def offset(self):
        return self._head_index


# class TokenStream:
#     """
#     A stream of tokens where tokens is an iterable of tokens.Token instances.
#     """
#
#     def __init__(self, _tokens):
#         if isinstance(_tokens, (list, tuple)):
#             self._tokens = _tokens
#         else:
#             self._tokens = tuple(_tokens)
#
#     @property
#     def head(self):
#         """
#         Returns the head of the token stream. Never mutates the stream itself, will always return
#         the same head on the same instance of TokenStream.
#
#         Raises a ParsingError if ran out of tokens and head was requested.
#         """
#         if self._tokens:
#             return self._tokens[0]
#         else:
#             raise ParsingError('Unexpected end of TOML source')
#
#     def skip(self, n):
#         """
#         Returns a new TokenStream with n tokens skipped.
#         """
#         if len(self._tokens) < n:
#             return TokenStream(list())
#         else:
#             return TokenStream(self._tokens[n:])
#
#     @property
#     def tail(self):
#         return self.skip(1)
#
#     @property
#     def whitespace_count(self):
#         if self.head.type == TYPE_WHITESPACE:
#             return
#
#     def __len__(self):
#         return len(self._tokens)

