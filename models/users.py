from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, object_session
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import exc
from utils.settings import db


#user_roles = db.Table(
#    'user_roles',
#    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
#    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE')),
#    db.UniqueConstraint('user_id', name='unique_user_constraint')
#     )

class Users(db.Model):
    req_fields = {'username', 'password'}
    opt_fields = {'role'}
    allowed_fields = req_fields.union(opt_fields)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[str] = mapped_column(db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)

    roles: Mapped['Roles'] = db.relationship('Roles', uselist=False, back_populates='users') 

    @hybrid_property
    def role(self):
       return self.roles.name 
    
    @role.setter
    def role(self, role: str):
        if isinstance(role, Roles):
            self.role_id = role.id
        else:
            user_role = db.session.query(Roles).filter_by(name=role).first()
            if user_role:
                self.role_id = user_role.id
            else:
                user_role = Roles(**{'name': role})
                db.session.add(user_role)
                db.session.flush()
                self.role_id = user_role.id

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

    users: Mapped[list['Users']] = db.relationship('Users', back_populates='roles', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Role: {self.id}. {self.name}'
