from fastapi import APIRouter, HTTPException
from app.database import vehicles, counters
from app.models import Vehicle

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])
 
@router.post("/", status_code=201)
def create_vehicle(vehicle: Vehicle):
    vehicle_id = counters["vehicle"]

    data = vehicle.model_dump()
    data["id"] = vehicle_id

    vehicles[vehicle_id] = data
    counters["vehicle"] += 1

    return data


@router.get("/")
def get_vehicles():
    return list(vehicles.values())


@router.get("/{vehicle_id}")
def get_vehicle(vehicle_id: int):
    if vehicle_id not in vehicles:
        raise HTTPException(404, "Vehicle not found")

    return vehicles[vehicle_id]


@router.put("/{vehicle_id}")
def update_vehicle(vehicle_id: int, vehicle: Vehicle):
    if vehicle_id not in vehicles:
        raise HTTPException(404, "Vehicle not found")

    data = vehicle.model_dump()
    data["id"] = vehicle_id

    vehicles[vehicle_id] = data
    return data


@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int):
    if vehicle_id not in vehicles:
        raise HTTPException(404, "Vehicle not found")

    del vehicles[vehicle_id]
    return {"message": "Vehicle deleted"}