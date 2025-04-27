from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
use_sql_database = True


skip_tests = dict(crud_json=False,
        crud_sql=False,
        integration=False,
        authentication=False,
        routes_json=False,
        routes_sql=False,
        models=False
        )

