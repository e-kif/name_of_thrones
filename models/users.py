from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, exc
from utils.settings import db


user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE')),
    db.UniqueConstraint('user_id', name='unique_user_constraint')
     )

class Users(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    roles = db.relationship('Roles', secondary='user_roles', uselist=False, backref='users', cascade='all, delete-orphan')

    @hybrid_property
    def role(self):
       return self.roles.name if self.roles else None

    @role.setter
    def role(self, role: str):
        try:
            db_role = Roles.filter_by(name=role)
            return db_role
        except exc.NoResultFound:
            return Roles(**{'name': role})

    @role.expression
    def expression(cls):
        return Roles.name

    def __repr__(self):
        return f'{self.id}. {self.username} ({self.role})'


class Roles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

