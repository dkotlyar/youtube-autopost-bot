from flask import Flask

from app import config


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='pasthere',
        SQLALCHEMY_DATABASE_URI=config.DB_CONNECTION_STRING,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    return app
