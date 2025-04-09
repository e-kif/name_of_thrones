from data.json_data_manager import JSONDataManager as json_db


def get_characters() -> list[dict]:
    """Returns full list of characters"""
    return json_db().characters


def get_characters_length() -> int:
    """Returns amount of the characters in storage"""
    return len(get_characters())


def get_optional_fields() -> set:
    """Returns a set of all character keys that can have 'null' value"""
    fields = set()
    for character in get_characters():
        for key, value in character.items():
            if value is None and key not in fields:
                fields.add(key)
    return fields


def get_character_keys() -> set:
    """Returns a set of all character keys"""
    return set(get_characters()[0].keys())


def filter_characters(filter_key: str,
                      filter_value: str | None) -> list | None:
    """Filters characters based on the filter_value of filter_key.
    Both parameters are case insensitive.
    """
    filter_key = filter_key.lower()
    if filter_key.lower() in get_character_keys():
        if filter_value is None:
            result = [character for character in get_characters()
                      if character[filter_key] is filter_value]
        else:
            filter_value = filter_value.lower()
            result = [character for character in get_characters()
                      if character[filter_key]
                      and character[filter_key].lower() == filter_value]
        return result


def get_characters_values(key: str,
                          characters: list = get_characters()) -> list | None:
    """Returns values of a particular key for provided characters"""
    if key.lower() in get_character_keys():
        return [character[key.lower()] for character in characters]


if __name__ == '__main__':
    print('total characters:', get_characters_length())
    print('optional fields:', get_optional_fields())
    print('character keys:', get_character_keys())
    print('names of characters without House:',
          get_characters_values('name', filter_characters('HOUSE', None)))
    print('names of characters of House Stark:',
          get_characters_values('name', filter_characters('HOuSE', 'stARk')))
