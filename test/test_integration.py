import pytest
from data.json_data_manager import JSONDataManager as json_db
from data.data_manager import DataManager
import abc
from utils.settings import skip_tests
from app import create_app


@pytest.mark.skipif(skip_tests['integration'], reason='Skipped by config')
def test_data_manager_abstract_method():
    DataManager.__abstractmethods__ = set()
    assert isinstance(DataManager, abc.ABCMeta)

    class Dummy(DataManager):
        pass

    assert Dummy().read_characters() is None
    assert Dummy().read_character(1) is None
    assert Dummy().remove_character(1) is None
    assert Dummy().add_character({'name': 'Frodo Beggins'}) is None
    assert Dummy().update_character(1, {'name': 'Bilbo Beggins'}) is None


@pytest.mark.skipif(skip_tests['integration'], reason='Skipped by config')
def test_json_db_integration():
    assert json_db().__getattribute__('__init__'), 'Constructor method is missing'
    assert json_db().__getattribute__('load_json_file'), 'Load json method is missing'
    assert json_db().__getattribute__('read_characters'), 'Read characters method is missing'
    assert json_db().__getattribute__('read_character'), 'Read character method is missing'
    assert json_db().__getattribute__('add_character'), 'Add character method is missing'
    assert json_db().__getattribute__('update_character'), 'Update character method is missing'
    assert json_db().__getattribute__('characters'), 'Characters getter method is missing'
    with pytest.raises(FileNotFoundError):
        assert json_db('some_file.json'), 'Non existent file does not raise an exception'


@pytest.mark.skipif(skip_tests['integration'], reason='Skipped by config')
def test_main_app_run(monkeypatch):
    called = {}

    def fake_run(self, debug):
        called['run'] = debug

    app = create_app(use_sql=True)
    monkeypatch.setattr(app.__class__, 'run', fake_run)

    from app import main
    main()

    assert called['run'] is True
