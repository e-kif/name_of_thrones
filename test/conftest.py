import os
import pytest
import tempfile
import json
from app import create_app


@pytest.fixture(scope='function')
def client():
    """Test client setup with temporary database file"""
    db_fd, db_path = tempfile.mkstemp()

    with open(os.path.join('storage', 'characters.json'), 'r', encoding='utf8') as original:
        with open(db_path, 'w', encoding='utf8') as f:
            f.write(json.dumps(json.loads(original.read())))

    app = create_app(db_path)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    with open(db_path, 'r') as f:
        print(f.read())

    os.close(db_fd)
    os.remove(db_path)


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
