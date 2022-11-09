"""
Module containing logic for registering command functions.
"""

from typing import Dict, Callable


class ActionRegistry(dict):
    def __str__(self, prefix: str = "\t") -> str:
        return f"Currently stored actions:\n{prefix}" + f"\n{prefix}".join([str(action_name) for action_name in self.keys()])


__action_registry_dict: ActionRegistry = ActionRegistry()


def __action_registry() -> Callable:
    """
    Rregisters all functions using @command decorator to a signle global registry object.
    """
    def registrator(func) -> Callable:
        __action_registry_dict[func.__name__] = func
        return func

    return registrator


action = __action_registry()
registry = __action_registry_dict
