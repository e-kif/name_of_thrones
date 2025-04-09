import os
import json
from data.data_manager import DataManager


class JSONDataManager(DataManager):
    """Data manager for interacting with JSON type storage"""

    def __init__(
            self,
            storage_file: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'storage', 'characters.json')
            ):
        """Constructor method loads data from json file
        into self.storage instance variable
        """
        self.storage = self.load_json_file(storage_file)

    def load_json_file(self, filename: str) -> list | dict:
        """Loads info from JSON file as a Python object (list or dictionary)"""
        with open(filename, 'r', encoding='utf8') as file_object:
            return json.load(file_object)

    def read_characters(self):
        """Returns current state of the instance storage"""
        return self.storage

    def add_character(self, character):
        """Adds new character to the instance storage"""
        return super().add_character(character)

    def read_character(self, character_id):
        """Reads a character with id=character_id from the instance storage"""
        return super().read_character(character_id)

    def remove_character(self, character_id):
        """Deletes a character with id=character_id
        from the instance storage
        """
        return super().remove_character(character_id)

    def update_character(self, character_id, character):
        """Updates character info for the caracter with id=character_id"""
        return super().update_character(character_id, character)

    @property
    def characters(self):
        """Getter method for returning current instance storage"""
        return self.read_characters
