import pytest


class TestSignupAPI:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_student_returns_200(self, client):
        """Test successful signup for a new student"""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200

    def test_signup_new_student_response_message(self, client):
        """Test that signup response contains success message"""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_student_appears_in_participants(self, client):
        """Test that student appears in participants after signup"""
        email = "testuser@mergington.edu"
        
        # Sign up student
        signup_response = client.post(
            f"/activities/Programming Class/signup?email={email}"
        )
        assert signup_response.status_code == 200
        
        # Verify student is in participants list
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities["Programming Class"]["participants"]
        assert email in participants

    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test signup to non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Activity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_duplicate_student_returns_400(self, client):
        """Test that signup with same email twice returns 400"""
        email = "duplicate@mergington.edu"
        activity = "Chess Club"
        
        # First signup should succeed
        response1 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"].lower()

    def test_signup_multiple_students_same_activity(self, client):
        """Test that multiple different students can sign up for same activity"""
        activity = "Gym Class"
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        
        # Sign up multiple students
        for email in emails:
            response = client.post(
                f"/activities/{activity}/signup?email={email}"
            )
            assert response.status_code == 200
        
        # Verify all are in participants
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity]["participants"]
        for email in emails:
            assert email in participants
