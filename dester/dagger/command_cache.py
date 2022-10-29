"""
Classes for holding ran commands, with the option to save them either in a function or file.
"""

from typing import List, Dict


class Command:
    def __init__(self, command: str) -> None:
        self.command = command
        self.valid = None

    def execute(self, current_vars: Dict[str, any]):
        self.valid = True

        try:
            result = eval(self.command, current_vars)
            if result:
                print(result)
        except:
            try:
                exec(self.command, current_vars)
            except Exception as e:
                self.valid = False
                print(e)

    def __str__(self) -> str:
        return f"{self.command}"


class CommandCache:
    def __init__(self):
        self.commands: List[Command] = []
        pass

    def add(self, command: Command) -> None:
        self.commands.append(command)

    def save(self, path: str) -> None:
        pass

    def __clear(self) -> None:
        pass

    def __str__(self, prefix: str = "\t") -> str:
        return f"Currently stored commands:\n{prefix}" + f"\n{prefix}".join([str(command) for command in self.commands])
