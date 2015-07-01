from contoml.elements.table import TableElement
from contoml.elements import factory as element_factory


class FreshTable(TableElement):
    """
    A fresh TableElement that gets appended to the TOMLFile on the first setitem operation on it.
    """

    def __init__(self, toml_file, name):
        TableElement.__init__(self, sub_elements=[])

        self._toml_file = toml_file
        self._name = name

        # As long as this flag is false, setitem() operations will append the table header and this table
        # to the toml_file's elements
        self.__written = False

    def _write_to_toml_file(self):
        if self.__written:
            return
        self._toml_file.append_elements([
            element_factory.create_table_header_element(self._name),
            self,
            element_factory.create_newline_element(),
        ])
        self.__written = True

    def __setitem__(self, key, value):
        TableElement.__setitem__(self, key, value)
        self._write_to_toml_file()
