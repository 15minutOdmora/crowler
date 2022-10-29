"""
Dagger debuger module for executing python commands in a shell like environment.
Current debugging sessions will get injected with all imported or defined variables.

Usefull for running Selenium Driver commands.
"""

from inspect import getframeinfo, stack
import sys

from dester.dagger.command_cache import Command, CommandCache


quit_commands = [":q", "quit", "exit"]


def __get_current_variables():
    frame = sys._getframe(2)  # 2. frame in the call stack
    return frame.f_globals.copy()


def __print_debug_info(caller_info: str):
    output = f"Dagger debug session on:\n\t{caller_info.filename} line: {caller_info.lineno}\nWrite either {', '.join(quit_commands)} to exit debug mode."
    print(output)


def debug(save: bool = False):
    """
    Starts an interactive debugging session containing all variables up to the function call.
    Execute normal Python logic with access to imported or defined variables up to that point.

    Args:
        save (bool, optional): If executed commands should be saved and then displayed. Defaults to False.
    """
    current_vars = __get_current_variables()
    caller_info = getframeinfo(stack()[1][0])

    __print_debug_info(caller_info)

    command_cache = CommandCache()

    while True:
        command_str = input(">>> ")

        if command_str in quit_commands:
            break

        if command_str == "cache":
            print(command_cache)
            continue
        
        command = Command(command_str)
        command.execute(current_vars)

        command_cache.add(command)
