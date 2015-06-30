import itertools

from contoml import elements
from contoml.file import elementsanitizer, structurer, entries
from contoml.file.cascadedict import CascadeDict
from contoml.elements.table import TableElement
from contoml.elements.tableheader import TableHeaderElement


class TOMLFile:
    """
    A TOMLFile object that tries its best to prserve formatting and order of mappings of the input source.

    Raises InvalidTOMLFileError on invalid input elements.
    """

    def __init__(self, _elements):
        sanitized_elements = elementsanitizer.sanitize(_elements)
        elementsanitizer.sanitize(_elements)

        self._elements = sanitized_elements

        self._navigable = structurer.structure(entries.extract(self._elements))

    def __getitem__(self, item):
        return self._navigable[item]

    def serialized(self):
        """
        Returns the TOML file serialized back to str.
        """
        return ''.join(element.serialized() for element in self._elements)

    def keys(self):
        raise NotImplementedError   # TODO

    def values(self):
        raise NotImplementedError   # TODO

    def items(self):
        return self.primitive.items()

    @property
    def primitive(self):
        """
        Returns a primitive object representation for this container (which is a dict).

        WARNING: The returned container does not contain any markup or formatting metadata.
        """
        raise NotImplementedError   # TODO
