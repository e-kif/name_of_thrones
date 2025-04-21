def test_read_characters_json(client, jon_snow, daenerys, olenna_tyrell):
    random20 = client.get('/characters/', follow_redirects=True)
    assert random20.status_code == 200, 'Endpoint returns wrong status code'
    assert len(random20.json) == 20, 'Wrong character cont for empty limit and skip parameters'
    first10 = client.get('/characters/?limit=10')
    assert len(first10.json) == 10, 'Wrong character amount for limit=10'
    assert first10.json[0] == jon_snow, 'wrong first character'
    assert first10.json[1] == daenerys, 'wrong second character'
    for i in range(1, 51):
        assert len(client.get(f'/characters/?limit={i}').json) == i
    wrong_limit = client.get('/characters/?limit=3.4')
    assert wrong_limit.status_code == 400, 'Wrong status code for limit parameter wrong type'
    assert wrong_limit.json == {'error': 'Limit and skip parameters should be integers.'}
    characters11_20 = client.get('/characters/?limit=10&skip=1')
    characters31_40 = client.get('/characters/?limit=10&skip=3')
    assert len(characters11_20.json) == 10, 'Wrong characters amount on page two'
    for i in range(10):
        assert characters11_20.json[i]['id'] == i + 11, 'Wrong character id for page 2'
        assert characters31_40.json[i]['id'] == i + 31, 'Wrong character id for page 4'
    out_of_range = client.get('/characters/?limit=20&skip=3')
    assert out_of_range.status_code == 404, 'Wrong status code for out of range limit+skip'
    assert out_of_range.json == {'error': 'There are no results for given limit and skip parameters.'}, 'Wrong message for out of range error'
    last10 = client.get('/characters/?limit=20&skip=2')
    assert last10.status_code == 200
    assert len(last10.json) == 10, 'Amount of remaining characters is wrong'
    assert last10.json[-1] == olenna_tyrell, 'Last character is wrong'
    wrong_age_filter_value_type = client.get('/characters/?age=twelve')
    assert wrong_age_filter_value_type.status_code == 400, 'Wrong status code for wrong age filter value type'
    assert wrong_age_filter_value_type.json == {'error': 'Age or/and death should be an integer.'}, 'Wrong message for wrong age filter value type'
    wrong_death_filter_value_type = client.get('/characters/?age=seven')
    assert wrong_death_filter_value_type.status_code == 400, 'Wrong status code for wrong death filter value type'
    assert wrong_death_filter_value_type.json == {'error': 'Age or/and death should be an integer.'}, 'Wrong message for wrong death filter value type'
    wrong_sorting_value = client.get('/characters/?sorting=beauty')
    assert wrong_sorting_value.status_code == 400, 'Wrong status code for wrong sorting value'
    assert wrong_sorting_value.json == {'error': 'Wrong sorting parameter beauty.'}, 'Wrong message code for wrong sorting value'


def test_read_character_json(client, jon_snow, daenerys, olenna_tyrell):
    jon = client.get('/characters/1')
    dany = client.get('/characters/2')
    olenna = client.get('/characters/50')
    wrong_character = client.get('/characters/222')
    assert jon.status_code == 200, 'Endpoint returns wrong status code'
    assert dany.status_code == 200, 'Endpoint returns wrong status code'
    assert olenna.status_code == 200, 'Endpoint returns wrong status code'
    assert wrong_character.status_code == 404, 'Endpoint returns wrong status code'
    assert jon.json == jon_snow, 'Endpoint returns wrong character'
    assert dany.json == daenerys, 'Endpoint returns wrong character'
    assert olenna.json == olenna_tyrell, 'Endpoint returns wrong character'
    assert wrong_character.json == {'error': 'Character with id=222 was not found.'}, '404 error returns wrong message'
    response4 = client.get('/characters/asdf')
    assert response4.status_code == 404, 'Endpoint returns wrong response code'


def test_create_character_json(client, daenerys, robert_baratheon, aemon):
    robert = client.post('/characters', json=robert_baratheon, follow_redirects=True)
    assert robert.status_code == 201, 'Wrong status code for character creation'
    assert robert.json.get('id', None), 'ID was not add during character creation'
    assert robert.json['id'] > 50, 'ID was not incremented during character creation'
    assert robert.json['nickname'] is None, 'Not provided optional field was not assigned during creation'
    robert_baratheon['id'], robert_baratheon['nickname'] = 51, None
    assert robert.json == robert_baratheon

    aemon_id, aemon_nameless, aemon_roleless, aemon_strengthless = [aemon.copy() for _ in range(4)]
    aemon_id['id'], aemon_nameless['name'], aemon_roleless['role'], aemon_strengthless['strength'] = 52, None, None, None
    create_aemon_id = client.post('/characters', json=aemon_id, follow_redirects=True)
    create_aemon_nameless = client.post('/characters', json=aemon_nameless, follow_redirects=True)
    create_aemon_roleless = client.post('/characters', json=aemon_roleless, follow_redirects=True)
    create_aemon_strengthless = client.post('/characters', json=aemon_strengthless, follow_redirects=True)
    assert create_aemon_id.status_code == 400, 'Creating a character with provided id did not return bad request status code'
    assert create_aemon_id.json == {'error': 'Character id should not be provided.'}, 'Wrong error message on provided character id'
    assert create_aemon_nameless.status_code == 400, 'Character creation with name=None returns wrong status code'
    assert create_aemon_nameless.json == {'error': 'Character\'s name can not be None.'}, 'Wrong error message on name=None'
    assert create_aemon_roleless.status_code == 400, 'Character creation with role=None returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Character\'s role can not be None.'}, 'Wrong error message on role=None'
    assert create_aemon_strengthless.status_code == 400, 'Character creation with strength=None returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Character\'s strength can not be None.'}, 'Wrong error message on strength=None'

    aemon_nameless['name'], aemon_roleless['role'], aemon_strengthless['strength'] = '', '', ''
    create_aemon_nameless = client.post('/characters', json=aemon_nameless, follow_redirects=True)
    create_aemon_roleless = client.post('/characters', json=aemon_roleless, follow_redirects=True)
    create_aemon_strengthless = client.post('/characters', json=aemon_strengthless, follow_redirects=True)
    assert create_aemon_nameless.status_code == 400, 'Character creation with empty name field returns wrong status code'
    assert create_aemon_nameless.json == {'error': 'Character\'s name can not be empty.'}, 'Wrong error message on empty name'
    assert create_aemon_roleless.status_code == 400, 'Character creation with empty role field returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Character\'s role can not be empty.'}, 'Wrong error message on empty role'
    assert create_aemon_strengthless.status_code == 400, 'Character creation with empty strength field returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Character\'s strength can not be empty.'}, 'Wrong error message on empty strength'

    aemon_nameless.pop('name'); aemon_roleless.pop('role'); aemon_strengthless.pop('strength')
    create_aemon_nameless = client.post('/characters', json=aemon_nameless, follow_redirects=True)
    create_aemon_roleless = client.post('/characters', json=aemon_roleless, follow_redirects=True)
    create_aemon_strengthless = client.post('/characters', json=aemon_strengthless, follow_redirects=True)
    assert create_aemon_nameless.status_code == 400, 'Missing name field returns wrong status'
    assert create_aemon_nameless.json == {'error': 'Missing required field(s): name.'}, 'Wrong error message on missing name field'
    assert create_aemon_roleless.status_code == 400, 'Missing role filed returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Missing required field(s): role.'}, 'Wrong error message on missing role field'
    assert create_aemon_strengthless.status_code == 400, 'Missing strength filed returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Missing required field(s): strength.'}, 'Wrong error message on missing strength field'

    daenerys.pop('id')
    create_dany = client.post('/characters', json=daenerys, follow_redirects=True)
    assert create_dany.status_code == 400, 'Wrong status code on creating existing character'
    assert create_dany.json == {'error': f'Character {daenerys["name"]} already exists.'}, 'Wrong error message on creating existing character'


def test_delete_character_json(client, jon_snow, daenerys, olenna_tyrell):
    jon = client.delete('/characters/1')
    assert jon.status_code == 200
    assert jon.json == jon_snow
    first_character = client.get('characters/1')
    assert first_character.status_code != 200, 'Character was not deleted'
    assert first_character.status_code == 404, 'Character is not found after deletion'
    assert first_character.json == {"error": "Character with id=1 was not found."}, 'Incorrect message for trying to read deleted character'
    for i in range(2, 51):
        client.delete(f'/characters/{i}')
    empty_response = client.get('/characters', follow_redirects=True)
    assert empty_response.status_code == 404, 'Wrong status code for empty database'
    assert isinstance(empty_response.json, list), 'Empty database return wrong type'
    assert empty_response.json == [], 'Empty database return wrong data'
    assert client.delete('/characters/1').status_code == 404


def test_update_character_json(client, jon_snow, daenerys, olenna_tyrell):
    jon_gendalf = client.put('/characters/1', json={'name': 'Gendalf'})
    assert jon_gendalf.json['name'] == 'Gendalf', 'Field was not updated'
    assert jon_gendalf.status_code == 200, 'Wrong response status code'
    wrong_character = client.put('/characters/52', json={'age': 120})
    assert wrong_character.status_code == 400, 'Update for non existing character wrong status code'
    assert wrong_character.json == {'error': 'Character with id=52 was not found.'}, 'Wrong message for 404 error'
    id_update = client.put('/characters/23', json={'id': 12, 'name': 'Helly R'})
    assert id_update.status_code == 400, 'ID update is prohibited'
    assert id_update.json == {'error': 'Updating ID field is not allowed.'}, 'Wrong message for id update error'



def test_read_characters_sql(sql_client, jon_snow, daenerys, olenna_tyrell):
    sql_client.get('/database/reset')
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


def test_read_character_sql(sql_client, jon_snow, daenerys, olenna_tyrell):
    sql_client.get('/database/reset')
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


def test_create_character_sql(sql_client, daenerys, robert_baratheon, aemon):
    sql_client.get('/database/reset')
    robert = sql_client.post('/characters', json=robert_baratheon, follow_redirects=True)
    assert robert.status_code == 201, 'Wrong status code for character creation'
    assert robert.json.get('id', None), 'ID was not add during character creation'
    assert robert.json['id'] > 50, 'ID was not incremented during character creation'
    assert robert.json['nickname'] is None, 'Not provided optional field was not assigned during creation'
    robert_baratheon['id'], robert_baratheon['nickname'] = 51, None
    assert robert.json == robert_baratheon

    aemon_id, aemon_nameless, aemon_roleless, aemon_strengthless = [aemon.copy() for _ in range(4)]
    aemon_id['id'], aemon_nameless['name'], aemon_roleless['role'], aemon_strengthless['strength'] = 52, None, None, None
    create_aemon_id = sql_client.post('/characters', json=aemon_id, follow_redirects=True)
    create_aemon_nameless = sql_client.post('/characters', json=aemon_nameless, follow_redirects=True)
    create_aemon_roleless = sql_client.post('/characters', json=aemon_roleless, follow_redirects=True)
    create_aemon_strengthless = sql_client.post('/characters', json=aemon_strengthless, follow_redirects=True)
    assert create_aemon_id.status_code == 400, 'Creating a character with provided id did not return bad request status code'
    assert create_aemon_id.json == {'error': 'Character id should not be provided.'}, 'Wrong error message on provided character id'
    assert create_aemon_nameless.status_code == 400, 'Character creation with name=None returns wrong status code'
    assert create_aemon_nameless.json == {'error': 'Character\'s name can not be None.'}, 'Wrong error message on name=None'
    assert create_aemon_roleless.status_code == 400, 'Character creation with role=None returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Character\'s role can not be None.'}, 'Wrong error message on role=None'
    assert create_aemon_strengthless.status_code == 400, 'Character creation with strength=None returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Character\'s strength can not be None.'}, 'Wrong error message on strength=None'

    aemon_nameless['name'], aemon_roleless['role'], aemon_strengthless['strength'] = '', '', ''
    create_aemon_nameless = sql_client.post('/characters', json=aemon_nameless, follow_redirects=True)
    create_aemon_roleless = sql_client.post('/characters', json=aemon_roleless, follow_redirects=True)
    create_aemon_strengthless = sql_client.post('/characters', json=aemon_strengthless, follow_redirects=True)
    assert create_aemon_nameless.status_code == 400, 'Character creation with empty name field returns wrong status code'
    assert create_aemon_nameless.json == {'error': 'Character\'s name can not be empty.'}, 'Wrong error message on empty name'
    assert create_aemon_roleless.status_code == 400, 'Character creation with empty role field returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Character\'s role can not be empty.'}, 'Wrong error message on empty role'
    assert create_aemon_strengthless.status_code == 400, 'Character creation with empty strength field returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Character\'s strength can not be empty.'}, 'Wrong error message on empty strength'

    aemon_nameless.pop('name'); aemon_roleless.pop('role'); aemon_strengthless.pop('strength')
    create_aemon_nameless = sql_client.post('/characters', json=aemon_nameless, follow_redirects=True)
    create_aemon_roleless = sql_client.post('/characters', json=aemon_roleless, follow_redirects=True)
    create_aemon_strengthless = sql_client.post('/characters', json=aemon_strengthless, follow_redirects=True)
    assert create_aemon_nameless.status_code == 400, 'Missing name field returns wrong status'
    assert create_aemon_nameless.json == {'error': 'Missing required field(s): name.'}, 'Wrong error message on missing name field'
    assert create_aemon_roleless.status_code == 400, 'Missing role filed returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Missing required field(s): role.'}, 'Wrong error message on missing role field'
    assert create_aemon_strengthless.status_code == 400, 'Missing strength filed returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Missing required field(s): strength.'}, 'Wrong error message on missing strength field'

    daenerys.pop('id')
    create_dany = sql_client.post('/characters', json=daenerys, follow_redirects=True)
    assert create_dany.status_code == 409, 'Wrong status code on creating existing character'
    assert create_dany.json == {'error': f'Character {daenerys["name"]} already exists.'}, 'Wrong error message on creating existing character'


def test_delete_character_sql(sql_client, jon_snow, daenerys, olenna_tyrell):
    sql_client.get('/database/reset')
    jon = sql_client.delete('/characters/1')
    assert jon.status_code == 200
    assert jon.json == jon_snow
    first_character = sql_client.get('characters/1')
    assert first_character.status_code != 200, 'Character was not deleted'
    assert first_character.status_code == 404, 'Character is not found after deletion'
    assert first_character.json == {"error": "Character with id=1 was not found."}, 'Incorrect message for trying to read deleted character'
    for i in range(2, 51):
        sql_client.delete(f'/characters/{i}')
    empty_response = sql_client.get('/characters', follow_redirects=True)
    assert empty_response.status_code == 404, 'Wrong status code for empty database'
    assert isinstance(empty_response.json, list), 'Empty database return wrong type'
    assert empty_response.json == [], 'Empty database return wrong data'
    assert sql_client.delete('/characters/1').status_code == 404


def test_update_character_sql(sql_client, jon_snow, daenerys, olenna_tyrell):
    sql_client.get('/database/reset')
    jon_gendalf = sql_client.put('/characters/1', json={'name': 'Gendalf'})
    assert jon_gendalf.json['name'] == 'Gendalf', 'Field was not updated'
    assert jon_gendalf.status_code == 200, 'Wrong response status code'
    wrong_character = sql_client.put('/characters/52', json={'age': 120})
    assert wrong_character.status_code == 400, 'Update for non existing character wrong status code'
    assert wrong_character.json == {'error': 'Character with id=52 was not found.'}, 'Wrong message for 400 error'
    id_update = sql_client.put('/characters/23', json={'id': 12, 'name': 'Helly R'})
    assert id_update.status_code == 400, 'ID update is prohibited'
    assert id_update.json == {'error': 'Updating ID field is not allowed.'}, 'Wrong message for id update error'
