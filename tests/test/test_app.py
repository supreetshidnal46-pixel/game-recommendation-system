
import pytest
from app import app, recommend_games


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_action_games():
    results = recommend_games("Action", "All", 8.0)
    assert len(results) > 0
    assert all(g["genre"] == "Action" for g in results)


def test_minimum_rating():
    results = recommend_games("All", "All", 9.5)
    assert all(g["rating"] >= 9.5 for g in results)


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_form_submission(client):
    response = client.post("/", data={
        "genre": "Sports",
        "platform": "All",
        "min_rating": "8"
    })
    assert response.status_code == 200
    assert b"FIFA 25" in response.data
    assert b"Rocket League" in response.data
