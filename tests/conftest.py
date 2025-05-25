import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app

from my_models import Car, Campus, CarType, Brand
from db import db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_setup(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_car(app):
    with app.app_context():
        campus = Campus(name="Downtown")
        brand = Brand(name="Toyota")
        cartype = CarType(name="Sedan")

        db.session.add_all([campus, brand, cartype])
        db.session.commit()

        car = Car(
            model="Civic",
            year=2020,
            color="Blue",
            rate=35.0,
            milage=10000,
            brand_id=brand.id,
            campus_id=campus.id,
            carType_id=cartype.id
        )
        db.session.add(car)
        db.session.commit()
        return car.id
