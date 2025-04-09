import os
import json
from data_manager import DataManager


class JSONDataManager(DataManager):
    """Data manager for interacting with JSON type storage"""

    def __init__(
            self,
            storage_file: str = os.path.join(['storage', 'characters.json'])
            ):
        """Constructor method loads data from json file
        into self.storage instance variable
        """
        self.storage = self.load_json_file()

    def load_json_file(self, filename: str) -> list | dict:
        """Loads info from JSON file as a Python object (list or dictionary)"""
        with open(filename, 'r', encoding='utf8') as file_object:
            return json.load(file_object)

    def read_characters(self):
        """Returns current state of the instance storage"""
        return self.storage

    @property
    def characters(self):
        """Getter method for returning current instance storage"""
        return self.read_characters
