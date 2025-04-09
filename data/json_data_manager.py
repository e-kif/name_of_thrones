import os
import json
from data.data_manager import DataManager


class JSONDataManager(DataManager):
    """Data manager for interacting with JSON type storage"""

    def __init__(
            self,
            storage_file: str = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '..',
                'storage', 'characters.json')
            ):
        """Constructor method loads data from json file
        into self.storage instance variable
        """
        self.storage = self.load_json_file(storage_file)

    def load_json_file(self, filename: str) -> list | dict:
        """Loads info from JSON file as a Python object (list or dictionary)"""
        with open(filename, 'r', encoding='utf8') as file_object:
            return json.load(file_object)

    def read_characters(self) -> list:
        """Returns current state of the instance storage"""
        return self.storage

    def add_character(self, character) -> dict:
        """Adds new character to the instance storage"""
        return super().add_character(character)

    def read_character(self, character_id) -> dict:
        """Retrieves a character with id=character_id
        from the instance storage using binary search algorithm"""

        left, right = 0, len(self.storage)
        while left <= right:
            mid = (left + right) // 2
            if mid >= len(self.storage):
                break
            if self.storage[mid]['id'] == character_id:
                return self.storage[mid]
            elif self.storage[mid]['id'] < character_id:
                left = mid + 1
            else:
                right = mid - 1

        raise KeyError(
            f'There is no character with id={character_id} in database.')

    def remove_character(self, character_id):
        """Deletes a character with id=character_id
        from the instance storage
        """
        return super().remove_character(character_id)

    def update_character(self, character_id, character):
        """Updates character info for the character with id=character_id"""
        return super().update_character(character_id, character)

    @property
    def characters(self) -> list:
        """Getter method for returning current instance storage"""
        return self.read_characters()

    def __len__(self) -> int:
        """Returns total amount of characters in the instance storage"""
        return len(self.storage)
