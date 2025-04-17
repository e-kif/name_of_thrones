from flask import Blueprint, jsonify, request, current_app


database_bp = Blueprint('database', __name__)


def db():
    """Helper function that returns current app's data manager"""
    return current_app.data_manager


@database_bp.route('/reset', methods=['GET'])
def reset_database():
    db()._reset_database()
    return jsonify({'message': 'Database was reset successfuly.'}), 200
