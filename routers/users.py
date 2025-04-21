from flask import Blueprint, jsonify, request
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
    
