from flask import Blueprint, jsonify, current_app
from utils.security import token_required

database_bp = Blueprint('database', __name__)


# @token_required
@database_bp.route('/reset', methods=['GET'])
@token_required(required_role='Regional Manager')
def reset_database():
    """Resets whole database to predefined by json files characters and users"""
    current_app.data_manager._reset_database()
    return jsonify({'message': 'Database was reset successfully.'}), 200
