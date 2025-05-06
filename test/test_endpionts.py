import pytest
from utils.settings import skip_tests
from utils.security import generate_access_token


@pytest.mark.skipif(skip_tests['routes_json'], reason='Skipped by config')
def test_read_characters_json(json_client, jon_snow, daenerys, olenna_tyrell):
    random20 = json_client.get('/characters/', follow_redirects=True)
    assert random20.status_code == 200, 'Endpoint returns wrong status code'
    assert len(random20.json) == 20, 'Wrong character cont for empty limit and skip parameters'
    first10 = json_client.get('/characters/?limit=10')
    assert len(first10.json) == 10, 'Wrong character amount for limit=10'
    assert first10.json[0] == jon_snow, 'wrong first character'
    assert first10.json[1] == daenerys, 'wrong second character'
    for i in range(1, 51):
        assert len(json_client.get(f'/characters/?limit={i}').json) == i
    wrong_limit = json_client.get('/characters/?limit=3.4')
    assert wrong_limit.status_code == 400, 'Wrong status code for limit parameter wrong type'
    assert wrong_limit.json == {'error': 'Limit and skip parameters should be integers.'}
    characters11_20 = json_client.get('/characters/?limit=10&skip=1')
    characters31_40 = json_client.get('/characters/?limit=10&skip=3')
    assert len(characters11_20.json) == 10, 'Wrong characters amount on page two'
    for i in range(10):
        assert characters11_20.json[i]['id'] == i + 11, 'Wrong character id for page 2'
        assert characters31_40.json[i]['id'] == i + 31, 'Wrong character id for page 4'
    out_of_range = json_client.get('/characters/?limit=20&skip=3')
    assert out_of_range.status_code == 404, 'Wrong status code for out of range limit+skip'
    assert out_of_range.json == {'error': 'There are no results for given limit and skip parameters.'}, 'Wrong message for out of range error'
    last10 = json_client.get('/characters/?limit=20&skip=2')
    assert last10.status_code == 200
    assert len(last10.json) == 10, 'Amount of remaining characters is wrong'
    assert last10.json[-1] == olenna_tyrell, 'Last character is wrong'
    wrong_age_filter_value_type = json_client.get('/characters/?age=twelve')
    assert wrong_age_filter_value_type.status_code == 400, 'Wrong status code for wrong age filter value type'
    assert wrong_age_filter_value_type.json == {'error': 'Age or/and death should be an integer.'}, 'Wrong message for wrong age filter value type'
    wrong_death_filter_value_type = json_client.get('/characters/?age=seven')
    assert wrong_death_filter_value_type.status_code == 400, 'Wrong status code for wrong death filter value type'
    assert wrong_death_filter_value_type.json == {'error': 'Age or/and death should be an integer.'}, 'Wrong message for wrong death filter value type'
    wrong_sorting_value = json_client.get('/characters/?sorting=beauty')
    assert wrong_sorting_value.status_code == 400, 'Wrong status code for wrong sorting value'
    assert wrong_sorting_value.json == {'error': 'Wrong sorting parameter beauty.'}, 'Wrong message code for wrong sorting value'


@pytest.mark.skipif(skip_tests['routes_json'], reason='Skipped by config')
def test_read_character_json(json_client, jon_snow, daenerys, olenna_tyrell):
    jon = json_client.get('/characters/1')
    dany = json_client.get('/characters/2')
    olenna = json_client.get('/characters/50')
    wrong_character = json_client.get('/characters/222')
    assert jon.status_code == 200, 'Endpoint returns wrong status code'
    assert dany.status_code == 200, 'Endpoint returns wrong status code'
    assert olenna.status_code == 200, 'Endpoint returns wrong status code'
    assert wrong_character.status_code == 404, 'Endpoint returns wrong status code'
    assert jon.json == jon_snow, 'Endpoint returns wrong character'
    assert dany.json == daenerys, 'Endpoint returns wrong character'
    assert olenna.json == olenna_tyrell, 'Endpoint returns wrong character'
    assert wrong_character.json == {'error': 'Character with id=222 was not found.'}, '404 error returns wrong message'
    response4 = json_client.get('/characters/asdf')
    assert response4.status_code == 404, 'Endpoint returns wrong response code'


@pytest.mark.skipif(skip_tests['routes_json'], reason='Skipped by config')
def test_create_character_json(json_client, daenerys, robert_baratheon, aemon, headers_json):
    robert = json_client.post('/characters', json=robert_baratheon, headers=headers_json, follow_redirects=True)
    assert robert.status_code == 201, 'Wrong status code for character creation'
    assert robert.json.get('id', None), 'ID was not add during character creation'
    assert robert.json['id'] > 50, 'ID was not incremented during character creation'
    assert robert.json['nickname'] is None, 'Not provided optional field was not assigned during creation'
    robert_baratheon['id'], robert_baratheon['nickname'] = 51, None
    assert robert.json == robert_baratheon

    aemon_id, aemon_nameless, aemon_roleless, aemon_strengthless = [aemon.copy() for _ in range(4)]
    aemon_id['id'], aemon_nameless['name'], aemon_roleless['role'], aemon_strengthless['strength'] = 52, None, None, None
    create_aemon_id = json_client.post('/characters', json=aemon_id, headers=headers_json, follow_redirects=True)
    create_aemon_nameless = json_client.post('/characters', json=aemon_nameless, headers=headers_json, follow_redirects=True)
    create_aemon_roleless = json_client.post('/characters', json=aemon_roleless, headers=headers_json, follow_redirects=True)
    create_aemon_strengthless = json_client.post('/characters', json=aemon_strengthless, headers=headers_json, follow_redirects=True)
    assert create_aemon_id.status_code == 400, 'Creating a character with provided id did not return bad request status code'
    assert create_aemon_id.json == {'error': 'Character id should not be provided.'}, 'Wrong error message on provided character id'
    assert create_aemon_nameless.status_code == 400, 'Character creation with name=None returns wrong status code'
    assert create_aemon_nameless.json == {'error': 'Character\'s name can not be None.'}, 'Wrong error message on name=None'
    assert create_aemon_roleless.status_code == 400, 'Character creation with role=None returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Character\'s role can not be None.'}, 'Wrong error message on role=None'
    assert create_aemon_strengthless.status_code == 400, 'Character creation with strength=None returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Character\'s strength can not be None.'}, 'Wrong error message on strength=None'

    aemon_nameless['name'], aemon_roleless['role'], aemon_strengthless['strength'] = '', '', ''
    create_aemon_nameless = json_client.post('/characters', json=aemon_nameless, headers=headers_json, follow_redirects=True)
    create_aemon_roleless = json_client.post('/characters', json=aemon_roleless, headers=headers_json, follow_redirects=True)
    create_aemon_strengthless = json_client.post('/characters', json=aemon_strengthless, headers=headers_json, follow_redirects=True)
    assert create_aemon_nameless.status_code == 400, 'Character creation with empty name field returns wrong status code'
    assert create_aemon_nameless.json == {'error': 'Character\'s name can not be empty.'}, 'Wrong error message on empty name'
    assert create_aemon_roleless.status_code == 400, 'Character creation with empty role field returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Character\'s role can not be empty.'}, 'Wrong error message on empty role'
    assert create_aemon_strengthless.status_code == 400, 'Character creation with empty strength field returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Character\'s strength can not be empty.'}, 'Wrong error message on empty strength'

    aemon_nameless.pop('name')
    aemon_roleless.pop('role')
    aemon_strengthless.pop('strength')
    create_aemon_nameless = json_client.post('/characters', json=aemon_nameless, headers=headers_json, follow_redirects=True)
    create_aemon_roleless = json_client.post('/characters', json=aemon_roleless, headers=headers_json, follow_redirects=True)
    create_aemon_strengthless = json_client.post('/characters', json=aemon_strengthless, headers=headers_json, follow_redirects=True)
    assert create_aemon_nameless.status_code == 400, 'Missing name field returns wrong status'
    assert create_aemon_nameless.json == {'error': 'Missing required field(s): name.'}, 'Wrong error message on missing name field'
    assert create_aemon_roleless.status_code == 400, 'Missing role filed returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Missing required field(s): role.'}, 'Wrong error message on missing role field'
    assert create_aemon_strengthless.status_code == 400, 'Missing strength filed returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Missing required field(s): strength.'}, 'Wrong error message on missing strength field'

    daenerys.pop('id')
    create_dany = json_client.post('/characters', json=daenerys, headers=headers_json, follow_redirects=True)
    assert create_dany.status_code == 409, 'Wrong status code on creating existing character'
    assert create_dany.json == {'error': f'Character {daenerys["name"]} already exists.'}, 'Wrong error message on creating existing character'


@pytest.mark.skipif(skip_tests['routes_json'], reason='Skipped by config')
def test_delete_character_json(json_client, jon_snow, daenerys, olenna_tyrell, headers_json):
    jon = json_client.delete('/characters/1', headers=headers_json)
    assert jon.status_code == 200
    assert jon.json == jon_snow
    first_character = json_client.get('characters/1')
    assert first_character.status_code != 200, 'Character was not deleted'
    assert first_character.status_code == 404, 'Character is not found after deletion'
    assert first_character.json == {"error": "Character with id=1 was not found."}, 'Incorrect message for trying to read deleted character'
    for i in range(2, 51):
        json_client.delete(f'/characters/{i}', headers=headers_json)
    empty_response = json_client.get('/characters', follow_redirects=True)
    assert empty_response.status_code == 404, 'Wrong status code for empty database'
    assert isinstance(empty_response.json, list), 'Empty database return wrong type'
    assert empty_response.json == [], 'Empty database return wrong data'
    assert json_client.delete('/characters/1', headers=headers_json).status_code == 404


@pytest.mark.skipif(skip_tests['routes_json'], reason='Skipped by config')
def test_update_character_json(json_client, jon_snow, daenerys, olenna_tyrell, headers_json):
    jon_gendalf = json_client.put('/characters/1', json={'name': 'Gendalf'}, headers=headers_json)
    assert jon_gendalf.json['name'] == 'Gendalf', 'Field was not updated'
    assert jon_gendalf.status_code == 200, 'Wrong response status code'
    wrong_character = json_client.put('/characters/52', json={'age': 120}, headers=headers_json)
    assert wrong_character.status_code == 400, 'Update for non existing character wrong status code'
    assert wrong_character.json == {'error': 'Character with id=52 was not found.'}, 'Wrong message for 404 error'
    id_update = json_client.put('/characters/23', json={'id': 12, 'name': 'Helly R'}, headers=headers_json)
    assert id_update.status_code == 400, 'ID update is prohibited'
    assert id_update.json == {'error': 'Updating ID field is not allowed.'}, 'Wrong message for id update error'


@pytest.mark.skipif(skip_tests['routes_sql'], reason='Skipped by config')
def test_read_characters_sql(sql_db, sql_client, jon_snow, daenerys, olenna_tyrell):
    sql_db._reset_database()
    random20 = sql_client.get('/characters', follow_redirects=True)
    assert random20.status_code == 200, 'Endpoint returns wrong status code'
    assert len(random20.json) == 20, 'Wrong character cont for empty limit and skip parameters'
    first10 = sql_client.get('/characters/?limit=10')
    assert len(first10.json) == 10, 'Wrong character amount for limit=10'
    assert first10.json[0] == jon_snow, 'wrong first character'
    assert first10.json[1] == daenerys, 'wrong second character'
    for i in range(1, 51):
        assert len(sql_client.get(f'/characters/?limit={i}').json) == i
    wrong_limit = sql_client.get('/characters/?limit=3.4')
    assert wrong_limit.status_code == 400, 'Wrong status code for limit parameter wrong type'
    assert wrong_limit.json == {'error': 'Limit and skip parameters should be integers.'}
    characters11_20 = sql_client.get('/characters/?limit=10&skip=1')
    characters31_40 = sql_client.get('/characters/?limit=10&skip=3')
    assert len(characters11_20.json) == 10, 'Wrong characters amount on page two'
    for i in range(10):
        assert characters11_20.json[i]['id'] == i + 11, 'Wrong character id for page 2'
        assert characters31_40.json[i]['id'] == i + 31, 'Wrong character id for page 4'
    out_of_range = sql_client.get('/characters/?limit=20&skip=3')
    assert out_of_range.status_code == 404, 'Wrong status code for out of range limit+skip'
    assert out_of_range.json == {'error': 'There are no results for given limit and skip parameters.'}, 'Wrong message for out of range error'
    last10 = sql_client.get('/characters/?limit=20&skip=2')
    assert last10.status_code == 200
    assert len(last10.json) == 10, 'Amount of remaining characters is wrong'
    assert last10.json[-1] == olenna_tyrell, 'Last character is wrong'
    wrong_age_filter_value_type = sql_client.get('/characters/?age=twelve')
    assert wrong_age_filter_value_type.status_code == 400, 'Wrong status code for wrong age filter value type'
    assert wrong_age_filter_value_type.json == {'error': 'Age or/and death should be an integer.'}, 'Wrong message for wrong age filter value type'
    wrong_death_filter_value_type = sql_client.get('/characters/?age=seven')
    assert wrong_death_filter_value_type.status_code == 400, 'Wrong status code for wrong death filter value type'
    assert wrong_death_filter_value_type.json == {'error': 'Age or/and death should be an integer.'}, 'Wrong message for wrong death filter value type'
    wrong_sorting_value = sql_client.get('/characters/?sorting=beauty')
    assert wrong_sorting_value.status_code == 400, 'Wrong status code for wrong sorting value'
    assert wrong_sorting_value.json == {'error': 'Wrong sorting parameter beauty.'}, 'Wrong message code for wrong sorting value'


@pytest.mark.skipif(skip_tests['routes_sql'], reason='Skipped by config')
def test_read_character_sql(sql_db, sql_client, jon_snow, daenerys, olenna_tyrell):
    sql_db._reset_database()
    jon = sql_client.get('/characters/1')
    dany = sql_client.get('/characters/2')
    olenna = sql_client.get('/characters/50')
    wrong_character = sql_client.get('/characters/222')
    assert jon.status_code == 200, 'Endpoint returns wrong status code'
    assert dany.status_code == 200, 'Endpoint returns wrong status code'
    assert olenna.status_code == 200, 'Endpoint returns wrong status code'
    assert wrong_character.status_code == 404, 'Endpoint returns wrong status code'
    assert jon.json == jon_snow, 'Endpoint returns wrong character'
    assert dany.json == daenerys, 'Endpoint returns wrong character'
    assert olenna.json == olenna_tyrell, 'Endpoint returns wrong character'
    assert wrong_character.json == {'error': 'Character with id=222 was not found.'}, '404 error returns wrong message'
    response4 = sql_client.get('/characters/asdf')
    assert response4.status_code == 404, 'Endpoint returns wrong response code'


@pytest.mark.skipif(skip_tests['routes_sql'], reason='Skipped by config')
def test_create_character_sql(sql_db, sql_client, daenerys, robert_baratheon, aemon, headers_sql):
    sql_db._reset_database()
    robert = sql_client.post('/characters', json=robert_baratheon, headers=headers_sql, follow_redirects=True)
    print(f'{headers_sql=}')
    assert robert.status_code == 201, 'Wrong status code for character creation'
    assert robert.json.get('id', None), 'ID was not add during character creation'
    assert robert.json['id'] > 50, 'ID was not incremented during character creation'
    assert robert.json['nickname'] is None, 'Not provided optional field was not assigned during creation'
    robert_baratheon['id'], robert_baratheon['nickname'] = 51, None
    assert robert.json == robert_baratheon

    aemon_id, aemon_nameless, aemon_roleless, aemon_strengthless = [aemon.copy() for _ in range(4)]
    aemon_id['id'], aemon_nameless['name'], aemon_roleless['role'], aemon_strengthless['strength'] = 52, None, None, None
    create_aemon_id = sql_client.post('/characters', json=aemon_id, headers=headers_sql, follow_redirects=True)
    create_aemon_nameless = sql_client.post('/characters', json=aemon_nameless, headers=headers_sql, follow_redirects=True)
    create_aemon_roleless = sql_client.post('/characters', json=aemon_roleless, headers=headers_sql, follow_redirects=True)
    create_aemon_strengthless = sql_client.post('/characters', json=aemon_strengthless, headers=headers_sql, follow_redirects=True)
    assert create_aemon_id.status_code == 400, 'Creating a character with provided id did not return bad request status code'
    assert create_aemon_id.json == {'error': 'Character id should not be provided.'}, 'Wrong error message on provided character id'
    assert create_aemon_nameless.status_code == 400, 'Character creation with name=None returns wrong status code'
    assert create_aemon_nameless.json == {'error': 'Character\'s name can not be None.'}, 'Wrong error message on name=None'
    assert create_aemon_roleless.status_code == 400, 'Character creation with role=None returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Character\'s role can not be None.'}, 'Wrong error message on role=None'
    assert create_aemon_strengthless.status_code == 400, 'Character creation with strength=None returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Character\'s strength can not be None.'}, 'Wrong error message on strength=None'

    aemon_nameless['name'], aemon_roleless['role'], aemon_strengthless['strength'] = '', '', ''
    create_aemon_nameless = sql_client.post('/characters', json=aemon_nameless, headers=headers_sql, follow_redirects=True)
    create_aemon_roleless = sql_client.post('/characters', json=aemon_roleless, headers=headers_sql, follow_redirects=True)
    create_aemon_strengthless = sql_client.post('/characters', json=aemon_strengthless, headers=headers_sql, follow_redirects=True)
    assert create_aemon_nameless.status_code == 400, 'Character creation with empty name field returns wrong status code'
    assert create_aemon_nameless.json == {'error': 'Character\'s name can not be empty.'}, 'Wrong error message on empty name'
    assert create_aemon_roleless.status_code == 400, 'Character creation with empty role field returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Character\'s role can not be empty.'}, 'Wrong error message on empty role'
    assert create_aemon_strengthless.status_code == 400, 'Character creation with empty strength field returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Character\'s strength can not be empty.'}, 'Wrong error message on empty strength'

    aemon_nameless.pop('name')
    aemon_roleless.pop('role')
    aemon_strengthless.pop('strength')
    create_aemon_nameless = sql_client.post('/characters', json=aemon_nameless, headers=headers_sql, follow_redirects=True)
    create_aemon_roleless = sql_client.post('/characters', json=aemon_roleless, headers=headers_sql, follow_redirects=True)
    create_aemon_strengthless = sql_client.post('/characters', json=aemon_strengthless, headers=headers_sql, follow_redirects=True)
    assert create_aemon_nameless.status_code == 400, 'Missing name field returns wrong status'
    assert create_aemon_nameless.json == {'error': 'Missing required field(s): name.'}, 'Wrong error message on missing name field'
    assert create_aemon_roleless.status_code == 400, 'Missing role filed returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Missing required field(s): role.'}, 'Wrong error message on missing role field'
    assert create_aemon_strengthless.status_code == 400, 'Missing strength filed returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Missing required field(s): strength.'}, 'Wrong error message on missing strength field'

    daenerys.pop('id')
    create_dany = sql_client.post('/characters', json=daenerys, headers=headers_sql, follow_redirects=True)
    assert create_dany.status_code == 409, 'Wrong status code on creating existing character'
    assert create_dany.json == {'error': f'Character {daenerys["name"]} already exists.'}, 'Wrong error message on creating existing character'


@pytest.mark.skipif(skip_tests['routes_sql'], reason='Skipped by config')
def test_delete_character_sql(sql_db, sql_client, jon_snow, headers_sql):
    sql_db._reset_database()
    jon = sql_client.delete('/characters/1', headers=headers_sql)
    assert jon.status_code == 200
    assert jon.json == jon_snow
    first_character = sql_client.get('characters/1', headers=headers_sql)
    assert first_character.status_code != 200, 'Character was not deleted'
    assert first_character.status_code == 404, 'Character is not found after deletion'
    assert first_character.json == {"error": "Character with id=1 was not found."}, 'Incorrect message for trying to read deleted character'
    for i in range(2, 51):
        sql_client.delete(f'/characters/{i}', headers=headers_sql)
    empty_response = sql_client.get('/characters', headers=headers_sql, follow_redirects=True)
    assert empty_response.status_code == 404, 'Wrong status code for empty database'
    assert isinstance(empty_response.json, list), 'Empty database return wrong type'
    assert empty_response.json == [], 'Empty database return wrong data'
    assert sql_client.delete('/characters/1', headers=headers_sql).status_code == 404


@pytest.mark.skipif(skip_tests['routes_sql'], reason='Skipped by config')
def test_update_character_sql(sql_db, sql_client, jon_snow, daenerys, olenna_tyrell, headers_sql):
    sql_db._reset_database()
    jon_gendalf = sql_client.put('/characters/1', json={'name': 'Gendalf'}, headers=headers_sql)
    assert jon_gendalf.json['name'] == 'Gendalf', 'Field was not updated'
    assert jon_gendalf.status_code == 200, 'Wrong response status code'
    wrong_character = sql_client.put('/characters/52', json={'age': 120}, headers=headers_sql)
    assert wrong_character.status_code == 404, 'Update for non existing character wrong status code'
    assert wrong_character.json == {'error': 'Character with id=52 was not found.'}, 'Wrong message for 400 error'
    id_update = sql_client.put('/characters/23', json={'id': 12, 'name': 'Helly R'}, headers=headers_sql)
    assert id_update.status_code == 400, 'ID update is prohibited'
    assert id_update.json == {'error': 'Updating ID field is not allowed.'}, 'Wrong message for id update error'


@pytest.mark.skipif(skip_tests['routes_sql'], reason='Skipped by config')
def test_crash_endpoint(sql_app, sql_client):
    sql_app.config['PROPAGATE_EXCEPTIONS'] = False
    crash = sql_client.get('/crash')
    assert crash.json == {'error': 'Internal Server Error'}
    sql_app.config['PROPAGATE_EXCEPTIONS'] = True


@pytest.mark.skipif(skip_tests['routes_sql'], reason='Skipped by config')
def test_create_user(sql_client):
    missing_username = sql_client.post('/users/', json={'password': 'der_password'})
    missing_password = sql_client.post('/users/', json={'username': 'Gendalf'})
    assert missing_username.status_code == 400, 'Wrong status code for missing username'
    assert missing_password.status_code == 400, 'Wrong status code for missing password'
    assert missing_username.json == {'error': 'Missing required field(s): username.'}, 'Wrong message for missing username'
    assert missing_password.json == {'error': 'Missing required field(s): password.'}, 'Wrong message for missing password'
    empty_username = sql_client.post('/users/', json={'username': '    ', 'password': 'der_password'})
    assert empty_username.status_code == 400, 'Wrong status code for empty username'
    assert empty_username.json == {'error': 'Username can not be empty.'}, 'Wrong message for empty username'
    wrong_fields = sql_client.post('/users/', json={'username': 'Gandalf', 'password': 'der_password', 'color': 'grey', 'role': 'wizard'})
    assert wrong_fields.status_code == 400, 'Wrong status code on wrong field'
    assert wrong_fields.json == {'error': 'Not allowed field(s): color.'}, 'Wrong message on wrong field'
    correct_user = sql_client.post('/users/', json={'username': 'Gendalf', 'password': 'der_password', 'role': 'wizard'})
    assert correct_user.status_code == 201, 'Wrong status code on correct user creation'
    assert correct_user.json == {'username': 'Gendalf', 'role': 'wizard', 'id': 1}, 'Wrong user response on correct request'
    # user_no_role = sql_client.post('/users/', json={'username': 'Frodo', 'password': 'Baggins'})
    # assert user_no_role.json == {'username': 'Frodo', 'id': 2}


@pytest.mark.skipif(skip_tests['routes_sql'], reason='Skipped by config')
def test_delete_user(sql_client, sql_db, headers_sql):
    sql_db._reset_users()
    user_count = len(sql_client.get('/users/', headers=headers_sql).json)
    user_2 = sql_client.delete('/users/2', headers=headers_sql)
    assert user_2.status_code == 200, 'Wrong status code on user delete'
    assert user_2.json == {'username': 'Jim', 'role': 'Salesman', 'id': 2}, 'Wrong response for user delete'
    assert len(sql_client.get('/users/', headers=headers_sql).json) == user_count - 1, 'User count was not reduced after user deletion'
    delete_wrong_user = sql_client.delete('/users/102', headers=headers_sql)
    assert delete_wrong_user.status_code == 404, 'Wrong status code on deleting non existing user'
    assert delete_wrong_user.json == {'error': 'User with id=102 was not found.'}, 'Wrong message on deleting non existing user'
    dwight_token = generate_access_token('Dwight').json['access_token']
    delete_dwight = sql_client.delete('/users/me', headers={'Authorization': f'Bearer {dwight_token}'})
    assert delete_dwight.status_code == 200
    assert delete_dwight.json == {'username': 'Dwight', 'role': 'Assistant to the Regional Manager', 'id': 4}
    assert sql_client.get('/users/4', headers=headers_sql).status_code == 404


@pytest.mark.skipif(skip_tests['routes_sql'], reason='Skipped by config')
def test_read_user(sql_client, sql_db, headers_sql):
    non_existing_user = sql_client.get('/users/24', headers=headers_sql)
    assert non_existing_user.status_code == 404
    assert non_existing_user.json == {'error': 'User with id=24 was not found.'}
    sql_db._reset_users()
    jim = sql_client.get('/users/2', headers=headers_sql)
    assert jim.status_code == 200
    assert jim.json == {'username': 'Jim', 'role': 'Salesman', 'id': 2}
    read_me = sql_client.get('/users/me', headers=headers_sql)
    assert read_me.status_code == 200
    assert read_me.json == {'username': 'Michael', 'role': 'Regional Manager', 'id': 1}


@pytest.mark.skipif(skip_tests['routes_sql'], reason='Skipped by config')
def test_update_user(sql_client, sql_db, headers_sql):
    non_existing_user = sql_client.put('/users/24', headers=headers_sql, json={'username': 'Jon'})
    assert non_existing_user.status_code == 404
    assert non_existing_user.json == {'error': 'User with id=24 was not found.'}
    no_fields = sql_client.put('/users/1', headers=headers_sql, json={})
    assert no_fields.status_code == 400
    assert no_fields.json == {'error': 'None of the fields was provided ("username", "password", "role").'}
    wrong_field = sql_client.put('/users/1', headers=headers_sql, json={'username': 'Bilbo', 'height': '124cm'})
    assert wrong_field.status_code == 400
    assert wrong_field.json == {'error': 'Not allowed field(s): height.'}
    sql_db._reset_users()
    new_jim = sql_client.put('/users/2', headers=headers_sql, json={'username': 'Jimmy', 'role': 'Management'})
    assert new_jim.status_code == 200
    assert new_jim.json == {'username': 'Jimmy', 'role': 'Management', 'id': 2}
    
    token1 = sql_client.post('/login', data={'username': 'Michael', 'password': 'Scott'}).json['access_token']
    check_token1 = sql_client.delete('/characters/3', headers={'Authorization': f'Bearer {token1}'})
    assert check_token1.status_code == 404
    assert sql_client.put('/users/1', headers=headers_sql, json={'password': 'Scottish'}).status_code == 200
    token2 = sql_client.post('/login', data={'username': 'Michael', 'password': 'Scottish'}).json['access_token']
    check_token2 = sql_client.delete('/characters/3', headers={'Authorization': f'Bearer {token2}'})
    assert check_token2.status_code == 404
    dwight_header = {'Authorization': f'Bearer {generate_access_token('Dwight').json["access_token"]}'}
    new_role = sql_client.put('/users/me', headers=dwight_header, json={'role': 'Assistant Regional Manager'})
    assert new_role.status_code == 200
    assert new_role.json == {'username': 'Dwight', 'role': 'Assistant Regional Manager', 'id': 4}
    wrong_update = sql_client.put('/users/me', headers=dwight_header, json={'name': 'Kevin'})
    assert wrong_update.status_code == 400
    assert wrong_update.json == {'error': 'None of the fields was provided ("username", "password", "role").'}
    wrong_field_update = sql_client.put('/users/me', headers=dwight_header, json={'username': 'Kevin', 'eyes': 'Brown'})
    assert wrong_field_update.status_code == 400
    assert wrong_field_update.json == {'error': 'Not allowed field(s): eyes.'}
    new_password = sql_client.put('/users/me', headers=dwight_header, json={'password': 'secret'})
    new_dwight_token = sql_client.post('/login', data={'username': 'Dwight', 'password': 'secret'})
    assert new_dwight_token.status_code == 200
