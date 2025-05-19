import pytest


def validate_email(email):
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Invalid email format")
    return email

def validate_password(password):
    has_letter = any(char.isalpha() for char in password)
    has_number = any(char.isdigit() for char in password)
    if len(password) < 8 or not has_letter or not has_number:
        raise ValueError("Password must be at least 8 characters long and contain both letters and numbers")
    return password

# --- Pytest test cases ---

def test_validate_email_valid():
    assert validate_email("user@example.com") == "user@example.com"

def test_validate_email_invalid():
    with pytest.raises(ValueError):
        validate_email("userexample.com")

def test_validate_password_valid():
    assert validate_password("abc12345") == "abc12345"

def test_validate_password_invalid_short():
    with pytest.raises(ValueError):
        validate_password("a1b2")

def test_validate_password_invalid_no_digit():
    with pytest.raises(ValueError):
        validate_password("abcdefgh")

def test_validate_password_invalid_no_letter():
    with pytest.raises(ValueError):
        validate_password("12345678")