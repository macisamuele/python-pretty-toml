
from contoml.file import elementsanitizer, structurer, entries, raw


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
        raise NotImplementedError   # TODO

    def items(self):
        return self.primitive.items()

    @property
    def primitive(self):
        """
        Returns a primitive object representation for this container (which is a dict).

        WARNING: The returned container does not contain any markup or formatting metadata.
        """
        return raw.to_raw(self._navigable)
