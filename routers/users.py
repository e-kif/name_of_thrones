from flask import Blueprint, jsonify, request, current_app
from utils.security import is_user_credentials_valid, generate_access_token, hash_password


users_bp = Blueprint('users', __name__)
authentication_bp = Blueprint('auth', __name__)


@authentication_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if any([not data, 'username' not in data, 'password' not in data]):
        return jsonify({'error': 'Missing username or password'}), 400
    
    username, password = data['username'], data['password']
    
    if not is_user_credentials_valid(username, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    return generate_access_token(username), 200
   

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if any([not data, 'username' not in data, 'password'not in data]):
        return jsonify({'error': 'Missing required field(s)'}), 400

    username, password, role = data['username'], hash_password(data['password']), data.get('role')
    if username.strip == '':
        return jsonify({'error': 'Username can not be empty'}), 400
    forbidden_fields = set(data.keys()).difference({'username', 'password', 'role'})
    if forbidden_fields:
        return jsonify({'error': f'Not allowed field(s): {", ".join(forbidden_fields)}'}), 400
    db_user = current_app.data_manager.add_user(
        {'username': username,
        'password': password,
        'role': role})
    return jsonify(db_user[0]), db_user[1]


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    delete_user = current_app.data_manager.delete_user(user_id)
    return jsonify(delete_user[0]), delete_user[1]

