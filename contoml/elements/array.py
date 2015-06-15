from contoml import tokens
from contoml.elements import common, factory
from contoml.elements.factory import create_element
from contoml.elements.metadata import PunctuationElement


class ArrayElement(common.ContainerElement):
    """
    A sequence-like container element containing other atomic elements or other containers.
    """

    def __init__(self, sub_elements):
        common.ContainerElement.__init__(self, sub_elements)

    def _non_metadata_sub_elements(self):
        return [element for element in self.sub_elements if element.type != common.TYPE_METADATA]

    def __len__(self):
        return len(self._non_metadata_sub_elements())

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    @property
    def value(self):
        return self     # Self is a sequence-like value

    def get(self, i):
        """
        Returns the element at the ith index, which can be a primitive value, a seq-lie, or a dict-like object.
        """
        if i >= len(self):
            raise IndexError
        i %= len(self)  # Turn a negative index positive

        return self._non_metadata_sub_elements()[i].value

    def _ith_non_metadata_index(self, i):
        """
        Returns the index in self.sub_elements of the ith non-metadata element.
        """

        if i >= len(self):
            raise IndexError

        i %= len(self)      # Turn a negative index positive

        index = -1
        for actual_index, element in enumerate(self.sub_elements):
            if element.type != common.TYPE_METADATA:
                index += 1
            if index == i:
                return actual_index
        raise IndexError

    def set(self, i, value):
        """
        Sets the element at the ith index to the given value.
        """
        self.sub_elements[self._ith_non_metadata_index(i)] = create_element(value)

    def append(self, v):
        self.sub_elements.insert(-1, factory.create_operator_element(','))
        self.sub_elements.insert(-1, factory.create_whitespace_element())
        self.sub_elements.insert(-1, create_element(v))

    def _entry_elements(self, i):
        """
        Returns the set of indices belonging to the ith entry in the array.
        """
        element_main_index = self._ith_non_metadata_index(i)

        begin = element_main_index - 1  # Should be the index of the previous element that is not a comma or a '[' op
        while True:
            element = self.sub_elements[begin]
            if isinstance(element, PunctuationElement) and element.token.type in \
                    (tokens.TYPE_OP_SQUARE_LEFT_BRACKET, tokens.TYPE_OP_COMMA):
                break
            begin -= 1

        end = element_main_index + 1  # First non-metadata element after the ith entry element
        while self.sub_elements[end].type != common.TYPE_METADATA:
            end += 1

        return begin, end

    def __delitem__(self, i):
        begin, end = self._entry_elements(i)
        del self.sub_elements[begin:end]
