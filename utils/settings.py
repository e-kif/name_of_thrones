from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
use_sql_database = True


skip_tests = dict(crud_json=True,
        crud_sql=True,
        integration=True,
        authentication=True,
        routes_json=True,
        routes_sql=False,
        models=True
        )

