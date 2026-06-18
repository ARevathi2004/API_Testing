import requests
from conftest import BASE_URL


def test_create_vehicle():

    payload = {
        "make_model": "Tata Ace",
        "plate_number": "MP09AB1234",
        "capacity_kg": 1000,
        "status": "Available"
    }

    response = requests.post(
        f"{BASE_URL}/vehicles/",
        json=payload
    )

    assert response.status_code == 201

   