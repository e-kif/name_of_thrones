from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import exc, LargeBinary
from utils.settings import db


class Users(db.Model):
    """Database Users class"""

    req_fields = {'username', 'password'}
    opt_fields = {'role'}
    allowed_fields = req_fields.union(opt_fields)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    role_id: Mapped[str] = mapped_column(db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)

    roles: Mapped['Roles'] = db.relationship('Roles', uselist=False, back_populates='users')

    @hybrid_property
    def role(self):
        """User role hybrid property getter"""
        return self.roles.name

    @role.setter
    def role(self, role: str):
        """User role hybrid property setter"""
        if isinstance(role, Roles):
            self.role_id = role.id
        else:
            user_role = db.session.query(Roles).filter_by(name=role).first()
            if user_role:
                self.role_id = user_role.id
                if 'roles' in self.__dict__:  # clear cashed role
                    del self.__dict__['roles']
            else:
                user_role = Roles(**{'name': role})
                db.session.add(user_role)
                db.session.flush()
                self.role_id = user_role.id

    @property
    def dict(self):
        """User serialization dict property getter"""
        return {'id': self.id,
                'username': self.username,
                'role': self.role}

    def __repr__(self):
        return f'{self.id}. {self.username} ({self.role})'


class Roles(db.Model):
    """Database Roles class"""

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    users: Mapped[list['Users']] = db.relationship('Users', back_populates='roles', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Role: {self.id}. {self.name}'
