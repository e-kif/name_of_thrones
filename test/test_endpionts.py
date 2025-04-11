def test_read_characters(client, jon_snow, daenerys, olenna_tyrell):
    all_characters = client.get('/characters', follow_redirects=True)
    assert all_characters.status_code == 200, 'Endpoint returns wrong status code'
    assert all_characters.json[0] == jon_snow, 'Wrong first character'
    assert all_characters.json[1] == daenerys, 'Wrong second character'
    assert all_characters.json[-1] == olenna_tyrell, 'Wrong last character'


def test_read_character(client, jon_snow, daenerys, olenna_tyrell):
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


def test_create_character(client, daenerys, olenna_tyrell, robert_baratheon, aemon):
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
    assert create_aemon_nameless.json == {'error': 'Character name can not be None.'}, 'Wrong error message on name=None'
    assert create_aemon_roleless.status_code == 400, 'Character creation with role=None returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Character role can not be None.'}, 'Wrong error message on role=None'
    assert create_aemon_strengthless.status_code == 400, 'Character creation with strength=None returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Character strength can not be None.'}, 'Wrong error message on strength=None'

    aemon_nameless['name'], aemon_roleless['role'], aemon_strengthless['strength'] = '', '', ''
    create_aemon_nameless = client.post('/characters', json=aemon_nameless, follow_redirects=True)
    create_aemon_roleless = client.post('/characters', json=aemon_roleless, follow_redirects=True)
    create_aemon_strengthless = client.post('/characters', json=aemon_strengthless, follow_redirects=True)
    assert create_aemon_nameless.status_code == 400, 'Character creation with empty name field returns wrong status code'
    assert create_aemon_nameless.json == {'error': 'Character name can not be empty.'}, 'Wrong error message on empty name'
    assert create_aemon_roleless.status_code == 400, 'Character creation with empty role field returns wrong status code'
    assert create_aemon_roleless.json == {'error': 'Character role can not be empty.'}, 'Wrong error message on empty role'
    assert create_aemon_strengthless.status_code == 400, 'Character creation with empty strength field returns wrong status code'
    assert create_aemon_strengthless.json == {'error': 'Character strength can not be empty.'}, 'Wrong error message on empty strength'

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


def test_delete_character(client, jon_snow, daenerys, olenna_tyrell):
    jon = client.delete('/characters/1')
    assert jon.status_code == 200
    assert jon.json == {'removed character': jon_snow}
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


def test_update_character(client, jon_snow, daenerys, olenna_tyrell):
    jon_gendalf = client.put('/characters/1', json={'name': 'Gendalf'})
    assert jon_gendalf.json['name'] == 'Gendalf', 'Field was not updated'
    assert jon_gendalf.status_code == 200, 'Wrong response status code'
    wrong_character = client.put('/characters/52', json={'age': 120})
    assert wrong_character.status_code == 404, 'Update for non existing character wrong status code'
    assert wrong_character.json == {'error': 'Character with id=52 was not found.'}, 'Wrong message for 404 error'
    id_update = client.put('/characters/23', json={'id': 12, 'name': 'Helly R'})
    assert id_update.status_code == 400, 'ID update is prohibited'
    assert id_update.json == {'error': 'Character id is not allowed to be changed.'}, 'Wrong message for id update error'
