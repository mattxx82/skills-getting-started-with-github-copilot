import pytest
from fastapi.testclient import TestClient
from src.app import app


def get_test_activities():
    """
    Provides fresh test activities data for each test.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    }


@pytest.fixture
def client():
    """
    Provides a TestClient instance with isolated test data for each test.
    Uses dependency injection to override the app's activities dictionary.
    """
    # Reset app state before each test
    test_activities = get_test_activities()
    
    # Override the activities dictionary in the app
    app.dependency_overrides.clear()
    original_activities = app.__dict__.get('activities_backup')
    
    # Directly override the module-level activities
    import src.app
    src.app.activities = test_activities
    
    client = TestClient(app)
    
    yield client
    
    # Cleanup after test
    if original_activities:
        src.app.activities = original_activities


@pytest.fixture
def sample_activities():
    """
    Provides sample activity data for tests.
    """
    return get_test_activities()
