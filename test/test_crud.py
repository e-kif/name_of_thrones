import pytest
from data.json_data_manager import JSONDataManager as json_db


def test_json_read_operations():
    assert isinstance(json_db().read_characters(), list), 'Wrong data storage type'
    assert len(json_db().read_characters()) == 20, 'Wrong characters count without set limit'
    assert json_db().read_characters() != json_db().read_characters(), 'Characters not random'
    assert isinstance(json_db().read_character(1), dict), 'Worng object type for read_character'
    with pytest.raises(KeyError):
        assert json_db().read_character(101), 'Key error was not raised for character_id > len(characters)'
    assert set(json_db().read_character(1).keys()) == {'id', 'name', 'house', 'animal', 'symbol', 'nickname', 'role', 'age', 'death', 'strength'}, 'Not all character keys were retrieved'
    with pytest.raises(FileNotFoundError):
        json_db('wrong_file.json')


def test_json_create_operation(robert_baratheon):
    db = json_db()
    robert_db = db.add_character(robert_baratheon)
    assert len(db) == 51, 'Character was not added'
    assert robert_db.get('id'), 'New character does not have "id" key'
    assert robert_db['id'] == 51, 'New character id is wrong'
    assert robert_db.get('nickname') is None, 'Omitted optional field was not created'
    assert robert_db['nickname'] is None, 'Omitted optional field has wrong value'
    with pytest.raises(ValueError):
        db.add_character({'id': 55, 'name': 'Mock', 'role': 'Mocker', 'strength': 'Mocking'})
    with pytest.raises(ValueError):
        db.add_character({'role': 'Nameless person', 'strength': 'Stealth'})


def test_json_delete_operation(jon_snow):
    db = json_db()
    assert isinstance(db.remove_character(2), dict), 'Remove method returns wrong data type'
    assert len(db) == 49, 'Remove method did not reduce amount of characters'
    assert db.remove_character(1) == jon_snow, 'Remove method returned wrong data'
    with pytest.raises(KeyError):
        db.remove_character(58)
    with pytest.raises(KeyError):
        db.remove_character(1)
    with pytest.raises(TypeError):
        db.remove_character('1')


def test_json_update_operation(jon_snow):
    db = json_db()
    assert db.update_character(1, {'name': 'Gendalf'})['name'] == 'Gendalf', 'Function returns not updated field'
    jon_snow.update({'name': 'Gendalf'})
    assert db.read_character(1) == jon_snow, 'Character was not updated in the database'
    with pytest.raises(AttributeError):
        db.update_character(2, {'id': 22}), 'ID update did not raise an error'
    with pytest.raises(AttributeError):
        db.update_character(5, {'hair': None}), 'Update with not allowed field'
