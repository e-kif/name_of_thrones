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
    pass


def test_update_character(client, jon_snow, daenerys, olenna_tyrell):
    pass
