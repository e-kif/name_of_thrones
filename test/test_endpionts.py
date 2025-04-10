def test_read_characters(client, jon_snow, daenerys, olenna_tyrell):
    response = client.get('/characters', follow_redirects=True)
    assert response.status_code == 200, 'Endpoint returns wrong status code'
    assert response.json[0] == jon_snow, 'Wrong first character'
    assert response.json[1] == daenerys, 'Wrong second character'
    assert response.json[-1] == olenna_tyrell, 'Wrong last character'


def test_read_character(client, jon_snow, daenerys, olenna_tyrell):
    response0 = client.get('/characters/1')
    response1 = client.get('/characters/2')
    response2 = client.get('/characters/50')
    response3 = client.get('/characters/222')
    assert response0.status_code == 200, 'Endpoint returns wrong status code'
    assert response1.status_code == 200, 'Endpoint returns wrong status code'
    assert response2.status_code == 200, 'Endpoint returns wrong status code'
    assert response3.status_code == 404, 'Endpoint returns wrong status code'
    assert response0.json == jon_snow, 'Endpoint returns wrong character'
    assert response1.json == daenerys, 'Endpoint returns wrong character'
    assert response2.json == olenna_tyrell, 'Endpoint returns wrong character'
    assert response3.json == {'error': 'Character with id=222 was not found.'}, '404 error returns wrong message'
    response4 = client.get('/characters/asdf')
    assert response4.status_code == 404, 'Endpoint returns wrong response code'


def test_create_character(client, jon_snow, daenerys, olenna_tyrell):
    pass


def test_delete_character(client, jon_snow, daenerys, olenna_tyrell):
    response = client.delete('/characters/1')
    assert response.status_code == 200
    assert response.json == {'removed character': jon_snow}
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
    response = client.put('/characters/1', json={'name': 'Gendalf'})
    assert response.json['name'] == 'Gendalf', 'Field was not updated'
    assert response.status_code == 200, 'Wrong response status code'
    wrong_character = client.put('/characters/52', json={'age': 120})
    assert wrong_character.status_code == 404, 'Update for non existing character wrong status code'
    assert wrong_character.json == {'error': 'Character with id=52 was not found.'}, 'Wrong message for 404 error'
    id_update = client.put('/characters/23', json={'id': 12, 'name': 'Helly R'})
    assert id_update.status_code == 400, 'ID update is prohibited'
    assert id_update.json == {'error': 'Character id is not allowed to be changed.'}, 'Wrong message for id update error'
