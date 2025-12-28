import pytest
from flask import Flask

from app.infrastructure.database import db, init_db


@pytest.fixture
def app_context(tmp_path):
    app = Flask(__name__)
    database_path = tmp_path / "test.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    init_db(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
