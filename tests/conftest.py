"""
Shared test configuration and fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a known state before each test."""
    activities.clear()
    activities.update({
        "Test Activity": {
            "description": "A test activity for unit testing",
            "schedule": "Monday 3:00 PM",
            "max_participants": 5,
            "participants": ["alice@example.com", "bob@example.com"],
        },
        "Another Activity": {
            "description": "Another test activity",
            "schedule": "Tuesday 4:00 PM",
            "max_participants": 3,
            "participants": ["carol@example.com"],
        },
    })

    yield

    activities.clear()


@pytest.fixture
def test_activities_data():
    """Provide reference to the activities dictionary for assertions."""
    return activities
