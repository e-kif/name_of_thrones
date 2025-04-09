from flask import Blueprint, jsonify, request
from data.json_data_manager import JSONDataManager as json_db

characters_bp = Blueprint('character', __name__)


@characters_bp.route('/', methods=['GET'])
def get_characters():
    return json_db().characters


@characters_bp.route('/<int:character_id>', methods=['GET'])
def get_character(character_id):
    return json_db().read_character(character_id)
