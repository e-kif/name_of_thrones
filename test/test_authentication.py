import pytest
from utils.settings import skip_tests
from utils.security import generate_access_token


@pytest.mark.skipif(skip_tests['authentication'], reason='Skipped by config')
def test_is_user_credentials_valid_json(validate_user_json):
    assert validate_user_json('Michael', 'Scott')
    assert validate_user_json('michael', 'Scott')
    assert validate_user_json('miCHael', 'Scott')
    with pytest.raises(KeyError):
        assert not validate_user_json('Micha', 'Scott')
    assert not validate_user_json('Michael', 'scott')


@pytest.mark.skipif(skip_tests['authentication'], reason='Skipped by config')
def test_token_generation_sql(sql_client, sql_db):
    sql_db._reset_database()
    # sql_client.get('/database/reset', headers={})
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
    assert sql_client.delete('/characters/33',
                             headers={'Authorization': f'Bearer {correct_token.json["token"]}'}).status_code == 200


@pytest.mark.skipif(skip_tests['authentication'], reason='Skipped by config')
def test_sql_protected_endpoints(sql_client, headers_sql, robert_baratheon):
    wrong_credentials = sql_client.post('/login', json={'username': 'Michael', 'password': 'der_password'})
    assert wrong_credentials.status_code == 401, 'Wrong status code for invalid credentials'
    assert wrong_credentials.json == {'error': 'Invalid username or password'}, 'Wrong message for invalid credentials'
    non_auth = sql_client.post('/characters/')
    assert non_auth.status_code == 401, 'Wrong status code for protected endpoint'
    assert non_auth.json == {'error': 'Authentication failed: no token provided.'}
    sql_client.post('/users/', json={'username': 'tmp', 'password': 't', 'role': 'ghost'})
    ghost_token = sql_client.post('/login', json={'username': 'tmp', 'password': 't'}).json['token']
    sql_client.delete(f'/users/me', headers={'Authorization': f'Bearer {ghost_token}'})
    with pytest.raises(KeyError):
        sql_client.post('/characters/', json=robert_baratheon, headers={'Authorization': f'Bearer {ghost_token}'})
    expired_token = generate_access_token('Michael', 0.000001).json['token']
    expired = sql_client.post('/characters/', headers={'Authorization': f'Bearer {expired_token}'})
    assert expired.status_code == 401
    assert expired.json == {'error': 'Token has expired.'}
    invalid_token = generate_access_token('Michael').json['token'][4:]
    invalid = sql_client.post('/characters/', headers={'Authorization': f'Bearer {invalid_token}'})
    assert invalid.status_code == 401
    assert invalid.json == {'error': 'Token is invalid.'}
