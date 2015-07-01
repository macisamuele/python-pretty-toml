

def parse_token_stream(token_stream):
    """
    Parses the given token_stream into a sequence of top-level TOML elements.
    """
    from .parser import toml_file_elements
    from .elementsanitizer import sanitize

    elements, _ = toml_file_elements(token_stream)

    return sanitize(elements)
