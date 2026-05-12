"""
Tests for participant signup and unregister endpoints.
Uses AAA (Arrange-Act-Assert) testing pattern for clarity.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provides TestClient for signup tests."""
    return TestClient(app)


class TestSignupEndpoint:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_success_new_participant(self, client):
        """
        Arrange: Define a new email and activity name.
        Act: Register the email for an activity.
        Assert: Verify 200 status and success message.
        """
        # Arrange
        email = "newstudent@test.com"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
        assert activity in response.json()["message"]
    
    def test_signup_invalid_activity_returns_404(self, client):
        """
        Arrange: Define an email and a non-existent activity.
        Act: Attempt to register for non-existent activity.
        Assert: Verify 404 status and error detail.
        """
        # Arrange
        email = "student@test.com"
        invalid_activity = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_duplicate_participant_returns_400(self, client):
        """
        Arrange: Register a participant once, then attempt to register again.
        Act: Post signup twice with the same email for the same activity.
        Assert: First succeeds (200), second fails (400).
        """
        # Arrange
        email = "duplicate@test.com"
        activity = "Tennis Club"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert - First signup succeeds
        assert response1.status_code == 200
        
        # Act - Second signup attempt
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert - Second signup fails
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"].lower()
    
    def test_signup_multiple_different_participants(self, client):
        """
        Arrange: Define two different emails.
        Act: Register both emails to the same activity.
        Assert: Both signups succeed independently.
        """
        # Arrange
        email1 = "student1@test.com"
        email2 = "student2@test.com"
        activity = "Art Studio"
        
        # Act
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email1 in response1.json()["message"]
        assert email2 in response2.json()["message"]


class TestUnregisterEndpoint:
    """Test suite for DELETE /activities/{activity_name}/participants endpoint."""
    
    def test_unregister_success(self, client):
        """
        Arrange: First signup a participant, then prepare to unregister.
        Act: Delete the participant from an activity.
        Assert: Verify 200 status and success message.
        """
        # Arrange
        email = "unregister@test.com"
        activity = "Robotics Club"
        
        # Signup first
        client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Act
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email in response.json()["message"]
    
    def test_unregister_invalid_activity_returns_404(self, client):
        """
        Arrange: Define email and non-existent activity.
        Act: Attempt to unregister from non-existent activity.
        Assert: Verify 404 status.
        """
        # Arrange
        email = "student@test.com"
        invalid_activity = "Fake Club"
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_not_registered_participant_returns_404(self, client):
        """
        Arrange: Define email that was never registered.
        Act: Attempt to unregister email that is not in participants list.
        Assert: Verify 404 status and error detail.
        """
        # Arrange
        email = "notregistered@test.com"
        activity = "Debate Team"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_then_signup_again(self, client):
        """
        Arrange: Signup, unregister, then signup again to verify state is clean.
        Act: Cycle signup -> unregister -> signup.
        Assert: All three operations succeed.
        """
        # Arrange
        email = "cycler@test.com"
        activity = "Music Band"
        
        # Act - First signup
        signup1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Unregister
        unregister = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )
        
        # Sign up again
        signup2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert signup1.status_code == 200
        assert unregister.status_code == 200
        assert signup2.status_code == 200
