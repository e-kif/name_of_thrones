from flask import Blueprint, jsonify, request, current_app
from schemas.characters import CharacterOut

characters_bp = Blueprint('character', __name__)


def db():
    """Helper function that returns current app's data manager"""
    return current_app.data_manager


@characters_bp.route('/', methods=['GET'])
def get_characters():
    limit, skip, sorting = request.args.get('limit'), request.args.get('skip'), request.args.get('sorting')
    character_keys = {'name', 'house', 'animal', 'symbol', 'nickname', 'role', 'age', 'death', 'strength'}
    filter_keys = character_keys.difference({'age', 'death'})
    sort_values = character_keys.union({'id'})
    filter = {key.lower(): value for key, value in request.args.items() if key.lower() in filter_keys}
    try:
        [filter.update({key: int(value)}) for key, value in request.args.items()
         if key in {'age', 'age_more_than', 'age_less_then', 'death', 'age_less_than'} and value.strip() != '']
        [filter.update({key: None}) for key, value in request.args.items() if value.strip() == '']
    except ValueError:
        return jsonify({'error': 'Age or/and death should be an integer.'}), 400
    [filter.update({key: None}) for key, value in filter.items() if value == '']
    order = request.args.get('order')
    if sorting and sorting not in sort_values:
        return jsonify({'error': f'Wrong sorting parameter {sorting}.'}), 400
    
    try:
        limit, skip = int(limit) if limit else None, int(skip) if skip else None
    except ValueError:
        return jsonify({'error': 'Limit and skip parameters should be integers.'}), 400
    try:
        characters = db().read_characters(limit=limit, skip=skip,
                                          filter=filter,
                                          sorting=sorting, order=order)
    except IndexError:
        return jsonify({'error': 'There are no results for given limit and skip parameters.'}), 404
    except AttributeError as error:
        return jsonify({'error': str(error)}), 409
    if characters:
        return jsonify(characters), 200
    else:
        return jsonify([]), 404


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
        db_character = db().update_character(character_id, updated_character)
        return db_character
    except KeyError as error:
        return jsonify({'error': error.args[0]}), 404
    except AttributeError as error:
        return jsonify({'error': error.args[0]}), 400
