import pytest
from app.models.user import User

RL_Trip = False

def test_RL(client):
    payload = {"email": "DOC@test.com", "password": "StrongPass123"}
    for _ in range(25):
        r = client.post("auth/login", json=payload)
        if r.status_code == 429:
            RL_Trip = True
            break

    assert RL_Trip == True