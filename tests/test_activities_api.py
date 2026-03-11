import pytest


class TestActivitiesAPI:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns a 200 status code"""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary of activities"""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_expected_structure(self, client):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        activities = response.json()
        
        # Check if at least one activity exists
        assert len(activities) > 0
        
        # Verify structure of first activity
        first_activity = next(iter(activities.values()))
        assert "description" in first_activity
        assert "schedule" in first_activity
        assert "max_participants" in first_activity
        assert "participants" in first_activity

    def test_get_activities_participants_is_list(self, client):
        """Test that participants field is a list"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity in activities.values():
            assert isinstance(activity["participants"], list)

    def test_get_activities_max_participants_is_int(self, client):
        """Test that max_participants is an integer"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity in activities.values():
            assert isinstance(activity["max_participants"], int)
            assert activity["max_participants"] > 0
