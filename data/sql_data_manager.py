from sqlalchemy import exc, desc
from sqlalchemy.sql import func
from data.data_manager import DataManager
from models.characters import *
from models.users import Users, Roles
from data.json_data_manager import JSONDataManager


class SQLDataManager(DataManager):

    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.session = self.db.session

    def _reset_database(self):
        """Drops all tables, creates them and loads characters from json file"""
        json_characters = JSONDataManager().read_characters(limit=50)[0]
        self.db.drop_all()
        self.db.create_all()
        for character in json_characters:
            del character['id']
            self.add_character(character, refresh=False)

    def read_character(self, character_id: int, return_object=False):
        """Returns a character with id = character_id or an error message
        if character was not found
        """
        try:
            db_character = self.session.query(Characters)\
                .filter_by(id=character_id).one()
            return db_character if return_object else (db_character.dict, 200)
        except exc.NoResultFound:
            return {'error': f'Character with id={character_id} was not found.'}, 404

    def read_characters(self, limit: int = None, skip: int = None,
                        filter: dict = None, sorting: str = None, order: str = None):
        if all([limit is None, sorting is None, not filter, order is None]):
            return self._read_random_n_characters(20), 200

        query = self.session.query(Characters)
        if filter:
            query = self._apply_filter(query, filter)
        if sorting:
            query = self._apply_sorting(query, sorting, order)
        if limit:
            query = self._apply_pagination(query, limit, skip)
        characters = query.all()
        return ([character.dict for character in characters], 200) if characters else ([], 404)
    
    @staticmethod
    def _apply_filter(query, filter, model=Characters):
        allowed_filter_fields = model.allowed_fields.union({'age_less_than', 'age_less_then', 'age_more_than'})
        for key, value in filter.items():
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
    
    @staticmethod
    def _apply_sorting(query, sorting, order, model = Characters):
        sort_properties = model.allowed_fields.union({'id'})
        if sorting not in sort_properties:
            raise ValueError(f'Wrong sorting parameter provided: {sorting}.')
        if order in {'desc', 'sort_des'}:
            return query.order_by(desc(getattr(Characters, sorting)))
        return query.order_by(getattr(Characters, sorting))
    
    @staticmethod
    def _apply_pagination(query, limit, skip, model=Characters):
        if limit and skip:
            skip = limit * skip
            if skip > query.order_by(None).with_entities(func.count(model.id)).scalar():
                raise IndexError
        return query.limit(limit).offset(skip)

    def _read_random_n_characters(self, n: int):
        """Returns random n characters ordered by id. If n >= character count in database -
        returns all database characters"""
        character_amount = len(self)
        n = n if n < character_amount else character_amount
        characters = self.session.query(Characters).order_by(func.random()).limit(n).all()
        return sorted([character.dict for character in characters], key=lambda char: char['id'])

    def add_character(self, character: dict, refresh: bool = True):
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

        character_req = {key: value for key, value in character.items()\
                         if value is not None and key in Characters.req_fields}
        character_opt = {key: value for key, value in character.items()\
                         if value is not None and key in Characters.opt_fields}
        add_character = Characters(**character_req)
        try:
            self.session.add(add_character)
            self.session.flush()
            if character_opt:
                [setattr(add_character, key, value) for key, value in character_opt.items()]
            self.session.commit()
            if refresh:
                self.session.refresh(add_character)
            return (add_character.dict, 201) if refresh else (character, 201)
        except exc.IntegrityError as error:
            self.session.rollback()
            return {'message': 'Integrity error occurred.', 'error': str(error)}, 409
        except exc.SQLAlchemyError as error:
            self.session.rollback()
            return {'message': f'A database error occurred.', 'error': str(error)}, 500

    def remove_character(self, character_id):
        if not isinstance(character_id, int):
            raise TypeError
        rem_character = self.read_character(character_id, return_object=True)
        if isinstance(rem_character, tuple) and rem_character[1] == 404:
            raise KeyError(rem_character)
        return self._delete(rem_character)

    def update_character(self, character_id, character):
        wrong_fields = set(character.keys()).difference(Characters.allowed_fields)
        if 'id' in wrong_fields:
            raise AttributeError('Updating ID field is not allowed.')
        if wrong_fields:
            raise AttributeError(f'Not allowed filed(s): {", ".join(wrong_fields.difference({"id"}))}.')
        if self._character_exists(character.get('name')):
            raise AttributeError(f'Character {character["name"]} already exists.')
        upd_character = self.read_character(character_id, return_object=True)
        if not isinstance(upd_character, Characters):
            return upd_character[0], 400
        [setattr(upd_character, key, value) for key, value in character.items()]
        try:
            self.session.commit()
            self.session.refresh(upd_character)
        except exc.IntegrityError:
            self.session.rollback()
            raise exc.IntegrityError
        return upd_character.dict, 200

    def __len__(self):
        return self.session.query(func.count(Characters.id)).scalar()
        
    def _delete(self, instance):
        """Delete an instance from the database with error handling and rollback"""
        instance_dict = instance.dict
        try:
            self.session.delete(instance)
            self.session.commit()
        except exc.SQLAlchemyError as error:
            self.session.rollback()
            return {'message': 'A database error occurred.', 'error': str(error)}, 500
        return instance_dict, 200
    
    def _character_exists(self, character_name: str) -> bool:
        try:
            character = self.session.query(Characters).filter_by(name=character_name).one()
            return True
        except exc.NoResultFound:
            return False

    def add_user(self, user: dict):
        missing_fields = Users.req_fields.difference(set(user.keys()))
        if missing_fields:
            return {'error': f'Missing required field(s): {", ".join(missing_fields)}.'}, 400
        wrong_fields = set(user.keys()).difference(Users.allowed_fields)
        if wrong_fields:
            return {'error': f'Not allowed field(s): {", ".join(wrong_fields)}.'}, 400
        role = user.get('role')
        add_user = Users(username=user['username'],
                         password=user['password'])
        if role:
            add_user.role = role
        try:
            self.session.add(add_user)
            self.session.commit()
            self.session.refresh(add_user)
            return add_user.dict, 201
        except exc.IntegrityError as e:
            self.session.rollback()
            return {'error': f'User {user["username"]} already exists.'}, 409

    def read_user(self, user_id):
        return self._get_user_by_id(user_id)

    def read_users(self):
        users = self.session.query(Users).all()
        return [user.dict for user in users], 200 if users else 404

    def update_user(self, user_id, user):
        pass

    def delete_user(self, user_id):
        delete_user = self._get_user_by_id(user_id, return_object=True)
        if isinstance(delete_user, tuple):
            return delete_user
        user_dict = delete_user.dict
        user_role = self.session.query(Roles).filter_by(id=delete_user.role_id).one()
        try:
            self.session.delete(delete_user)
            if not self.session.query(Users).filter_by(role_id=user_role.id).first():
                self.session.delete(user_role)
            self.session.commit()
            return user_dict, 200
        except exc.IntegrityError as error:
            self.session.rollback()
            return {'error': 'Database error'}, 500

    def _get_user_by_id(self, user_id, return_object=False):
        try:
            db_user = self.session.query(Users).filter_by(id=user_id).one()
            return db_user if return_object else (db_user.dict, 200)
        except exc.NoResultFound:
            return {'error': f'User with id={user_id} was not found.'}, 404
