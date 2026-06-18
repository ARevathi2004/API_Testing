from fastapi import APIRouter, HTTPException

from app.database import customers, counters
from app.models import Customer

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post("/", status_code=201)
def create_customer(customer: Customer):
    # Check for duplicate email
    for existing_customer in customers.values():
        if existing_customer["email"] == customer.email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    customer_id = counters["customer"]

    data = customer.model_dump()
    data["id"] = customer_id

    customers[customer_id] = data
    counters["customer"] += 1

    return data


@router.get("/")
def get_customers():
    return list(customers.values())


@router.get("/{customer_id}")
def get_customer(customer_id: int):
    if customer_id not in customers:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customers[customer_id]


@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    if customer_id not in customers:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Prevent duplicate email during update
    for existing_id, existing_customer in customers.items():
        if (
            existing_id != customer_id
            and existing_customer["email"] == customer.email
        ):
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    data = customer.model_dump()
    data["id"] = customer_id

    customers[customer_id] = data

    return data


@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    if customer_id not in customers:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    del customers[customer_id]

    return {"message": "Customer deleted successfully"}