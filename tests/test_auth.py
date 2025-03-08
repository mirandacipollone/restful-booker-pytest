import requests
import logging
from config import BASE_URL, USERNAME, PASSWORD, WRONG_USERNAME, WRONG_PASSWORD

logger = logging.getLogger(__name__)

def test_auth_valid():
    """
    TC 1.1 - Call /auth endpoint with valid credentials.
    Expect 200 OK and a valid auth token.
    """
    logger.info("\n[Test Auth Valid] Requesting valid auth token...")
    url = f"{BASE_URL}/auth"
    payload = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(url, json=payload)
    logger.info(f"[Test Auth Valid] Status: {response.status_code}")
    logger.info(f"[Test Auth Valid] Response: {response.json()}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "token" in response.json(), "No token found in response"

def test_auth_invalid():
    """
    TC 1.2 - Use invalid credentials with /auth.
    Expect 403 Forbidden.
    **Note: the implementation of the Restful booker API returns 200 OK even when credentials are invalid
    """
    logger.info("\n[Test Auth Invalid] Requesting auth token with invalid credentials...")
    url = f"{BASE_URL}/auth"
    payload = {"username": WRONG_USERNAME, "password": WRONG_PASSWORD}
    response = requests.post(url, json=payload)
    logger.info(f"[Test Auth Invalid] Status: {response.status_code}")
    logger.info(f"[Test Auth Invalid] Response: {response.text}")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
