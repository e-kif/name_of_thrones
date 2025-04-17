from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property


class Base(DeclarativeBase):
    pass
    

db = SQLAlchemy(model_class=Base)

character_house = db.Table(
    'character_house',
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True),
    db.Column('house_id', db.Integer, db.ForeignKey('houses.id'), nullable=False),
    db.UniqueConstraint('character_id', name='unique_character_constraint')
    )

character_symbol = db.Table(
    'character_symbol',
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True),
    db.Column('symbol_id', db.Integer, db.ForeignKey('symbols.id'), nullable=False),
    db.UniqueConstraint('character_id', name='unique_character_constraint')
    )

character_animal = db.Table(
    'character_animal',
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True),
    db.Column('animal_id', db.Integer, db.ForeignKey('animals.id'), nullable=False),
    db.UniqueConstraint('character_id', name='unique_character_constraint')
    )

class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    strength: Mapped[str] = mapped_column(nullable=False)

    ages = db.relationship('Age', backref='character')
    houses = db.relationship('Houses', secondary=character_house, uselist=False, backref='residents')
    nicknames = db.relationship('Nicknames', uselist=False, backref='characters')
    symbols = db.relationship('Symbols', secondary=character_symbol, uselist=False, backref='characters')
    animals = db.relationship('Animals', secondary=character_animal, uselist=False, backref='characters')
    
    @hybrid_property
    def age(self):
        return self.ages[0].age if self.ages else None
    
    @hybrid_property
    def house(self):
        return self.houses.name if self.houses else None
    
    @hybrid_property
    def nickname(self):
        return self.nicknames.name if self.nicknames else None
    
    @hybrid_property
    def symbol(self):
        return self.symbols.name if self.symbols else None
    
    @hybrid_property
    def animal(self):
        return self.animals.name if self.animals else None


class Age(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int] = mapped_column(nullable=False)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('characters.id'), nullable=False)


class Death(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    death: Mapped[int] = mapped_column(nullable=False)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('characters.id'), nullable=False)


class Houses(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class Symbols(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Animals(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class Nicknames(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('characters.id'), nullable=False)
