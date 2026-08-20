class LocatorResolutionError(Exception):
    """
    Raised when a locator cannot be resolved.
    This exception is eligible for AI locator healing.
    """
    pass


class LocatorNotFoundError(

    LocatorResolutionError

):
    pass
