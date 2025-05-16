import pytest
from models import User, Car, Brand, Campus, CarType, db

def test_user(app):
    with app.app_context():
        user = User(username="Robert Mann", email="robert.mann@test.com", password="robert123")
        db.session.add(user)
        db.session.commit()
        assert user.id is not None
        assert user.username == "Robert Mann"
        assert user.email == "robert.mann@test.com"
        assert user.password == "robert123"