import requests
import pytest
import logging
from config import BASE_URL
from utils import generate_random_booking

# Set up logger for this module
logger = logging.getLogger(__name__)

@pytest.mark.malformed
def test_create_booking_missing_required_field():
    """
    Test creating a booking with a missing required field.

    """
    logger.info("[Test Malformed] Creating booking with missing 'firstname' field...")
    payload = generate_random_booking()
    removed = payload.pop("firstname", None)
    assert removed is not None, "Expected 'firstname' to be present in the generated payload"
    
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    logger.info(f"[Test Malformed] Status code: {response.status_code}")
    logger.info(f"[Test Malformed] Response: {response.text}")
    
    assert response.status_code == 500, f"Expected 500 for missing required field, got {response.status_code}"

@pytest.mark.malformed
def test_create_booking_invalid_data_type():
    """
    Test creating a booking with an invalid data type for a field.

    """
    logger.info("[Test Malformed] Creating booking with invalid data type for 'totalprice'")
    payload = generate_random_booking()
    payload["totalprice"] = "invalid_price"  # invalid data type
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    logger.info(f"[Test Malformed] Status code: {response.status_code}")
    logger.info(f"[Test Malformed] Response: {response.text}")

    if response.status_code == 200:
        data = response.json().get("booking", {})
        assert data.get("totalprice") is None, "Expected totalprice to be null for invalid data type"
    else:
        assert response.status_code == 400, f"Expected 400 for invalid data type, got {response.status_code}"

@pytest.mark.malformed
def test_create_booking_invalid_bookingdates():
    """
    Test creating a booking with an invalid structure for bookingdates.

    """
    logger.info("[Test Malformed] Creating booking with invalid 'bookingdates' structure")
    payload = generate_random_booking()
    payload["bookingdates"] = "malformed"  # invalid structure
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    logger.info(f"[Test Malformed] Status code: {response.status_code}")
    logger.info(f"[Test Malformed] Response: {response.text}")
    
    assert response.status_code == 500, f"Expected 500 for invalid bookingdates structure, got {response.status_code}"

@pytest.mark.malformed
def test_update_booking_invalid_payload(create_booking, auth_token):
    """
    Test updating an existing booking with an invalid payload.
    
    """
    booking_id, original_payload = create_booking
    logger.info(f"[Test Malformed] Updating booking ID {booking_id} with invalid payload missing 'lastname'")
    url = f"{BASE_URL}/booking/{booking_id}"
    headers = {"Cookie": f"token={auth_token}"}
    invalid_payload = original_payload.copy()
    removed = invalid_payload.pop("lastname", None)
    assert removed is not None, "Expected 'lastname' to be present in the original payload"
    
    response = requests.put(url, json=invalid_payload, headers=headers)
    logger.info(f"[Test Malformed] Update response status: {response.status_code}")
    logger.info(f"[Test Malformed] Update response: {response.text}")
    
    assert response.status_code == 400, f"Expected 400 for invalid update payload, got {response.status_code}"
