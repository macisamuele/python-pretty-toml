from contoml.elements import abstracttable, factory
from contoml.elements.common import Element


class TableElement(abstracttable.AbstractTable):
    """
    An Element containing an unnamed top-level table.

    Implements dict-like interface.

    Assumes input sub_elements are correct.
    """

    def __init__(self, sub_elements):
        abstracttable.AbstractTable.__init__(self, sub_elements)

    def __setitem__(self, key, value):
        if key in self:
            self._update(key, value)
        else:
            self._insert(key, value)

    def _update(self, key, value):
        _, value_i = self._find_key_and_value(key)
        self._sub_elements[value_i] = value if isinstance(value, Element) else factory.create_element(value)

    def _insert(self, key, value):

        new_element = value if isinstance(value, Element) else factory.create_element(value)

        if self:    # If not empty
            insertion_index = len(self.sub_elements)   # Index of last value + 1
            elements = [
                factory.create_newline_element(),
                factory.create_element(key),
                factory.create_whitespace_element(),
                factory.create_operator_element('='),
                factory.create_whitespace_element(),
                new_element,
                factory.create_newline_element(),
            ]
            self._sub_elements = self.sub_elements[:insertion_index] + elements + self.sub_elements[insertion_index:]
        else:
            self._sub_elements = [
                factory.create_element(key),
                factory.create_whitespace_element(),
                factory.create_operator_element('='),
                factory.create_whitespace_element(),
                new_element,
                factory.create_newline_element(),
            ]

    def __delitem__(self, key):
        begin, _ = self._find_key_and_value(key)
        preceding_newline = self._find_preceding_newline(begin)
        if preceding_newline >= 0:
            begin = preceding_newline
        end = self._find_following_newline(begin)
        if end < 0:
            end = len(tuple(self._sub_elements))
        self._sub_elements = self.sub_elements[:begin] + self.sub_elements[end:]

    def value(self):
        return self
