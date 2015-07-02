from contoml.elements.table import TableElement
from contoml.file.freshtable import FreshTable


class ArrayOfTables(list):

    def __init__(self, parent, name, iterable=None):
        if iterable:
            list.__init__(self, iterable)
        self._name = name
        self._parent = parent

    def append(self, table):
        if isinstance(table, TableElement):
            list.append(self, table)
        else:
            # TODO: Convert to a TableElement and insert
            raise NotImplementedError   # TODO

    def __getitem__(self, item):
        try:
            return list.__getitem__(self, item)
        except IndexError:
            if item == len(self):
                return FreshTable(parents=(self,), name=self._name, is_array=True)
            else:
                raise

    def append_fresh_table(self, fresh_table):
        list.append(self, fresh_table)
        if self._parent:
            self._parent.append_fresh_table(fresh_table)
