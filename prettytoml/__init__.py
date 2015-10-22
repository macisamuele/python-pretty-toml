from ._version import VERSION

__version__ = VERSION


def prettify(toml_text):
    """
    Prettifies and returns the TOML file content provided.
    """
    raise NotImplementedError   # TODO


def prettify_from_file(file_path):
    """
    Reads, prettifies and returns the TOML file specified by the file_path.
    """
    with open(file_path, 'r') as fp:
        return prettify(fp.read())
