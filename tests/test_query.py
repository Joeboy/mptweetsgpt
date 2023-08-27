from fastapi.testclient import TestClient
from web import app


def test_homepage():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert (
        "Please be aware that ChatGPT often generates unreliable results!"
        in response.text
    )


def test_query():
    client = TestClient(app)
    response = client.post(
        "/ask", json={"topic": "industrial action", "twitter_handle": "@zarahsultana"}
    )
    assert response.status_code == 200
    assert "We asked ChatGPT" in response.text
