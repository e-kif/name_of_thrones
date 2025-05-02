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
    with pytest.raises(KeyError):
        sql_client.post('/login', data={'username': 'micha', 'password': 'whatever'})
    missing_user = sql_client.post('/login', data={'password': 'qwerty'})
    assert missing_user.status_code == 400, 'Wrong status code for missing username'
    assert missing_user.json == {'error': 'Missing username or password'}, 'Wrong message on missing username'
    missing_password = sql_client.post('/login', data={'username': 'qwerty'})
    assert missing_password.status_code == 400, 'Wrong status code for missing password'
    assert missing_password.json == {'error': 'Missing username or password'}, 'Wrong message on missing password'
    with pytest.raises(KeyError):
        sql_client.post('/login', data={'username': 'qwerty', 'password': 'qwerty'})
    correct_token = sql_client.post('/login', data={'username': 'Michael', 'password': 'Scott'})
    assert correct_token.status_code == 200, 'Wrong status code on successful token'
    assert correct_token.json.get('access_token'), 'There is no token key in response'
    sql_client.get('/database/reset', headers={'Authorization': f'Bearer {correct_token.json["access_token"]}'})
    assert sql_client.delete('/characters/33',
                             headers={'Authorization': f'Bearer {correct_token.json["access_token"]}'}).status_code == 200


@pytest.mark.skipif(skip_tests['authentication'], reason='Skipped by config')
def test_sql_protected_characters_endpoints(sql_client, headers_sql, robert_baratheon):
    wrong_credentials = sql_client.post('/login', data={'username': 'Michael', 'password': 'der_password'})
    assert wrong_credentials.status_code == 401, 'Wrong status code for invalid credentials'
    assert wrong_credentials.json == {'error': 'Invalid username or password'}, 'Wrong message for invalid credentials'
    non_auth = sql_client.post('/characters/')
    assert non_auth.status_code == 401, 'Wrong status code for protected endpoint'
    assert non_auth.json == {'error': 'Authentication failed: no token provided.'}
    sql_client.post('/users/', json={'username': 'tmp', 'password': 't', 'role': 'ghost'})
    ghost_token = sql_client.post('/login', data={'username': 'tmp', 'password': 't'}).json['access_token']
    sql_client.delete(f'/users/me', headers={'Authorization': f'Bearer {ghost_token}'})
    with pytest.raises(KeyError):
        sql_client.post('/characters/', json=robert_baratheon, headers={'Authorization': f'Bearer {ghost_token}'})
    expired_token = generate_access_token('Michael', 0.000001).json['access_token']
    expired = sql_client.post('/characters/', headers={'Authorization': f'Bearer {expired_token}'})
    assert expired.status_code == 401
    assert expired.json == {'error': 'Token has expired.'}
    invalid_token = generate_access_token('Michael').json['access_token'][4:]
    invalid = sql_client.post('/characters/', headers={'Authorization': f'Bearer {invalid_token}'})
    assert invalid.status_code == 401
    assert invalid.json == {'error': 'Token is invalid.'}


@pytest.mark.skipif(skip_tests['authentication'], reason='Skipped by config')
def test_sql_protected_users_endpoints(sql_client, sql_db, headers_sql):
    sql_db._reset_database()
    non_authorized = sql_client.get('/users/me')
    assert non_authorized.status_code == 401
    assert non_authorized.json == {'error': 'Authentication failed: no token provided.'}
    token_pam = generate_access_token('Pam').json['access_token']
    auth_pam = sql_client.get('/users/me', headers={'Authorization': f'Bearer {token_pam}'})
    assert auth_pam.json == {'username': 'Pam', 'role': 'Receptionist', 'id': 3}
    token_jim = generate_access_token('Jim').json['access_token']
    auth_jim = sql_client.get('/users/me', headers={'Authorization': f'Bearer {token_jim}'})
    assert auth_jim.json == {'username': 'Jim', 'role': 'Salesman', 'id': 2}
    token_dwight = generate_access_token('Dwight').json['access_token']
    auth_dwight = sql_client.get('/users/me', headers={'Authorization': f'Bearer {token_dwight}'})
    assert auth_dwight.json == {'username': 'Dwight', 'role': 'Assistant to the Regional Manager', 'id': 4}
    token_michael = generate_access_token('Michael').json['access_token']
    auth_michael = sql_client.get('/users/me', headers={'Authorization': f'Bearer {token_michael}'})
    assert auth_michael.json == {'username': 'Michael', 'role': 'Regional Manager', 'id': 1}
    wrong_role = sql_client.get('/users/', headers={'Authorization': f'Bearer {token_dwight}'})
    assert wrong_role.status_code == 401
    assert wrong_role.json == {'error': 'Only Regional Manager is allowed to access this endpoint.'}
    wrong_role = sql_client.get('/users/4', headers={'Authorization': f'Bearer {token_dwight}'})
    assert wrong_role.status_code == 401
    assert wrong_role.json == {'error': 'Only Regional Manager is allowed to access this endpoint.'}
    correct_role = sql_client.get('/users/', headers={'Authorization': f'Bearer {token_michael}'})
    assert correct_role.status_code == 200
