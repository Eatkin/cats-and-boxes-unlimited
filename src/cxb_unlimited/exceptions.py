class ValidationError(Exception):
    """Board is in invalid state"""

    pass


class OutOfBoundsError(Exception):
    """Tile exceeds board boundaries"""

    pass


class BoardSetupError(Exception):
    """Attempted to setup board when already has tiles"""

    pass
