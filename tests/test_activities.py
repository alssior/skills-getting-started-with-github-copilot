"""Tests for the activities endpoints"""
import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""
    
    def test_get_activities_returns_list(self, client, reset_activities):
        """Test that get_activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
    
    def test_get_activities_contains_expected_activities(self, client, reset_activities):
        """Test that activities list contains expected activity names"""
        response = client.get("/activities")
        data = response.json()
        
        expected_activities = [
            "Basketball", "Soccer", "Art Club", "Drama Club",
            "Debate Team", "Science Club", "Chess Club",
            "Programming Class", "Gym Class"
        ]
        
        for activity in expected_activities:
            assert activity in data
    
    def test_get_activities_activity_structure(self, client, reset_activities):
        """Test that each activity has the expected structure"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestRootEndpoint:
    """Test suite for GET / endpoint"""
    
    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
