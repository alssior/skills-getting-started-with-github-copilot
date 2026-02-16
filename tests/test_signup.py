"""Tests for the signup functionality"""
import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_student_success(self, client, reset_activities):
        """Test successful signup of a new student"""
        response = client.post(
            "/activities/Basketball/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]
        assert "Basketball" in data["message"]
    
    def test_signup_nonexistent_activity(self, client, reset_activities):
        """Test signup for a non-existent activity"""
        response = client.post(
            "/activities/Nonexistent/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_duplicate_student(self, client, reset_activities):
        """Test that a student cannot sign up twice for the same activity"""
        # Try to signup an already enrolled student
        response = client.post(
            "/activities/Basketball/signup",
            params={"email": "james@mergington.edu"}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_multiple_students(self, client, reset_activities):
        """Test that multiple different students can sign up"""
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        
        for email in emails:
            response = client.post(
                "/activities/Soccer/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all students are in the activity
        activities_response = client.get("/activities")
        soccer = activities_response.json()["Soccer"]
        for email in emails:
            assert email in soccer["participants"]
    
    def test_signup_different_activities(self, client, reset_activities):
        """Test that a student can sign up for multiple activities"""
        email = "multisport@mergington.edu"
        activities_to_join = ["Basketball", "Soccer", "Art Club"]
        
        for activity in activities_to_join:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify student is in all activities
        activities_response = client.get("/activities")
        data = activities_response.json()
        for activity in activities_to_join:
            assert email in data[activity]["participants"]
    
    def test_signup_updates_participants_list(self, client, reset_activities):
        """Test that signup properly updates the participants list"""
        email = "newemail@mergington.edu"
        
        # Get initial count
        response = client.get("/activities")
        initial_count = len(response.json()["Art Club"]["participants"])
        
        # Sign up
        client.post(
            "/activities/Art Club/signup",
            params={"email": email}
        )
        
        # Get updated count
        response = client.get("/activities")
        updated_count = len(response.json()["Art Club"]["participants"])
        
        assert updated_count == initial_count + 1
