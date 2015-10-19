# -*- coding: utf-8 -*-

from collections import OrderedDict
import json
import contoml
from contoml.errors import TOMLError, DuplicateKeysError, DuplicateTablesError, InvalidTOMLFileError


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
    assert set(file.keys()) == {'apple', ''}
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
other_name = "nevermind"


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
another_dict = true
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
    REDIS_PASSWORD = "MYPASSWORD"
    #REDIS_PASSWORD = ""
"""

    assert expected == f.dumps()


def test_loading_complex_file_1():

    toml = """
[main]
gid = 1
nid = 10
max_jobs = 100
message_id_file = "./.mid"
history_file = "./.history"
agent_controllers = ["http://localhost:8966/"]

[cmds]
    [cmds.execute_js_py]
    binary = "python2.7"
    cwd = "./jumpscripts"
    script = "{domain}/{name}.py"

    [cmds.sync]
    #syncthing extension
    binary = "python2.7"
    cwd = "./extensions/sync"
    script = "{name}.py"
    [cmds.sync.env]
    PYTHONPATH = "../"
    JUMPSCRIPTS_HOME = "../../jumpscripts"
    SYNCTHING_URL = "http://localhost:8384"

[channel]
cmds = [0] # long polling from agent 0

[logging]
    [logging.db]
    type = "DB"
    log_dir = "./logs"
    levels = [2, 4, 7, 8, 9]  # (all error messages) empty for all

    [logging.ac]
    type = "AC"
    flush_int = 300 # seconds (5min)
    batch_size = 1000 # max batch size, force flush if reached this count.
    agent_controllers = [] # to all agents
    levels = [2, 4, 7, 8, 9]  # (all error messages) empty for all

    [logging.console]
    type = "console"
    levels = [2, 4, 7, 8, 9]

[stats]
interval = 60 # seconds
agent_controllers = []
"""

    contoml.loads(toml)


def test_weird_edge_case_1():
    toml_text = """l = "t"
creativity = "on vacation"
"""

    f = contoml.loads(toml_text)
    assert f['']['l'] == 't'


def test_weird_edge_case_2():
    toml_text = """telegram = "971507192009"
description = ""
firstname = "adnan"
lastname = "fatayerji"
git_aydo = ""
emails = ["adnan@incubaid.com", "fatayera@incubaid.com", "adnan.fatayerji@incubaid.com", "adnan@greenitglobe.com", "fatayera@greenitglobe.com", "adnan.fatayerji@greenitglobe.com"]
git_github = ""
groups = ["sales", "dubai", "mgmt"]
skype = ""
id = "fatayera"
mobiles = ["971507192009"]"""

    f = contoml.loads(toml_text)
    f.prettify()


def test_creating_toml_files_with_none_value():
    data = {'description': None,
            'emails': ['adnan@incubaid.com'],
            'firstname': 'adnan',
            'git_aydo': None,
            'git_github': None,
            'groups': [u'sales'],
            'id': 'fatayera',
            'lastname': 'fatayerji',
            'mobiles': ['971507192009'],
            'skype': None,
            'telegram': '971507192009'}

    toml_text = contoml.dumps(data)
    assert contoml.loads(toml_text)['']['description'] == ''


def test_parsing_to_raw_primitive_and_dumping_back_to_toml_should_be_inverses():

    data = {u'description': u'',
            u'emails': [u'adnan@incubaid.com',
                        u'fatayera@incubaid.com',
                        u'adnan.fatayerji@incubaid.com',
                        u'adnan@greenitglobe.com',
                        u'fatayera@greenitglobe.com',
                        u'adnan.fatayerji@greenitglobe.com'],
            u'firstname': u'adnan',
            u'git_aydo': u'',
            u'git_github': u'',
            u'groups': [u'sales', u'dubai', u'mgmt'],
            u'id': u'fatayera',
            u'lastname': u'fatayerji',
            u'mobiles': [u'971507192009'],
            u'skype': u'',
            u'telegram': u'971507192009'}

    assert contoml.loads(contoml.dumps(data)).primitive == data


def test_accessing_deeply_nested_dicts():
    t = """[cmds]
    [cmds.sync]
    #syncthing extension
    binary = "python2.7"
    cwd = "./extensions/sync"
    script = "{name}.py"
        [cmds.sync.env]
        PYTHONPATH = "../"
        JUMPSCRIPTS_HOME = "../../jumpscripts"
        SYNCTHING_URL = "http://localhost:8384"
"""

    f = contoml.loads(t)

    assert f['cmds']['sync']['env']['SYNCTHING_URL'] == 'http://localhost:8384'

    f['cmds']['sync']['env']['SYNCTHING_URL'] = 'Nowhere'

    expected_toml = """[cmds]
    [cmds.sync]
    #syncthing extension
    binary = "python2.7"
    cwd = "./extensions/sync"
    script = "{name}.py"
        [cmds.sync.env]
        PYTHONPATH = "../"
        JUMPSCRIPTS_HOME = "../../jumpscripts"
        SYNCTHING_URL = "Nowhere"
"""

    assert expected_toml == f.dumps()


def test_creating_empty_arrays():
    d = {
        "hash.service.actions.lua": "",
        "hash.service.actions.py <http://hash.service.actions.py>": "",
        "actions": [],
    }

    toml = contoml.dumps(d, prettify=True)
    expected_toml = """actions = []
"hash.service.actions.lua" = ""
"hash.service.actions.py <http://hash.service.actions.py>" = ""


"""

    assert expected_toml == toml


def test_issue_18():
    toml_text = """[main]
gid = 1
nid = 1
max_jobs = 100
message_id_file = "./.mid"
history_file = "./.history"
roles = ["agent"]
include = "./conf"

[controllers]
    [controllers.main]
    url = "https://dev2/controller/"
        [controllers.main.security]
        client_certificate = "/opt/jumpscale7/hrd/apps/agent2__node1/client_node1.crt"
        client_certificate_key = "/opt/jumpscale7/hrd/apps/agent2__node1/client_node1.key"
        certificate_authority = "/opt/jumpscale7/hrd/apps/agent2__node1/server.crt"

[channel]
cmds = [] # empty for long polling from all defined controllers, or specif controllers keys

[extensions]
    #the very basic agent extensions. Also please check the toml files under
    #the Main.Include folder for more extensions
    [extensions.syncthing]
    binary = "./syncthing"
    cwd = "./extensions/syncthing"
    args = ["-home", "./home", "-gui-address", "127.0.0.1:28384"]

    [extensions.sync]
    #syncthing extension
    binary = "python2.7"
    cwd = "./extensions/sync"
    args = ["{name}.py"]
        [extensions.sync.env]
        PYTHONPATH = "../:/opt/jumpscale7/lib"
        JUMPSCRIPTS_HOME = "/opt/jumpscale7/apps/agent2/jumpscripts/"
        SYNCTHING_URL = "http://localhost:28384"

    [extensions.jumpscript]
    binary = "python2.7"
    cwd = "./extensions/jumpscript"
    args = ["wrapper.py", "modern", "{domain}", "{name}"]
        [extensions.jumpscript.env]
        SOCKET = "/tmp/jumpscript.sock"
        PYTHONPATH = "../"

    [extensions.legacy]
    binary = "python2.7"
    cwd = "./extensions/jumpscript"
    args = ["wrapper.py", "legacy", "{domain}", "{name}"]
        [extensions.legacy.env]
        PYTHONPATH = "../" # for utils
        SOCKET = "/tmp/jumpscript.sock"

    [extensions.js_daemon]
    binary = "python2.7"
    cwd = "./extensions/jumpscript"
    args = ["executor.py"]
        [extensions.js_daemon.env]
        SOCKET = "/tmp/jumpscript.sock"
        PYTHONPATH = "../:/opt/jumpscale7/lib"
        JUMPSCRIPTS_HOME = "/opt/jumpscale7/apps/agent2/jumpscripts/"
        JUMPSCRIPTS_LEGACY_HOME = "/opt/jumpscale7/apps/agent2/legacy/"

[logging]
    [logging.db]
    type = "DB"
    log_dir = "./logs"
    levels = [2, 4, 7, 8, 9, 11]  # (all error messages + debug) empty for all

    [logging.ac]
    type = "AC"
    flush_int = 300 # seconds (5min)
    batch_size = 1000 # max batch size, force flush if reached this count.
    controllers = [] # empty for all controllers, or controllers keys
    levels = [2, 4, 7, 8, 9, 11]  # (all error messages + debug) empty for all

    [logging.console]
    type = "console"
    levels = [2, 4, 7, 8, 9]

[stats]
interval = 60 # seconds
controllers = [] # empty for all controllers, or controllers keys

[hubble]
controllers = [] # accept forwarding commands and connections from all controllers. Or specific controllers by name

[startup]
    [startup.syncthing]
    name = "syncthing"
        [startup.syncthing.args]
        loglevels_db = '*'
        domain = "agent"
        name = "syncthing"

    [startup.legacy]
    name = "js_legacy_daemon"
        [startup.legacy.args]
        max_restart = 10
        domain = "agent"
        name = "legacy"

    [startup.jumpscript]
    name = "js_daemon"
        [startup.jumpscript.args]
        max_restart = 10
        domain = "agent"
        name = "jumpscript"
"""

    toml = contoml.loads(toml_text)

    toml['extensions']['redis'] = {
            'binary': './redis-server',
            'cwd': '/opt/jumpscale7/apps/redis',
            'args': ['/opt/jumpscale7/var/redis/ovh4/redis.conf']
        }
    toml['startup']['redis'] = {
            'name': 'redis',
            'args': {
                'max_restart': 1,
                'domain': 'jumpscale',
                'name': 'redis',
            }
        }

    contoml.dumps(toml, prettify=True)
    # No errors, test passed!


def test_table_with_pound_in_title():
    toml = """["key#group"]
answer = 42"""

    parsed = contoml.loads(toml)

    assert parsed.primitive['key#group']['answer'] == 42


def test_detects_duplicate_keys():
    toml = """[fruit]
type = "apple"

[fruit.type]
apple = "yes" """

    try:
        contoml.loads(toml)
        assert False, "Parsing that TOML snippet should have thrown an exception"
    except DuplicateKeysError:
        pass


def test_detects_duplicate_tables():
    toml = "[a]\n[a]"
    try:
        contoml.loads(toml)
        assert False, "Parsing that TOML snippet should have thrown an exception"
    except DuplicateTablesError:
        pass


# There is no simple way to make this work since [[ is a token as well as [ and we're doing
# maximal-munch tokenizing
# def test_parsing_empty_arrays():
#     toml = """thevoid = [[[[[]]]]]"""
#
#     parsed = contoml.loads(toml)
#
#     assert len(parsed['']['thevoid']) == 1


def test_fails_to_parse_bad_escape_characters():
    toml = r"""
invalid-escape = r"This string has a bad \a escape character."
"""
    try:
        contoml.loads(toml)
        assert False, "Should raise an exception before getting here"
    except TOMLError:
        pass


def test_parsing_multiline_strings_correctly():

    toml = r'''multiline_empty_one = """"""
multiline_empty_two = """
"""
multiline_empty_three = """\
    """
multiline_empty_four = """\
   \
   \
   """

equivalent_one = "The quick brown fox jumps over the lazy dog."
equivalent_two = """
The quick brown \


  fox jumps over \
    the lazy dog."""

equivalent_three = """\
       The quick brown \
       fox jumps over \
       the lazy dog.\
       """
'''

    parsed = contoml.loads(toml)

    assert parsed['']['multiline_empty_one'] == parsed['']['multiline_empty_two'] == \
           parsed['']['multiline_empty_three'] == parsed['']['multiline_empty_four']


def test_unicode_string_literals():
    toml = u'answer = "δ"\n'
    parsed = contoml.loads(toml)
    assert parsed['']['answer'] == u"δ"


def test_one_entry_array_of_tables():
    t = '''[[people]]
first_name = "Bruce"
last_name = "Springsteen"
'''

    parsed = contoml.loads(t)

    assert parsed['people'][0]['first_name'] == 'Bruce'
    assert parsed['people'][0]['last_name'] == 'Springsteen'


def test_should_not_create_multiline_string_in_inline_map():
    t = contoml.new()
    t['']['inline_map'] = {
        'app': 'Redis',
        'Enabled': True,
        'key_path': '/opt/code/github/jumpscale/ays2/services/agentcontroller2!main/tls/verylongname/cert.pem'
    }

    assert len(tuple(filter(bool, t.dumps().split('\n')))) == 1
