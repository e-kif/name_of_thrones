from sqlalchemy import exc, desc
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from data.data_manager import DataManager
from models.characters import *
from models.users import Users, Roles
from data.json_data_manager import JSONDataManager
from utils.security import hash_password


class SQLDataManager(DataManager):

    def __init__(self, database: SQLAlchemy):
        self.db = database
        self.session = self.db.session

    def _reset_database(self):
        """Drops all tables, creates them and loads characters and users from json files"""
        json_characters = JSONDataManager().read_characters(limit=50)[0]
        self.db.session.remove()
        self.db.drop_all()
        self.db.create_all()
        for character in json_characters:
            del character['id']
            self.add_character(character, refresh=False)
        self._reset_users()

    def _reset_users(self):
        """Resets users and roles to default state: drops tables Users and Roles,
        creates them again and populates with the date read from users.json file.
        """
        json_users = JSONDataManager().users
        [table.__table__.drop(self.db.engine, checkfirst=True) for table in [Users, Roles]]
        [table.__table__.create(self.db.engine, checkfirst=True) for table in [Roles, Users]]
        for user in json_users:
            del user['id']
            user['password'] = hash_password(user['password'])
            self.add_user(user)

    def read_character(self, character_id: int, return_object: bool = False) -> tuple | Characters:
        """Returns a tuple (character with id=character_id  and status code) or an error message
        if character was not found. If :return_object: is True -
        returns Characters sqlalchemy object.
        """
        try:
            db_character = self.session.query(Characters)\
                .filter_by(id=character_id).one()
            return db_character if return_object else (db_character.dict, 200)
        except exc.NoResultFound:
            return {'error': f'Character with id={character_id} was not found.'}, 404

    def read_characters(self, limit: int = None, skip: int = None,
                        char_filter: dict = None, sorting: str = None, order: str = None) -> tuple:
        """Returns a tuple with a list of characters with applied filters, sorting and pagination
        and a status code. Returns empty list and 404 if no characters found matching criteria.
        If no filters, sorting or pagination parameters were provided - returns list
        of 20 random characters sorted by id.
        """
        if all([limit is None, sorting is None, not char_filter, order is None]):
            return self._read_random_n_characters(20), 200

        query = self.session.query(Characters)
        if char_filter:
            query = self._apply_filter(query, char_filter)
        if sorting:
            query = self._apply_sorting(query, sorting, order)
        if limit:
            query = self._apply_pagination(query, limit, skip)
        characters = query.all()
        return ([character.dict for character in characters], 200) if characters else ([], 404)
    
    @staticmethod
    def _apply_filter(query, char_filter, model=Characters):
        """Validates character filter. If valid applies filter(s) to a given
        sqlalchemy query object.
        """
        allowed_filter_fields = model.allowed_fields.union({'age_less_than', 'age_less_then', 'age_more_than'})
        for key, value in char_filter.items():
            key = key.lower()
            if key not in allowed_filter_fields:
                raise ValueError(f'Parameter {key} is not allowed.')
            attribute = getattr(model, key, None)
            
            if key == 'age_more_than':
                query = query.filter(Characters.age >= value)
                continue
            if key in {'age_less_then', 'age_less_than'}:
                query = query.filter(Characters.age <= value)
                continue

            match value:
                case str() if value.strip() == '':
                    query = query.filter(attribute.is_(None))
                case str():
                    query = query.filter(func.lower(attribute) == value.lower())
                case _:
                    query = query.filter(attribute == value)
        return query
    
    @classmethod
    def _apply_sorting(cls, query, sorting, order, model=Characters):
        """Validates sorting parameters. If invalid raises ValueError.
        If valid applies them to a give query, return modified query.
        """
        cls._validate_sorting(sorting, order, model)
        if order in {'desc', 'sort_des'}:
            return query.order_by(desc(getattr(Characters, sorting)))
        return query.order_by(getattr(Characters, sorting))
    
    @staticmethod
    def _apply_pagination(query, limit, skip, model=Characters):
        """Validates pagination parameters. If invalid raises IndexError.
        If valid modifies given query and returns it.
        """
        if limit and skip:
            skip = limit * skip
            if skip > query.order_by(None).with_entities(func.count(model.id)).scalar():
                raise IndexError
        return query.limit(limit).offset(skip)

    def _read_random_n_characters(self, n: int) -> list:
        """Returns random n characters ordered by id. If n >= character count in database -
        returns all database characters"""
        character_amount = len(self)
        n = n if n < character_amount else character_amount
        characters = self.session.query(Characters).order_by(func.random()).limit(n).all()
        return sorted([character.dict for character in characters], key=lambda char: char['id'])

    def add_character(self, character: dict, refresh: bool = True) -> tuple:
        """Validates given character dict. If invalid raises a ValueError (invalid dict)
        or an AttributeError (if character already exists in database). If valid:
        adds a character to the database and returns tuple with created character and a status code
        """
        self._validate_add_character(character)
        character_req = {key: value for key, value in character.items()
                         if value is not None and key in Characters.req_fields}
        character_opt = {key: value for key, value in character.items()
                         if value is not None and key in Characters.opt_fields}
        add_character = Characters(**character_req)
        self.session.add(add_character)
        self.session.flush()
        if character_opt:
            [setattr(add_character, key, value) for key, value in character_opt.items()]
        self.session.commit()
        if refresh:
            self.session.refresh(add_character)
        return (add_character.dict, 201) if refresh else (character, 201)

    def remove_character(self, character_id: int) -> tuple:
        """Validates type of character_id. If not integer - raises a Type Error.
        If character with given id was not found - raises a KeyError.
        Deletes a character and returns a tuple with deleted character and a status code."""
        if not isinstance(character_id, int):
            raise TypeError
        rem_character = self.read_character(character_id, return_object=True)
        if isinstance(rem_character, tuple) and rem_character[1] == 404:
            raise KeyError(rem_character)
        return self._delete(rem_character)

    def update_character(self, character_id, character) -> tuple:
        """Validates type of character_id and character dict. Updates provided 
        character's fields, returns a tuple with an updates user and status code"""
        self._validate_update_character(character_id, character)
        upd_character = self.read_character(character_id, return_object=True)
        if not isinstance(upd_character, Characters):
            return upd_character[0], upd_character[1]
        [setattr(upd_character, key, value) for key, value in character.items()]
        self.session.commit()
        self.session.refresh(upd_character)
        return upd_character.dict, 200

    def __len__(self) -> int:
        """Returns a count of characters in a database"""
        return self.session.query(func.count(Characters.id)).scalar()
        
    def _delete(self, instance) -> tuple:
        """Delete an instance from the database with error handling and rollback.
        Returns a tuple with deleted instance and a status code."""
        instance_dict = instance.dict
        self.session.delete(instance)
        self.session.commit()
        return instance_dict, 200
    
    def _character_exists(self, character_name: str) -> bool:
        """Checks if character with given character_name is present in a database"""
        try:
            self.session.query(Characters).filter_by(name=character_name).one()
            return True
        except exc.NoResultFound:
            return False

    def add_user(self, user: dict, refresh=True) -> tuple:
        """Validates user dict fields and values. If invalid - returns error message
         and a corresponding error code. If valid - add a user and returns created
         user dict with success status code.
         """
        missing_fields = Users.req_fields.difference(set(user.keys()))
        if missing_fields:
            return {'error': f'Missing required field(s): {", ".join(missing_fields)}.'}, 400
        wrong_fields = set(user.keys()).difference(Users.allowed_fields)
        if wrong_fields:
            return {'error': f'Not allowed field(s): {", ".join(wrong_fields)}.'}, 400
        role = user.get('role')
        if not isinstance(user['password'], bytes):
            user['password'] = hash_password(user['password'])
        add_user = Users(username=user['username'],
                         password=user['password'])
        if role:
            add_user.role = role
        try:
            self.session.add(add_user)
            self.session.commit()
            if refresh:
                self.session.refresh(add_user)
            return add_user.dict, 201
        except exc.IntegrityError:
            self.session.rollback()
            return {'error': f'User {user["username"]} already exists.'}, 409

    def read_user(self, user_id) -> tuple:
        """Returns a tuple of user dict and status code or an error message
        and error status code (if user not found).
        """
        return self._get_user_by_id(user_id)

    def read_users(self) -> tuple:
        """Returns a tuple with users' dicts and status code (if user(s) found),
        or with empty list and 404 status code.
        """
        users = self.session.query(Users).all()
        return ([user.dict for user in users], 200) if users else ([], 404)

    def update_user(self, user_id: int, user: dict) -> tuple:
        """Validates user dict, checks if user with given id is present in database,
        returns tuple with an updated user and success code
        or an error message and error's status code.
        """
        wrong_fields = set(user.keys()).difference(Users.allowed_fields)
        if wrong_fields:
            return {'error': f'Not allowed field(s): {", ".join(wrong_fields)}.'}, 400
        db_user = self._get_user_by_id(user_id, return_object=True)
        if isinstance(db_user, tuple):
            return db_user[0], db_user[1]
        if 'role' in user.keys():
            user_role_id = db_user.role_id
        [setattr(db_user, key, value) for key, value in user.items()]
        try:
            self.session.flush()
            if 'role' in user.keys():
                self._check_orphan_user_role(user_role_id)
            self.session.commit()
            self.session.refresh(db_user)
            return db_user.dict, 200
        except exc.IntegrityError:
            return {'error': f'User with name {user["username"]} already exists.'}, 409

    def delete_user(self, user_id: int) -> tuple:
        """Checks if user with given id is present in a database, deletes user,
        returns tuple with a deleted user and status code or an error message
        and an error status code.
        """
        delete_user = self._get_user_by_id(user_id, return_object=True)
        if isinstance(delete_user, tuple):
            return delete_user
        user_dict = delete_user.dict
        user_role_id = delete_user.role_id
        self.session.delete(delete_user)
        self._check_orphan_user_role(user_role_id)
        self.session.commit()
        return user_dict, 200

    def get_user_by_name(self, username: str) -> dict:
        """Returns a dict of a user found by his/her name with included
        hashed user's password.
        """
        db_user = self.session.query(Users).filter_by(username=username).first()
        if not db_user:
            raise KeyError(f'User with username "{username}" was not found.')
        result = db_user.dict
        result.update({'password': db_user.password})
        return result 

    def _get_user_by_id(self, user_id: int, return_object: bool = False) -> tuple | Users:
        """Returns a tuple (user dict and success code) or sqlalchemy Users object
        if user found or a tuple with an error and 404 status code if not.
        """
        try:
            db_user = self.session.query(Users).filter_by(id=user_id).one()
        except exc.NoResultFound:
            return {'error': f'User with id={user_id} was not found.'}, 404
        return db_user if return_object else (db_user.dict, 200)

    def _check_orphan_user_role(self, role_id: int):
        """Checks if user role has no associated users. If not - deletes the role."""
        role = self.session.query(Roles).filter_by(id=role_id).one()
        if not self.session.query(Users).filter_by(role_id=role_id).first():
            self.session.delete(role)
