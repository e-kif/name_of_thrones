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

    def read_characters(self, limit: int = None, skip: int = None,
                        filter: dict = None, sorting: str = None,
                        order: str = None) -> list:
        """Returns current state of the instance storage"""
        if not self.storage:
            return [], 404
        if not any([limit, skip, order, sorting, filter]) and len(self) >= 20:
            return self._read_random_n_characters(20), 200
        
        characters = self.characters
        if filter:
            characters = self._filter_characters(characters, filter)
        if sorting:
            characters = self._sort_characters(characters, sorting, order)
        if limit:
            characters = self._characters_pagination(characters, limit, skip)
        return (characters, 200) if characters else ([], 404)
    
    def _filter_characters(self, characters, filter):
        allowed_filer_keys = self.allowed_fields.union({'age_more_than', 'age_less_then', 'age_less_than'})
        if any([key for key in filter.keys() if key.lower() not in allowed_filer_keys]):
            raise ValueError
        characters = [character for character in characters \
                    if all([value.lower() in character.get(key).lower() \
                    if isinstance(character.get(key), str) and isinstance(value, str) \
                    else value == character.get(key) for key, value in filter.items() \
                    if key not in {'age_more_than', 'age_less_then'}])]
        if filter.get('age_more_than'):
            characters = [character for character in characters if character['age']
                            and character['age'] >= filter['age_more_than']]
        if filter.get('age_less_then'):
            characters = [character for character in characters if character['age']
                            and character['age']<= filter['age_less_then']]
        return characters
    
    def _sort_characters(self, characters, sorting, order):
        if sorting not in self.allowed_fields.union({'id'}):
            raise ValueError
        match order:
            case 'sort_des' | 'desc':
                reverse = True
            case None | 'asc' | 'sort_asc':
                reverse = False
        return sorted(characters, key=lambda char: (char[sorting] is None, char[sorting]), reverse=reverse)

    def _characters_pagination(self, characters, limit, skip):
        start, end = limit * skip if skip else 0, limit * (skip + 1) if skip else limit
        if start >= len(self):
            raise IndexError
        return characters[start:end]

    def _read_random_n_characters(self, n: int = 20):
        return sorted(sample(self.storage, 20), key=lambda char: char['id'])
        
    def add_character(self, character) -> dict:
        """Adds new character to the instance storage"""
        if 'id' in character.keys():
            raise ValueError('Character id should not be provided.')
        missing_required_fields = self.req_fields.difference(set(character.keys()))
        if missing_required_fields:
            raise ValueError('Missing required field(s): '
                             f'{", ".join(missing_required_fields)}.')
        not_defined_req_fields = [field for field in self.req_fields if character[field] is None]
        if not_defined_req_fields:
            raise ValueError(f"Character's {', '.join(not_defined_req_fields)} can not be None.")
        empty_req_fields = [field for field in self.req_fields if character[field].strip() == '']
        if empty_req_fields:
            raise ValueError(f"Character's {', '.join(empty_req_fields)} can not be empty.")
        if self._character_exists(character['name']):
            raise ValueError(f'Character {character["name"]} already exists.')
        character.update({'id': self.next_character_index})
        [character.update({key: None}) for key in self.opt_fields
         if key not in character.keys()]
        self.storage.append(character)
        self.next_character_index += 1
        return character, 201

    def read_character(self, character_id, return_dict=False) -> dict:
        """Retrieves a character with id=character_id
        from the instance storage using binary search algorithm"""
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
        raise KeyError(
            f'Character with id={character_id} was not found.')

    def remove_character(self, character_id):
        """Deletes a character with id=character_id
        from the instance storage
        """
        remove_character = self.read_character(character_id, return_dict=True)
        if remove_character:
            self.storage.remove(remove_character)
        return remove_character, 200

    def update_character(self, character_id, character):
        """Updates character info for the character with id=character_id"""
        if character.get('id'):
            raise AttributeError('Updating ID field is not allowed.')
        not_allowed_keys = set(character.keys()).difference(self.allowed_fields)
        if not_allowed_keys:
            raise AttributeError('Not allowed key(s): '
                                 f'{", ".join(not_allowed_keys)}.')
        if 'name' in character.keys() and self._character_exists(character['name']):
            raise AttributeError(f'Character {character["id"]} already exists.')
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
        for character in self.characters:
            if character['name'] == character_name:
                return True
        return False
