import os
import pytest
import tempfile
import json
from app import create_app
from data.json_data_manager import JSONDataManager as json_data_manager
from utils.security import is_user_credentials_valid


@pytest.fixture(scope='function')
def json_app():
    """"Test application that uses in-memory JSON file as a storage"""
    db_fd, db_path = tempfile.mkstemp()
    with open(os.path.join('storage', 'characters.json'), 'r', encoding='utf8') as original:
        with open(db_path, 'w', encoding='utf8') as f:
            f.write(json.dumps(json.loads(original.read())))
    app = create_app(db_path, use_sql=False)
    app.config['TESTING'] = True
    yield app
    os.close(db_fd)
    os.remove(db_path)


@pytest.fixture(scope='function')
def json_client(json_app):
    """Test client setup with temporary database file"""
    with json_app.test_client() as client:
        yield client


@pytest.fixture(scope='function')
def json_db(json_app):
    """JSON database manager with in-memory storage"""
    yield json_app.data_manager


@pytest.fixture(scope='function')
def sql_app():
    """Test app that uses in-memory sql database as a storage"""
    db_uri = 'sqlite:///:memory:'
    app = create_app(db_uri, use_sql=True)
    app.config['TESTING'] = True
    with app.app_context():
        @app.route('/crash')
        def crash():
            raise RuntimeError('Testing crash')
    yield app


@pytest.fixture(scope='function')
def sql_db(sql_app):
    """In-memory sql database instance for testing CRUD operations"""
    with sql_app.app_context():
        yield sql_app.data_manager
    

@pytest.fixture(scope='function')
def sql_client(sql_app):
    """Client for testing endpoints using in-memory sql database"""
    with sql_app.test_client() as client:
        yield client


@pytest.fixture()
def headers_json(json_client):
    token = json_client.post('/login', json={'username': 'Michael', 'password': 'Scott'}).json['token']
    yield {'Authorization': f'Bearer {token}'}


@pytest.fixture(scope='function')
def headers_sql(sql_client, sql_db):
    sql_db._reset_users()
    token = sql_client.post('/login', json={'username': 'Michael', 'password': 'Scott'}).json['token']
    yield {'Authorization': f'Bearer {token}'}


@pytest.fixture()
def validate_user_json(json_app):
    with json_app.app_context():
        yield is_user_credentials_valid


@pytest.fixture()
def jon_snow():
    return {'age': 25,
            'animal': 'Direwolf',
            'death': None,
            'house': 'Stark',
            'id': 1,
            'name': 'Jon Snow',
            'nickname': 'King in the North',
            'role': 'King',
            'strength': 'Physically strong',
            'symbol': 'Wolf'}


@pytest.fixture()
def daenerys():
    return {'age': 24,
            'animal': 'Dragon',
            'death': 8,
            'house': 'Targaryen',
            'id': 2,
            'name': 'Daenerys Targaryen',
            'nickname': 'Mother of Dragons',
            'role': 'Queen',
            'strength': 'Cunning',
            'symbol': 'Dragon'}


@pytest.fixture()
def olenna_tyrell():
    return {'age': 70,
            'animal': None,
            'death': 7,
            'house': 'Tyrell',
            'id': 50,
            'name': 'Olenna Tyrell',
            'nickname': 'Queen of Thorns',
            'role': 'Matriarch',
            'strength': 'Cunning',
            'symbol': 'Rose'}


@pytest.fixture()
def robert_baratheon():
    return {'name': 'Robert Baratheon',
            'house': 'Baratheon',
            'animal': 'Stag',
            'symbol': 'Crowned Stag',
            'role': 'Lord of the Seven Kingdoms',
            'age': 36,
            'death': 1,
            'strength': 'Immense physical strength'}

@pytest.fixture()
def aemon():
    return {'name': 'Aemon Targaryen',
            'age': 102,
            'role': 'Maester of the Night\'s Watch',
            'strength': 'Wisdom and loyalty'}

