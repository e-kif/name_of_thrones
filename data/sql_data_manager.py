import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, exc
from data.data_manager import DataManager
from models.characters import *
from data.json_data_manager import JSONDataManager


class SQLDataManager(DataManager):

    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.session = self.db.session

    def _reset_database(self):
        """Drops all tables, creates them and loads characters from json file"""
        json_characters = JSONDataManager().read_characters(limit=50)
        self.db.drop_all()
        self.db.create_all()
        for character in json_characters:
            self.add_character(character, refresh=False)

    def read_character(self, character_id: int):
        try:
            db_character = self.session.query(Characters).filter_by(id=character_id).one().dict
            return db_character
        except exc.NoResultFound:
            return {'message': f'Character with id={character_id} was not found.'}, 404

    def read_characters(self, limit: int = 20, skip: int = 0, filter: dict = None, sorting: str = None, order: str = None):
        characters = self.session.query(Characters).all()
        print(type(characters))
        return [character.dict for character in characters]

    def add_character(self, character: dict, refresh: bool = True):
        required_fields = {'name', 'role', 'strength'}
        optional_fields = {'animal', 'age', 'house', 'death', 'symbol', 'nickname'}
        character_req = {key: value for key, value in character.items() if value is not None and key in required_fields}
        character_opt = {key: value for key, value in character.items() if value is not None and key in optional_fields}
        add_character = Characters(**character_req)
        try:
            self.session.add(add_character)
            self.session.flush()
            if character_opt:
                [setattr(add_character, key, value) for key, value in character_opt.items()]
            self.session.commit()
            if refresh:
                self.session.refresh(add_character)
            return add_character if refresh else character
        except exc.IntegrityError as error:
            self.session.rollback()
            return {'message': 'Integrity error occurred.', 'error': str(error)}, 409
        except exc.SQLAlchemyError as error:
            self.session.rollback()
            return {'message': f'A database error occurred.', 'error': str(error)}, 500


    def remove_character(self, character_id):
        pass

    def update_character(self, character_id, character):
        pass

    # def _add(self, instance, refresh: bool = True):
    #     """Add instance to database with error handling and db rollbacks"""
    #     try:
    #         self.session.add(instance)
    #         self.session.commit()
    #     except exc.IntegrityError as error:
    #         db.session.rollback()
    #         return {'message': 'Integrity error occurred.', 'error': str(error)}, 409
    #     except exc.SQLAlchemyError as error:
    #         db.session.rollback()
    #         return {'message': f'A database error occurred.', 'error': str(error)}, 500
    #     if refresh:
    #         return self.session.refresh(instance), 201
        
    # def _delete(self, instance):
    #     """Delete an instance from the database with wrror handling and rollback"""
    #     try:
    #         self.session.delete(instance)
    #         self.session.commit()
    #     except exc.SQLAlchemyError as error:
    #         self.session.rollback()
    #         return {'message': 'A database error occurred.', 'error': str(error)}, 500
    #     return instance, 200
        

if __name__ == '__main__':
    load_dotenv()
    db_uri = os.getenv('DATABASE_URI')
    db = SQLDataManager(db_uri)
    db._reset_database()
    # print(db.read_characters())
