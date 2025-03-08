import logging
import pytest
import requests
from config import BASE_URL, USERNAME, PASSWORD
from utils import generate_random_booking

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def auth_token():
    """
    TC 1.1: Fixture to obtain a valid authentication token.
    logger.infos detailed info for reporting.
    """
    logger.info("\n[Fixture] Requesting auth token with valid credentials...")
    url = f"{BASE_URL}/auth"
    payload = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(url, json=payload)
    logger.info(f"[Fixture] Auth response status: {response.status_code}")
    logger.info(f"[Fixture] Auth response JSON: {response.json()}")
    assert response.status_code == 200, "Authentication failed"
    token = response.json()["token"]
    logger.info(f"[Fixture] Received token: {token}")
    return token

@pytest.fixture
def create_booking():
    """
    TC 2.1: Fixture to create a booking using randomized data and return its ID along with the payload.
    logger.infos details of the creation.
    """
    logger.info("\n[Fixture] Creating a new booking with random data...")
    url = f"{BASE_URL}/booking"
    payload = generate_random_booking()
    response = requests.post(url, json=payload)
    logger.info(f"[Fixture] Create booking response status: {response.status_code}")
    logger.info(f"[Fixture] Create booking response JSON: {response.json()}")
    assert response.status_code == 200, "Booking creation failed"
    booking_id = response.json()["bookingid"]
    logger.info(f"[Fixture] Created booking with ID: {booking_id}")
    # Return both the booking_id and the payload used so we can validate later
    yield booking_id, payload
    # Optional teardown: delete the booking if needed.
