from flask import Blueprint, jsonify, request
from data.json_data_manager import JSONDataManager as json_db
from schemas.characters import CharacterInOpt, CharacterOut

characters_bp = Blueprint('character', __name__)


@characters_bp.route('/', methods=['GET'])
def get_characters():
    return json_db().characters, 200


@characters_bp.route('/<int:character_id>', methods=['GET'])
def get_character(character_id):
    return json_db().read_character(character_id), 200


@characters_bp.route('/', methods=['POST'])
def add_character() -> CharacterOut:
    new_character = request.get_json()
    return json_db().add_character(new_character), 201
