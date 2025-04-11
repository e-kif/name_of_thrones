import os
import json
from data.data_manager import DataManager


class JSONDataManager(DataManager):
    """Data manager for interacting with JSON type storage"""
    optional_fields = {'nickname', 'death', 'symbol', 'house', 'animal', 'age'}
    required_fields = {'name', 'strength', 'role'}

    def __init__(
            self,
            storage_file: str = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '..',
                'storage', 'characters.json')
            ):
        """Constructor method loads data from json file, sorts the list by character IDs,
        assigns sorted character list to self.storage instance variable, creates variable
        for keeping track of the next character id
        """
        self.storage = sorted(self.load_json_file(storage_file), key=lambda character: character['id'])
        self.next_character_index = len(self) + 1

    def load_json_file(self, filename: str) -> list | dict:
        """Loads info from JSON file as a Python object (list or dictionary)"""
        with open(filename, 'r', encoding='utf8') as file_object:
            return json.load(file_object)

    def read_characters(self) -> list:
        """Returns current state of the instance storage"""
        return self.storage

    def add_character(self, character) -> dict:
        """Adds new character to the instance storage"""
        if character.get('id'):
            raise ValueError('Character id should not be provided.')
        missing_required_fields = self.required_fields\
            .difference(set(character.keys()))
        if missing_required_fields:
            raise ValueError('Missing required field(s): '
                             f'{", ".join(missing_required_fields)}.')
        not_defined_req_fields = [field for field in self.required_fields if character[field] is None]
        if not_defined_req_fields:
            raise ValueError(f"Character's {', '.join(not_defined_req_fields)} can not be None.")
        empty_req_fields = [field for field in self.required_fields if character[field] == '']
        if empty_req_fields:
            raise ValueError(f"Character's {', '.join(empty_req_fields)} can not be empty.")
        if self.character_exists(character['name']):
            raise ValueError(f'Character {character["name"]} already exists.')
        character.update({'id': self.next_character_index})
        [character.update({key: None}) for key in self.optional_fields
         if key not in character.keys()]
        print(f'{character=}')
        self.storage.append(character)
        self.next_character_index += 1
        return character

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
            f'Character with id={character_id} was not found.')

    def remove_character(self, character_id):
        """Deletes a character with id=character_id
        from the instance storage
        """
        remove_character = self.read_character(character_id)
        if remove_character:
            self.storage.remove(remove_character)
        return remove_character

    def update_character(self, character_id, character):
        """Updates character info for the character with id=character_id"""
        if character.get('id'):
            raise AttributeError('Character id is not allowed to be changed.')
        not_allowed_keys = set(character.keys())\
            .difference(self.optional_fields)\
            .difference(self.required_fields)
        if not_allowed_keys:
            raise AttributeError('Not allowed key(s): '
                                 f'{", ".join(not_allowed_keys)}.')
        db_character = self.read_character(character_id)
        db_character.update(character)
        return db_character

    @property
    def characters(self) -> list:
        """Getter method for returning current instance storage"""
        return self.read_characters()

    def __len__(self) -> int:
        """Returns total amount of characters in the instance storage"""
        return len(self.storage)

    def character_exists(self, character_name: str) -> bool:
        for character in self.characters:
            if character['name'] == character_name:
                return True
        return False
