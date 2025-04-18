from sqlalchemy import create_engine, exc
from sqlalchemy.sql import func
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
        """Returns a character with id = caracter_id or an error message
        if character was not found
        """
        try:
            db_character = self.session.query(Characters).filter_by(id=character_id).one().dict
            return db_character
        except exc.NoResultFound:
            return {'error': f'Character with id={character_id} was not found.'}, 404

    def read_characters(self, limit: int = None, skip: int = None, filter: dict = None, sorting: str = None, order: str = None):
        print(f'{limit=} {sorting=} {filter=}, {order=}')
        if all([limit is None, sorting is None, not filter, order is None]):
            return self._read_random_n_characters(20)
        characters = self.session.query(Characters).order_by(Characters.id).limit(limit).offset(skip).all()
        return [character.dict for character in characters]
    
    def _read_random_n_characters(self, n: int):
        """Returns random n characters ordered by id. If n >= character count in database -
        returns all database characters"""
        character_amount = self.session.query(func.count(Characters.id)).scalar()
        n = n if n < character_amount else character_amount
        characters = self.session.query(Characters).order_by(func.random()).limit(n).all()
        return sorted([character.dict for character in characters], key=lambda char: char['id'])

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
        
