from contoml.parser.errors import ParsingError


class Captured:
    """
    Recursive-descent matching DSL. Yeah..
    """

    def __init__(self, token_stream, value=tuple(), error=None):
        self._token_stream = token_stream
        self._value = value
        self._error = error

    def extract(self, element_factory):
        try:
            element, pending_ts = element_factory(self._token_stream.fork)
            if not isinstance(element, (tuple, list)):
                element = (element,)
            return Captured(pending_ts, value=self.value() + element)
        except ParsingError as e:
            return Captured(self._token_stream, error=e)
        except StopIteration:
            return Captured(self._token_stream, error=ParsingError('Unexpected end of tokens'))

    def value(self, expectation_msg=None):
        if self._error:
            if expectation_msg:
                raise ParsingError(expectation_msg, token=self._token_stream.peek())
            else:
                raise self._error
        return self._value

    @property
    def pending_tokens(self):
        return self._token_stream

    def or_extract(self, element_factory):
        if self._error:
            return Captured(self._token_stream).extract(element_factory)
        else:
            return self

    def and_extract(self, element_factory):
        if self._error:
            raise self._error
        return Captured(self.pending_tokens, self.value()).extract(element_factory)


def capture_from(token_stream):
    return Captured(token_stream)

