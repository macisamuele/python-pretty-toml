# Consistent TOML for Python

[![Build Status](https://travis-ci.org/Jumpscale/python-consistent-toml.svg?branch=master)](https://travis-ci.org/Jumpscale/python-consistent-toml)
[![Pypi](https://img.shields.io/pypi/pyversions/contoml.svg)](https://pypi.python.org/pypi/contoml)
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

# You can modify table values, or add new values to pre-existing tables, 
# but you cannot create new top-level tables.
>>> toml_file['fruit'][1]['variety'][0]['points'][0]['y'] = 42

>>> toml_file['servers']['alpha']['ip'] = '192.168.0.111'

# Serialize back to TOML text at any point
>>> toml_file.dump('sample_modified.toml')

# If you would like to drop all the formatting metadata and markup information, you 
# can decode to regular Python. primitives
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
