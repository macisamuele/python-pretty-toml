
import prettytoml

from .tableindent import table_entries_should_be_uniformly_indented


def test_table_entries_should_be_uniformly_indented():
    toml_text = """
    [firstlevel]
hello = "my name"
    my_id = 12

    [firstlevel.secondlevel]
      my_truth = False
"""

    expected_toml_text = """
[firstlevel]
hello = "my name"
my_id = 12

  [firstlevel.secondlevel]
  my_truth = False
"""

    f = prettytoml.loads(toml_text)
    f.prettify(prettifiers=[table_entries_should_be_uniformly_indented])
    assert expected_toml_text == f.dumps()
