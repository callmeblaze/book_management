import pytest
import requests
from requests.auth import HTTPBasicAuth
import config


def test_book_recommendations():
    payload = {
        "genres": ["Fiction"],
        "authors": ["Harper Lee"],
        "keywords": ["racial inequality"]
    }

    response = requests.post(
        "http://localhost:8000/recommendations",
        json=payload,
        auth=HTTPBasicAuth(config.BASIC_AUTH_USERNAME, config.PASSWORD)
    )

    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.text}")

    assert response.status_code == 200
    recommendations = response.json()

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0


def test_generate_summary():
    text = "To Kill a Mockingbird"

    response = requests.post(
        f"http://localhost:8000/generate-summary?text={text}",
        auth=HTTPBasicAuth(config.BASIC_AUTH_USERNAME, config.PASSWORD)
    )

    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.text}")

    assert response.status_code == 200
    summary_response = response.json()

    assert "summary" in summary_response
    assert len(summary_response["summary"]) > 0


if __name__ == "__main__":
    pytest.main()
