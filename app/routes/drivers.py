from fastapi import APIRouter, HTTPException
from app.database import drivers, vehicles, counters
from app.models import Driver

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.post("/", status_code=201)
def create_driver(driver: Driver):

    if driver.vehicle_id and driver.vehicle_id not in vehicles:
        raise HTTPException(400, "Vehicle not found")

    for d in drivers.values():
        if d["license_number"] == driver.license_number:
            raise HTTPException(400, "License already exists")

    driver_id = counters["driver"]

    data = driver.model_dump()
    data["id"] = driver_id

    drivers[driver_id] = data
    counters["driver"] += 1

    return data


@router.get("/")
def get_drivers():
    return list(drivers.values())

@router.get("/{driver_id}")
def get_driver(driver_id: int):
    if driver_id not in drivers:
        raise HTTPException(404, "Driver not found")

    return drivers[driver_id]


@router.put("/{driver_id}")
def update_driver(driver_id: int, driver: Driver):
    if driver_id not in drivers:
        raise HTTPException(404, "Driver not found")

    if driver.vehicle_id is not None and driver.vehicle_id not in vehicles:
        raise HTTPException(400, "Vehicle not found")

    data = driver.model_dump()
    data["id"] = driver_id

    drivers[driver_id] = data

    return data


@router.delete("/{driver_id}")
def delete_driver(driver_id: int):
    if driver_id not in drivers:
        raise HTTPException(404, "Driver not found")

    del drivers[driver_id]

    return {"message": "Driver deleted"}