from flask import Blueprint, jsonify, request, current_app
from utils.security import is_user_credentials_valid, generate_access_token


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
    if any([not data, 'username' not in data, 'password'not in data, 'role' not in data]):
        return jsonify({'error': 'Missing required field(s)'}), 400

    username, password, role = data['username'], data['password'], data['role']
    if username.strip == '' or role.strip() == '':
        return jsonify({'error': 'Username and role can not be empty'}), 400
    forbidden_fields = set(data.keys()).difference({'username', 'password', 'role'})
    if forbidden_fields:
        return jsonify({'error': f'Not allowed field(s): {", ".join(forbidden_fields)}'}), 400
    db_user = current_app.data_manager.add_user(data)
    db_user.pop('password')
    return jsonify(db_user), 201

