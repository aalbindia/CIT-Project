import pytest
from  db import db

def test_user(app):
    with app.app_context():
        from my_models import User
        user = User(username="Robert Mann", email="robert.mann@test.com", password="robert123")
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == "Robert Mann"
        assert user.email == "robert.mann@test.com"
        assert user.password == "robert123"