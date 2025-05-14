#from models.rental import Rental
import pytest
from db import db
def test_create_rental_missing_fields(db_session):
    from models.rental import Rental
    rental = Rental()  # Missing required fields like car_id and user_id
    db_session.add(rental)
    with pytest.raises(Exception):  # Could be IntegrityError or similar
        db_session.commit()


@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()
