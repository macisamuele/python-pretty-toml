import six
from contoml.elements import traversal as t, factory as element_factory
from contoml.elements.atomic import AtomicElement
from contoml.elements.table import TableElement


MAXIMUM_LINE_LENGTH = 120


def line_lingth_limiter(toml_file_elements):
    """
    Rule: Lines whose lengths exceed 120 characters whose values are strings, arrays, or inline tables
    should have the array or string value broken onto multiple lines and the inline table turned into
    a multiline table section so as to try to maintain a maximum line length of 120.
    """

    for element in toml_file_elements:
        if isinstance(element, TableElement):
            _do_table(element.sub_elements)


def _do_table(table_elements):

    it = float('-inf')

    def next_newline():
        return t.find_following(table_elements, t.predicates.newline, it)

    def next_key():
        return t.find_following(table_elements, t.predicates.non_metadata, it)

    def next_value():
        return t.find_following(table_elements, t.predicates.non_metadata, next_key())

    def line_length():
        elements = table_elements[it:next_newline()] if it > float('inf') else table_elements[:next_newline()]
        return len(''.join(e.serialized() for e in elements))

    while next_newline() >= 0:

        if line_length() > MAXIMUM_LINE_LENGTH:
            value_i = next_value()
            value = table_elements[value_i]
            if isinstance(value, AtomicElement) and isinstance(value.value, six.string_types):
                table_elements[value_i] = element_factory.create_multiline_string(value.value, MAXIMUM_LINE_LENGTH)

        it = next_newline()
