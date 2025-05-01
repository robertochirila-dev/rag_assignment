import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

test_cases = [
    # (Prompt, expected_status, expected_in_response)
    (
        "I measure 34 underbust and 38 bust, my band rides up and my straps keep falling off.",
        200,
        {"recommendation": "34D"}
    ),
    (
        "My underbust is 32 and bust is 37.",
        200,
        {"recommendation": "32C"}
    ),
    (
        "My band rides up.",
        400,
        {"detail": "Could not extract both underbust and bust measurements."}
    ),
    (
        "I have quadraboob.",
        400,
        {"detail": "Could not extract both underbust and bust measurements."}
    ),
    (
        "My underbust is 20 and bust is 25.",
        400,
        {"detail": "Measurements out of plausible range or bust not greater than underbust."}
    ),
    (
        "My underbust is 50 and bust is 60.",
        200,
        {"recommendation": None}
    ),
    (
        "38 bust, 34 underbust, straps keep falling off, band rides up, cups wrinkle, quadraboob, gore floats, band too tight, band too loose.",
        200,
        {"recommendation": "34D"}
    ),
    (
        "",
        422,
        {"detail": "Input must be a non-empty string."}
    ),
]

@pytest.mark.parametrize("prompt, expected_status, expected_in_response", test_cases)
def test_bra_fitting_api(prompt, expected_status, expected_in_response):
    response = client.post("/api/bra-fitting", json={"text": prompt})
    assert response.status_code == expected_status
    for key, value in expected_in_response.items():
        assert response.json().get(key) == value