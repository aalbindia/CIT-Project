import pytest
from models.user import User

def test_user():
    user = User(username = "Robert Mann", email = "robert.mann@test.com", password = "robert123")

    assert user.id is not None
    assert user.username == "Robert Mann"
    assert user.email == "robert.mann@test.com"
    assert user.password == "robert123"