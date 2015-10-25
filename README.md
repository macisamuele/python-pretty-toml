# Pretty TOML for Python

[![Build Status](https://travis-ci.org/Jumpscale/python-pretty-toml.svg?branch=master)](https://travis-ci.org/Jumpscale/python-pretty-toml)
[![Python Versions](https://img.shields.io/pypi/pyversions/prettytoml.svg)](https://pypi.python.org/pypi/prettytoml)
[![Release](https://img.shields.io/pypi/v/prettytoml.svg)](https://pypi.python.org/pypi/prettytoml)
![Wheel](https://img.shields.io/pypi/wheel/prettytoml.svg)


A formatter for [TOML](https://github.com/toml-lang/toml) files.

## Installation ##
```bash
pip install --upgrade prettytoml
```

## Usage ##

```python
>>> import prettytoml
>>> prettified_content = prettytoml.prettify_from_file('sample.toml')
>>> with open('sample-prettified.toml', 'w') as fp:
      fp.write(prettified_content)
```

## Formatting Rules ##

* Entries within a single table should be ordered lexicographically by key
* Every key and value pair in any table should be separated by the triplet (single space character, an assignment character `=`, single space character)
* Anonymous table should never be indented
* Nth-level table sections should be indented by `(N-1)*2` spaces
* Line-terminating comments should always be prefixed by a single tab character whitespace only
* Lines whose lengths exceed `120` characters whose values are strings, arrays, or inline tables should have the array or string value broken onto multiple lines and the inline table turned into a multiline table section so as to try to maintain a maximum line length of `120`
* Tables should always be separated by an empty newline
