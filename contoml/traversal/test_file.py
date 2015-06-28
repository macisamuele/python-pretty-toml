from contoml.elements.test_common import dummy_file_elements
from contoml.traversal.file import TOMLFile


def test_file():
    toml_file = TOMLFile(_elements=dummy_file_elements())

    assert toml_file['']['name'] == 'fawzy'
    assert toml_file['']['another_name'] == 'another_fawzy'

    assert toml_file['details']['id'] == 42
    assert toml_file['details']['section'] == 'fourth'

    assert toml_file['details']['extended']['number'] == 313

    assert toml_file['person'][0]['dest'] == 'north'
    assert toml_file['person'][1]['dest'] == 'south'
