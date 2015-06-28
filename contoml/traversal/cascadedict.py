import operator
from functools import reduce

class CascadeDict:
    """
    A dict-like object made up of one or more other dict-like objects where querying for an item cascade-gets
    it from all the internal dicts in order of their listing, and setting an item sets it on the first dict listed.
    """

    def __init__(self, internal_dicts):
        assert internal_dicts, 'internal_dicts cannot be empty'
        self._internal_dicts = tuple(internal_dicts)

    def __getitem__(self, item):
        for d in self._internal_dicts:
            try:
                return d[item]
            except KeyError:
                pass
        raise KeyError

    def __setitem__(self, key, value):
        self._internal_dicts[0][key] = value

    def keys(self):
        return set(reduce(operator.or_, (set(d.keys()) for d in self._internal_dicts)))

    def items(self):
        all_items = reduce(operator.add, (list(d.items()) for d in reversed(self._internal_dicts)))
        unique_items = {k: v for k, v in all_items}.items()
        return set(unique_items)
