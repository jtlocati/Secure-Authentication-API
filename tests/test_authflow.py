import pytest
import app.models.user

def test_register_success(client, db_session):
    payload = {"email": "Jet2@test.com", "password": "StrongPAss123"}
    