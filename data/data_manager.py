from abc import ABC, abstractmethod
from models.characters import *


class DataManager(ABC):
    """Abstract class for data management. Includes basic CRUD operations"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read_characters(self):
        pass

    @abstractmethod
    def read_character(self, character_id: int):
        pass

    @abstractmethod
    def add_character(self, character):
        pass

    @abstractmethod
    def remove_character(self, character_id: int):
        pass

    @abstractmethod
    def update_character(self, character_id: int, character):
        pass

    def _validate_add_character(self, character: dict):
        """Validates character dict before adding a new character"""
        if 'id' in character.keys():
            raise ValueError('Character id should not be provided.')
        missing_req_fields = Characters.req_fields.difference(set(character.keys()))
        if missing_req_fields:
            raise ValueError(f'Missing required field(s): {", ".join(missing_req_fields)}.')
        req_fields_none = [key for key in Characters.req_fields if character[key] is None]
        if req_fields_none:
            raise ValueError(f'Character\'s {req_fields_none[0]} can not be None.')
        empty_req_fields = [key for key in Characters.req_fields if character[key].strip() == '']
        if empty_req_fields:
            raise ValueError(f'Character\'s {empty_req_fields[0]} can not be empty.')
        if self._character_exists(character['name']):
            raise AttributeError(f'Character {character["name"]} already exists.')
        self._validate_character_field_type(character)

    def _validate_update_character(self, character_id, character:dict):
        """Validates character dict before updating a character"""
        if not isinstance(character_id, int):
            raise TypeError
        wrong_fields = set(character.keys()).difference(Characters.allowed_fields)
        if 'id' in wrong_fields:
            raise AttributeError('Updating ID field is not allowed.')
        if wrong_fields:
            raise AttributeError(f'Not allowed filed(s): {", ".join(wrong_fields.difference({"id"}))}.')
        if self._character_exists(character.get('name')):
            raise AttributeError(f'Character {character["name"]} already exists.')
        self._validate_character_field_type(character)

    @staticmethod
    def _validate_character_field_type(character):
        for field in {'age', 'death'}:
            if character.get(field) and not isinstance(character[field], int):
                raise TypeError(f'Character\'s {field} should be an integer.')
        for field in Characters.allowed_fields.difference({'age', 'death'}):
            if character.get(field) and not isinstance(character[field], str):
                raise TypeError(f'Character\'s {field} should be a string.')

