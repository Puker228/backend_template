from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_add_name():
    response = client.post("/add_name", json={"name": "John Doe"})
    assert response.status_code == 200
    assert response.json() == {"message": "Name 'John Doe' added to Redis."}


def test_get_name():
    client.post("/add_name", json={"name": "John Doe"})

    response = client.get("/names")
    assert response.status_code == 200
    assert response.json() == {"name": "John Doe"}


def test_get_name_not_found():
    response = client.get("/names")
    assert response.status_code == 404
    assert response.json() == {"detail": "Name not found"}
