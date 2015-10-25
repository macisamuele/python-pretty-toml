
"""
    This testing module depends on all the other modules.
"""

from .anontableindent import deindent_anonymous_tables
from .common import assert_prettifier_works


def test_anon_table_indent():
    toml_text = """
    key=value
          another_key =44
noname = me
"""

    expected_toml_text = """
key=value
another_key =44
noname = me
"""
    assert_prettifier_works(toml_text, expected_toml_text, deindent_anonymous_tables)
