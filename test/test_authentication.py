import pytest
from utils.security import is_user_credentials_valid


def test_is_user_credentials_valid():
    assert is_user_credentials_valid('Michael', 'Scott')
    assert is_user_credentials_valid('michael', 'Scott')
    assert is_user_credentials_valid('miCHael', 'Scott')
    with pytest.raises(KeyError):
        assert not is_user_credentials_valid('Micha', 'Scott')
    assert not is_user_credentials_valid('Michael', 'scott')


def test_tocken_generation_sql(sql_client):
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
    correct_token = sql_client.post('/login', json={'username': 'michael', 'password': 'Scott'})
    assert correct_token.status_code == 200, 'Wrong status code on successful token'
    assert correct_token.json.get('token'), 'There is no token key in response'
    sql_client.get('/database/reset', headers={'Authorization': f'Bearer {correct_token.json["token"]}'})
    assert sql_client.delete('/characters/33', headers={'Authorization': f'Bearer {correct_token.json["token"]}'}).status_code == 200
    

def test_sql_protected_endpoints(sql_client, headers_sql):
    non_auth = sql_client.post('/characters/')
    assert non_auth.status_code == 401, 'Wrong status code for protected endpoint'
    assert non_auth.json ==  {'error': 'Authenification failed: no token provided.'}
    wrong_username_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1pY2hhIiwicm9sZSI6IlJlY2VwdGlvbmlzdCIsImV4cCI6MTc0NTQxMDA0MX0.V-x-Ih0aVmha7JohOEtkMdbTwn9roqpEs-Z9uEKfHw8"
    with pytest.raises(Exception):
        sql_client.post('/characters/', heders={'Authorization': f'Bearer {wrong_username_token}'})
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlBhbSIsInJvbGUiOiJSZWNlcHRpb25pc3QiLCJleHAiOjE3NDU0MTIwNzh9.LuZeRxWouTQ8w-S1SfKZDufCFD1Qu0rmr9ZAFXntxR4"
    expired = sql_client.post('/characters/', headers={'Authorization': f'Bearer {expired_token}'})
    assert expired.status_code == 401
    assert expired.json == {'error': 'Token has expired.'}
    invalid_token = "eyJhbGciasdfewer34InR5cCI6IkpXVCJ9.eyJ1c2VybmwefdfasdfzxcvbSIsInJvbGUiOiJSZWNlcHRpb25pc3QiLCJleHAiOjE3NDU0MTIwNzh9.LuZeRxWouTQ8w-S1SfKZDufCFD1Qu0rmr9ZAFXntxR4"
    invalid = sql_client.post('/characters/', headers={'Authorization': f'Bearer {invalid_token}'})
    assert invalid.status_code == 401
    assert invalid.json == {'error': 'Token is invalid.'}
