from contoml import tokens
from contoml.elements import common, metadata
from contoml.elements.metadata import PunctuationElement


class ContainerTraversalOps(common.ContainerElement):
    """
    A mix-in to ContainerElement to provide handy traversal operations.
    """

    def _enumerate_non_metadata_sub_elements(self):
        """
        Returns a sequence of of (index, sub_element) of the non-metadata sub-elements.
        """
        return ((i, element) for i, element in enumerate(self.sub_elements) if element.type != common.TYPE_METADATA)

    def _find_preceding_comma(self, index):
        """
        Returns the index of the preceding comma element to the given index, or -Infinity.
        """
        for i, element in reversed(tuple(enumerate(self.sub_elements))[:index]):
            if isinstance(element, metadata.PunctuationElement) and element.token.type == tokens.TYPE_OP_COMMA:
                return i
        return float('-inf')

    def _find_following_comma(self, index):
        """
        Returns the index of the following comma element after the given index, or -Infinity.
        """
        for i, element in tuple(enumerate(self.sub_elements))[index+1:]:
            if isinstance(element, metadata.PunctuationElement) and element.token.type == tokens.TYPE_OP_COMMA:
                return i
        return float('-inf')

    def _find_following_curly_bracket(self, index):
        """
        Returns the index of the following closing curly bracket element after the given index, or -Infinity.
        """
        for i, element in tuple(enumerate(self.sub_elements))[index+1:]:
            if isinstance(element, metadata.PunctuationElement) and \
                            element.token.type == tokens.TYPE_OP_CURLY_RIGHT_BRACKET:
                return i
        return float('-inf')

    def _find_following_non_metadata(self, index):
        """
        Returns the index to the following non-metadata element after the given index, or -Infinity.
        """
        for i, element in tuple(enumerate(self.sub_elements))[index+1:]:
            if element.type != common.TYPE_METADATA:
                return i
        return float('-inf')

    def _find_closing_square_bracket(self):
        """
        Returns the index to the closing square bracket, or raises an Error.
        """
        for i, element in reversed(tuple(enumerate(self.sub_elements))):
            if isinstance(element, PunctuationElement) and element.token.type == tokens.TYPE_OP_SQUARE_RIGHT_BRACKET:
                return i
        raise RuntimeError('Not finding a closing square bracket is unexpected!!')

    def _find_closing_curly_bracket(self):
        """
        Returns the index to the closing curly bracket, or raises an Error.
        """
        for i, element in reversed(tuple(enumerate(self.sub_elements))):
            if isinstance(element, PunctuationElement) and element.token.type == tokens.TYPE_OP_CURLY_RIGHT_BRACKET:
                return i
        raise RuntimeError('Not finding a closing square bracket is unexpected!!')
