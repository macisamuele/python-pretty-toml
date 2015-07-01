
from contoml.file import structurer, entries, raw
from contoml.parser import elementsanitizer
from contoml.file.freshtable import FreshTable


class TOMLFile:
    """
    A TOMLFile object that tries its best to prserve formatting and order of mappings of the input source.

    Raises InvalidTOMLFileError on invalid input elements.
    """

    def __init__(self, _elements):
        self._elements = []
        self._navigable = {}
        self.append_elements(_elements)

    def __getitem__(self, item):
        try:
            return self._navigable[item]
        except KeyError:
            return FreshTable(self, item)

    def append_elements(self, elements):
        """
        Appends more elements to the contained internal elements.
        """
        self._elements = self._elements + list(elements)
        if self._elements:
            self._navigable = structurer.structure(entries.extract(self._elements))

    def dumps(self):
        """
        Returns the TOML file serialized back to str.
        """
        return ''.join(element.serialized() for element in self._elements)

    def dump(self, file_path):
        with open(file_path, mode='w') as fp:
            fp.write(self.dumps())

    def keys(self):
        return self._navigable.keys()

    def values(self):
        return self._navigable.values()

    def items(self):
        return self._navigable.items()

    @property
    def primitive(self):
        """
        Returns a primitive object representation for this container (which is a dict).

        WARNING: The returned container does not contain any markup or formatting metadata.
        """
        return raw.to_raw(self._navigable)
