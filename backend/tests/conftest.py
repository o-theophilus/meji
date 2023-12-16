import pytest
from application import create_app


@pytest.fixture()
def app(monkeypatch):
    un = 'tbdnifxw'
    ps = 's16TIDEw5N0iI1yolcN2N4Spypn504ec'
    monkeypatch.setenv(
        'DATABASE_URI',
        f'postgres://{un}:{ps}@isabelle.db.elephantsql.com/{un}'
        # "meji.db"
    )

    app = create_app("../tests/config.py")
    yield app

    monkeypatch.delenv('DATABASE    _URI', raising=False)


@pytest.fixture()
def client(app):
    return app.test_client()
