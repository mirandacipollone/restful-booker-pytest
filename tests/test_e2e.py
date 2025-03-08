import requests
import pytest
import logging
from faker import Faker
from config import BASE_URL, USERNAME, PASSWORD
from utils import generate_random_booking, get_headers

logger = logging.getLogger(__name__)
fake = Faker()

@pytest.mark.endtoend
def test_end_to_end_booking_flow():
    """
    e2e scenario:
      1. Create a booking
      2. Retrieve the booking and validate details.
      3. Authenticate to get a valid token.
      4. Update the booking with new data.
      5. Retrieve the updated booking and validate changes.
      6. Partially update the booking (PATCH) to change only the 'firstname'.
      7. Delete the booking.
      8. Confirm the booking is no longer retrievable.
    """

    # 1: Create a booking
    logger.info("\n[End-to-End] Creating booking")
    create_url = f"{BASE_URL}/booking"
    booking_payload = generate_random_booking()
    create_response = requests.post(create_url, json=booking_payload)
    assert create_response.status_code == 200, f"Expected 200, got {create_response.status_code}"
    booking_id = create_response.json()["bookingid"]
    logger.info(f"[End-to-End] Created booking with ID: {booking_id}")
    
    # 2: Retrieve the booking and validate details
    retrieve_url = f"{BASE_URL}/booking/{booking_id}"
    retrieve_response = requests.get(retrieve_url)
    assert retrieve_response.status_code == 200, f"Expected 200, got {retrieve_response.status_code}"
    retrieved_data = retrieve_response.json()
    logger.info(f"[End-to-End] Retrieved booking data: {retrieved_data}")
    # Validate each key from the original payload
    for key in booking_payload:
        if key == "bookingdates":
            assert retrieved_data["bookingdates"]["checkin"] == booking_payload["bookingdates"]["checkin"], "Checkin date mismatch"
            assert retrieved_data["bookingdates"]["checkout"] == booking_payload["bookingdates"]["checkout"], "Checkout date mismatch"
        else:
            assert retrieved_data[key] == booking_payload[key], f"Mismatch in {key}: expected {booking_payload[key]}, got {retrieved_data[key]}"
    
    # 3: Authenticate to get a token for update/deletion
    logger.info("\n[End-to-End] Authenticating for updates")
    auth_url = f"{BASE_URL}/auth"
    auth_payload = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(auth_url, json=auth_payload)
    assert auth_response.status_code == 200, f"Expected 200, got {auth_response.status_code}"
    token = auth_response.json()["token"]
    logger.info(f"[End-to-End] Received token: {token}")
    headers = get_headers(token)
    
    # Step 4: Update the booking with new data
    logger.info("\n[End-to-End] Updating booking with new data")
    update_url = f"{BASE_URL}/booking/{booking_id}"
    update_payload = generate_random_booking()  # new random data for update
    update_response = requests.put(update_url, json=update_payload, headers=headers)
    assert update_response.status_code == 200, f"Expected 200, got {update_response.status_code}"
    updated_data = update_response.json()
    logger.info(f"[End-to-End] Updated booking data: {updated_data}")
    # Validate update by comparing fields
    for key in update_payload:
        if key == "bookingdates":
            assert updated_data["bookingdates"]["checkin"] == update_payload["bookingdates"]["checkin"], "Checkin date not updated"
            assert updated_data["bookingdates"]["checkout"] == update_payload["bookingdates"]["checkout"], "Checkout date not updated"
        else:
            assert updated_data[key] == update_payload[key], f"{key} not updated correctly"
    
    # Step 5: Retrieve updated booking for extra validation
    get_updated_response = requests.get(update_url)
    assert get_updated_response.status_code == 200, f"Expected 200, got {get_updated_response.status_code}"
    logger.info(f"[End-to-End] Retrieved updated booking: {get_updated_response.json()}")
    
    # Step 6: Partially update the booking
    logger.info("\n[End-to-End] Partially updating booking")
    partial_payload = {"firstname": "PartialUpdateName"}
    patch_response = requests.patch(update_url, json=partial_payload, headers=headers)
    assert patch_response.status_code == 200, f"Expected 200, got {patch_response.status_code}"
    patched_data = patch_response.json()
    logger.info(f"[End-to-End] Patched booking data: {patched_data}")
    assert patched_data["firstname"] == "PartialUpdateName", "Firstname was not updated in PATCH"
    # Verify other fields remain unchanged by comparing with update_payload
    for key in update_payload:
        if key != "firstname":
            if key == "bookingdates":
                assert patched_data["bookingdates"]["checkin"] == update_payload["bookingdates"]["checkin"], "Checkin changed unexpectedly"
                assert patched_data["bookingdates"]["checkout"] == update_payload["bookingdates"]["checkout"], "Checkout changed unexpectedly"
            else:
                assert patched_data[key] == update_payload[key], f"{key} changed unexpectedly"
    
    # Step 7: Delete the booking
    logger.info("\n[End-to-End] Deleting booking")
    delete_response = requests.delete(update_url, headers=headers)
    assert delete_response.status_code == 201, f"Expected 201, got {delete_response.status_code}"
    logger.info(f"[End-to-End] Booking deleted. Status: {delete_response.status_code}")
    
    # Step 8: Confirm deletion by attempting to retrieve the booking
    logger.info("\n[End-to-End] Confirming deletion of booking")
    confirm_response = requests.get(retrieve_url)
    assert confirm_response.status_code == 404, f"Expected 404, got {confirm_response.status_code}"
    logger.info(f"[End-to-End] Deletion confirmed. Retrieval status: {confirm_response.status_code}")
