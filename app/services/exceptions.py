"""Domain exceptions translated into safe HTTP responses by route handlers."""


class EmailAlreadyRegistered(Exception):
    """Raised when a registration email is already in use."""


class InvalidCredentials(Exception):
    """Raised for an unknown email or an incorrect password."""


class EmailAlreadyInUse(Exception):
    """Raised when a profile update tries to use another account's email."""


class InvalidCurrentPassword(Exception):
    """Raised when the current password supplied for a change is incorrect."""


class ReusedPassword(Exception):
    """Raised when the new password matches the current password."""
