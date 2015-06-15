from abc import abstractmethod
from contoml import toml2py, py2toml, tokens

TYPE_METADATA = 'element-metadata'
TYPE_ATOMIC = 'element-atomic'
TYPE_CONTAINER = 'element-container'


class Element:
    """
    An Element:
        - is one or more Token instances, or one or more other Element instances. Not both.
        - knows how to serialize its value back to valid TOML code.

    A non-metadata Element is an Element that:
        - knows how to deserialize its content into usable Python primitive, seq-like,  or dict-like value.
        - knows how to update its content from a Python primitive, seq-like, or dict-like value
            while maintaining its formatting.
    """

    def __init__(self, _type):
        self._type = _type

    @property
    def type(self):
        return self._type

    @abstractmethod
    def serialized(self):
        """
        TOML serialization of this element as str.
        """
        raise NotImplementedError


class TokenElement(Element):
    """
    An Element made up of tokens
    """

    def __init__(self, _tokens, _type):
        Element.__init__(self, _type)
        self._validate_tokens(_tokens)
        self._tokens = list(_tokens)

    @property
    def tokens(self):
        return self._tokens

    @abstractmethod
    def _validate_tokens(self, _tokens):
        raise NotImplementedError

    def serialized(self):
        return ''.join(token.source_substring for token in self._tokens)


class ContainerElement(Element):
    """
    An Element containing exclusively other elements.
    """

    def __init__(self, sub_elements):
        Element.__init__(self, TYPE_CONTAINER)
        self._sub_elements = sub_elements

    @property
    def sub_elements(self):
        return self._sub_elements

    def serialized(self):
        return ''.join(element.serialized() for element in self._sub_elements)


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

    def _validate_tokens(self, _tokens):
        assert _tokens
        assert tokens.is_operator(_tokens[0])


class AtomicElement(TokenElement):
    """
    An element containing a sequence of tokens representing a single atomic value that can be updated in place.
    """

    def __init__(self, _tokens):
        TokenElement.__init__(self, _tokens, TYPE_ATOMIC)

    def _validate_tokens(self, _tokens):
        # Must  contain only one non-metadata token
        assert len([token for token in _tokens if not token.type.is_metadata]) == 1

    def serialized(self):
        return ''.join(token.source_substring for token in self.tokens)

    def _value_token_index(self):
        """
        Finds the token where the value is stored.
        """
        # TODO: memoize this value
        for i, token in enumerate(self.tokens):
            if not token.type.is_metadata:
                return i
        raise RuntimeError('could not find a value token')

    @property
    def value(self):
        """
        Returns a Python value contained in this atomic element.
        """
        return toml2py.deserialize(self._tokens[self._value_token_index()])

    def set(self, value):
        """
        Sets the contained value to the given one.
        """
        token_index = self._value_token_index()
        token_type = self._tokens[token_index].type
        new_token = py2toml.serialize(value, token_type)
        self._tokens[token_index] = new_token


class ArrayElement(ContainerElement):
    """
    A sequence-like container element containing other atomic elements or other containers.
    """

    def __init__(self, sub_elements):
        ContainerElement.__init__(self, sub_elements)

    def _non_metadata_sub_elements(self):
        return [element for element in self.sub_elements if element.type != TYPE_METADATA]

    def __len__(self):
        return len(self._non_metadata_sub_elements())

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    @property
    def value(self):
        return self

    def get(self, i):
        """
        Returns the element at the ith index, which can be a primitive value, a seq-lie, or a dict-like object.
        """
        return self._non_metadata_sub_elements()[i].value

    def set(self, i, value):
        """
        Sets the element at the ith index to the given value.
        """
        pass
