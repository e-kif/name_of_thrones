import os
from flask import Flask
from dotenv import load_dotenv
from routers.characters import characters_bp
from data.json_data_manager import JSONDataManager
from data.sql_data_manager import SQLDataManager


def create_app(db_path: str = os.path.join('storage', 'characters.json')):
    """Creates the app, registers all blueprints, return the app"""
    load_dotenv()
    app = Flask(__name__)
    # app.data_manager = JSONDataManager(db_path)
    app.data_manager = SQLDataManager(os.getenv('DATABASE_URI'))
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
