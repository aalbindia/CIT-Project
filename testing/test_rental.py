import pytest
from app import app as flask_app, db
from models import User, Car, Rental
from datetime import datetime
@pytest.fixture
def app_context():
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield

def test_rental(app_context):
    user = User(username="r", email="r@example.com", password="123")
    car = Car(model="Grand Caravan", year="2006", color="blue", milage=17000, rate=15.6)

    db.session.add(user)
    db.session.add(car)
    db.session.commit()  # Assign IDs to user and car

    rental = Rental(user_id=user.id, car_id=car.id, start_date=datetime.now())
    db.session.add(rental)
    db.session.commit()

    result = db.session.get(Rental, rental.id)

    assert result is not None
    assert result.id is not None
    assert result.return_date is None
    assert result.car_id == car.id
    assert result.user_id == user.id
