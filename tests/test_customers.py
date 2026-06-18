import requests

BASE_URL = "http://127.0.0.1:8000"


def test_create_customer():
    payload = {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "delivery_address": "123 MG Road, Indore"
    }

    response = requests.post(
        f"{BASE_URL}/customers/",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "id" in data


def test_get_all_customers():
    response = requests.get(f"{BASE_URL}/customers/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customer_by_id():
    create_response = requests.post(
        f"{BASE_URL}/customers/",
        json={
            "name": "Bob Smith",
            "email": "bob@example.com",
            "delivery_address": "456 Ring Road, Bhopal"
        }
    )

    customer_id = create_response.json()["id"]

    response = requests.get(
        f"{BASE_URL}/customers/{customer_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == customer_id
    assert data["name"] == "Bob Smith"


def test_update_customer():
    create_response = requests.post(
        f"{BASE_URL}/customers/",
        json={
            "name": "Charlie",
            "email": "charlie@example.com",
            "delivery_address": "Old Address"
        }
    )

    customer_id = create_response.json()["id"]

    update_payload = {
        "name": "Charlie Updated",
        "email": "charlie.updated@example.com",
        "delivery_address": "New Address"
    }

    response = requests.put(
        f"{BASE_URL}/customers/{customer_id}",
        json=update_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == update_payload["name"]
    assert data["email"] == update_payload["email"]
    assert data["delivery_address"] == update_payload["delivery_address"]


def test_delete_customer():
    create_response = requests.post(
        f"{BASE_URL}/customers/",
        json={
            "name": "Delete User",
            "email": "delete@example.com",
            "delivery_address": "Temporary Address"
        }
    )

    customer_id = create_response.json()["id"]

    response = requests.delete(
        f"{BASE_URL}/customers/{customer_id}"
    )

    assert response.status_code == 200

    get_response = requests.get(
        f"{BASE_URL}/customers/{customer_id}"
    )

    assert get_response.status_code == 404


def test_create_customer_with_duplicate_email():
    payload = {
        "name": "Duplicate User",
        "email": "duplicate@example.com",
        "delivery_address": "Address One"
    }

    requests.post(
        f"{BASE_URL}/customers/",
        json=payload
    )

    response = requests.post(
        f"{BASE_URL}/customers/",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"


def test_create_customer_with_invalid_email():
    payload = {
        "name": "Invalid Email User",
        "email": "invalid-email",
        "delivery_address": "Address Two"
    }

    response = requests.post(
        f"{BASE_URL}/customers/",
        json=payload
    )

    assert response.status_code == 422


def test_get_non_existing_customer():
    response = requests.get(
        f"{BASE_URL}/customers/99999"
    )

    assert response.status_code == 404