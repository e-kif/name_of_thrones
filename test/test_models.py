from models.users import *
from models.characters import *


def test_user_model(sql_db):
    role = Roles(name='Receptionist')
    sql_db.session.add(role)
    sql_db.session.flush()

    user = Users(username='Pam', password='Br'.encode('utf8'), role_id=role.id)
    sql_db.session.add(user)
    sql_db.session.flush()

    assert repr(user) == '1. Pam (Receptionist)'
    assert repr(role) == 'Role: 1. Receptionist'
    assert user.dict == {'username': 'Pam', 'id': 1, 'role': 'Receptionist'}
    

def test_user_role_setter_str(sql_db):
    user = Users(username='Jim', password='12345'.encode('utf8'))
    user.role = 'Salesman'
    sql_db.session.add(user)
    sql_db.session.flush()

    assert user.role == 'Salesman'


def test_user_role_setter_obj(sql_db):
    role = Roles(name='Regional Manager')
    sql_db.session.add(role)
    sql_db.session.flush()
    
    user = Users(username='Jim', password='12345'.encode('utf8'))
    user.role = role
    sql_db.session.add(user)
    sql_db.session.flush()

    assert user.role == 'Regional Manager'


def test_user_role_setter_existing_obj(sql_db):
    assistant_regional_manager = Roles(name='Assistant Regional Manager')
    sql_db.session.add(assistant_regional_manager)
    
    assistant_to_regional_manager = Roles(name='Assistant to a Regional Manager')
    sql_db.session.add(assistant_to_regional_manager)
    sql_db.session.flush()

    dwight = Users(username='Dwight', password=''.encode('utf8'))
    dwight.role = assistant_to_regional_manager
    sql_db.session.add(dwight)
    sql_db.session.flush()
    assert repr(dwight) == '1. Dwight (Assistant to a Regional Manager)'
    
    dwight.role = 'Assistant Regional Manager'
    sql_db.session.flush()

    assert repr(dwight) == '1. Dwight (Assistant Regional Manager)'


def test_character_model(sql_db):
    jon = Characters(
            name='Jon Snow',
            role='King',
            strength='Physically strong'
            )
    sql_db.session.add(jon)
    sql_db.session.flush()

    jon.house='Stark'
    jon.age=25
    jon.animal='Direwolf'
    jon.symbol='Wolf'
    jon.nickname='King in the North'
    assert repr(jon) == '1. Jon Snow (age 25, death None, house Stark)'
    assert jon.dict == {
            'id': 1,
            'name': 'Jon Snow',
            'role': 'King',
            'strength': 'Physically strong',
            'house': 'Stark',
            'age': 25,
            'animal': 'Direwolf',
            'symbol': 'Wolf',
            'nickname': 'King in the North',
            'death': None
            }
    assert repr(sql_db.session.query(Nicknames).filter_by(id=1).one()) == 'Jon Snow AKA King in the North (1)'
    assert repr(sql_db.session.query(Animals).filter_by(id=1).one()) == 'Animal Direwolf (1)'
    assert repr(sql_db.session.query(Symbols).filter_by(id=1).one()) == 'Symbol Wolf (1)'
    assert repr(sql_db.session.query(Houses).filter_by(id=1).one()) == 'House Stark (1)'
    assert repr(sql_db.session.query(Age).filter_by(id=1).one()) == 'Jon Snow is 25 years old'

    dany = Characters(name='Daenerys Targaryen', role='Queen', strength='Cunning')
    sql_db.session.add(dany)
    sql_db.session.flush()
    
    dany.death = 8
    dany.symbol = 'Dragon'
    sql_db.session.flush()
    assert repr(sql_db.session.query(Death).filter_by(id=1).one()) == 'Daenerys Targaryen died in season 8'

    jon.symbol = sql_db.session.query(Symbols).filter_by(id=2).one()
    assert jon.symbol == 'Dragon'
    jon.animal = None    
    jon.age = None    
    assert jon.dict['animal'] == None 
    assert jon.dict['age'] == None 
    
    dany.age = 24
    assert dany.dict['age'] == 24

    user1 = sql_db.session.query(Characters).filter(Characters.death == None).first()
    user2 = sql_db.session.query(Characters).filter(Characters.house == 'Stark').first()
    assert user1 == user2 == jon

