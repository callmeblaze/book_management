import pytest
from fastapi.testclient import TestClient
from main import app
from requests.auth import HTTPBasicAuth
import config

client = TestClient(app)


def test_create_book():
    response = client.post(
        "/books",
        json={"title": "Test Book", "author": "Test Author", "genre": "Test Genre", "year_published": 2022,
              "summary": "Test Summary"},
        auth=HTTPBasicAuth(config.BASIC_AUTH_USERNAME, config.PASSWORD)
    )
    assert response.status_code == 200


def test_read_book():
    response = client.get("/books/1", auth=HTTPBasicAuth(config.BASIC_AUTH_USERNAME, config.PASSWORD))
    assert response.status_code == 200


def test_update_book():
    response = client.put(
        "/books/1",
        json={"title": "Updated Test Book1"},
        auth=HTTPBasicAuth(config.BASIC_AUTH_USERNAME, config.PASSWORD)
    )
    assert response.status_code == 200


def test_delete_book():
    response = client.delete("/books/1", auth=HTTPBasicAuth(config.BASIC_AUTH_USERNAME, config.PASSWORD))

    if response.status_code == 404:
        print("No book found with ID 1 to delete")
    else:
        assert response.status_code == 200
        response_json = response.json()
        print(f"Response JSON: {response_json}")
        assert response_json.get("message") == "Book and associated reviews deleted successfully"


if __name__ == "__main__":
    pytest.main()
