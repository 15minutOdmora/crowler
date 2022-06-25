"""
Module for writing and saving data to files.

Contains:
    Json class -> for opening, saving and updating json files.
"""

from __future__ import annotations
from typing import Union
import json
import os
from pathlib import Path


class Json:
    """
    Class for reading, updating, and writing json files.
    """
    @staticmethod
    def open(file_path: str) -> Union[dict, list]:
        """
        Method opens json files and returns its contents as a dictionary.
        Args:
            file_path: Full file path to json file.
        Raises:
            ValueError: Gets raised if given file path does not exist.
        Returns:
            dict: Contents of json file
        """
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                json_object = json.load(f)
            return json_object
        else:
            raise FileNotFoundError(f"Json.open: Given file path {file_path} does not exists.")

    @staticmethod
    def save(file_path: str, json_object: Union[dict, list]) -> None:
        """
        Method opens(new) json file and saves the object, if file already exists it overwrites its contents.
        Args:
            file_path (str): Full file path to the json file.
            json_object (dict()): Json compatible object.
        """
        # Get folder path and create directory if it doesnt exist
        folder_path = Path(file_path).parent
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(json_object, f, indent=4, sort_keys=True)

    @staticmethod
    def update(file_path: str, json_object: Union[dict, list]):
        """
        Method opens json file, reads its dictionary, updates the dictionary with new object and saves to same path.
        Args:
            file_path: Full file path to json file.
            json_object: Json compatible object.
        """
        read_json = {}

        if os.path.isfile(file_path):  # Read only if file exists.
            with open(file_path, "r") as f:
                read_json = json.load(f)

        read_json.update(json_object)

        with open(file_path, "w") as f:
            json.dump(read_json, f, indent=4, sort_keys=True)

    @staticmethod
    def is_valid(file_path: str) -> bool:
        """
        Method tries to open the file path and convert it to a valid Python Json(dictionary).
        Returns True if file contains valid Json object.
        Args:
            file_path (str): File path to file
        Returns:
            bool: If file could be opened as a Json.
        """
        if not file_path:
            return False
        try:
            with open(file_path, "r") as f:
                loaded_data = json.load(f)
            return loaded_data
        except:
            return False