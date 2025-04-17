from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass
    

db = SQLAlchemy(model_class=Base)


class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    strength: Mapped[str] = mapped_column(nullable=False)

    # house_id = db.relationship('Houses', backref=db.backref(db.backref('house')))
    # symbol_id = db.relationship('Symbols', backref=db.backref(db.backref('symbol')))


class Age(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int] = mapped_column(nullable=False)
    character_id = db.relationship('Characters', backref=db.backref('age'))


class Death(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    death: Mapped[int] = mapped_column(nullable=False)
    character_id = db.relationship('Characters', backref=db.backref('death'))


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
    character_id = db.relationship('Characters', backref=db.backref('nickname'))


character_house = db.Table(
    'character_house',
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True),
    db.Column('house_id', db.Integer, db.ForeignKey('houses.id'), primary_key=True)
    )

character_symbol = db.Table(
    'character_symbol',
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True),
    db.Column('symbol_id', db.Integer, db.ForeignKey('symbols.id'), primary_key=True)
    )

character_animal = db.Table(
    'character_animal',
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True),
    db.Column('animal_id', db.Integer, db.ForeignKey('animals.id'), primary_key=True)
    )
