from pydantic import BaseModel, conint
from typing import Literal


class CharacterInRec(BaseModel):
    """Character schema with only required fields"""
    
    'name': str
    'role': str
    'strength': str
    

class CharacterInOpt(CharacterRequired):
    """Character schema with optional and required fields"""
    
    'age': conint(gt=0) | None = None
    'house': Literal['Greyjoy', 'Stormcrows', 'Clegane', 'Bolton',
                     'Targaryen', 'Free Folk', 'Unsullied', 'Martell',
                     'Dothraki', 'Reed', 'Payne', 'Tarth', 'Baratheon',
                     'Mormont', 'Sand', 'Tarly', 'Tyrell', 'Lannister', 'Stark'] | None = None
    'nickname': str | None = None
    'animal': str | None = None
    'death': coint(gt=0) | None = None
    

class CharacterOut(CharacterInOpt):
    'id': coint(gt=0)
    