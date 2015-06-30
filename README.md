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

# The anonymous table is accessible using the empty string key on the tom file
print(toml_file['']['title'])

# You can modify table values, or add new values to pre-existing tables, 
# but you cannot create new top-level tables.
toml_file['fruit'][1]['variety'][0]['points'][0]['y'] = 42
toml_file['servers']['alpha']['ip'] = '192.168.0.111'

# Serialize back to TOML text at any point
toml_file.dump('sample_modified.toml')
```
