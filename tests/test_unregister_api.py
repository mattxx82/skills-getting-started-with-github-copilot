import pytest


class TestUnregisterAPI:
    """Test suite for POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_existing_student_returns_200(self, client):
        """Test successful unregister of existing student"""
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Pre-existing participant
        
        response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert response.status_code == 200

    def test_unregister_existing_student_response_message(self, client):
        """Test that unregister response contains success message"""
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_unregister_removes_student_from_participants(self, client):
        """Test that student is removed from participants after unregister"""
        activity = "Chess Club"
        email = "daniel@mergington.edu"  # Pre-existing participant
        
        # Verify student is in participants before unregister
        activities_response = client.get("/activities")
        participants_before = activities_response.json()[activity]["participants"]
        assert email in participants_before
        
        # Unregister student
        unregister_response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert unregister_response.status_code == 200
        
        # Verify student is removed from participants
        activities_response = client.get("/activities")
        participants_after = activities_response.json()[activity]["participants"]
        assert email not in participants_after

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Test unregister from non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Activity/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_non_registered_student_returns_400(self, client):
        """Test unregister of student not registered returns 400"""
        activity = "Gym Class"
        email = "notregistered@mergington.edu"
        
        response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"].lower()

    def test_unregister_twice_same_student_returns_400(self, client):
        """Test that unregistering same student twice returns 400 on second attempt"""
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # First unregister should succeed
        response1 = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert response2.status_code == 400
        assert "not registered" in response2.json()["detail"].lower()

    def test_unregister_one_student_leaves_others(self, client):
        """Test that unregistering one student doesn't affect others"""
        activity = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"
        
        # Unregister one student
        response = client.post(
            f"/activities/{activity}/unregister?email={email_to_remove}"
        )
        assert response.status_code == 200
        
        # Verify removed student is gone but other remains
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity]["participants"]
        assert email_to_remove not in participants
        assert email_to_keep in participants
