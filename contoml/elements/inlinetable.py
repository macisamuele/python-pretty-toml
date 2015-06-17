from contoml.elements import common, factory, containertraversalops


class InlineTable(containertraversalops.ContainerTraversalOps):
    """
    An Element containing key-value pairs, representing an inline table.

    Implements dict-like interface.

    Assumes input sub_elements are correct for an inline table element.
    """

    def __init__(self, sub_elements):
        common.ContainerElement.__init__(self, sub_elements)

    def keys(self):
        for key, _ in self.items():
            yield key

    def __len__(self):
        return len(tuple(self.keys()))

    def _enumerate_items(self):
        """
        Returns ((key_index, key_element), (value_index, value_element)) for all the element key-value pairs.
        """
        non_metadata = self._enumerate_non_metadata_sub_elements()
        while True:
            key_i, key = next(non_metadata)
            value_i, value = next(non_metadata)
            if key_i and value_i:
                yield ((key_i, key), (value_i, value))
            else:
                break

    def items(self):
        for (key_i, key), (value_i, value) in self._enumerate_items():
            yield key.value, value.value

    def __contains__(self, item):
        return item in self.keys()

    def __getitem__(self, item):
        for key, value in self.items():
            if key == item:
                return value
        raise KeyError

    def _entry(self, entry_key):
        """
        Returns the [begin, end) range of indices including the key and value for the given key.

        Raises KeyError if key was not found.
        """

        # A comma followed by whitespace is a suffix to a key-value pair, not a prefix.
        # The last entry in the table will not contain a comma-followed-by-whitespace suffix.

        def find_beginning(key_index):
            # Finds the beginning element index of this entry
            preceding_comma = self._find_preceding_comma(key_index)
            if preceding_comma >= 0:
                return self._find_following_non_metadata(preceding_comma)
            return next(self._enumerate_non_metadata_sub_elements())[0]

        def find_end(key_index):
            # Finds end of the element where the given index belongs to the key
            following_comma = self._find_following_comma(key_index)
            if following_comma >= 0:
                return self._find_following_non_metadata(following_comma)
            return self._find_following_curly_bracket(key_index)

        key_index, _ = self._find_key_and_value(entry_key)
        return find_beginning(key_index), find_end(key_index)

    def _find_key_and_value(self, key):
        """
        Returns (key_i, value_i) corresponding to the given key value.

        Raises KeyError if no matching key found.
        """
        for (key_i, key_element), (value_i, value_element) in self._enumerate_items():
            if key_element.value == key:
                return key_i, value_i
        raise KeyError

    def _index_for_new_entry(self):
        """
        Returns the index where a new key-value pair can be inserted.
        """
        enumerated_non_metadata_elements = tuple(self._enumerate_non_metadata_sub_elements())
        if enumerated_non_metadata_elements:
            return enumerated_non_metadata_elements[-1][0] + 1      # Index following last non-metadata element
        else:
            return self._find_following_curly_bracket(0)

    def __setitem__(self, key, value):

        try:
            key_i, value_i = self._find_key_and_value(key)
            # Found, then replace the value element with a new one
            self._sub_elements = self.sub_elements[:value_i] + \
                                 [factory.create_element(value)] + \
                                 self.sub_elements[value_i+1:]

        except KeyError:    # Key does not exist!

            new_entry = [
                factory.create_element(key),
                factory.create_whitespace_element(),
                factory.create_operator_element('='),
                factory.create_whitespace_element(),
                factory.create_element(value),
            ]

            if self:    # If not empty
                new_entry = [
                    factory.create_operator_element(','),
                    factory.create_whitespace_element(),
                ] + new_entry

            insertion_index = self._index_for_new_entry()
            self._sub_elements = self.sub_elements[:insertion_index] + new_entry + self.sub_elements[insertion_index:]

    def __delitem__(self, key):
        begin, end = self._entry(key)
        preceding_comma = self._find_preceding_comma(begin)
        if preceding_comma >= 0:
            begin = preceding_comma
        self._sub_elements = self.sub_elements[:begin] + self.sub_elements[end:]

    def value(self):
        return self     # self is a dict-like value that is perfectly usable
