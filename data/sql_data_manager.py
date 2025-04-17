from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.data_manager import DataManager
from models.characters import *


class SQLDataManager(DataManager):

    def __init__(self, db_uri: str):
        self._engine = create_engine(db_uri, echo=False)
        Base.metadata.create_all(self._engine)
        self.session = sessionmaker(bind=self._engine)

    def read_character(self, character_id):
        pass

    def read_characters(self, limit, skip, filter, sorting, order):
        pass

    def add_character(self, character):
        pass

    def remove_character(self, character_id):
        pass

    def update_character(self, character_id, character):
        pass
