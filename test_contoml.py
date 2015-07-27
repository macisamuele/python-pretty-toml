from collections import OrderedDict
import json
import contoml
from contoml.errors import TOMLError


def test_it_should_correctly_load_sample_file():

    toml_file = contoml.load('dateless_sample.toml')
    assert set(toml_file.keys()) == {'fruit', 'clients', '', 'owner', 'database', 'servers', 'extra'}
    json_file = json.load(open('dateless_sample.json'))
    assert json_file == toml_file.primitive


def test_it_should_fail_loading_broken_file():
    try:
        toml_file = contoml.load('dateless_sample-broken.toml')
        assert set(toml_file.keys()) == {'fruit', 'clients', '', 'owner', 'database', 'servers', 'extra'}
        json_file = json.load(open('dateless_sample.json'))
        assert json_file == toml_file.primitive
    except TOMLError:
        return

    assert False, 'Should have thrown an error'


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
"other_name" = "nevermind"


# Nevermind
"""

    assert expected_toml == file.dumps()


def test_should_insert_with_sensible_indentation_in_tables():

    toml = """
[apple]
    color = "green"
    name = "yonagold"


# Nevermind
"""

    file = contoml.loads(toml)

    file['apple']['key'] = 23

    expected_toml = """
[apple]
    color = "green"
    name = "yonagold"
    key = 23


# Nevermind
"""

    assert file.dumps() == expected_toml


def test_setting_primitive_value_on_non_existing_section():

    f = contoml.new()
    f['details']['id'] = 12

    assert f.dumps() == '[details]\nid = 12\n\n'


def test_creating_an_array_of_tables():

    f = contoml.new()

    f.array('fruit')[0]['name'] = 'banana'
    f.array('fruit')[1]['name'] = 'grapes'
    f['fruit'][1]['name'] = 'grapes'

    assert f.dumps() == """[[fruit]]
name = "banana"

[[fruit]]
name = "grapes"

"""


def test_creating_tables_from_dicts():
    f = contoml.new()
    f['my table'] = OrderedDict((('really', False), ('noo', 'yeah!')))
    assert f.dumps() == """["my table"]
really = false
noo = "yeah!"

"""

    f['my table']['noo'] = 'indeed'
    assert f.dumps() == """["my table"]
really = false
noo = "indeed"

"""

    f['my table'] = OrderedDict((('another_dict', True), ('should replace other one', 'right')))
    assert f.dumps() == """["my table"]
"another_dict" = true
"should replace other one" = "right"

"""


def test_appending_to_an_array_of_tables():

    f = contoml.new()

    f.array('person').append(OrderedDict([('name', 'Chuck'), ('id', 12)]))

    assert f.dumps() == """[[person]]
name = "Chuck"
id = 12

"""

    f['person'].append(OrderedDict([('name', 'Kcuhc'), ('id', 21)]))

    assert f.dumps() == """[[person]]
name = "Chuck"
id = 12

[[person]]
name = "Kcuhc"
id = 21

"""


def test_creating_an_array_of_tables_all_at_once():

    f = contoml.new()

    f['person'] = [
        OrderedDict((('Name', "First Guy"), ('id', 0))),
        OrderedDict((('Name', "Second Guy"), ('id', 1))),
        OrderedDict((('Name', "Third Guy"), ('id', 2))),
    ]

    assert f.dumps() == """[[person]]
Name = "First Guy"
id = 0

[[person]]
Name = "Second Guy"
id = 1

[[person]]
Name = "Third Guy"
id = 2

"""


def test_creating_an_array_of_tables_all_at_once_via_dump():

    d = {
        'person': [
            OrderedDict((('Name', "First Guy"), ('id', 0))),
            OrderedDict((('Name', "Second Guy"), ('id', 1))),
            OrderedDict((('Name', "Third Guy"), ('id', 2))),
            ]
    }

    assert contoml.dumps(d) == """[[person]]
Name = "First Guy"
id = 0

[[person]]
Name = "Second Guy"
id = 1

[[person]]
Name = "Third Guy"
id = 2

"""


def test_creating_an_anonymous_table():

    f = contoml.new()

    f['']['creator'] = True
    f['']['id'] = 12

    assert f.dumps() == "creator = true\nid = 12\n\n"


def test_creating_an_anonymous_table_2():

    f = contoml.new()

    f[''] = {'Name': 'Fawzy'}

    assert f.dumps() == 'Name = "Fawzy"\n\n'


def test_dumping_a_dict():

    d = OrderedDict((('My string', 'string1'), ('My int', 42), ('My float', 12.111)))

    assert contoml.dumps(d) == """"My string" = "string1"
"My int" = 42
"My float" = 12.111

"""

    d21 = OrderedDict((('My string', 'string1'), ('My int', 42), ('My float', 12.111)))
    d22 = OrderedDict((('My string2', 'string2'), ('My int', 43), ('My float', 13.111)))

    d2 = OrderedDict((('d1', d21), ('d2', d22)))

    assert contoml.dumps(d2) == """[d1]
"My string" = "string1"
"My int" = 42
"My float" = 12.111

[d2]
"My string2" = "string2"
"My int" = 43
"My float" = 13.111

"""


def test_late_addition_to_anonymous_table():

    f = contoml.new()

    f['details']['name'] = 'John Doe'
    f['']['global'] = 42

    assert f.dumps() == """global = 42

[details]
name = "John Doe"

"""


def test_loading_toml_without_trailing_newline():
    toml_text = '[main]\nname = "azmy"'
    toml = contoml.loads(toml_text)

    assert toml['main']['name'] == 'azmy'


def test_array_edge_cases():

    # Parsing an empty array value
    toml_text = """[section]
key = []"""

    toml = contoml.loads(toml_text)

    assert 'section' in toml
    assert len(toml['section']['key']) == 0


def test_loading_an_empty_toml_source():

    toml_text = ''

    contoml.loads(toml_text)

    # Should not fail


def test_parsing_section_with_indentation_and_comment_lines():
    toml = """[main]
listen = ":8966"
redis_host =  "localhost:6379"
redis_password = ""

[influxdb]
host = "localhost:8086"
db   = "agentcontroller"
user = "ac"
password = "acctrl"

[handlers]
binary = "python2.7"
cwd = "./handlers"
    [handlers.env]
    PYTHONPATH = "/opt/jumpscale7/lib:../client"
    SYNCTHING_URL = "http://localhost:8384/"
    SYNCTHING_SHARED_FOLDER_ID = "jumpscripts"
    #SYNCTHING_API_KEY = ""
    REDIS_ADDRESS = "localhost"
    REDIS_PORT = "6379"
    #REDIS_PASSWORD = ""
"""

    f = contoml.loads(toml)

    assert f['handlers']['env']['REDIS_ADDRESS'] == 'localhost'
    assert 'REDIS_PASSWORD' not in f['handlers']['env']

    f['handlers']['env']['REDIS_PASSWORD'] = 'MYPASSWORD'

    expected = """[main]
listen = ":8966"
redis_host =  "localhost:6379"
redis_password = ""

[influxdb]
host = "localhost:8086"
db   = "agentcontroller"
user = "ac"
password = "acctrl"

[handlers]
binary = "python2.7"
cwd = "./handlers"
    [handlers.env]
    PYTHONPATH = "/opt/jumpscale7/lib:../client"
    SYNCTHING_URL = "http://localhost:8384/"
    SYNCTHING_SHARED_FOLDER_ID = "jumpscripts"
    #SYNCTHING_API_KEY = ""
    REDIS_ADDRESS = "localhost"
    REDIS_PORT = "6379"
    "REDIS_PASSWORD" = "MYPASSWORD"
    #REDIS_PASSWORD = ""
"""

    assert expected == f.dumps()
