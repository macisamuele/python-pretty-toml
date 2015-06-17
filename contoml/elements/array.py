from contoml import tokens
from contoml.elements import common, factory
from contoml.elements.factory import create_element
from contoml.elements.metadata import PunctuationElement, WhitespaceElement


class ArrayElement(common.ContainerElement):
    """
    A sequence-like container element containing other atomic elements or other containers.

    Implements list-like interface.

    Assumes input sub_elements are correct for an array element.
    """

    def __init__(self, sub_elements):
        common.ContainerElement.__init__(self, sub_elements)

    def __len__(self):
        return len(self._enumerate_non_metadata_sub_elements())

    def __getitem__(self, i):
        """
        Returns the ith entry, which can be a primitive value, a seq-lie, or a dict-like object.
        """
        return self._enumerate_non_metadata_sub_elements()[i][1].value

    def __setitem__(self, i, value):
        entry_elements = [
            factory.create_operator_element(','),
            factory.create_whitespace_element(),
            create_element(value),
        ]
        begin, end = self._entry(i)
        self._sub_elements = self._sub_elements[:begin] + entry_elements + self._sub_elements[end:]

    @property
    def value(self):
        return self     # self is a sequence-like value

    def _enumerate_non_metadata_sub_elements(self):
        """
        Returns a sequence of of (index, sub_element) of the non-metadata sub-elements.
        """
        return [(index, element)
                for index, element in enumerate(self.sub_elements)
                if element.type != common.TYPE_METADATA]

    def _entry(self, i):
        """
        Returns the range of indices comprising the ith entry and its punctuation.

        Raises IndexError if no entry exists.
        """
        index, _ = self._enumerate_non_metadata_sub_elements()[i]

        # Begins at the previous index of comma or lowest index of whitespace before the [ operator
        begin = next(element_i
                        for element_i, element in reversed(tuple(enumerate(self.sub_elements)))
                        if element_i < index and isinstance(element, PunctuationElement) and
                        element.token.type == tokens.TYPE_OP_COMMA)

        if begin is None:
            bracket_i = next(element_i for element_i, element in enumerate(self.sub_elements)
                             if isinstance(element, PunctuationElement) and
                             element.token.type == tokens.TYPE_OP_SQUARE_LEFT_BRACKET)
            begin = next(element_i for element_i, element in enumerate(self.sub_elements)
                         if element_i > bracket_i and isinstance(element, WhitespaceElement))

        begin = index if begin is None else begin

        # Ends at the next comma or closing bracket
        end = next(element_i for element_i, element in enumerate(self.sub_elements)
                   if element_i > index and isinstance(element, PunctuationElement) and
                   element.token.type in (tokens.TYPE_OP_COMMA, tokens.TYPE_OP_SQUARE_RIGHT_BRACKET))

        return begin, end

    def append(self, v):
        new_entry = [
            factory.create_operator_element(','),
            factory.create_whitespace_element(),
            create_element(v),
        ]

        last_bracket_index = next(element_i for element_i, element in reversed(tuple(enumerate(self.sub_elements)))
                                  if isinstance(element, PunctuationElement) and
                                  element.token.type == tokens.TYPE_OP_SQUARE_RIGHT_BRACKET)

        self._sub_elements = self._sub_elements[:last_bracket_index] + new_entry + \
                             self._sub_elements[last_bracket_index:]

    def __delitem__(self, i):
        begin, end = self._entry(i)
        self._sub_elements = self.sub_elements[:begin] + self._sub_elements[end:]
