"""
Module containing logic for registering command functions.
"""

from typing import Dict, Callable


__command_registry_dict: Dict[str, Callable] = {}


def __command_registry() -> Callable:
    """
    Rregisters all functions using @command decorator to a signle global registry object.
    """
    def registrator(func) -> Callable:
        __command_registry_dict[func.__name__] = func
        return func

    return registrator


command = __command_registry()
registry = __command_registry_dict
