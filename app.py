import os
from flask import Flask
from routers.characters import characters_bp
from data.json_data_manager import JSONDataManager


def create_app(db_path: str = os.path.join('storage', 'characters.json')):
    """Creates the app, registers all blueprints, return the app"""
    app = Flask(__name__)
    app.data_manager = JSONDataManager(db_path)
    app.register_blueprint(characters_bp, url_prefix='/characters')
    return app


def main():
    """Main function that starts the app"""
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()

    # todo convert character list into dict
    # todo swagger docs
    # todo sorting
    # todo filtering
    # todo database models
    # todo pydantic schemas
    # todo postgres database init
    # todo user list + database counterpart
    # todo jwt auth
    # todo test coverage
    # todo update requirements
    # todo update readme
    # todo deploy
    # todo ci/cd workflow
