

class TOMLError(Exception):
    """
    All errors raised by this module are descendants of this type.
    """

class InvalidTOMLFileError(TOMLError):
    pass

class NoArrayFound(TOMLError):
    """
    An array of tables was requested but none exist by the given name.
    """
