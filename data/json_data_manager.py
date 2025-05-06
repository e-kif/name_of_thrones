import os
import json
from random import sample
from data.data_manager import DataManager


class JSONDataManager(DataManager):
    """Data manager for interacting with JSON type storage"""
    opt_fields = {'nickname', 'death', 'symbol', 'house', 'animal', 'age'}
    req_fields = {'name', 'strength', 'role'}
    allowed_fields = req_fields.union(opt_fields)

    def __init__(
            self,
            storage_file: str = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '..',
                'storage', 'characters.json'),
            users_file: str = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '..',
                'storage', 'users.json'),
    ):
        """Constructor method loads data from json file, sorts the list by character IDs,
        assigns sorted character list to self.storage instance variable, creates variable
        for keeping track of the next character id
        """
        self.storage = sorted(self.load_json_file(storage_file), key=lambda character: character['id'])
        self.next_character_index = len(self) + 1
        self.users = sorted(self.load_json_file(users_file), key=lambda user: user['id'])

    @staticmethod
    def load_json_file(filename: str) -> list | dict:
        """Loads info from JSON file as a Python object (list or dictionary)"""
        with open(filename, 'r', encoding='utf8') as file_object:
            return json.load(file_object)

    def read_characters(self, limit: int = None, skip: int = None,
                        char_filter: dict = None, sorting: str = None,
                        order: str = None) -> tuple:
        """Returns current state of the instance storage"""
        if not self.storage:
            return [], 404
        if not any([limit, skip, order, sorting, char_filter]) and len(self) >= 20:
            return self._read_random_n_characters(20), 200

        characters = self.characters
        if char_filter:
            characters = self._filter_characters(characters, char_filter)
        if sorting:
            characters = self._sort_characters(characters, sorting, order)
        if limit:
            characters = self._characters_pagination(characters, limit, skip)
        return (characters, 200) if characters else ([], 404)

    def _filter_characters(self, characters: list, char_filter: dict) -> list:
        """Validates and applies character filters"""
        allowed_filer_keys = self.allowed_fields.union({'age_more_than', 'age_less_then', 'age_less_than'})
        if any([key for key in char_filter.keys() if key.lower() not in allowed_filer_keys]):
            raise ValueError
        characters = [character for character in characters
                      if all([value.lower() in character.get(key).lower()
                              if isinstance(character.get(key), str) and isinstance(value, str)
                              else value == character.get(key) for key, value in char_filter.items()
                              if key not in {'age_more_than', 'age_less_then'}])]
        if char_filter.get('age_more_than'):
            characters = [character for character in characters if character['age']
                          and character['age'] >= char_filter['age_more_than']]
        if char_filter.get('age_less_then'):
            characters = [character for character in characters if character['age']
                          and character['age'] <= char_filter['age_less_then']]
        return characters

    def _sort_characters(self, characters: list, sorting: str, order: str) -> list:
        """Validates and applies character sorting"""
        if sorting not in self.allowed_fields.union({'id'}):
            raise ValueError
        match order:
            case 'sort_des' | 'desc':
                reverse = True
            case None | 'asc' | 'sort_asc' | _:
                reverse = False
        return sorted(characters, key=lambda char: (char[sorting] is None, char[sorting]), reverse=reverse)

    def _characters_pagination(self, characters: list, limit: int, skip: int | None) -> list:
        """Validates and applies pagination parameters to a list of characters"""
        start, end = limit * skip if skip else 0, limit * (skip + 1) if skip else limit
        if start >= len(self):
            raise IndexError
        return characters[start:end]

    def _read_random_n_characters(self, n: int = 20) -> list:
        """Returns random n characters sorted by theirs id"""
        return sorted(sample(self.storage, n), key=lambda char: char['id'])

    def add_character(self, character: dict) -> tuple:
        """Validates character parameter, if valid: adds new character to the instance storage.
        If invalid: raises ValueError.
        """
        self._validate_add_character(character)
        character.update({'id': self.next_character_index})
        [character.update({key: None}) for key in self.opt_fields
         if key not in character.keys()]
        self.storage.append(character)
        self.next_character_index += 1
        return character, 201

    def read_character(self, character_id: int, return_dict: bool = False) -> dict:
        """Retrieves a character with id=character_id
        from the instance storage using binary search algorithm.
        If character was not found: raises KeyError"""
        left, right = 0, len(self.storage)
        while left <= right:
            mid = (left + right) // 2
            if mid >= len(self.storage):
                break
            if self.storage[mid]['id'] == character_id:
                return self.storage[mid] if return_dict else (self.storage[mid], 200)
            elif self.storage[mid]['id'] < character_id:
                left = mid + 1
            else:
                right = mid - 1
        raise KeyError(f'Character with id={character_id} was not found.')

    def remove_character(self, character_id: int) -> tuple:
        """Deletes a character with id=character_id
        from the instance storage
        """
        remove_character = self.read_character(character_id, return_dict=True)
        if remove_character:
            self.storage.remove(remove_character)
        return remove_character, 200

    def update_character(self, character_id: int, character: dict) -> tuple:
        """Updates character info for the character with id=character_id.
        Raises Attribute error for invalid character dict."""
        if character.get('id'):
            raise AttributeError('Updating ID field is not allowed.')
        not_allowed_keys = set(character.keys()).difference(self.allowed_fields)
        if not_allowed_keys:
            raise AttributeError('Not allowed key(s): '
                                 f'{", ".join(not_allowed_keys)}.')
        if 'name' in character.keys() and self._character_exists(character['name']):
            raise AttributeError(f'Character {character["name"]} already exists.')
        db_character = self.read_character(character_id, return_dict=True)
        db_character.update(character)
        return db_character, 200

    @property
    def characters(self) -> list:
        """Getter method for returning current instance storage"""
        return self.storage

    def __len__(self) -> int:
        """Returns total amount of characters in the instance storage"""
        return len(self.storage)

    def _character_exists(self, character_name: str) -> bool:
        """Checks if character with given character_name is present
        in a database
        """
        for character in self.characters:
            if character['name'] == character_name:
                return True
        return False

    def get_user_by_name(self, username: str) -> dict:
        """Returns a user found by his/her username.
        Raises KeyError if user was not found.
        """
        user_list = [user for user in self.users if user['username'].lower() == username.lower()]
        if not user_list:
            raise KeyError(f'User with username "{username}" was not found')
        return user_list[0]
