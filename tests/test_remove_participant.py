"""Tests for the remove participant functionality"""
import pytest


class TestRemoveParticipant:
    """Test suite for DELETE /activities/{activity_name}/participants/{email} endpoint"""
    
    def test_remove_existing_participant_success(self, client, reset_activities):
        """Test successful removal of an existing participant"""
        response = client.delete(
            "/activities/Basketball/participants/james@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Removed" in data["message"]
        assert "james@mergington.edu" in data["message"]
    
    def test_remove_nonexistent_activity(self, client, reset_activities):
        """Test removal from a non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent/participants/student@mergington.edu"
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_remove_nonexistent_participant(self, client, reset_activities):
        """Test removal of a participant who is not in the activity"""
        response = client.delete(
            "/activities/Basketball/participants/notinactivity@mergington.edu"
        )
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
    
    def test_remove_updates_participants_list(self, client, reset_activities):
        """Test that removal properly updates the participants list"""
        # Get initial count
        response = client.get("/activities")
        initial_count = len(response.json()["Soccer"]["participants"])
        
        # Remove a participant
        client.delete(
            "/activities/Soccer/participants/alex@mergington.edu"
        )
        
        # Get updated count
        response = client.get("/activities")
        updated_count = len(response.json()["Soccer"]["participants"])
        
        assert updated_count == initial_count - 1
        assert "alex@mergington.edu" not in response.json()["Soccer"]["participants"]
    
    def test_remove_then_signup_again(self, client, reset_activities):
        """Test that a participant can sign up again after being removed"""
        email = "james@mergington.edu"
        
        # Remove
        response = client.delete(
            f"/activities/Basketball/participants/{email}"
        )
        assert response.status_code == 200
        
        # Try to sign up again
        response = client.post(
            "/activities/Basketball/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify they're back in
        response = client.get("/activities")
        assert email in response.json()["Basketball"]["participants"]
    
    def test_remove_multiple_participants(self, client, reset_activities):
        """Test removing multiple participants from the same activity"""
        emails_to_remove = ["james@mergington.edu"]  # Only one participant in Basketball initially
        
        # Sign up additional participants
        for i in range(3):
            client.post(
                "/activities/Basketball/signup",
                params={"email": f"newplayer{i}@mergington.edu"}
            )
        
        # Remove one
        response = client.delete(
            "/activities/Basketball/participants/james@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify state
        response = client.get("/activities")
        participants = response.json()["Basketball"]["participants"]
        assert "james@mergington.edu" not in participants
        assert len([p for p in participants if p.startswith("newplayer")]) == 3
