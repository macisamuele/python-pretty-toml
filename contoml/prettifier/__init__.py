from .tableassignment import table_assignment_spacing
from .tableindent import table_entries_should_be_uniformly_indented

"""
    TOMLFile prettifiers

    Each prettifier is a function that accepts the list of Element instances that make up the
    TOMLFile and it is allowed to modify it as it pleases.
"""


UNIFORM_TABLE_INDENTATION = table_entries_should_be_uniformly_indented
UNIFORM_TABLE_ASSIGNMENT_SPACING = table_assignment_spacing


ALL = (
    UNIFORM_TABLE_INDENTATION,
    UNIFORM_TABLE_ASSIGNMENT_SPACING,
)


def prettify(toml_file, prettifiers=ALL):
    """
    Prettifies a TOMLFile instance according to pre-defined set of formatting rules.
    """
    for prettifier in prettifiers:
        prettifier(toml_file)
