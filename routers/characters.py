from flask import Blueprint, jsonify, request
from data.json_data_manager import JSONDataManager as json_db
from schemas.characters import CharacterInOpt, CharacterOut

characters_bp = Blueprint('character', __name__)

db = json_db()


@characters_bp.route('/', methods=['GET'])
def get_characters():
    return db.characters, 200


@characters_bp.route('/<int:character_id>', methods=['GET'])
def get_character(character_id: int) -> CharacterOut:
    return db.read_character(character_id), 200


@characters_bp.route('/', methods=['POST'])
def add_character() -> CharacterOut:
    new_character = request.get_json()
    return db.add_character(new_character), 201


@characters_bp.route('/<int:charter_id>', methods=['DELETE'])
def remove_character(character_id: int) -> CharacterOut:
    removed_character = db.remove_character(character_id)
    return removed_character


@characters_bp.route('/<int:character_id>', methods=['PUT'])
def update_character(character_id: int) -> CharacterOut:
    updated_character = request.get_json()
    db_character = db.update_character(updated_character)
    return db_character
    