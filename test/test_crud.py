import pytest
from data import JSONDataManager as json_data_manager
from utils.settings import skip_tests


@pytest.mark.skipif(skip_tests['crud_json'], reason='Skipped by config')
def test_json_read_operations(json_db):
    assert isinstance(json_db.read_characters()[0], list), 'Wrong data storage type'
    assert len(json_db.read_characters()[0]) == 20, 'Wrong characters count without set limit'
    assert json_db.read_characters() != json_db.read_characters(), 'Characters not random'
    assert isinstance(json_db.read_character(1), tuple), 'Wrong object type for read_character'
    with pytest.raises(KeyError):
        assert json_db.read_character(101), 'Key error was not raised for character_id > len(characters)'
    assert set(json_db.read_character(1)[0].keys()) == {'id', 'name', 'house', 'animal', 'symbol', 'nickname', 'role', 'age', 'death', 'strength'}, 'Not all character keys were retrieved'
    with pytest.raises(FileNotFoundError):
        json_data_manager('wrong_file.json')


@pytest.mark.skipif(skip_tests['crud_json'], reason='Skipped by config')
def test_json_read_characters_filters(json_db):
    assert all([character['house'] == None for character in json_db.read_characters(char_filter={'house': None})[0]]), 'Filter by house = None'
    assert all([character['house'] == 'Stark' for character in json_db.read_characters(char_filter={'house': 'Stark'})[0]]), 'Filter by house = Stark'
    assert all([character['house'] == 'Stark' for character in json_db.read_characters(char_filter={'house': 'stARk'})[0]]), 'Filter by house = stARk'
    assert all([character['house'] == 'Stark' for character in json_db.read_characters(char_filter={'hoUSe': 'stARk'})[0]]), 'Filter by hoUSe = stARk'
    assert all([character['house'] == 'Stark' for character in json_db.read_characters(char_filter={'hoUSe': 'stARk'})[0]]), 'Filter by hoUSe = tARk'
    with pytest.raises(ValueError):
        json_db.read_characters(char_filter={'planet': 'earth'})
    assert len(json_db.read_characters(char_filter={'age_more_than': 50})[0]) == 8
    assert len(json_db.read_characters(char_filter={'age_more_than': 50, 'age_less_then': 55})[0]) == 3


@pytest.mark.skipif(skip_tests['crud_json'], reason='Skipped by config')
def test_json_read_characters_sorting(json_db, jon_snow, daenerys, olenna_tyrell):
    assert json_db.read_characters(sorting='id')[0][0] == jon_snow
    assert json_db.read_characters(sorting='id', order='sort_asc')[0][0] == jon_snow
    assert json_db.read_characters(sorting='id', order='asc')[0][0] == jon_snow
    assert json_db.read_characters(sorting='id')[0][1] == daenerys
    assert json_db.read_characters(sorting='id', order='desc')[0][0] == olenna_tyrell
    assert json_db.read_characters(sorting='id', order='sort_des')[0][0] == olenna_tyrell
    with pytest.raises(ValueError):
        json_db.read_characters(sorting='family')


@pytest.mark.skipif(skip_tests['crud_json'], reason='Skipped by config')
def test_json_create_operation(json_db, robert_baratheon):
    robert_db = json_db.add_character(robert_baratheon)[0]
    assert len(json_db) == 51, 'Character was not added'
    assert robert_db.get('id'), 'New character does not have "id" key'
    assert robert_db['id'] == 51, 'New character id is wrong'
    assert robert_db.get('nickname') is None, 'Omitted optional field was not created'
    assert robert_db['nickname'] is None, 'Omitted optional field has wrong value'
    with pytest.raises(ValueError):
        json_db.add_character({'id': 55, 'name': 'Mock', 'role': 'Mocker', 'strength': 'Mocking'})
    with pytest.raises(ValueError):
        json_db.add_character({'role': 'Nameless person', 'strength': 'Stealth'})


@pytest.mark.skipif(skip_tests['crud_json'], reason='Skipped by config')
def test_json_delete_operation(json_db, jon_snow):
    assert isinstance(json_db.remove_character(2)[0], dict), 'Remove method returns wrong data type'
    assert len(json_db) == 49, 'Remove method did not reduce amount of characters'
    assert json_db.remove_character(1)[0] == jon_snow, 'Remove method returned wrong data'
    with pytest.raises(KeyError):
        json_db.remove_character(58)
    with pytest.raises(KeyError):
        json_db.remove_character(1)
    with pytest.raises(TypeError):
        json_db.remove_character('1')


@pytest.mark.skipif(skip_tests['crud_json'], reason='Skipped by config')
def test_json_update_operation(json_db, jon_snow, olenna_tyrell):
    assert json_db.update_character(1, {'name': 'Gendalf'})[0]['name'] == 'Gendalf', 'Function returns not updated field'
    jon_snow.update({'name': 'Gendalf'})
    assert json_db.read_character(1)[0] == jon_snow, 'Character was not updated in the database'
    with pytest.raises(AttributeError):
        json_db.update_character(2, {'id': 22}), 'ID update did not raise an error'
    with pytest.raises(AttributeError):
        json_db.update_character(5, {'hair': None}), 'Update with not allowed field'
    with pytest.raises(AttributeError):
        json_db.update_character(11, {'name': olenna_tyrell['name']}), 'Update character name to already existing character name'


@pytest.mark.skipif(skip_tests['crud_json'], reason='Skipped by config')
def test_sql_read_operation(sql_db, jon_snow, daenerys, olenna_tyrell):
    sql_db._reset_database()
    assert len(sql_db.read_characters()[0]) == 20
    assert sql_db.read_characters() != sql_db.read_characters()
    assert sql_db.read_character(1) == (jon_snow, 200)
    assert sql_db.read_character(2) == (daenerys, 200)
    assert sql_db.read_character(50) == (olenna_tyrell, 200)
    assert sql_db.read_characters(limit=50)[0][-1] == olenna_tyrell
    assert isinstance(sql_db.read_characters(), tuple), 'Wrong characters return data type'
    assert len(sql_db.read_characters()[0]) == 20, 'Wrong characters count without set limit'
    assert sql_db.read_characters() != sql_db.read_characters(), 'Characters are not random'
    assert isinstance(sql_db.read_character(1)[0], dict), 'Worng object type for read_character'
    assert sql_db.read_character(101) == ({'error': 'Character with id=101 was not found.'}, 404), 'Key error was not raised for character_id > len(characters)'
    assert set(sql_db.read_character(1)[0].keys()) == {'id', 'name', 'house', 'animal', 'symbol', 'nickname', 'role', 'age', 'death', 'strength'}, 'Not all character keys were retrieved'


@pytest.mark.skipif(skip_tests['crud_sql'], reason='Skipped by config')
def test_sql_read_characters_filters(sql_db):
    sql_db._reset_database()
    assert all([character['house'] is None for character in sql_db.read_characters(char_filter={'house': None})[0]]), 'Filter by house = None'
    assert all([character['house'] == 'Stark' for character in sql_db.read_characters(char_filter={'house': 'Stark'})[0]]), 'Filter by house = Stark'
    assert all([character['house'] == 'Stark' for character in sql_db.read_characters(char_filter={'house': 'stARk'})[0]]), 'Filter by house = stARk'
    assert all([character['house'] == 'Stark' for character in sql_db.read_characters(char_filter={'hoUSe': 'stARk'})[0]]), 'Filter by hoUSe = stARk'
    assert all([character['house'] == 'Stark' for character in sql_db.read_characters(char_filter={'hoUSe': 'stARk'})[0]]), 'Filter by hoUSe = tARk'
    assert all([character['symbol'] is None for character in sql_db.read_characters(char_filter={'sYmbOl': '   '})[0]]), 'Filter by Symbol = None'
    with pytest.raises(ValueError):
        sql_db.read_characters(char_filter={'planet': 'earth'})
    assert len(sql_db.read_characters(char_filter={'age_more_than': 50})[0]) == 8
    assert len(sql_db.read_characters(char_filter={'age_more_than': 50, 'age_less_then': 55})[0]) == 3


@pytest.mark.skipif(skip_tests['crud_sql'], reason='Skipped by config')
def test_sql_read_characters_sorting(sql_db, jon_snow, daenerys, olenna_tyrell):
    sql_db._reset_database()
    assert sql_db.read_characters(sorting='id')[0][0] == jon_snow
    assert sql_db.read_characters(sorting='id', order='sort_asc')[0][0] == jon_snow
    assert sql_db.read_characters(sorting='id', order='asc')[0][0] == jon_snow
    assert sql_db.read_characters(sorting='id')[0][1] == daenerys
    assert sql_db.read_characters(sorting='id', order='desc')[0][0] == olenna_tyrell
    assert sql_db.read_characters(sorting='id', order='sort_des')[0][0] == olenna_tyrell
    with pytest.raises(ValueError):
        sql_db.read_characters(sorting='family')


@pytest.mark.skipif(skip_tests['crud_sql'], reason='Skipped by config')
def test_sql_create_operation(sql_db, robert_baratheon):
    sql_db._reset_database()
    robert_db = sql_db.add_character(robert_baratheon)[0]
    assert len(sql_db) == 51, 'Character was not added'
    assert robert_db.get('id'), 'New character does not have "id" key'
    assert robert_db['id'] == 51, 'New character id is wrong'
    assert robert_db['nickname'] is None, 'Omitted optional field was not created or has wrong value'
    with pytest.raises(ValueError):
        sql_db.add_character({'id': 55, 'name': 'Mock', 'role': 'Mocker', 'strength': 'Mocking'})
    with pytest.raises(ValueError):
        sql_db.add_character({'role': 'Nameless person', 'strength': 'Stealth'})
    with pytest.raises(AttributeError):
        sql_db.add_character(robert_baratheon)


@pytest.mark.skipif(skip_tests['crud_sql'], reason='Skipped by config')
def test_sql_delete_operation(sql_db, jon_snow):
    sql_db._reset_database()
    assert isinstance(sql_db.remove_character(2), tuple), 'Remove method returns wrong data type'
    assert [char['id'] for char in sql_db.read_characters(sorting='id')[0]] == [1] + [i for i in range(3, 51)]
    assert len(sql_db) == 49, 'Remove method did not reduce amount of characters'
    assert sql_db.remove_character(1) == (jon_snow, 200), 'Remove method returned wrong data'
    with pytest.raises(KeyError):
        sql_db.remove_character(58)
    with pytest.raises(KeyError):
        sql_db.remove_character(1)
    with pytest.raises(TypeError):
        sql_db.remove_character('1')


@pytest.mark.skipif(skip_tests['crud_sql'], reason='Skipped by config')
def test_sql_update_operation(sql_db, jon_snow, olenna_tyrell):
    sql_db._reset_database()
    assert sql_db.update_character(1, {'name': 'Gendalf'})[0]['name'] == 'Gendalf', 'Function returns not updated field'
    jon_snow.update({'name': 'Gendalf'})
    assert sql_db.read_character(1)[0] == jon_snow, 'Character was not updated in the database'
    with pytest.raises(AttributeError):
        sql_db.update_character(2, {'id': 22}), 'ID update did not raise an error'
    with pytest.raises(AttributeError):
        sql_db.update_character(5, {'hair': None}), 'Update with not allowed field'
    with pytest.raises(AttributeError):
        sql_db.update_character(22, {'name': olenna_tyrell['name']}), 'Update with not allowed field'
    with pytest.raises(TypeError):
        sql_db.update_character('one', {'name': 'the_first'}), 'Update character with str for id'


@pytest.mark.skipif(skip_tests['crud_sql'], reason='Skipped by config')
def test_sql_user_creation(sql_db):
    assert sql_db.add_user({'username': 'no-password', 'role': 'careless'})[1] == 400, 'Wrong status code for incorrect add user request'
    assert sql_db.add_user({'username': 'no-password', 'role': 'careless'})[0] == {'error': 'Missing required field(s): password.'}, 'Wrong message for incorrect add user request'
    correct_user = sql_db.add_user({'username': 'user', 'password': '12345', 'role': 'careless'})
    assert correct_user[1] == 201, 'Wrong status code for correct add user request'
    assert correct_user[0] == {'username': 'user', 'id': 1, 'role': 'careless'}, 'Wrong return for correct add user request'
    assert sql_db.add_user({'username': 'Rex', 'password': 'T', 'role': 'Dino', 'color': 'green'}) == ({'error': 'Not allowed field(s): color.'}, 400), 'Wrong return for wrong field user creation'
    assert sql_db.add_user({'username': 'user', 'password': '12345', 'role': 'careless'}) == ({'error': 'User user already exists.'}, 409)


@pytest.mark.skipif(skip_tests['crud_sql'], reason='Skipped by config')
def test_sql_read_users(sql_db):
    assert sql_db.read_user(1) == ({'error': 'User with id=1 was not found.'}, 404), 'Wrong return on user not found'
    sql_db.add_user({'username': 'user', 'password': '12345', 'role': 'careless'})
    assert sql_db.read_user(1) == ({'username': 'user', 'role': 'careless', 'id': 1}, 200), 'Wrong return on found user'
    users = sql_db.read_users()
    assert isinstance(users[0], list), 'Wrong return type for read_users sql method'
    assert len(users[0]) == 1, 'Wrong amount of users'
    assert users == ([{'username': 'user', 'role': 'careless', 'id': 1}], 200), 'Wrong return on read_users method'
    
    
@pytest.mark.skipif(skip_tests['crud_sql'], reason='Skipped by config')
def test_sql_update_user(sql_db):
    sql_db._reset_users()
    assert sql_db.update_user(1, {'eye color': 'green'}) == ({'error': 'Not allowed field(s): eye color.'}, 400), 'Wrong return on user update with wrong field'
    assert sql_db.update_user(10, {'password': 'that is what she said'}) == ({'error': 'User with id=10 was not found.'}, 404), 'Wrong return on user not found for update user'
    assert sql_db.update_user(4, {'role': 'Assistant Regional Manager'}) == ({'username': 'Dwight', 'role': 'Assistant Regional Manager', 'id': 4}, 200), 'Wrong return on successful user role change'
    assert sql_db.update_user(3, {'username': 'Michael'}) == ({'error': 'User with name Michael already exists.'}, 409), 'Wrong return on update user name to existing user'


@pytest.mark.skipif(skip_tests['crud_sql'], reason='Skipped by config')
def test_sql_delete_user(sql_db):
    sql_db._reset_users()
    total_users = len(sql_db.read_users()[0])
    assert sql_db.delete_user(3) == ({'username': 'Pam', 'id': 3, 'role': 'Receptionist'}, 200), 'Wrong return on user delete'
    assert len(sql_db.read_users()[0]) == total_users - 1, 'User count did not change after deleting a user'
    assert sql_db.delete_user(88) == ({'error': 'User with id=88 was not found.'}, 404), 'Wrong return on deleting non existing user'
    
    
