import requests
from conftest import BASE_URL


def test_delivery_workflow():

    vehicle = requests.post(
        f"{BASE_URL}/vehicles/",
        json={
            "make_model": "Truck",
            "plate_number": "ABC123",
            "capacity_kg": 1000,
            "status": "Available"
        }
    ).json()

    driver = requests.post(
        f"{BASE_URL}/drivers/",
        json={
            "name": "John",
            "license_number": "LIC123",
            "status": "Active",
            "vehicle_id": vehicle["id"]
        }
    ).json()

    customer = requests.post(
        f"{BASE_URL}/customers/",
        json={
            "name": "Alice",
            "email": "alice@test.com",
            "delivery_address": "Indore"
        }
    ).json()

    delivery = requests.post(
        f"{BASE_URL}/deliveries/",
        json={
            "driver_id": driver["id"],
            "customer_id": customer["id"],
            "package_weight_kg": 200,
            "status": "Pending",
            "delivery_date": "2026-06-20"
        }
    )

    assert delivery.status_code == 201

    notifications = requests.get(
        f"{BASE_URL}/notifications/"
    )

    assert notifications.status_code == 200