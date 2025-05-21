import pytest
from app import app as flask_app, db
from models import User

@pytest.fixture
def client():
    # Test config
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    
    with flask_app.app_context():
        db.drop_all()
        db.create_all()


        user = User(email="test@example.com", password="test123", username="Test")
        db.session.add(user)
        db.session.commit()

    with flask_app.test_client() as client:
        yield client

def test_login_success(client):
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'test123'
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
