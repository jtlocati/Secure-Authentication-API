import pytest
from app.models.user import User

#change auth/register AND auth/login -> /auth/register AND /auth/login

def test_register_success(client, db_session):
    payload = {"email": "Jet2@test.com", "password": "StrongPAss123"}
    r = client.post("/auth/register", json=payload)

    assert r.status_code == 201, r.text
    data = r.json()
    assert "id" in data
    assert data["email"] == payload["email"]
    #because its hashed this should never leak
    assert "hashed_password" not in data 

    user = db_session.query(User).filter(User.email == payload["email"]).first()
    assert user != None
    assert user.email == payload["email"]
    assert user.hashed_password != payload["password"]

#posts two identical users into "auth/register"
def test_register_duplicate_email(client):
    payload = {"email": "dup@test.com", "password": "StrongPass123"}
    r1 = client.post("/auth/register", json=payload)
    assert r1.status_code == 201, r1.text

    #duplicate
    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == 400, r2.text
    assert "Email" in r2.text or "email" in r2.text


def test_login_success_returns_token(client):
    #register user first
    payload = {"email": "Locati@test.com", "password": "StringPass123"}
    r1 = client.post("auth/register", json=payload)
    assert r1.status_code == 201, r1.text

    #login user
    r2 = client.post("auth/login", json=payload)
    assert r2.status_code == 200, r2.text
    data = r2.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20 #confirm JWT format

def test_login_wrong_pass(client):
    payload = {"email": "Wrongpass@test.com", "password": "NotRight"}
    r = client.post("auth/register", json=payload)
    assert r.status_code == 201, r.text

    #Test for incorrect password
    r2 = client.post("auth/register", json={"email": payload["email"], "password": "SOMTHING_IS_WRONG_HERE"})
    assert r2.status_code == 401, r2.text

    #Likewise test for incorrect email
    r3 = client.post("auth/register", json={"email": "IDK_BRO", "password": payload["password"]})
    assert r3.status_code == 402, r3.text

def test_me_requires_token(client):
    r = client.get("/auth/me")
    assert r.status_code in (401, 403), r.text  # depending on how you raise auth errors


def test_me_with_token_returns_user(client):
    reg = {"email": "me@test.com", "password": "Password123!"}
    assert client.post("/auth/register", json=reg).status_code == 201

    login = client.post("/auth/login", json=reg)
    assert login.status_code == 200
    token = login.json()["access_token"]

    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["email"] == reg["email"]