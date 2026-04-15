import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (No special setup needed)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    client.delete(f"/activities/{activity}/unregister?email={test_email}")  # Ensure clean state

    # Act & Assert: Sign up
    response_signup = client.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response_signup.status_code == 200
    assert f"Signed up {test_email}" in response_signup.json()["message"]

    # Act & Assert: Duplicate sign up should fail
    response_duplicate = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response_duplicate.status_code == 400

    # Act & Assert: Unregister
    response_unreg = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response_unreg.status_code == 200
    assert f"Removed {test_email}" in response_unreg.json()["message"]

    # Act & Assert: Unregister again should fail
    response_unreg_again = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response_unreg_again.status_code == 404
