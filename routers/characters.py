from flask import Blueprint, jsonify, request, current_app
from schemas.characters import CharacterOut
from utils.security import token_required

characters_bp = Blueprint('character', __name__)


def db():
    """Helper function that returns current app's data manager"""
    return current_app.data_manager


@characters_bp.route('/', methods=['GET'])
def get_characters():
    """Returns characters with applied filtering, sorting and pagination.
    If no filter, sorting, pagination parameters provided: returns a list
    of random 20 characters ordered by id.
    """
    limit, skip, sorting = request.args.get('limit'), request.args.get('skip'), request.args.get('sorting')
    character_keys = {'name', 'house', 'animal', 'symbol', 'nickname', 'role', 'age', 'death', 'strength'}
    filter_keys = character_keys.difference({'age', 'death'})
    sort_values = character_keys.union({'id'})
    char_filter = {key.lower(): value for key, value in request.args.items() if key.lower() in filter_keys}
    try:
        [char_filter.update({key: int(value)}) for key, value in request.args.items()
         if key in {'age', 'age_more_than', 'age_less_then', 'death', 'age_less_than'} and value.strip() != '']
        [char_filter.update({key: None}) for key, value in request.args.items() if value.strip() == '']
    except ValueError:
        return jsonify({'error': 'Age or/and death should be an integer.'}), 400
    [char_filter.update({key: None}) for key, value in char_filter.items() if value == '']
    order = request.args.get('order')
    if sorting and sorting not in sort_values:
        return jsonify({'error': f'Wrong sorting parameter {sorting}.'}), 400
    
    try:
        limit, skip = int(limit) if limit else None, int(skip) if skip else None
    except ValueError:
        return jsonify({'error': 'Limit and skip parameters should be integers.'}), 400
    try:
        characters = db().read_characters(limit=limit, skip=skip,
                                          filter=char_filter,
                                          sorting=sorting, order=order)
    except IndexError:
        return jsonify({'error': 'There are no results for given limit and skip parameters.'}), 404
    if characters[0]:
        return jsonify(characters[0]), characters[1]
    else:
        return jsonify([]), 404


@characters_bp.route('/<int:character_id>', methods=['GET'])
def get_character(character_id: int):
    """Returns a character by its id. If character not found - 404 error."""
    try:
        character = db().read_character(character_id)
        return jsonify(character[0]), character[1]
    except KeyError as error:
        return jsonify({'error': error.args[0]}), 404


@characters_bp.route('/', methods=['POST'])
@token_required
def add_character():
    """Adds a new character to the application"""
    new_character = request.get_json()
    try:
        db_character = db().add_character(new_character)
        return jsonify(db_character[0]), db_character[1]
    except ValueError as error:
        return jsonify({'error': error.args[0]}), 400
    except AttributeError as error:
        return jsonify({'error': error.args[0]}), 409


@characters_bp.route('/<int:character_id>', methods=['DELETE'])
@token_required
def remove_character(character_id: int):
    """Deletes a character with given id from the application.
    If a character wasn't found - 404 error.
    """
    try:
        removed_character = db().remove_character(character_id)
        return jsonify(removed_character[0]), removed_character[1]
    except KeyError as error:
        return jsonify({'error': error.args[0]}), 404


@characters_bp.route('/<int:character_id>', methods=['PUT'])
@token_required
def update_character(character_id: int):
    """Updates a character with a given id with new data, provided in a payload.
    If a character was not found or invalid payload - returns error.
    """
    updated_character = request.get_json()
    try:
        db_character = db().update_character(character_id, updated_character)
        return db_character[0], db_character[1]
    except KeyError as error:
        return jsonify({'error': error.args[0]}), 400
    except AttributeError as error:
        return jsonify({'error': error.args[0]}), 400
