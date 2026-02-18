import pytest

from app.models.user import User

payload = {"email": "hash@test.com", "password": "StrongPass123"}

def test_password_is_hashed(client, db_session):
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 201, r.text

    user = db_session.query(User).filter(User.email == payload["email"]).first
    assert user != None

    assert user.hashed_password != payload["password"]
    assert isinstance(user.hashed_password, str) 
    assert len(user.hashed_password) > 20

def test_token_required(client):
    payload["email"] = "jwt@tester.org"
    assert client.post("/auth/register", json=payload).status_code == 201

    r = client.post("/auth/login", json=payload)
    assert r.status_code == 200, r.text

    token = r.json()["access_token"]
    assert token.count(".") == 2