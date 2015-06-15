

def is_sequence_like(x):
    """
    Returns True if x exposes a sequence-like interface.
    """
    required_attrs = (
        '__len__',
        '__getitem__'
    )
    return all(hasattr(x, attr) for attr in required_attrs)


def is_dict_like(x):
    """
    Returns True if x exposes a dict-like interface.
    """
    required_attrs = (
        '__len__',
        '__getitem__',
        'keys',
        'values',
    )
    return all(hasattr(x, attr) for attr in required_attrs)
