
import pytest
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def reset_users():
    main.users.clear()
    main.next_user_id = 1
    yield
    main.users.clear()
    main.next_user_id = 1


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "AI Software Development API is running"
    }


def test_create_user():
    response = client.post("/users", json={
        "name": "Stanislav",
        "email": "stanislav@example.com",
        "age": 22
    })

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Stanislav"


def test_get_users():
    client.post("/users", json={
        "name": "Andriy",
        "email": "andriy@example.com",
        "age": 25
    })

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Andriy"


def test_get_user_by_id():
    client.post("/users", json={
        "name": "Oleksandr",
        "email": "oleksandr@example.com",
        "age": 24
    })

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Oleksandr"


def test_user_not_found():
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_duplicate_email():
    user = {
        "name": "Stanislav",
        "email": "stanislav@example.com",
        "age": 22
    }

    client.post("/users", json=user)
    response = client.post("/users", json=user)

    assert response.status_code == 409


def test_invalid_email():
    response = client.post("/users", json={
        "name": "Stanislav",
        "email": "incorrect-email",
        "age": 22
    })

    assert response.status_code == 422


def test_invalid_age():
    response = client.post("/users", json={
        "name": "Stanislav",
        "email": "stanislav@example.com",
        "age": 15
    })

    assert response.status_code == 422


def test_invalid_name():
    response = client.post("/users", json={
        "name": "A",
        "email": "stanislav@example.com",
        "age": 22
    })

    assert response.status_code == 422
