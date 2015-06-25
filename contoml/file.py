import itertools
from contoml import elements
from contoml.cascadedict import CascadeDict
from contoml.elements.table import TableElement
from contoml.elements.tableheader import TableHeaderElement
from contoml.errors import InvalidTOMLFileError
from contoml.peekableit import PeekableIterator

class TOMLFile(elements.TraversalMixin):
    """
    A TOMLFile instance is made up of TableElement and TableHeaderElement elements.

    Raises InvalidTOMLFileError on invalid input elements.
    """

    def __init__(self, _elements, name_prefixes=(), traversal_index=None):
        TOMLFile._validate_elements(_elements)
        self._elements = _elements
        self._name_prefixes = name_prefixes
        self._traversal_index = traversal_index

    @staticmethod
    def _validate_elements(_elements):

        # Non-metadata elements must start with an optional TableElement, followed by
        # zero or more (TableHeaderElement, TableElement) pairs.

        if not _elements:
            return

        it = PeekableIterator(e for e in _elements if e.type != elements.TYPE_METADATA)

        if isinstance(it.peek(), TableElement):
            it.next()

        while it.peek():
            if not isinstance(it.next(), TableHeaderElement):
                raise InvalidTOMLFileError
            if not isinstance(it.next(), TableElement):
                raise InvalidTOMLFileError

    @property
    def elements(self):
        return self._elements

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._lookup_name(item)
        elif isinstance(item, int):
            return self._lookup_index(item)

    def _anonymous_table(self):
        """
        Returns the TableElement of the anonymous table, or raises a KeyError if not found.
        """
        non_metadata_lements = tuple(self._non_metadata_elements())
        if not isinstance(non_metadata_lements[0], TableElement):
            raise KeyError
        return non_metadata_lements[0]

    def _non_metadata_elements(self):
        for e in self.elements:
            if e.type != elements.TYPE_METADATA:
                yield e

    def _enumerate_table_headers(self):
        """
        Enumerates (element_index, table_header_element) of table headers.
        """
        for i, element in enumerate(self.elements):
            if isinstance(element, TableHeaderElement) and not element.is_array_of_tables:
                yield i, element

    def _enumerate_array_of_table_headers(self):
        """
        Enumerates (element_index, array_of_table_header_element) of array of table headers.
        """
        for i, element in enumerate(self.elements):
            if isinstance(element, TableHeaderElement) and element.is_array_of_tables:
                yield i, element

    def _lookup_name(self, name):
        if not self._name_prefixes:

            # Anonymous table check first`
            if name == '':
                return self._anonymous_table()

            # Try to find a full table match
            for i, table_header in self._enumerate_table_headers():
                if table_header.is_named((name,)):
                    table = self.elements[i+1]
                    return CascadeDict((table, TOMLFile(self.elements, name_prefixes=(name,))))

            # Try to find a full array of tables match
            for i, table_header in self._enumerate_array_of_table_headers():
                if table_header.is_named((name,)):
                    return TOMLFile(self.elements, name_prefixes=(name,))

            # Try to find a partial prefix match
            for _, table_header in \
                    itertools.chain(self._enumerate_table_headers(), self._enumerate_array_of_table_headers()):

                if table_header.has_name_prefix((name,)):
                    return TOMLFile(self.elements, name_prefixes=(name,))
        else:

            full_name = self._name_prefixes + (name,)

            # Try to find a full-name match
            for i, table_header in self._enumerate_table_headers():
                if table_header.is_named(full_name):
                    table = self.elements[i+1]
                    return CascadeDict((table, TOMLFile(self.elements, name_prefixes=full_name)))

            # Try to find a full array of tables match
            for i, table_header in self._enumerate_array_of_table_headers():
                if table_header.is_named(full_name):
                    return TOMLFile(self.elements, name_prefixes=full_name)

            # Try to find a partial match
            for i, table_header in \
                    itertools.chain(self._enumerate_table_headers(), self._enumerate_array_of_table_headers()):
                if table_header.names == full_name:
                    return TOMLFile(self.elements, name_prefixes=full_name)

        # Give up
        raise KeyError

    def _lookup_index(self, index):

        if not self._name_prefixes:
            raise IndexError

        matching_headers = tuple((i, header) for i, header in self._enumerate_array_of_table_headers()
                                 if header.is_named(self._name_prefixes))

        return self.elements[matching_headers[index][0]+1]

    def serialized(self):
        """
        Returns the TOML file serialized back to str.
        """
        return ''.join(element.serialized() for element in self.elements)
