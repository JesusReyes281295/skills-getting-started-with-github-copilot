"""
Tests for activities listing and root endpoint.
Uses AAA (Arrange-Act-Assert) testing pattern for clarity.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provides TestClient for activities tests."""
    return TestClient(app)


class TestGetActivities:
    """Test suite for GET /activities endpoint."""
    
    def test_get_activities_returns_200_and_dict(self, client):
        """
        Arrange: No special setup needed; activities pre-populated in app.
        Act: Make GET request to /activities.
        Assert: Verify status 200 and response is a dictionary.
        """
        # Arrange & Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
    
    def test_get_activities_contains_expected_activities(self, client):
        """
        Arrange: No special setup needed.
        Act: Fetch all activities.
        Assert: Verify expected activities are present in response.
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
    
    def test_get_activities_includes_full_activity_details(self, client):
        """
        Arrange: No special setup needed.
        Act: Fetch activities and inspect a specific one.
        Assert: Verify activity has required fields (description, schedule, max_participants, participants).
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        # Assert
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)


class TestRootEndpoint:
    """Test suite for GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """
        Arrange: Prepare client with follow_redirects disabled.
        Act: Make GET request to /.
        Assert: Verify redirect status and location header.
        """
        # Arrange & Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code in [301, 302, 307]
        assert "/static/index.html" in response.headers.get("location", "")
