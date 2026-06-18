from fastapi import APIRouter, HTTPException

from app.database import notifications, deliveries, counters
from app.models import Notification

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.post("/", status_code=201)
def create_notification(notification: Notification):
    # Validate delivery exists
    if notification.delivery_id not in deliveries:
        raise HTTPException(
            status_code=400,
            detail="Delivery not found"
        )

    notification_id = counters["notification"]

    data = notification.model_dump()
    data["id"] = notification_id

    notifications[notification_id] = data
    counters["notification"] += 1

    return data


@router.get("/")
def get_notifications():
    return list(notifications.values())


@router.get("/{notification_id}")
def get_notification(notification_id: int):
    if notification_id not in notifications:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return notifications[notification_id]


@router.put("/{notification_id}")
def update_notification(
    notification_id: int,
    notification: Notification
):
    if notification_id not in notifications:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    # Validate delivery exists
    if notification.delivery_id not in deliveries:
        raise HTTPException(
            status_code=400,
            detail="Delivery not found"
        )

    data = notification.model_dump()
    data["id"] = notification_id

    notifications[notification_id] = data

    return data


@router.delete("/{notification_id}")
def delete_notification(notification_id: int):
    if notification_id not in notifications:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    del notifications[notification_id]

    return {"message": "Notification deleted successfully"}