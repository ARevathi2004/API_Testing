import requests
from datetime import date, datetime

BASE_URL = "http://127.0.0.1:8000"


def create_delivery_workflow():
    # Create vehicle
    vehicle_response = requests.post(
        f"{BASE_URL}/vehicles/",
        json={
            "make_model": "Ashok Leyland",
            "plate_number": f"MP09NL{datetime.now().strftime('%H%M%S%f')}",
            "capacity_kg": 1500,
            "status": "Available"
        }
    )

    assert vehicle_response.status_code == 201, vehicle_response.text
    vehicle_id = vehicle_response.json()["id"]

    # Create driver
    driver_response = requests.post(
        f"{BASE_URL}/drivers/",
        json={
            "name": "Notification Driver",
            "license_number": f"LIC{datetime.now().strftime('%H%M%S%f')}",
            "status": "Active",
            "vehicle_id": vehicle_id
        }
    )

    assert driver_response.status_code == 201, driver_response.text
    driver_id = driver_response.json()["id"]

    # Create customer
    customer_response = requests.post(
        f"{BASE_URL}/customers/",
        json={
            "name": "Notification Customer",
            "email": f"notify{datetime.now().strftime('%H%M%S%f')}@example.com",
            "delivery_address": "Indore"
        }
    )

    assert customer_response.status_code == 201, customer_response.text
    customer_id = customer_response.json()["id"]

    # Create delivery
    delivery_response = requests.post(
        f"{BASE_URL}/deliveries/",
        json={
            "driver_id": driver_id,
            "customer_id": customer_id,
            "package_weight_kg": 500,
            "status": "Pending",
            "delivery_date": str(date.today())
        }
    )

    assert delivery_response.status_code == 201, delivery_response.text

    return delivery_response.json()["id"]


def test_get_all_notifications():
    response = requests.get(f"{BASE_URL}/notifications/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_notification():
    delivery_id = create_delivery_workflow()

    payload = {
        "delivery_id": delivery_id,
        "message": "Manual notification",
        "type": "Email",
        "sent_status": "Pending"
    }

    response = requests.post(
        f"{BASE_URL}/notifications/",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["delivery_id"] == delivery_id
    assert data["message"] == payload["message"]
    assert "id" in data


def test_get_notification_by_id():
    delivery_id = create_delivery_workflow()

    create_response = requests.post(
        f"{BASE_URL}/notifications/",
        json={
            "delivery_id": delivery_id,
            "message": "SMS notification",
            "type": "SMS",
            "sent_status": "Pending"
        }
    )

    notification_id = create_response.json()["id"]

    response = requests.get(
        f"{BASE_URL}/notifications/{notification_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == notification_id


def test_update_notification():
    delivery_id = create_delivery_workflow()

    create_response = requests.post(
        f"{BASE_URL}/notifications/",
        json={
            "delivery_id": delivery_id,
            "message": "Initial notification",
            "type": "Email",
            "sent_status": "Pending"
        }
    )

    notification_id = create_response.json()["id"]

    response = requests.put(
        f"{BASE_URL}/notifications/{notification_id}",
        json={
            "delivery_id": delivery_id,
            "message": "Updated notification",
            "type": "SMS",
            "sent_status": "Sent"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Updated notification"
    assert data["sent_status"] == "Sent"


def test_delete_notification():
    delivery_id = create_delivery_workflow()

    create_response = requests.post(
        f"{BASE_URL}/notifications/",
        json={
            "delivery_id": delivery_id,
            "message": "Delete me",
            "type": "Email",
            "sent_status": "Pending"
        }
    )

    notification_id = create_response.json()["id"]

    response = requests.delete(
        f"{BASE_URL}/notifications/{notification_id}"
    )

    assert response.status_code == 200

    get_response = requests.get(
        f"{BASE_URL}/notifications/{notification_id}"
    )

    assert get_response.status_code == 404


def test_create_notification_with_invalid_delivery():
    response = requests.post(
        f"{BASE_URL}/notifications/",
        json={
            "delivery_id": 99999,
            "message": "Invalid notification",
            "type": "Email",
            "sent_status": "Pending"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Delivery not found"


def test_auto_notification_created_after_delivery():
    delivery_id = create_delivery_workflow()

    response = requests.get(f"{BASE_URL}/notifications/")

    assert response.status_code == 200

    notifications = response.json()

    matching_notifications = [
        n for n in notifications
        if n["delivery_id"] == delivery_id
    ]

    assert len(matching_notifications) >= 1

    auto_notification = matching_notifications[0]

    assert auto_notification["message"] == "Delivery created"
    assert auto_notification["sent_status"] == "Pending"


def test_get_non_existing_notification():
    response = requests.get(
        f"{BASE_URL}/notifications/99999"
    )

    assert response.status_code == 404
