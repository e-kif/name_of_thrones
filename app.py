from flask import Flask
from routers.characters import characters_bp


def create_app():
    """Creates the app, registers all blueprints, return the app"""
    app = Flask(__name__)
    app.register_blueprint(characters_bp, url_prefix='/characters')
    return app


def main():
    """Main function that starts the app"""
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()

    # todo flask routers with blueprints
    # todo swagger docs
    # todo crud operations
    # todo pagination
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
