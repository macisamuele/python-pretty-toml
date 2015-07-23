# Consistent TOML for Python

[![Build Status](https://travis-ci.org/Jumpscale/python-consistent-toml.svg?branch=master)](https://travis-ci.org/Jumpscale/python-consistent-toml)
[![Python Versions](https://img.shields.io/pypi/pyversions/contoml.svg)](https://pypi.python.org/pypi/contoml)
[![Release](https://img.shields.io/pypi/v/contoml.svg)](https://pypi.python.org/pypi/contoml)
![Wheel](https://img.shields.io/pypi/wheel/contoml.svg)
[![Join the chat at https://gitter.im/Jumpscale/python-consistent-toml](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Jumpscale/python-consistent-toml?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


A [TOML](https://github.com/toml-lang/toml) serializer/deserializer for Python that tries its best to preserve order of table mappings, formatting of source file, and comments during a deserialize/update/serialize job. This is achieved by preserving the parsed/constructed TOML data structures as lexical tokens internally and having the data manipulations performed directly on the tokens.

## Installation ##
```bash
pip install --upgrade contoml
```

## Usage ##

```python
>>> import contoml

>>> toml_file = contoml.load('sample.toml')

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

# If you like, you can at any moment drop all the formatting metadata preserved in the 
# lodaded TOML file and obtain a primive Python container out of it
>>> toml_file.primitive
{'': {'title': 'TOML Example'},
 'clients': {'data': [['gamma', 'delta'], [1, 2]],
  'hosts': ['alpha', 'omega'],
  'key3': 'The quick brown fox jumps over the lazy dog.',
  'lines': 'The first newline is\ntrimmed in raw strings.\n   All other whitespace\n   is preserved.\n',
  'quoted': 'Tom "Dubs" Preston-Werner',
  'regex': '<\\i\\c*\\s*>',
  'regex2': "I [dw]on't need \\d{2} apples",
  'str2': 'The quick brown fox jumps over the lazy dog.',
  'str_multiline': 'Roses are red\nViolets are blue',
  'str_quoted': 'I\'m a string. "You can quote me". Name\tJosé\nLocation\tSF.',
  'winpath': 'C:\\Users\\nodejs\\templates',
  'winpath2': '\\\\ServerX\\admin$\\system32\\'},
 'database': {'connection_max': 5000,
  'enabled': True,
  'ports': [8001, 8001, 8002],
  'server': '192.168.1.1'},
 'disks': [{'cap': '230', 'dev': '/dev/sda'},
  {'cap': '120', 'dev': '/dev/sdb'}],
 'environment': {'OS': 'Arch Linux', 'Type': 'GNU/Linux'},
 'fruit': [{'name': 'apple',
   'physical': {'color': 'red', 'shape': 'round'},
   'variety': [{'name': 'red delicious'}, {'name': 'granny smith'}]},
  {'name': 'banana',
   'variety': [{'name': 'plantain',
     'points': [{'x': 1, 'y': 42, 'z': 3},
      {'x': 7, 'y': 8, 'z': 9},
      {'x': 2, 'y': 4, 'z': 8}]}]}],
 'owner': {'dob': datetime.datetime(1979, 5, 27, 15, 32, tzinfo=<UTC>),
  'name': 'Tom Preston-Werner'},
 'servers': {'alpha': {'dc': 'eqdc10', 'ip': '192.168.0.111'},
  'beta': {'dc': 'eqdc10', 'ip': '10.0.0.2'}}}

# You can serialize your TOML file back to TOML text at any point
>>> toml_file.dump('updated_sample.toml')
```

This produces the following TOML file:

```toml
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

```

Which is equivalent to the following data structure:

```json
{
 "": {"title": "TOML Example"},
 "owner": {
  "name": "Tom Preston-Werner",
  "dob": "1979-05-27 15:32:00+00:00"
 },
 "database": {
  "ports": [8001, 8001, 8002],
  "enabled": true,
  "connection_max": 5000,
  "server": "192.168.1.1"
 },
 "clients": {
  "lines": "The first newline is\ntrimmed in raw strings.\n   All other whitespace\n   is preserved.\n",
  "str_multiline": "Roses are red\nViolets are blue",
  "regex": "<\\i\\c*\\s*>",
  "winpath": "C:\\Users\\nodejs\\templates",
  "data": [
   ["gamma", "delta"],
   [1, 2]
  ],
  "hosts": [
   "alpha",
   "omega"
  ],
  "key3": "The quick brown fox jumps over the lazy dog.",
  "str_quoted": "I'm a string. \"You can quote me\". Name\tJos\u00e9\nLocation\tSF.",
  "quoted": "Tom \"Dubs\" Preston-Werner",
  "str2": "The quick brown fox jumps over the lazy dog.",
  "winpath2": "\\\\ServerX\\admin$\\system32\\",
  "regex2": "I [dw]on't need \\d{2} apples"
 },
 "servers": {
  "alpha": {
   "dc": "eqdc10",
   "ip": "192.168.0.111"
  },
  "beta": {
   "dc": "eqdc10",
   "ip": "10.0.0.2"
  }
 },
 "fruit": [
  {
   "name": "apple",
   "variety": [
    {
     "name": "red delicious"
    },
    {
     "name": "granny smith"
    }
   ],
   "physical": {
    "shape": "round",
    "color": "red"
   }
  },
  {
   "name": "banana",
   "variety": [
    {
     "name": "plantain",
     "points": [
      {"y": 42, "x": 1, "z": 3},
      {"y": 8, "x": 7, "z": 9},
      {"y": 4, "x": 2, "z": 8}
     ]
    }
   ]
  }
 ],
 "disks": [
  {"cap": "230", "dev": "/dev/sda"},
  {"cap": "120", "dev": "/dev/sdb"}
 ],
 "environment": {
  "Type": "GNU/Linux",
  "OS": "Arch Linux"
 }
}
```
