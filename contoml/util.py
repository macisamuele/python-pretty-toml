import math


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


def join_with(iterable, separator):
    """
    Joins elements from iterable with separator and returns the produced sequence as a list.

    separator must be addable to a list.
    """
    inputs = list(iterable)
    b = []
    for i, element in enumerate(inputs):
        if isinstance(element, (list, tuple, set)):
            b += tuple(element)
        else:
            b += [element]
        if i < len(inputs)-1:
            b += separator
    return b


def chunkate_string(text, length):
    """
    Iterates over the given seq in chunks of at maximally the given length. Will never break a whole word.
    """
    iterator_index = 0

    def next_newline():
        try:
            return next(i for (i, c) in enumerate(text) if i > iterator_index and c == '\n')
        except StopIteration:
            return len(text)

    def next_breaker():
        try:
            return next(i for (i, c) in reversed(tuple(enumerate(text)))
                        if i >= iterator_index and
                        (i < iterator_index+length) and
                        c in (' ', '\t'))
        except StopIteration:
            return len(text)

    while iterator_index < len(text):
        next_chunk = text[iterator_index:min(next_newline(), next_breaker()+1)]
        iterator_index += len(next_chunk)
        yield next_chunk


def flatten_nested_dicts(nested_dicts):
    """
    Flattens dicts into one dict with tuples of keys representing the nested keys.

    Example
    >>> dd = { \
        'dict1': {'name': 'Jon', 'id': 42}, \
        'dict2': {'name': 'Sam', 'id': 41}, \
    }

    >>> flatten_nested_dicts(dd) == { \
        ('dict1', 'name'): 'Jon', ('dict1', 'id'): 42, \
        ('dict2', 'name'): 'Sam', ('dict2', 'id'): 41}
    True
    """
    assert isinstance(nested_dicts, dict), 'Only works with a dict parameter'

    def flatten(dd):
        output = {}
        for k, v in dd.items():
            if isinstance(v, dict):
                for child_key, child_value in flatten(v).items():
                    output[(k,) + child_key] = child_value
            else:
                output[(k,)] = v
        return output

    # return flatten({(k,): v for k, v in nested_dicts.items()})
    return flatten(nested_dicts)
