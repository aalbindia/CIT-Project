import pytest
from models import User, Rental, Car 

def test_rental():
    user = User(username = "r", email = "r@example.com", password = "123")
    car = Car(name = "Toyota", rented = False)
    rental = Rental(user_id = user.id, car_id = car.id)

    assert rental.id is not None
    assert rental.return_date is None
    assert rental.car_id == car.id
    assert rental.user_id == user.id