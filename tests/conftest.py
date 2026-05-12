"""
Shared test fixtures and utilities using pytest.
Implements state isolation through autouse fixture to reset in-memory activities database.
"""
import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that runs before and after each test to reset the in-memory activities database.
    This ensures test isolation and prevents state leakage between tests.
    """
    # Store original activities snapshot
    original_activities = copy.deepcopy(activities)
    
    yield
    
    # Restore original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def client():
    """
    Provides a TestClient for the FastAPI app for all tests.
    """
    return TestClient(app)
