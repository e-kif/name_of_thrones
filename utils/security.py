import os
import jwt
import datetime
import bcrypt
import json
from flask import request, jsonify, current_app
from functools import wraps
from utils.settings import use_sql_database


def token_required(endpoint_function):
    """Decorator middleware for checking JWT. Valid token should be provided
    in request's header: 'Authorization': 'Bearer {token}'"""    
    @wraps(endpoint_function)
    def wrapper(*args, **kwargs):
        token = None
        
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        
        if not token:
            return jsonify({'error': 'Authenification failed: no token provided.'}), 401

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = get_user_by_name(payload['username'])
            if not current_user:
                raise Exception('User not found.')
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid.'}), 401

        return endpoint_function(*args, **kwargs)
    return wrapper


def get_users(users_file: str = os.path.join('storage', 'users.json'),
              use_sql: bool = use_sql_database) -> list[dict]:
    """Reads users from a json file or from a database"""
    if use_sql:
        users = current_app.data_manager.get_users()
        return users
    with open(users_file, 'r', encoding='utf8') as file:
        return json.loads(file.read())
    

def get_user_by_name(username: str, use_sql: bool = use_sql_database) -> dict:
    """Returns user dict found by username in users.json file or in database.
    If user not found - raises KeyError"""
    if use_sql:
        db_user = current_app.data_manager.get_user_by_name(username)
        return db_user
    users = get_users()
    for user in users:
        if user['username'].lower() == username.lower():
            return user
    raise KeyError(f'User with username {username} was not found.')


def is_user_credentials_valid(username: str, password: str) -> bool:
    """Returns True if both username and password are valid,
    otherwise - False"""
    user = get_user_by_name(username)
    return bcrypt.checkpw(password.encode(), user['password']) if use_sql_database\
            else password == user['password']

def generate_access_token(username: str, exp_minutes: int = 30):
    """Generates JWT access token with encoded username, role and expiration time"""
    user = get_user_by_name(username)
    token_payload = {
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=exp_minutes)
    }
    token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))

