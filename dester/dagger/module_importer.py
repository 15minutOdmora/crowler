"""
Module used for importing modules from inside directory.
"""

from typing import List
import os
import inspect
import importlib


ignore_directories = ["venv", "env"]


def create_module_import_string(package_name: str, module_path: str) -> str:
    """
    Function creates a module import string (ex. foo.bar.module) based on the package name and file path of python
    file.

    Import string will be created from the package_name ahead (not including package name at beginning).

    Args:
        package_name (str): Name of package where the python module is contained (root. dir. of project).
        module_path (str): Absolute path of module.
    Returns:
        str: Module import string
    """
    # Normalize path string into proper os path string
    relative_file_path = os.path.normpath(module_path)

    # Create list with directory names, split at os separator, use lambda to remove .py from file names
    path_list = list(map(
        lambda name: name.replace(".py", "") if ".py" in name else name,
        relative_file_path.split(os.sep)
    ))

    # Check if passed module is from package
    if package_name not in path_list:
        return  # Raise error here

    # Get index of package, return import string from package name on
    package_root_index = path_list.index(package_name)
    return ".".join(path_list[package_root_index + 1:])


def get_all_import_strings(dir_path: str, called_from_module: str) -> List[str]:
    """
    Function reads and creates all needed import strings in the directory structure except the called_from_module.

    Args:
        dir_path (str): Directory root to import all modules from its structure.
        called_from_module (str): Absolute path of module where call originated (main module), will be ignored.
    """
    import_strings = []

    # Get directory of module the call originated from
    package_name = os.path.basename(os.path.dirname(called_from_module))

    # Traverse directory structure, ignore some directories
    for root, directories, files in os.walk(dir_path):
        directories[:] = [d for d in directories if d not in ignore_directories]

        for filename in files:
            # Only use .py files and exclude files starting with __ (such as __init__)
            if filename.endswith(".py") and not filename.startswith("__"):
                file_path = os.path.join(root, filename)

                # Check file is not the one where the call originated from (this would cause double imports)
                if not os.path.samefile(file_path, called_from_module):
                    # Create module-import string and import the module
                    import_strings.append(create_module_import_string(package_name, os.path.join(root, filename)))

    return import_strings


def import_all_modules(dir_path: str, called_from_module: str) -> None:
    """
    Function imports all modules in the directory structure except the called_from_module.

    Args:
        dir_path (str): Directory root to import all modules from its structure.
        called_from_module (str): Absolute path of module where call originated (main module), will be ignored.
    """
    import_strings = get_all_import_strings(dir_path, called_from_module)

    for import_string in import_strings:
        importlib.import_module(import_string)


def setup(call_from: inspect.FrameInfo, directory: str = None) -> None:
    """
    Function imports all modules in the directory. If directory is not passed it will import all modules in the
    directory where the call originated from i.e. call_from modules parent directory.

    Args:
        call_from (inspect.FrameInfo): FrameInfo object where the call originated from, this object should be fetched
            from inspect.stack() when calling function, in argument.
        directory (str): Absolute or relative path of directory to search and import modules.
    """
    # Get module file where call originated from
    module_file = inspect.getmodule(call_from[0]).__file__ 

    # Check directory argument
    if not directory:  # If not passed grab modules parent directory
        directory = os.path.dirname(module_file)
    elif not os.path.isabs(directory):  # If passed as relative, join with directory of module
        directory = os.path.join(os.path.dirname(module_file), directory)

    # Normalize path
    directory = os.path.normpath(directory)

    # Import all modules except the one where the call originated from
    import_all_modules(dir_path=directory, called_from_module=module_file)
