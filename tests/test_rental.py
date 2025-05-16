import pytest
from my_models import User, Rental, Car

def test_rental():
    user = User(username = "r", email = "r@example.com", password = "123")
    rental = Rental(user_id = user.id)

    assert rental.return_date is None
    assert rental.user_id == user.id