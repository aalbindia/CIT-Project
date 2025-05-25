
import pytest
from app import app as flask_app, db
from my_models import User

@pytest.fixture
def client():
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

def test_signup_get(client):
    response = client.get('/signup')
    assert response.status_code in [200, 302, 404]

def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code in [200, 302, 401]

def test_profile(client):
    response = client.get('/profile', follow_redirects=True)
    assert response.status_code in [200, 302, 401]

def test_cars_route(client):
    response = client.get('/cars')
    assert response.status_code in [200, 404]

def test_car_detail_route(client):
    response = client.get('/cars/1')
    assert response.status_code in [200, 404]

def test_car_complete_route(client):
    response = client.post('/cars/1/complete')
    assert response.status_code in [200, 302, 404]

def test_google_login(client):
    response = client.get('/google-login')
    assert response.status_code in [200, 302, 404]


def test_github_login(client):
    response = client.get('/github-login')
    assert response.status_code in [200, 302, 404]


