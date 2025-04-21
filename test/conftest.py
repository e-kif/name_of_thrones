import os
import pytest
import tempfile
import json
from app import create_app
from data.json_data_manager import JSONDataManager as json_data_manager


# def test_app(db_uri, use_sql: bool = True):
#     if use_sql:
#         app = create_app(db_uri)
#     else:
#         app = create_app(db_uri)
#     app.config['TESTING'] = True
#     return app


@pytest.fixture(scope='function')
def client():
    """Test client setup with temporary database file"""
    db_fd, db_path = tempfile.mkstemp()

    with open(os.path.join('storage', 'characters.json'), 'r', encoding='utf8') as original:
        with open(db_path, 'w', encoding='utf8') as f:
            f.write(json.dumps(json.loads(original.read())))

    app = create_app(db_path)

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.remove(db_path)


@pytest.fixture(scope='function')
def json_db():
    """JSON database manager with in-memory storage"""
    return json_data_manager()


@pytest.fixture(scope='function')
def sql_db():
    """In-memory sql database instance for testing CRUD operations"""
    # db_uri = 'postgres://user:password@host/mock_db'
    db_uri = 'sqlite:///:memory:'
    app = create_app(db_uri, use_sql=True)
    app.config['TESTING'] = True
    with app.app_context():
        yield app.data_manager
    

@pytest.fixture(scope='function')
def sql_client():
    """Client for testing endpoints using in-memory sql database"""
    db_uri = 'sqlite:///:memory:'
    app = create_app(db_uri, use_sql=True)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


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
