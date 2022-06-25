"""
Dagger debuger module for executing python commands in a shell like environment.
Current debugging sessions will get injected with all imported or defined variables.

Usefull for running Selenium Driver commands.
"""

from inspect import getframeinfo, stack
import sys


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

    saved_commands = []

    while True:
        command = input(">>> ")
        failed = False

        if command in quit_commands:
            break
        
        try:
            result = eval(command, current_vars)
            if result:
                print(result)
        except:
            try:
                exec(command, current_vars)
            except Exception as e:
                failed = True
                print(e)

        if save and not failed:
            saved_commands.append(command)
    
    if save:
        print("Ran commands:", end="\n  ")
        print("\n  ".join(saved_commands))
