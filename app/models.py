from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class Vehicle(BaseModel):
    make_model: str
    plate_number: str
    capacity_kg: float
    status: str


class Driver(BaseModel):
    name: str
    license_number: str
    status: str
    vehicle_id: Optional[int] = None


class Customer(BaseModel):
    name: str
    email: EmailStr
    delivery_address: str


class Delivery(BaseModel):
    driver_id: int
    customer_id: int
    package_weight_kg: float
    status: str
    delivery_date: date


class Notification(BaseModel):
    delivery_id: int
    message: str
    type: str
    sent_status: str