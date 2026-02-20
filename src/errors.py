class ConsoleRPGError(Exception):
    """Base exception for the project."""


class ConfigError(ConsoleRPGError):
    """Raised when configuration files are invalid."""


class GameplayError(ConsoleRPGError):
    """Raised when an impossible gameplay action is requested."""
