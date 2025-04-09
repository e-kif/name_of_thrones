import pytest
from data.json_data_manager import JSONDataManager as json_db


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
