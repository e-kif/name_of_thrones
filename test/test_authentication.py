import pytest
from utils.settings import skip_tests


@pytest.mark.skipif(skip_tests['authentication'], reason='Skipped by config')
def test_is_user_credentials_valid_json(validate_user_json):
    assert validate_user_json('Michael', 'Scott')
    assert validate_user_json('michael', 'Scott')  
    assert validate_user_json('miCHael', 'Scott')
    with pytest.raises(KeyError):
        assert not validate_user_json('Micha', 'Scott')
    assert not validate_user_json('Michael', 'scott')


@pytest.mark.skipif(skip_tests['authentication'], reason='Skipped by config')
def test_tocken_generation_sql(sql_client, sql_db):
    sql_client.get('/database/reset') 
    with pytest.raises(Exception):
        sql_client.post('/login', json={'username': 'micha', 'password': 'whatever'})
    missing_user = sql_client.post('/login', json={'password': 'qwerty'})
    assert missing_user.status_code == 400, 'Wrong status code for missing username'
    assert missing_user.json == {'error': 'Missing username or password'}, 'Wrong message on missing username'
    missing_password = sql_client.post('/login', json={'username': 'qwerty'})
    assert missing_password.status_code == 400, 'Wrong status code for missing password'
    assert missing_password.json == {'error': 'Missing username or password'}, 'Wrong message on missing password'
    with pytest.raises(KeyError):
        sql_client.post('/login', json={'username': 'qwerty', 'password': 'qwerty'})
    correct_token = sql_client.post('/login', json={'username': 'Michael', 'password': 'Scott'})
    assert correct_token.status_code == 200, 'Wrong status code on successful token'
    assert correct_token.json.get('token'), 'There is no token key in response'
    sql_client.get('/database/reset', headers={'Authorization': f'Bearer {correct_token.json["token"]}'})
    assert sql_client.delete('/characters/33', headers={'Authorization': f'Bearer {correct_token.json["token"]}'}).status_code == 200
    

@pytest.mark.skipif(skip_tests['authentication'], reason='Skipped by config')
def test_sql_protected_endpoints(sql_client, headers_sql, robert_baratheon):
    wrong_credentials = sql_client.post('/login', json={'username': 'Michael', 'password': 'der_password'})
    assert wrong_credentials.status_code == 401, 'Wrong status code for invalid credentials'
    assert wrong_credentials.json == {'error': 'Invalid username or password'}, 'Wrong message for invalid credentials'
    non_auth = sql_client.post('/characters/')
    assert non_auth.status_code == 401, 'Wrong status code for protected endpoint'
    assert non_auth.json ==  {'error': 'Authenification failed: no token provided.'}
    ghost_id = sql_client.post('/users/', json={'username': 'tmp', 'password': 't', 'role': 'Ghoust'}).json['id']
    ghost_token = sql_client.post('/login', json={'username': 'tmp', 'password': 't'}).json['token']
    sql_client.delete(f'/users/{ghost_id}')
    with pytest.raises(KeyError):
       sql_client.post('/characters/', json=robert_baratheon, headers={'Authorization': f'Bearer {ghost_token}'})
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlBhbSIsInJvbGUiOiJSZWNlcHRpb25pc3QiLCJleHAiOjE3NDU0MTIwNzh9.LuZeRxWouTQ8w-S1SfKZDufCFD1Qu0rmr9ZAFXntxR4"
    expired = sql_client.post('/characters/', headers={'Authorization': f'Bearer {expired_token}'})
    assert expired.status_code == 401
    assert expired.json == {'error': 'Token has expired.'}
    invalid_token = "eyJhbGciasdfewer34InR5cCI6IkpXVCJ9.eyJ1c2VybmwefdfasdfzxcvbSIsInJvbGUiOiJSZWNlcHRpb25pc3QiLCJleHAiOjE3NDU0MTIwNzh9.LuZeRxWouTQ8w-S1SfKZDufCFD1Qu0rmr9ZAFXntxR4"
    invalid = sql_client.post('/characters/', headers={'Authorization': f'Bearer {invalid_token}'})
    assert invalid.status_code == 401
    assert invalid.json == {'error': 'Token is invalid.'}
