
import pytest
from flask import session

def test_car_details_404(client):
    response = client.get("/cars/9999")
    assert response.status_code == 404
    
def test_signup_route_exists(client):
    response = client.get("/signup")
    assert response.status_code == 200

def test_signup_invalid_email(client):
    response = client.post("/signup", data={
        "email": "invalidemail",
        "password": "Password123",
        "name": "Tester"
    }, follow_redirects=True)
    assert b"Email is not valid" in response.data

def test_signup_weak_password(client):
    response = client.post("/signup", data={
        "email": "test@example.com",
        "password": "short",
        "name": "Tester"
    }, follow_redirects=True)
    assert b"Password must be at least 8 characters" in response.data

def test_signup_duplicate_email(client, db_setup):
    client.post("/signup", data={
        "email": "test@example.com",
        "password": "Password123",
        "name": "Tester"
    })
    response = client.post("/signup", data={
        "email": "test@example.com",
        "password": "Password123",
        "name": "Tester"
    }, follow_redirects=True)
    assert b"A user with that email already exists" in response.data

def test_profile_post_not_logged_in(client):
    response = client.post("/profile")
    assert response.status_code == 302
    assert "/login" in response.location

