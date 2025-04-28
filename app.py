import os
from flask import Flask, g
from flasgger import Swagger
from dotenv import load_dotenv
from routers import database_bp, characters_bp, errorhandlers_bp, authentication_bp, users_bp
from data.json_data_manager import JSONDataManager
from data.sql_data_manager import SQLDataManager
from utils.settings import db, use_sql_database
from utils.docs import swagger_template


def create_app(db_path: str = None, use_sql: bool = False):
    """Creates the app, registers all blueprints, return the app"""
    load_dotenv()
    app = Flask(__name__)

    if use_sql:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_path or os.getenv('DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

        with app.app_context():
            db.create_all()
            app.data_manager = SQLDataManager(db)
    
        app.register_blueprint(database_bp, url_prefix='/database')
    else:
        app.data_manager = JSONDataManager(db_path) if db_path\
            else JSONDataManager(os.path.join('storage', 'characters.json'))
        with app.app_context():
            g.use_sql = use_sql
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['USE_SQL'] = use_sql
    app.register_blueprint(characters_bp, url_prefix='/characters')
    app.register_blueprint(errorhandlers_bp)
    app.register_blueprint(authentication_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    return app


def main():
    """Main function that starts the app"""
    app = create_app(use_sql=use_sql_database)
    Swagger(app, template=swagger_template)
    app.run(debug=True)


if __name__ == '__main__':
    main()  # pragma: no cover

    # todo pydantic schemas
    # todo update requirements
    # todo update readme
    # todo deploy
    # todo ci/cd workflow
