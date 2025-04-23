import os
from flask import Flask
from dotenv import load_dotenv
from routers import database_bp, characters_bp, errorhandlers_bp, authentication_bp
from data.json_data_manager import JSONDataManager
from data.sql_data_manager import SQLDataManager
from models.characters import db


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
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.register_blueprint(characters_bp, url_prefix='/characters')
    app.register_blueprint(errorhandlers_bp)
    app.register_blueprint(authentication_bp)
    return app


def main():
    """Main function that starts the app"""
    app = create_app(use_sql=True)
    app.run(debug=True)


if __name__ == '__main__':
    main()

    # todo swagger docs
    # todo pydantic schemas
    # todo user list + database counterpart
    # todo test coverage
    # todo update requirements
    # todo update readme
    # todo deploy
    # todo ci/cd workflow
