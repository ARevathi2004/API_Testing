from fastapi import APIRouter, HTTPException
from app.database import (
    deliveries,
    drivers,
    customers,
    notifications,
    counters
)
from app.models import Delivery

router = APIRouter(prefix="/deliveries", tags=["Deliveries"])


@router.post("/", status_code=201)
def create_delivery(delivery: Delivery):

    if delivery.driver_id not in drivers:
        raise HTTPException(400, "Driver not found")

    if delivery.customer_id not in customers:
        raise HTTPException(400, "Customer not found")

    delivery_id = counters["delivery"]

    data = delivery.model_dump()
    data["id"] = delivery_id

    deliveries[delivery_id] = data
    counters["delivery"] += 1

    notification_id = counters["notification"]

    notifications[notification_id] = {
        "id": notification_id,
        "delivery_id": delivery_id,
        "message": "Delivery created",
        "type": "Email",
        "sent_status": "Pending"
    }

    counters["notification"] += 1

    return data