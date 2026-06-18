# FleetFlow API Testing Project


## Overview

FleetFlow is a RESTful API project developed using FastAPI to manage fleet operations such as vehicles, drivers, customers, deliveries, and notifications.

The project demonstrates API development and automated API testing using Python, FastAPI, Pytest, and Requests.

## Features

* Vehicle management (Create, Read, Update, Delete)
* Driver management with vehicle assignment
* Customer management with email validation
* Delivery workflow management
* Notification management
* Automated notification generation after delivery creation
* Duplicate data validation
* Error handling for invalid requests

## Tech Stack

* Python 3.13
* FastAPI
* Pytest
* Requests
* Uvicorn
* Git & GitHub

## Project Structure

```text
fleetflow/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── routes/
│       ├── vehicles.py
│       ├── drivers.py
│       ├── customers.py
│       ├── deliveries.py
│       └── notifications.py
│
├── tests/
│   ├── test_vehicles.py
│   ├── test_drivers.py
│   ├── test_customers.py
│   ├── test_deliveries.py
│   └── test_notifications.py
│
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## API Modules

### Vehicles

* Create vehicle
* Get all vehicles
* Get vehicle by ID
* Update vehicle
* Delete vehicle

### Drivers

* Create driver
* Assign vehicle to driver
* Validate duplicate license numbers
* Get, update, and delete drivers

### Customers

* Create customer
* Validate email addresses
* Prevent duplicate emails
* Get, update, and delete customers

### Deliveries

* Create delivery
* Link drivers and customers
* Track delivery status

### Notifications

* Create notifications
* Auto-generate notification after delivery creation
* Get, update, and delete notifications

## Installation

Clone the repository:

```bash
git clone https://github.com/ARevathi2004/API_Testing.git
```

Navigate to the project folder:

```bash
cd API_Testing
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Running Tests

Run all test cases:

```bash
python -m pytest -v
```

Current test status:

* Total Tests: 26
* Passed: 26
* Failed: 0

## Sample Test Execution

```text
================= 26 passed in 1.67s =================
```

## Key Testing Scenarios

* CRUD operations validation
* Positive and negative test cases
* Duplicate data validation
* Invalid input validation
* End-to-end delivery workflow testing
* Auto-notification verification
* HTTP status code validation

## Future Enhancements

* Database integration using PostgreSQL or MySQL
* Authentication and authorization
* Docker containerization
* CI/CD using GitHub Actions
* Test coverage reporting
* Postman collection integration

## Author

Revathi A

GitHub: https://github.com/ARevathi2004/API_Testing
