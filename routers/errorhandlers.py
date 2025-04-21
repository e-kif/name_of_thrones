from flask import Blueprint, jsonify

errorhandlers_bp = Blueprint('errors', __name__)


@errorhandlers_bp.app_errorhandler(404)
def not_found_error(error):
    return jsonify({'error': str(error)}), 404


@errorhandlers_bp.app_errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': str(error)}), 500
