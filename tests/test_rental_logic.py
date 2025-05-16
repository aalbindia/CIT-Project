import pytest
from datetime import datetime
from my_models.rental import Rental

def validate_start_date(start_date):
    if start_date > datetime.now():
        raise ValueError("Start date cannot be in the future.")
    return start_date

def validate_return_date(start_date, return_date):
    if return_date and start_date and return_date < start_date:
        raise ValueError("Return date cannot be before start date.")
    return return_date

# --- Pytest test cases ---

def test_validate_return_date_same_day():
    start_date = datetime.now()
    return_date = start_date
    assert validate_return_date(start_date, return_date) == return_date

def test_validate_start_date_invalid():
    future_date = datetime(2999, 1, 1, 12, 0, 0)
    with pytest.raises(ValueError):
        validate_start_date(future_date)

def test_validate_return_date_none():
    start_date = datetime.now()
    return_date = None
    assert validate_return_date(start_date, return_date) is None