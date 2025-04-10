from flask import Blueprint, jsonify, request, current_app
from schemas.characters import CharacterOut

characters_bp = Blueprint('character', __name__)


def db():
    """Helper function that returns current app's data manager"""
    return current_app.data_manager


@characters_bp.route('/', methods=['GET'])
def get_characters():
    characters = db().characters
    if characters:
        return jsonify(characters), 200
    else:
        return jsonify({'error': 'No characters were found'}), 404


@characters_bp.route('/<int:character_id>', methods=['GET'])
def get_character(character_id: int) -> CharacterOut:
    try:
        character = db().read_character(character_id)
        return jsonify(character), 200
    except KeyError as error:
        return jsonify({'error': error.args[0]}), 404


@characters_bp.route('/', methods=['POST'])
def add_character() -> CharacterOut:
    new_character = request.get_json()
    try:
        return db().add_character(new_character), 201
    except ValueError as error:
        return jsonify({'error': error.args[0]}), 400


@characters_bp.route('/<int:character_id>', methods=['DELETE'])
def remove_character(character_id: int) -> CharacterOut:
    try:
        removed_character = db().remove_character(character_id)
        return jsonify({'removed character': removed_character}), 200
    except KeyError as error:
        return jsonify({'error': error.args[0]}), 404


@characters_bp.route('/<int:character_id>', methods=['PUT'])
def update_character(character_id: int) -> CharacterOut:
    updated_character = request.get_json()
    try:
        db_character = db().update_character(updated_character)
        return db_character
    except ValueError as error:
        return jsonify({'error': error.args[0]}), 404
    except AttributeError as error:
        return jsonify({'error': error.args[0]}), 400
