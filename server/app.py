from flask import Flask
import os
import sys
import click
from werkzeug.exceptions import HTTPException
import traceback


from dotenv import load_dotenv

load_dotenv()


def create_app():
    sys.path.append(".")  # to allow sub modules to access the parent module easily

    from db.db import db
    from api import api as api_blueprint

    app = Flask(__name__)
    database_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DB_PATH", f"sqlite:///{database_path}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    app.register_blueprint(api_blueprint, url_prefix="/api")

    @app.errorhandler(Exception)
    def handle_exception(e):
        # pass through HTTP errors. You wouldn't want to handle these generically.
        if isinstance(e, HTTPException):
            return e

        # now you're handling non-HTTP exceptions only
        return {"message": repr(e), "stack": traceback.format_exc()}, 500

    @app.cli.command()
    @click.argument("test_names", nargs=-1)
    def test(test_names):
        """Run the unit tests."""

        import pytest

        if test_names:
            sys.exit(pytest.main(["-vv", *test_names]))
        else:
            sys.exit(pytest.main(["-vv", "tests/"]))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
