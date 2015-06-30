import json
import contoml

def test_it_should_correctly_load_sample_file():

    toml_file = contoml.load('dateless_sample.toml')

    assert set(toml_file.keys()) == {'fruit', 'clients', '', 'owner', 'database', 'servers'}

    json_file = json.load(open('dateless_sample.json'))

    assert json_file == toml_file.primitive
