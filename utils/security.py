import jwt
import datetime
import bcrypt
from flask import request, jsonify, current_app
from functools import wraps


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
            return jsonify({'error': 'Authentication failed: no token provided.'}), 401

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_app.data_manager.get_user_by_name(payload['username'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid.'}), 401
        except KeyError as error:
            return jsonify({'error': error.args[0]}), 404

        return endpoint_function(*args, **kwargs)

    return wrapper


def is_user_credentials_valid(username: str, password: str) -> bool:
    """Returns True if both username and password are valid,
    otherwise - False"""
    user = current_app.data_manager.get_user_by_name(username)
    return bcrypt.checkpw(password.encode(), user['password']) if current_app.config['USE_SQL'] \
        else password == user['password']


def generate_access_token(username: str, exp_minutes: int = 30):
    """Generates JWT access token with encoded username, role and expiration time"""
    user = current_app.data_manager.get_user_by_name(username)
    token_payload = {
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=exp_minutes)
    }
    token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
