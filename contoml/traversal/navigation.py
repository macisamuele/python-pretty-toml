from contoml import elements
from contoml.elements.table import TableElement
from contoml.elements.tableheader import TableHeaderElement
from contoml.file.cascadedict import CascadeDict


class _Traversable(elements.TraversalMixin):

    def __init__(self, elements):
        self.elements = elements

    def anonymous_table(self):
        """
        Returns the TableElement of the anonymous table, or raises a KeyError if not found.
        """
        non_metadata_lements = tuple(self._enumerate_non_metadata_sub_elements())
        if not non_metadata_lements or not isinstance(non_metadata_lements[0][1], TableElement):
            raise KeyError
        return non_metadata_lements[0]


def _names_remove_prefix(prefix, names):
    for i, name in enumerate(names):
        if name != prefix[i]:
            return names[i:]
    return tuple()


def _validate_elements(elements):
    # Elements must be structured as a first optional table, followed by zero or more pairs of (table header, table).
    # TODO
    pass


def create(elements):
    """
    Creates and returns a navigable data structure that can be used to navigate to TableBody elements
    using their assigned names according to the TOML spec.
    """
    _validate_elements(elements)
    traversable = _Traversable(elements)

    struct = dict()

    def _make_sure_names_exist(names):
        # Makes sure struct has the given names as items in their listing order
        d = struct
        for name in names:
            if name not in d:
                d[name] = dict()
            d = d[name]

    def _handle_table(header_i, header):
        names = header.name
        _make_sure_names_exist(names[:-1])  # Make sure parent containers exist
        next_table_i = traversable._find_following_table(header_i)
        child = elements[next_table_i]
        child_name = names[-1]

        parent = _navigate(struct, names[:-1])
        if child_name not in parent:
            parent[child_name] = CascadeDict((child,))
        else:
            parent[child_name] = parent.cascaded_with(CascadeDict(({child_name: child},)))

    def _handle_array_of_tables(header_i, header, iterator):
        # iterator is over enumerate(elements)

        names = header.name

        # Make sure parents exist, and the named sequence exists
        _make_sure_names_exist(struct, names[:-1])
        if names[0] not in _navigate(struct, names[:-1]):
            _navigate(struct, names[:-1])[names[-1]] = list()

        seq = _navigate(struct, names[:-1])[names[-1]]

        following_table_i = traversable._find_following_table(header_i)
        following_header = traversable._find_following_table_header(header_i)
        if following_table_i < following_header:
            seq.append(elements[following_table_i])

        # Find the end of this entry as the first table header not prefixed with `names`, or end of elements
        reign_end = ((element_i for element_i, element in enumerate(elements)
                      if element_i > header_i and isinstance(element, TableHeaderElement) and
                      not '.'.join(element.name).startswith('.'.join(names))), float('inf'))

        for element_i, element in tuple(enumerate(elements))[header_i:reign_end]:

            if isinstance(element, TableHeaderElement) and not element.is_array_of_tables:
                following_table_i = traversable._find_following_table(element_i)
                unprefixed_name = _names_remove_prefix(names, header.name)
                seq[-1][unprefixed_name] = elements[following_table_i]

            if isinstance(element, TableHeaderElement) and element.is_array_of_tables:
                unprefixed_name = _names_remove_prefix(names, header.name)
                seq[-1][unprefixed_name] = elements[traversable._find_following_table(element_i)]

        # Advance the iterator to the end of this entry's reign
        while True:
            try:
                i, element = next(iterator)
                if i == (reign_end - 1):
                    break
            except StopIteration:
                break

    try:
        struct[''] = traversable.anonymous_table()
    except KeyError:
        pass

    iterator = enumerate(elements)
    for element_i, element in iterator:

        if not isinstance(element, TableHeaderElement):
            continue

        # If TableHeader of a regular table, return Table following it
        if not element.is_array_of_tables:
            _handle_table(element_i, element)

        # If TableHeader of an array of tables, do your thing
        elif element.is_array_of_tables:
            _handle_array_of_tables(element_i, element, iterator)

    return struct


def _navigate(d, indices):
    """
    Navigates the given container using the given indices and returns the navigated-to value.
    """
    dl = d
    for index in indices:
        dl = dl[index]
    return dl
