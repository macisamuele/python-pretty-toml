
import contoml

def test_it_should_correctly_load_sample_file():
    parsed = contoml.load('sample.toml')

    print(parsed)
