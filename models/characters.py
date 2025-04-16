from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
    pass
    

db = SQLAlchemy(model_class=Base)


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[str] = mapped_column(nullabla=False)
    strength: Mapped[str] = mapped_column(nullable=False)

    house_id = db.relationship('House', backref=db.backref(db.backref('house')))
    symbol_id = db.relationship('Symbol', backref=db.backref(db.backref('symbol')))


class Age(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int] = mapped_column(nullable=False)
    character_id = db.relationship('Character', backref=db.backref('age'))


class Death(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    death: Mapped[int] = mapped_column(nullable=False)
    character_id = db.relationship('Character', backref=db.backref('death'))


class House(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class Symbol(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Animal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nulable=False)


class Nickname(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    character_id = db.relationship('Character', nullable=False, backref=db.backref('nickname'))


character_house = db.Table(
    'character_house',
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True),
    db.Column('house_id', db.Integer, db.ForeignKey('house.id'), primary_key=True)
    )

character_symbol = db.Table(
    'character_symbol',
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True),
    db.Column('symbol_id', db.Integer, db.ForeignKey('symbol.id'), primary_key=True)
    )

character_animal = db.Table(
    'character_animal',
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True),
    db.Column('animal_id', db.Integer, db.ForeignKey('animal.id'), primary_key=True)
    )
