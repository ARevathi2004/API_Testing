import pytest

BASE_URL = "http://127.0.0.1:8000"

from app.database import (
    vehicles,
    drivers,
    customers,
    deliveries,
    notifications,
    counters
)


@pytest.fixture(autouse=True)
def reset_database():

    vehicles.clear()
    drivers.clear()
    customers.clear()
    deliveries.clear()
    notifications.clear()

    counters["vehicle"] = 1
    counters["driver"] = 1
    counters["customer"] = 1
    counters["delivery"] = 1
    counters["notification"] = 1

    yield