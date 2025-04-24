from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, object_session
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import exc
from utils.settings import db


user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE')),
    db.UniqueConstraint('user_id', name='unique_user_constraint')
     )

class Users(db.Model):
    req_fields = {'username', 'password'}
    opt_fields = {'role'}
    allowed_fields = req_fields.union(opt_fields)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    roles = db.relationship('Roles', secondary='user_roles', uselist=False, backref='users', passive_deletes=True)

    @hybrid_property
    def role(self):
       return self.roles.name if self.roles else None

    @role.setter
    def role(self, role: str):
        print(f'{type(role)=} {role=}')
        if role is None:
            self.roles.clear()
        else:
            if isinstance(role, Roles):
                self.roles = role
            else:
                user_role = db.session.query(Roles).filter_by(name=role).first()
                print(f'{user_role=}')
                if user_role:
                    self.roles = user_role
                else:
                    user_role = Roles(**{'name': role})
                    db.session.add(user_role)
                    self.roles = user_role

    @role.expression
    def expression(cls):
        return Roles.name

    @property
    def dict(self):
        return {'id': self.id,
                'username': self.username,
                'role': self.role}

    def __repr__(self):
        return f'{self.id}. {self.username} ({self.role})'


class Roles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    def __repr__(self):
        return f'Role: {self.id}. {self.name}'
