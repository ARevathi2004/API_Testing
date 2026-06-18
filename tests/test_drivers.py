import requests

BASE_URL = "http://127.0.0.1:8000"


def create_vehicle():
    response = requests.post(
        f"{BASE_URL}/vehicles/",
        json={
            "make_model": "Tata Ace",
            "plate_number": f"MP09AB{requests.get(f'{BASE_URL}/vehicles/').status_code}",
            "capacity_kg": 1000,
            "status": "Available"
        }
    )

    return response.json()["id"]


def test_create_driver():
    vehicle_id = create_vehicle()

    payload = {
        "name": "John Doe",
        "license_number": "LIC1001",
        "status": "Active",
        "vehicle_id": vehicle_id
    }

    response = requests.post(
        f"{BASE_URL}/drivers/",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == payload["name"]
    assert data["license_number"] == payload["license_number"]
    assert data["vehicle_id"] == vehicle_id
    assert "id" in data


def test_get_all_drivers():
    response = requests.get(f"{BASE_URL}/drivers/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_driver_by_id():
    vehicle_id = create_vehicle()

    create_response = requests.post(
        f"{BASE_URL}/drivers/",
        json={
            "name": "Jane Doe",
            "license_number": "LIC1002",
            "status": "Active",
            "vehicle_id": vehicle_id
        }
    )

    driver_id = create_response.json()["id"]

    response = requests.get(
        f"{BASE_URL}/drivers/{driver_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == driver_id
    assert data["name"] == "Jane Doe"


def test_update_driver():
    vehicle_id = create_vehicle()

    create_response = requests.post(
        f"{BASE_URL}/drivers/",
        json={
            "name": "David",
            "license_number": "LIC1003",
            "status": "Active",
            "vehicle_id": vehicle_id
        }
    )

    driver_id = create_response.json()["id"]

    update_payload = {
        "name": "David Updated",
        "license_number": "LIC1003",
        "status": "Inactive",
        "vehicle_id": vehicle_id
    }

    response = requests.put(
        f"{BASE_URL}/drivers/{driver_id}",
        json=update_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == update_payload["name"]
    assert data["status"] == update_payload["status"]


def test_delete_driver():
    vehicle_id = create_vehicle()

    create_response = requests.post(
        f"{BASE_URL}/drivers/",
        json={
            "name": "Delete Driver",
            "license_number": "LIC1004",
            "status": "Active",
            "vehicle_id": vehicle_id
        }
    )

    driver_id = create_response.json()["id"]

    response = requests.delete(
        f"{BASE_URL}/drivers/{driver_id}"
    )

    assert response.status_code == 200

    get_response = requests.get(
        f"{BASE_URL}/drivers/{driver_id}"
    )

    assert get_response.status_code == 404


def test_create_driver_with_invalid_vehicle():
    payload = {
        "name": "Invalid Driver",
        "license_number": "LIC1005",
        "status": "Active",
        "vehicle_id": 99999
    }

    response = requests.post(
        f"{BASE_URL}/drivers/",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Vehicle not found"


def test_create_driver_with_duplicate_license():
    vehicle_id = create_vehicle()

    payload = {
        "name": "Duplicate Driver",
        "license_number": "LIC1006",
        "status": "Active",
        "vehicle_id": vehicle_id
    }

    requests.post(
        f"{BASE_URL}/drivers/",
        json=payload
    )

    response = requests.post(
        f"{BASE_URL}/drivers/",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "License already exists"


def test_get_non_existing_driver():
    response = requests.get(
        f"{BASE_URL}/drivers/99999"
    )

    assert response.status_code == 404