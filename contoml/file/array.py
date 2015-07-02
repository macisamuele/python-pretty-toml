from contoml.elements.table import TableElement


class ArrayOfTables(list):

    def __init__(self, name, iterable=None):
        list.__init__(self, iterable)
        self._name = name

    def append(self, table):
        if isinstance(table, TableElement):
            list.append(self, table)
        else:
            # TODO: Convert to a TableElement and insert
            raise NotImplementedError   # TODO
