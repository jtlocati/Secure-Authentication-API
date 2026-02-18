import pytest
from app.models.user import User

import pytest

# Update these imports if your paths differ
from app.models.user import User


def register_and_login(client, email, password):
    r1 = client.post("/auth/register", json={"email": email, "password": password})
    assert r1.status_code == 201, r1.text

    r2 = client.post("/auth/login", json={"email": email, "password": password})
    assert r2.status_code == 200, r2.text
    return r2.json()["access_token"]


def test_admin_only_requires_auth(client):
    r = client.get("/auth/admin-only")
    assert r.status_code in (401, 403), r.text


def test_admin_only_for_normal_user_is_403(client):
    token = register_and_login(client, "user@test.com", "Password123!")
    r = client.get("/auth/admin-only", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403, r.text


def test_admin_only_for_admin_is_200(client, db_session):
    email = "admin@test.com"
    password = "Password123!"
    token = register_and_login(client, email, password)

    # promote in DB
    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None
    user.role = "admin"
    db_session.commit()
    db_session.refresh(user)

    # login again to get token containing role=admin
    login2 = client.post("/auth/login", json={"email": email, "password": password})
    assert login2.status_code == 200, login2.text
    admin_token = login2.json()["access_token"]

    r = client.get("/auth/admin-only", headers={"Authorization": f"Bearer {admin_token}"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("ok") is True
