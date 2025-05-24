import pytest
from app import create_app
from db import db
from my_models import User

@pytest.fixture
def app():
    app = create_app('testing')  # make sure this returns a fully registered app
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_success(client, app):
    with app.app_context():
        user = User(email="test@example.com", password="test123", username="Tester")
        db.session.add(user)
        db.session.commit()

    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "test123"
    }, follow_redirects=True)

    assert b"User Profile" in response.data
    assert response.status_code == 200

def test_login_fail(client):
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'wrongpass'
    }, follow_redirects=True)

    assert b"Please check your login details and try again." in response.data
    assert response.status_code == 200
