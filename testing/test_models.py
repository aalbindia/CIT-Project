import pytest
from app import app as flask_app, db
from models.user import User

@pytest.fixture
def app_context():
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield

def test_user(app_context):
    user = User(username="Robert Mann", email="robert.mann@test.com", password="robert123")
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.username == "Robert Mann"
    assert user.email == "robert.mann@test.com"
    assert user.password == "robert123"