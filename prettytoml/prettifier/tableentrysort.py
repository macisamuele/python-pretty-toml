import operator
from prettytoml import tokens
from prettytoml.elements.common import TokenElement
from prettytoml.elements.metadata import NewlineElement
from prettytoml.elements.table import TableElement
from itertools import *
from functools import *


def sort_table_entries(toml_file_elements):
    """
    Rule: Entries within a single table should be ordered lexicographically by key
    """
    return [_sorted_table(element) if isinstance(element, TableElement) else element for element in toml_file_elements]


def _lines(elements):
    """
    Splits a sequence of elements into a sub-sequence of each line.
    """

    def __next_line(es):
        # Returns the next line and the remaining sequence of elements
        line = tuple(takewhile(lambda e: not isinstance(e, NewlineElement), es))
        line += (es[len(line)],)
        return line, es[len(line):]

    left_elements = tuple(elements)
    while left_elements:
        line, left_elements = __next_line(left_elements)
        yield line


def _line_key(line_elements):
    """
    Given a sequence of elements comprising a single line, returns an orderable value to use in ordering lines.
    """
    for e in line_elements:
        if isinstance(e, TokenElement) and tokens.is_string(e.first_token):
            return e.primitive_value
    return 'z' * 10     # Metadata lines should be at the end


def _sorted_table(table):
    """
    Returns another TableElement where the table entries are sorted lexicographically by key.
    """
    assert isinstance(table, TableElement)

    # Discarding TokenElements with no tokens in them
    table_elements = filter(lambda e: not (isinstance(e, TokenElement) and not e.tokens), table.sub_elements)
    lines = tuple(_lines(table_elements))
    sorted_lines = sorted(lines, key=_line_key)
    sorted_elements = reduce(operator.concat, sorted_lines)

    return TableElement(sorted_elements)
