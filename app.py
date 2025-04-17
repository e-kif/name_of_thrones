import os
from flask import Flask
from dotenv import load_dotenv
from routers.characters import characters_bp
from routers.database_management import database_bp
from data.json_data_manager import JSONDataManager
from data.sql_data_manager import SQLDataManager
from models.characters import db


def create_app(db_path: str = os.path.join('storage', 'characters.json')):
    """Creates the app, registers all blueprints, return the app"""
    load_dotenv()
    app = Flask(__name__)

    use_postgres_database = True

    if use_postgres_database:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
        db.init_app(app)

        with app.app_context():
            db.create_all()
            app.data_manager = SQLDataManager(db)
    
        app.register_blueprint(database_bp, url_prefix='/database')
    else:
        app.data_manager = JSONDataManager(db_path)

    
    app.register_blueprint(characters_bp, url_prefix='/characters')
    
    return app

def main():
    """Main function that starts the app"""
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()

    # todo swagger docs
    # todo pydantic schemas
    # todo user list + database counterpart
    # todo jwt auth
    # todo test coverage
    # todo update requirements
    # todo update readme
    # todo deploy
    # todo ci/cd workflow
