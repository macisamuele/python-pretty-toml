from contoml.file.freshtable import FreshTable


class FreshArrayOfTables(list):

    def __init__(self, toml_file, name):
        list.__init__(self)
        self._toml_file = toml_file
        self._name = name

    def append(self, p_object):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __getitem__(self, item):
        try:
            return list.__getitem__(self, item)
        except IndexError:
            if item == len(self):
                return FreshTable(parent=self, name=self._name, is_array=True)
            else:
                raise

    def append_fresh_table(self, fresh_table):
        list.append(self, fresh_table)
        self._toml_file.append_fresh_table(fresh_table)
