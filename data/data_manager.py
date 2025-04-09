from abc import ABC, abstractmethod


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
