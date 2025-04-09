import pytest
from data.json_data_manager import JSONDataManager as json_db


def test_json_read_operations():
    assert isinstance(json_db().read_characters(), list), 'Wrong data storage type'
    assert not isinstance(json_db().read_characters(), str), 'Wrong data storage type'
    assert len(json_db().read_characters()) == 50, 'Not all characters were retrieved'
    assert json_db().read_characters() == json_db().characters, 'Getter characters error'
    assert isinstance(json_db().read_character(1), dict), 'Worng object type for read_character'
    assert json_db().read_character(1)['name'] == 'Jon Snow', 'Wrong character name for character_id=1'
    assert json_db().read_character(2)['name'] == 'Daenerys Targaryen', 'Wrong character name for character_id=2'
    assert json_db().read_character(50)['name'] == 'Olenna Tyrell', 'Wrong character name for character_id=50'
    assert json_db().read_character(1) == {
                                            'id': 1,
                                            'name': 'Jon Snow',
                                            'house': 'Stark',
                                            'animal': 'Direwolf',
                                            'symbol': 'Wolf',
                                            'nickname': 'King in the North',
                                            'role': 'King',
                                            'age': 25,
                                            'death': None,
                                            'strength': 'Physically strong'
                                        }, 'Wrong data for read_character(1)'
    assert json_db().read_character(2) == {
                                            'id': 2,
                                            'name': 'Daenerys Targaryen',
                                            'house': 'Targaryen',
                                            'animal': 'Dragon',
                                            'symbol': 'Dragon',
                                            'nickname': 'Mother of Dragons',
                                            'role': 'Queen',
                                            'age': 24,
                                            'death': 8,
                                            'strength': 'Cunning'
                                        }, 'Wrong data for read_character(2)'
    with pytest.raises(KeyError):
        assert json_db().read_character(101), 'Key error was not raised for character_id > len(characters)'
    assert set(json_db().read_character(1).keys()) == {'id', 'name', 'house', 'animal', 'symbol', 'nickname', 'role', 'age', 'death', 'strength'}, 'Not all character keys were retrieved'


def test_json_create_operation():
    robert_dict = {
        'name': 'Robert Baratheon',
        'house': 'Baratheon',
        'animal': 'Stag',
        'symbol': 'Crowned Stag',
        'role': 'Lord of the Seven Kingdoms',
        'age': 36,
        'death': 1,
        'strength': 'Immense physical strength'
    }
    db = json_db()
    robert_db = db.add_character(robert_dict)
    assert len(db) == 51, 'Character was not added'
    assert robert_db.get('id'), 'New character does not have "id" key'
    assert robert_db['id'] == 51, 'New character id is wrong'
    assert robert_db.get('nickname') is None, 'Omitted optional field was not created'
    assert robert_db['nickname'] is None, 'Omitted optional field has wrong value'
    with pytest.raises(ValueError):
        db.add_character({'id': 55, 'name': 'Mock', 'role': 'Mocker', 'strength': 'Mocking'})
    with pytest.raises(ValueError):
        db.add_character({'role': 'Nameless person', 'strength': 'Stealth'})
