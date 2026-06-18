from fastapi import FastAPI

from app.routes import (
    vehicles,
    drivers,
    customers,
    deliveries,
    notifications
)

app = FastAPI(title="FleetFlow API")

@app.get("/")
def home():
    return {"message": "Welcome to FleetFlow API"}

app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(customers.router)
app.include_router(deliveries.router)
app.include_router(notifications.router)


    

