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

    @abstractmethod
    def _character_exists(self, character_name: str) -> bool:
        pass

    def _validate_add_character(self, character: dict):
        """Validates character dict before adding a new character.
        Raises AttributeError if character with the same name already exists.
        If id is provided or required fields missing or empty raises ValueError.
        """
        if 'id' in character.keys():
            raise ValueError('Character id should not be provided.')
        self._validate_character_field_type(character)
        missing_req_fields = Characters.req_fields.difference(set(character.keys()))
        if missing_req_fields:
            raise ValueError(f'Missing required field(s): {", ".join(missing_req_fields)}.')
        req_fields_none = [key for key in Characters.req_fields if character[key] is None]
        if req_fields_none:
            raise ValueError(f"Character's {req_fields_none[0]} can not be None.")
        empty_req_fields = [key for key in Characters.req_fields if character[key].strip() == '']
        if empty_req_fields:
            raise ValueError(f"Character's {empty_req_fields[0]} can not be empty.")
        if self._character_exists(character['name']):
            raise AttributeError(f'Character {character["name"]} already exists.')

    def _validate_update_character(self, character_id, character: dict):
        """Validates character dict before updating a character. For wrong type of character_id
        raises a TypeError. For invalid character dict raises an AttributeError
        with corresponding message.
        """
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
        """Validates fields data types, raises TypeError if invalid """
        for field in {'age', 'death'}:
            if character.get(field) and not isinstance(character[field], int):
                raise TypeError(f"Character's {field} should be an integer.")
        for field in Characters.allowed_fields.difference({'age', 'death'}):
            if character.get(field) and not isinstance(character[field], str):
                raise TypeError(f"Character's {field} should be a string.")

    @classmethod
    def _validate_sorting(cls, sorting: str, order: str, model=Characters):
        """Validates sorting and order parameters, raises ValueError if invalid"""
        sort_properties = model.allowed_fields.union({'id'})
        if sorting not in sort_properties:
            raise ValueError(f'Wrong sorting parameter provided: {sorting}.')
        if order is not None and order not in {'desc', 'sort_des', 'asc', 'sort_asc'}:
            raise ValueError(f'Wrong order_by parameter provided: {order}.')
