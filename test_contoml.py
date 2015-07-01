import json
import contoml

def test_it_should_correctly_load_sample_file():

    toml_file = contoml.load('dateless_sample.toml')

    assert set(toml_file.keys()) == {'fruit', 'clients', '', 'owner', 'database', 'servers', 'extra'}

    json_file = json.load(open('dateless_sample.json'))

    assert json_file == toml_file.primitive


def test_works_fine_without_anonymous_section():

    toml =  """
[apple]
color = "green"
name = "yonagold"
"""

    file = contoml.loads(toml)
    assert set(file.keys()) == {'apple'}
    assert file['apple']['color'] == 'green'
    assert file['apple']['name'] == 'yonagold'


def test_table_should_insert_new_entries_right_after_last_entry():

    toml =  """
[apple]
color = "green"
name = "yonagold"


# Nevermind
"""

    file = contoml.loads(toml)

    file['apple']['other_name'] = 'nevermind'

    expected_toml = """
[apple]
color = "green"
name = "yonagold"
"other_name" = nevermind


# Nevermind
"""

    assert expected_toml == file.dumps()
