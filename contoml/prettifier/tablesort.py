
from contoml.elements.table import TableElement
from contoml.elements import traversal as t, factory as element_factory


def sort_table_entries(toml_file):
    for element in toml_file.elements:
        if isinstance(element, TableElement):
            __do_table(element)


def __do_table(table):

    elements = table.sub_elements

    def line_ranges():
        # Returns [start, stop) indices of lines in the table
        next_start = 0
        while True:
            next_end = t.find_following(elements, t.predicates.newline, next_start)
            if next_end > next_start:
                yield (next_start, next_end+1)
                next_start = next_end + 1
            else:
                break

    def line_key(line_start, line_stop):
        # Returns the key to sort the lines by
        i = t.find_following(elements, t.predicates.non_metadata, line_start-1)
        assert(i >= 0)
        assert(i < line_stop)
        return elements[i].value

    old_elements = table.elements[:]
    sorted_ranges = sorted(tuple(line_ranges()), key=lambda r: line_key(*r))

    del table.elements[:]
    for (start, stop) in sorted_ranges:
        for e in old_elements[start:stop]:
            table.elements.append(e)

