# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)


# def test_home():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json()["message"] == "Employee Management System"


# def test_about():
#     response = client.get("/about")
#     assert response.status_code == 200
#     assert response.json()["message"] == "a fully functional api"


# def test_view():
#     response = client.get("/view")
#     assert response.status_code == 200

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Employee Management System"


def test_about():
    response = client.get("/about")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "A fully functional Employee Management API"
    )


def test_view():
    response = client.get("/view")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_employee_not_found():
    response = client.get("/emp/P99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_create_employee():
    employee = {
        "name": "Test Employee",
        "age": 25,
        "department": "Testing",
        "salary": 40000,
        "email": "test@example.com",
    }

    response = client.post("/create", json=employee)

    assert response.status_code == 201
    assert response.json()["message"] == "Employee created successfully"

    employee_id = response.json()["id"]

    delete_response = client.delete(f"/delete/{employee_id}")

    assert delete_response.status_code == 200


def test_invalid_employee():
    employee = {
        "name": "A",
        "age": 10,
        "department": "IT",
        "salary": -100,
        "email": "wrong-email",
    }

    response = client.post("/create", json=employee)

    assert response.status_code == 422


def test_update_employee_not_found():
    employee = {
        "salary": 60000
    }

    response = client.put(
        "/update/P99999",
        json=employee,
    )

    assert response.status_code == 404