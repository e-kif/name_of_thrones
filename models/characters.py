from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, object_session
from sqlalchemy.ext.hybrid import hybrid_property
# from flask import current_app
from sqlalchemy import select


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

character_house = db.Table(
    'character_house',
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'), primary_key=True),
    db.Column('house_id', db.Integer, db.ForeignKey('houses.id'), nullable=False),
    db.UniqueConstraint('character_id', name='unique_character_constraint_house')
    )

character_symbol = db.Table(
    'character_symbol',
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'), primary_key=True),
    db.Column('symbol_id', db.Integer, db.ForeignKey('symbols.id'), nullable=False),
    db.UniqueConstraint('character_id', name='unique_character_constraint_symbol')
    )

character_animal = db.Table(
    'character_animal',
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'), primary_key=True),
    db.Column('animal_id', db.Integer, db.ForeignKey('animals.id'), nullable=False),
    db.UniqueConstraint('character_id', name='unique_character_constraint_animal')
    )


def dynamic_hybrid_property(property_name, attribute_name, model_class,
                            remote_id: str = None, local_id: str = 'character_id',
                            always_create_new_record: bool = False,
                            secondary_table=None):
    """Dynamically creates a hybrid property for related entities"""

    def field_getter(self):
        relation = getattr(self, attribute_name)
        return getattr(relation, property_name) if relation else None
    
    def field_setter(self, value):
        relation = getattr(self, attribute_name)

        def resolve(val):
            if isinstance(val, model_class):
                return val
            
            if always_create_new_record:
                return model_class(**{property_name: val})
            item = db.session.query(model_class).filter(getattr(model_class, property_name) == val).first()
            if not item:
                item = model_class(**{property_name: val})
                db.session.add(item)
            return item
        
        if value is None:
            relation.clear()
        else:
            setattr(self, attribute_name, resolve(value))

    def field_expression(cls):
        query = select(getattr(model_class, property_name))
        
        if secondary_table is not None:
            query = query.join(secondary_table,
                               secondary_table.c[remote_id] == getattr(model_class, 'id'))\
            .where(secondary_table.c[local_id] == cls.id)
        else:
            query = query.where(getattr(model_class, local_id) == cls.id)
            
        return query.correlate(cls).scalar_subquery()
    
    return hybrid_property(fget=field_getter, fset=field_setter).expression(field_expression)
    

class Age(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int] = mapped_column(nullable=False)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('characters.id'), nullable=False, unique=True)

    def __repr__(self):
        return f'{self.character.name} is {self.age} years old'


class Death(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    death: Mapped[int] = mapped_column(nullable=False)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('characters.id'), nullable=False, unique=True)

    def __repr__(self):
        return f'{self.character.name} dead in season {self.death}'


class Houses(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    def __repr__(self):
        return f'House {self.name} ({self.id})'


class Symbols(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    def __repr__(self):
        return f'Symbol {self.name} ({self.id})'


class Animals(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    def __repr__(self):
        return f'Animal {self.name} ({self.id})'


class Nicknames(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('characters.id'), nullable=False)

    def __repr__(self):
        return f'{self.character.name} AKA {self.name} ({self.id})'
    

class Characters(db.Model):

    req_fields = {'name', 'role', 'strength'}
    opt_fields = {'house', 'symbol', 'animal', 'nickname', 'age', 'death'}
    allowed_fields = req_fields.union(opt_fields)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    strength: Mapped[str] = mapped_column(nullable=False)

    houses = db.relationship('Houses', secondary=character_house, uselist=False, backref='residents', passive_deletes=True)
    nicknames = db.relationship('Nicknames', uselist=False, backref='characters', cascade='all, delete-orphan')
    symbols = db.relationship('Symbols', secondary=character_symbol, uselist=False, backref='characters', passive_deletes=True)
    animals = db.relationship('Animals', secondary=character_animal, uselist=False, backref='characters', passive_deletes=True)
    ages = db.relationship('Age', uselist=False, backref='character', cascade='all, delete-orphan')
    deaths = db.relationship('Death', uselist=False, backref='character', cascade='all, delete-orphan')

    house = dynamic_hybrid_property('name', 'houses', Houses, remote_id='house_id', secondary_table=character_house)
    symbol = dynamic_hybrid_property('name', 'symbols', Symbols, remote_id='symbol_id', secondary_table=character_symbol)
    animal = dynamic_hybrid_property('name', 'animals', Animals, remote_id='animal_id', secondary_table=character_animal)
    nickname = dynamic_hybrid_property('name', 'nicknames', Nicknames, always_create_new_record=True)
    age = dynamic_hybrid_property('age', 'ages', Age, always_create_new_record=True)
    death = dynamic_hybrid_property('death', 'deaths', Death, always_create_new_record=True)
    
    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'house': self.house,
            'age': self.age,
            'role': self.role,
            'animal': self.animal,
            'symbol': self.symbol,
            'death': self.death,
            'strength': self.strength,
            'nickname': self.nickname
        }
    
    def __repr__(self):
        return f'{self.id}. {self.name} (age {self.age}, death {self.death}, house {self.house})'
