from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def setup_module(module):
    # ensure sample data is reset before tests
    activities.clear()
    activities.update({
        "Test Activity": {
            "description": "desc",
            "schedule": "now",
            "max_participants": 5,
            "participants": ["alice@example.com", "bob@example.com"],
        }
    })


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Test Activity" in data


def test_signup_duplicate():
    resp = client.post(
        "/activities/Test%20Activity/signup?email=alice@example.com"
    )
    assert resp.status_code == 400


def test_signup_new():
    resp = client.post(
        "/activities/Test%20Activity/signup?email=charlie@example.com"
    )
    assert resp.status_code == 200
    assert "charlie@example.com" in activities["Test Activity"]["participants"]


def test_unregister_missing():
    resp = client.delete(
        "/activities/Test%20Activity/participants?email=doesnotexist@example.com"
    )
    assert resp.status_code == 400


def test_unregister_success():
    resp = client.delete(
        "/activities/Test%20Activity/participants?email=alice@example.com"
    )
    assert resp.status_code == 200
    assert "alice@example.com" not in activities["Test Activity"]["participants"]
