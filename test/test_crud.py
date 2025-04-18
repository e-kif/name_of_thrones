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


def test_json_read_characters_filters():
    assert all([character['house'] == None for character in json_db().read_characters(filter={'house': None})]), 'Filter by house = None'
    assert all([character['house'] == 'Stark' for character in json_db().read_characters(filter={'house': 'Stark'})]), 'Filter by house = Stark'
    assert all([character['house'] == 'Stark' for character in json_db().read_characters(filter={'house': 'stARk'})]), 'Filter by house = stARk'
    assert all([character['house'] == 'Stark' for character in json_db().read_characters(filter={'hoUSe': 'stARk'})]), 'Filter by hoUSe = stARk'
    assert all([character['house'] == 'Stark' for character in json_db().read_characters(filter={'hoUSe': 'stARk'})]), 'Filter by hoUSe = tARk'
    with pytest.raises(ValueError):
        json_db().read_characters(filter={'planet': 'earth'})
    assert len(json_db().read_characters(filter={'age_more_than': 50})) == 8
    assert len(json_db().read_characters(filter={'age_more_than': 50, 'age_less_then': 55})) == 3


def test_json_read_characters_sorting(jon_snow, daenerys, olenna_tyrell):
    assert json_db().read_characters(sorting='id')[0] == jon_snow
    assert json_db().read_characters(sorting='id', order='sort_asc')[0] == jon_snow
    assert json_db().read_characters(sorting='id', order='asc')[0] == jon_snow
    assert json_db().read_characters(sorting='id')[1] == daenerys
    assert json_db().read_characters(sorting='id', order='desc')[0] == olenna_tyrell
    assert json_db().read_characters(sorting='id', order='sort_des')[0] == olenna_tyrell
    with pytest.raises(ValueError):
        json_db().read_characters(sorting='family')


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


def test_sql_read_operation(sql_db, jon_snow, daenerys, olenna_tyrell):
    assert len(sql_db.read_characters()) == 20
    assert sql_db.read_characters() != sql_db.read_characters()
    assert sql_db.read_character(1) == jon_snow
    assert sql_db.read_character(2) == daenerys
    assert sql_db.read_character(50) == olenna_tyrell
    assert sql_db.read_characters(limit=50)[-1] == olenna_tyrell
    assert isinstance(sql_db.read_characters(), list), 'Wrong data storage type'
    assert len(sql_db.read_characters()) == 20, 'Wrong characters count without set limit'
    assert sql_db.read_characters() != sql_db.read_characters(), 'Characters not random'
    assert isinstance(sql_db.read_character(1), dict), 'Worng object type for read_character'
    assert sql_db.read_character(101) == ({'error': 'Character with id=101 was not found.'}, 404), 'Key error was not raised for character_id > len(characters)'
    assert set(sql_db.read_character(1).keys()) == {'id', 'name', 'house', 'animal', 'symbol', 'nickname', 'role', 'age', 'death', 'strength'}, 'Not all character keys were retrieved'


def test_sql_read_characters_filters(sql_db):
    sql_db._reset_database()
    assert all([character['house'] == None for character in sql_db.read_characters(filter={'house': None})]), 'Filter by house = None'
    assert all([character['house'] == 'Stark' for character in sql_db.read_characters(filter={'house': 'Stark'})]), 'Filter by house = Stark'
    assert all([character['house'] == 'Stark' for character in sql_db.read_characters(filter={'house': 'stARk'})]), 'Filter by house = stARk'
    assert all([character['house'] == 'Stark' for character in sql_db.read_characters(filter={'hoUSe': 'stARk'})]), 'Filter by hoUSe = stARk'
    assert all([character['house'] == 'Stark' for character in sql_db.read_characters(filter={'hoUSe': 'stARk'})]), 'Filter by hoUSe = tARk'
    with pytest.raises(ValueError):
        sql_db.read_characters(filter={'planet': 'earth'})
    assert len(sql_db.read_characters(filter={'age_more_than': 50})) == 8
    assert len(sql_db.read_characters(filter={'age_more_than': 50, 'age_less_then': 55})) == 3


def test_sql_read_characters_sorting(sql_db, jon_snow, daenerys, olenna_tyrell):
    assert sql_db.read_characters(sorting='id')[0] == jon_snow
    assert sql_db.read_characters(sorting='id', order='sort_asc')[0] == jon_snow
    assert sql_db.read_characters(sorting='id', order='asc')[0] == jon_snow
    assert sql_db.read_characters(sorting='id')[1] == daenerys
    assert sql_db.read_characters(sorting='id', order='desc')[0] == olenna_tyrell
    assert sql_db.read_characters(sorting='id', order='sort_des')[0] == olenna_tyrell
    with pytest.raises(ValueError):
        sql_db.read_characters(sorting='family')


def test_sql_create_operation(sql_db, robert_baratheon):
    robert_db = sql_db.add_character(robert_baratheon)
    assert len(sql_db) == 51, 'Character was not added'
    assert getattr(robert_db, 'id'), 'New character does not have "id" key'
    assert robert_db.id == 51, 'New character id is wrong'
    assert robert_db.nickname is None, 'Omitted optional field was not created'
    assert robert_db.nickname is None, 'Omitted optional field has wrong value'
    with pytest.raises(ValueError):
        sql_db.add_character({'id': 55, 'name': 'Mock', 'role': 'Mocker', 'strength': 'Mocking'})
    with pytest.raises(ValueError):
        sql_db.add_character({'role': 'Nameless person', 'strength': 'Stealth'})


def test_sql_delete_operation(sql_db, jon_snow):
    assert isinstance(sql_db.remove_character(2), dict), 'Remove method returns wrong data type'
    assert len(sql_db) == 49, 'Remove method did not reduce amount of characters'
    assert sql_db.remove_character(1) == jon_snow, 'Remove method returned wrong data'
    with pytest.raises(KeyError):
        sql_db.remove_character(58)
    with pytest.raises(KeyError):
        sql_db.remove_character(1)
    with pytest.raises(TypeError):
        sql_db.remove_character('1')


def test_sql_update_operation(sql_db, jon_snow):
    assert sql_db.update_character(1, {'name': 'Gendalf'})['name'] == 'Gendalf', 'Function returns not updated field'
    jon_snow.update({'name': 'Gendalf'})
    assert sql_db.read_character(1) == jon_snow, 'Character was not updated in the database'
    with pytest.raises(AttributeError):
        sql_db.update_character(2, {'id': 22}), 'ID update did not raise an error'
    with pytest.raises(AttributeError):
        sql_db.update_character(5, {'hair': None}), 'Update with not allowed field'
