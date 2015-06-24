
class TokenStream:
    """
    An immutable subset of a token sequence
    """

    Nothing = tuple()

    def __init__(self, _tokens, offset=0):
        if isinstance(_tokens, tuple):
            self._tokens = _tokens
        else:
            self._tokens = tuple(_tokens)
        self._next_index = offset

    @property
    def fork(self):
        """
        Returns a clone of this TokenStream over the same token sequence and at the current offset. Advancing the
        clone will not affect this instance.
        """
        return TokenStream(self._tokens, self._next_index)

    @property
    def offset(self):
        return self._next_index

    def next(self):
        """
        Advances this iterator and returns the next item in the sequence, or raises StopIteration.
        """
        return self.__next__()

    def peek(self):
        """
        Returns the next item without advancing the iterator, or TokenStream.Nothing if the end of the sequence
        had been reached.
        """
        try:
            return self._tokens[self._next_index+1]
        except IndexError:
            return TokenStream.Nothing

    def __next__(self):
        try:
            item = self._tokens[self._next_index]
            self._next_index += 1
            return item
        except IndexError:
            raise StopIteration

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

