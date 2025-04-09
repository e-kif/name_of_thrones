import pytest
from app import create_app


@pytest.fixture(scope="session")
def app():
    """Session-wide test 'app' fixture."""
    app = create_app()
    app.config.update({'TESTING': True})
    yield app


@pytest.fixture
def client(app):
    """Test client for the application"""
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def jon_snow():
    return {"age": 25,
            "animal": "Direwolf",
            "death": None,
            "house": "Stark",
            "id": 1,
            "name": "Jon Snow",
            "nickname": "King in the North",
            "role": "King",
            "strength": "Physically strong",
            "symbol": "Wolf"}


@pytest.fixture()
def daenerys():
    return {"age": 24,
            "animal": "Dragon",
            "death": 8,
            "house": "Targaryen",
            "id": 2,
            "name": "Daenerys Targaryen",
            "nickname": "Mother of Dragons",
            "role": "Queen",
            "strength": "Cunning",
            "symbol": "Dragon"}


@pytest.fixture()
def olenna_tyrell():
    return {"age": 70,
            "animal": None,
            "death": 7,
            "house": "Tyrell",
            "id": 50,
            "name": "Olenna Tyrell",
            "nickname": "Queen of Thorns",
            "role": "Matriarch",
            "strength": "Cunning",
            "symbol": "Rose"}
