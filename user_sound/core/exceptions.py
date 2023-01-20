class InsertError(Exception):
    """
    Errors inserting values.
    """
    pass


class DeleteError(Exception):
    """
    Errors deleting values.
    """
    pass


class NotFound(Exception):
    """
    Object was not found.
    """
    pass
