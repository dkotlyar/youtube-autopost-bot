import os.path

from flask_migrate import init as _init, show as _show, migrate as _migrate, upgrade as _upgrade, heads as _heads, \
    downgrade as _downgrade
from main import app


def init(directory='migrations'):
    with app.app_context():
        if not os.path.exists(directory):
            _init(directory)


def show(directory='migrations'):
    with app.app_context():
        _show(directory)


def commit(directory='migrations', message=''):
    with app.app_context():
        _migrate(directory, message)
        # _upgrade(directory)


def update(directory='migrations', revision='head'):
    with app.app_context():
        _upgrade(directory, revision)


def downgrade(directory='migrations', revision=-1):
    with app.app_context():
        _downgrade(directory, revision)


def heads(directory='migrations'):
    with app.app_context():
        _heads(directory)
