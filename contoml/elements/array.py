from contoml.elements import common, factory, containertraversalops
from contoml.elements.factory import create_element


class ArrayElement(containertraversalops.ContainerTraversalOps):
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
        value_i, _ = self._enumerate_non_metadata_sub_elements()[i]
        self._sub_elements = self.sub_elements[:value_i] + \
                             [factory.create_element(value)] + self.sub_elements[value_i+1:]

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

    def append(self, v):
        new_entry = [create_element(v)]

        if self:    # If not empty, we need a comma and whitespace prefix!
            new_entry = [
                factory.create_operator_element(','),
                factory.create_whitespace_element(),
            ] + new_entry

        last_bracket_index = self._find_closing_square_bracket()

        self._sub_elements = self._sub_elements[:last_bracket_index] + new_entry + \
                             self._sub_elements[last_bracket_index:]

    def __delitem__(self, i):
        value_i, value = self._enumerate_non_metadata_sub_elements()[i]

        begin, end = value_i, value_i+1

        preceding_comma_i = self._find_preceding_comma(value_i)
        if preceding_comma_i >= 0:
            begin = preceding_comma_i
        following_comma_i = self._find_following_comma(value_i)
        if following_comma_i >= 0:
            end = following_comma_i
        else:
            end = self._find_closing_square_bracket()

        self._sub_elements = self.sub_elements[:begin] + self._sub_elements[end:]
