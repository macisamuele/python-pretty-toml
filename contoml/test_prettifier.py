import contoml


def test_works():
    f = contoml.load('sample.toml')
    f.prettify()
    f.dump('sample-prettified.toml')
