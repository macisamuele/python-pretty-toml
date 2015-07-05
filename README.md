# Consistent TOML for Python

[![Build Status](https://travis-ci.org/Jumpscale/python-consistent-toml.svg?branch=master)](https://travis-ci.org/Jumpscale/python-consistent-toml)
![Python Versions](https://img.shields.io/pypi/pyversions/contoml.svg)
[![Release](https://img.shields.io/pypi/v/contoml.svg)](https://pypi.python.org/pypi/contoml)
[![Join the chat at https://gitter.im/Jumpscale/python-consistent-toml](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Jumpscale/python-consistent-toml?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


A [TOML](https://github.com/toml-lang/toml) serializer/deserializer for Python that tries its best to preserve order of table mappings, formatting of source file, and comments during a deserialize/update/serialize job.

## Installation ##
```bash
pip install contoml
```

## Usage ##

```python
import contoml

toml_file = contoml.load('sample.toml')

# The anonymous table is accessible using the empty string key on the TOML file
>>> toml_file['']['title']
'TOML Example'

# You can modify table values, add new values, or new tables
>>> toml_file['fruit'][1]['variety'][0]['points'][0]['y'] = 42

>>> toml_file['servers']['alpha']['ip'] = '192.168.0.111'

>>> toml_file['environment'] = {'OS': 'Arch Linux', 'Type': 'GNU/Linux'}

# Or append to an array of tables!
>>> toml_file.array('disks').append({'dev': '/dev/sda', 'cap': '230'})
>>> toml_file.array('disks').append({'dev': '/dev/sdb', 'cap': '120'})

# Serialize back to TOML text at any point
>>> print(toml_file.dumps())
# This is a TOML document.

title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00 # First class dates

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]

  # Indentation (tabs and/or spaces) is allowed but not required
  [servers.alpha]
  ip = "192.168.0.111"
  dc = "eqdc10"

  [servers.beta]
  ip = "10.0.0.2"
  dc = "eqdc10"

[clients]
data = [ ["gamma", "delta"], [1, 2] ]

# Line breaks are OK when inside arrays
hosts = [
  "alpha",
  "omega"
]

str_multiline = """
Roses are red
Violets are blue"""

str_quoted = "I'm a string. \"You can quote me\". Name\tJos\u00E9\nLocation\tSF."

str2 = """
The quick brown \


  fox jumps over \
    the lazy dog."""

key3 = """\
       The quick brown \
       fox jumps over \
       the lazy dog.\
       """

# What you see is what you get.
winpath  = 'C:\Users\nodejs\templates'
winpath2 = '\\ServerX\admin$\system32\'
quoted   = 'Tom "Dubs" Preston-Werner'
regex    = '<\i\c*\s*>'

regex2 = '''I [dw]on't need \d{2} apples'''
lines  = '''
The first newline is
trimmed in raw strings.
   All other whitespace
   is preserved.
'''


[[fruit]]
  name = "apple"

  [fruit.physical]
    color = "red"
    shape = "round"

  [[fruit.variety]]
    name = "red delicious"

  [[fruit.variety]]
    name = "granny smith"

[[fruit]]
  name = "banana"

  [[fruit.variety]]
    name = "plantain"


points = [ { x = 1, y = 42, z = 3 },         # This value is so special to me
           { x = 7, y = 8, z = 9 },
           { x = 2, y = 4, z = 8 } ]


[environment]
Type = "GNU/Linux"
OS = "Arch Linux"

[[disks]]
cap = 230
dev = "/dev/sda"

[[disks]]
cap = 120
dev = "/dev/sdb"

# If you would like to drop all the formatting metadata and markup information, you 
# can decode to regular Python primitives
>>> toml_file.primitive
{'': {'title': u'TOML Example'},
 'clients': {'data': [[u'gamma', u'delta'], [1, 2]],
  'hosts': [u'alpha', u'omega'],
  'key3': u'The quick brown fox jumps over the lazy dog.',
  'lines': 'The first newline is\ntrimmed in raw strings.\n   All other whitespace\n   is preserved.\n',
  'quoted': 'Tom "Dubs" Preston-Werner',
  'regex': '<\\i\\c*\\s*>',
  'regex2': "I [dw]on't need \\d{2} apples",
  'str2': u'The quick brown fox jumps over the lazy dog.',
  'str_multiline': u'Roses are red\nViolets are blue',
  'str_quoted': u'I\'m a string. "You can quote me". Name\tJos\xe9\nLocation\tSF.',
  'winpath': 'C:\\Users\\nodejs\\templates',
  'winpath2': '\\\\ServerX\\admin$\\system32\\'},
 'database': {'connection_max': 5000,
  'enabled': True,
  'ports': [8001, 8001, 8002],
  'server': u'192.168.1.1'},
 'disks': [{'cap': '230', 'dev': u'/dev/sda'},
  {'cap': '120', 'dev': u'/dev/sdb'}],
 'environment': {'OS': u'Arch Linux', 'Type': u'GNU/Linux'},
 'fruit': [{'name': u'apple',
   'physical': {'color': u'red', 'shape': u'round'},
   'variety': [{'name': u'red delicious'}, {'name': u'granny smith'}]},
  {'name': u'banana',
   'variety': [{'name': u'plantain',
     'points': [{'x': 1, 'y': 42, 'z': 3},
      {'x': 7, 'y': 8, 'z': 9},
      {'x': 2, 'y': 4, 'z': 8}]}]}],
 'owner': {'dob': datetime.datetime(1979, 5, 27, 15, 32, tzinfo=<UTC>),
  'name': u'Tom Preston-Werner'},
 'servers': {'alpha': {'dc': u'eqdc10', 'ip': u'192.168.0.111'},
  'beta': {'dc': u'eqdc10', 'ip': u'10.0.0.2'}}}
```
