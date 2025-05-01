from flask import Blueprint, jsonify, request, current_app, g
from utils.security import is_user_credentials_valid, generate_access_token, hash_password, token_required

users_bp = Blueprint('users', __name__)
authentication_bp = Blueprint('auth', __name__)


@authentication_bp.route('/login', methods=['POST'])
def login():
    """Checks for provided login data in payload. If valid returns token with success status code.
    If invalid - error message with error status code (400 or 401).
    """
    username = request.form.get('username')
    password = request.form.get('password')
    if any([username is None, password is None]):
        return jsonify({'error': 'Missing username or password'}), 400
    # username, password = data['username'], data['password']
    if not is_user_credentials_valid(username, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    token_str = generate_access_token(username).json['token']
    token = {'access_token': token_str, 'token_type': 'bearer'}
    return token, 200


@users_bp.route('/', methods=['POST'])
def create_user():
    """Checks provided payload. If valid - creates a new user, returns user data
    (except the password). If invalid - error message with corresponding status code.
    """
    data = request.get_json()
    missing_fields = {'username', 'password'}.difference(set(data.keys()))
    if missing_fields:
        return jsonify({'error': f'Missing required field(s): {", ".join(missing_fields)}.'}), 400

    username, password, role = data['username'], hash_password(data['password']), data.get('role')
    if username.strip() == '':
        return jsonify({'error': 'Username can not be empty.'}), 400
    forbidden_fields = set(data.keys()).difference({'username', 'password', 'role'})
    if forbidden_fields:
        return jsonify({'error': f'Not allowed field(s): {", ".join(forbidden_fields)}.'}), 400
    db_user = current_app.data_manager.add_user(
        {'username': username,
         'password': password,
         'role': role})
    return jsonify(db_user[0]), db_user[1]


@users_bp.route('/me', methods=['DELETE'])
@token_required()
def delete_current_user():
    """Deletes the current user."""
    del_user = current_app.data_manager.delete_user(g.current_user['id'])
    return jsonify(del_user[0]), del_user[1]


@users_bp.route('/me', methods=['GET'])
@token_required()
def read_current_user():
    """Returns the current user's info."""
    db_user = current_app.data_manager.read_user(g.current_user['id'])
    return jsonify(db_user[0]), db_user[1]


@users_bp.route('/me', methods=['PUT'])
@token_required()
def update_current_user():
    """Validates payload. If valid updates current user's info and returns it."""
    data = request.get_json()
    if not any(['username' in data, 'password' in data, 'role' in data]):
        return jsonify({'error': 'None of the fields was provided ("username", "password", "role").'}), 400
    wrong_fields = set(data.keys()).difference({'username', 'password', 'role'})
    if wrong_fields:
        return jsonify({'error': f'Not allowed field(s): {", ".join(wrong_fields)}.'}), 400
    if 'password' in data.keys():
        data['password'] = hash_password(data['password'])
    updated_user = current_app.data_manager.update_user(g.current_user['id'], data)
    return jsonify(updated_user[0]), updated_user[1]


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required(required_role='Regional Manager')
def delete_user(user_id: int):
    """Deletes a user found by user_id. Returns deleted user info with success status code.
    If user not found - returns error message with 404 status code.
    """
    del_user = current_app.data_manager.delete_user(user_id)
    return jsonify(del_user[0]), del_user[1]


@users_bp.route('/<int:user_id>', methods=['GET'])
@token_required(required_role='Regional Manager')
def read_user(user_id: int):
    """Returns user info for a user with a given id. If user not found -
    error message with 404 status code.
    """
    db_user = current_app.data_manager.read_user(user_id)
    return jsonify(db_user[0]), db_user[1]


@users_bp.route('/', methods=['GET'])
@token_required(required_role='Regional Manager')
def read_users():
    """Returns a list of registered users (if any) or empty list with 404 status code."""
    db_users = current_app.data_manager.read_users()
    return jsonify(db_users[0]), db_users[1]


@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required(required_role='Regional Manager')
def update_user(user_id: int):
    """Validates payload. If valid updates and returns user info found by a given user_id.
    If a user not found or payload is invalid - error message with error status code.
    """
    data = request.get_json()
    if not any(['username' in data, 'password' in data, 'role' in data]):
        return jsonify({'error': 'None of the fields was provided ("username", "password", "role").'}), 400
    wrong_fields = set(data.keys()).difference({'username', 'password', 'role'})
    if wrong_fields:
        return jsonify({'error': f'Not allowed field(s): {", ".join(wrong_fields)}.'}), 400
    if 'password' in data.keys():
        data['password'] = hash_password(data['password'])
    updated_user = current_app.data_manager.update_user(user_id, data)
    return jsonify(updated_user[0]), updated_user[1]
