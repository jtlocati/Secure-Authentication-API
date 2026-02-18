import pytest
from app.models.user import User

def rate_limit_trips(client):

    RL_trip = False

    payload_dos = {"email": "NonReal@test.com", "password": "NonRealPassword"}

    for _ in range(25):
        r = client.post("/auth/login", json=payload_dos)
        if r.status_code == 429:
            RL_trip =True
            break

    assert RL_trip == True
