import requests
import logging
from config import BASE_URL
from utils import get_headers, generate_random_booking

logger = logging.getLogger(__name__)

def test_create_booking_and_validate():
    """
    TC 2.1 & TC 2.2: Create booking with random data and validate by retrieving it.
    Checks that a booking ID is returned and the details match the generated data.
    """
    logger.info("\n[TC 2.1] Creating a booking with random data...")
    url = f"{BASE_URL}/booking"
    payload = generate_random_booking()
    response = requests.post(url, json=payload)
    logger.info(f"[TC 2.1] Create booking status: {response.status_code}")
    logger.info(f"[TC 2.1] Response JSON: {response.json()}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    booking_id = response.json()["bookingid"]
    assert isinstance(booking_id, int), "Booking id is not an integer"
    
    # Retrieve booking to validate details
    get_url = f"{BASE_URL}/booking/{booking_id}"
    get_response = requests.get(get_url)
    logger.info(f"[TC 2.2] Retrieve booking status: {get_response.status_code}")
    logger.info(f"[TC 2.2] Response JSON: {get_response.json()}")
    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    booking_data = get_response.json()
    # Validate each field matches the payload generated earlier
    assert booking_data["firstname"] == payload["firstname"], "Firstname does not match"
    assert booking_data["lastname"] == payload["lastname"], "Lastname does not match"
    assert booking_data["totalprice"] == payload["totalprice"], "Total price does not match"
    assert booking_data["depositpaid"] == payload["depositpaid"], "Deposit paid does not match"
    assert booking_data["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"], "Checkin date does not match"
    assert booking_data["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"], "Checkout date does not match"
    assert booking_data["additionalneeds"] == payload["additionalneeds"], "Additional needs do not match"

def test_retrieve_invalid_booking():
    """
    TC 2.3 - Call /booking/{non-existent-id} to get 404 Not Found.
    """
    logger.info("\n[TC 2.3] Retrieving non-existent booking...")
    invalid_id = 999999999
    url = f"{BASE_URL}/booking/{invalid_id}"
    response = requests.get(url)
    logger.info(f"[TC 2.3] Status: {response.status_code}")
    logger.info(f"[TC 2.3] Response text: {response.text}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"

def test_update_booking(create_booking, auth_token):
    """
    TC 3.1 - Update an existing booking with a valid token.
    Then retrieve the booking to validate that changes are applied.
    """
    booking_id, original_payload = create_booking
    logger.info(f"\n[TC 3.1] Updating booking ID: {booking_id} with valid token...")
    url = f"{BASE_URL}/booking/{booking_id}"
    headers = get_headers(auth_token)
    # Create a new payload for update; here we change the firstname and increase totalprice.
    update_payload = {
        "firstname": "Juan Actualizado",
        "lastname": original_payload["lastname"],  # keep lastname for comparison
        "totalprice": original_payload["totalprice"] + 50,
        "depositpaid": original_payload["depositpaid"],
        "bookingdates": original_payload["bookingdates"],
        "additionalneeds": "Desayuno y Cena"
    }
    response = requests.put(url, json=update_payload, headers=headers)
    logger.info(f"[TC 3.1] Update response status: {response.status_code}")
    logger.info(f"[TC 3.1] Update response JSON: {response.json()}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # Validate update by retrieving booking
    get_response = requests.get(url)
    logger.info(f"[TC 3.1] Retrieve updated booking status: {get_response.status_code}")
    updated_data = get_response.json()
    logger.info(f"[TC 3.1] Updated booking data: {updated_data}")
    assert updated_data["firstname"] == update_payload["firstname"], "Firstname not updated"
    assert updated_data["totalprice"] == update_payload["totalprice"], "Total price not updated"

def test_unauthorized_update(create_booking):
    """
    TC 3.2 - Attempt to update booking without a valid token.
    Expected result: 403 Forbidden.
    """
    booking_id, _ = create_booking
    logger.info(f"\n[TC 3.2] Attempting unauthorized update on booking ID: {booking_id}...")
    url = f"{BASE_URL}/booking/{booking_id}"
    payload = {"firstname": "ShouldNotUpdate"}
    response = requests.put(url, json=payload)  # No token header provided
    logger.info(f"[TC 3.2] Response status: {response.status_code}")
    logger.info(f"[TC 3.2] Response text: {response.text}")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"

def test_delete_booking(create_booking, auth_token):
    """
    TC 4.1 - Delete booking with a valid token.
    Expected result: 201 Created; subsequent retrieval should yield 404.
    """
    booking_id, _ = create_booking
    logger.info(f"\n[TC 4.1] Deleting booking ID: {booking_id} with valid token...")
    url = f"{BASE_URL}/booking/{booking_id}"
    headers = get_headers(auth_token)
    response = requests.delete(url, headers=headers)
    logger.info(f"[TC 4.1] Delete response status: {response.status_code}")
    logger.info(f"[TC 4.1] Delete response text: {response.text}")
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
    # Verify booking no longer exists
    get_response = requests.get(url)
    logger.info(f"[TC 4.1] Retrieve deleted booking status: {get_response.status_code}")
    logger.info(f"[TC 4.1] Retrieve deleted booking text: {get_response.text}")
    assert get_response.status_code == 404, "Booking still exists after deletion"

def test_unauthorized_deletion(create_booking):
    """
    TC 4.2 - Attempt to delete booking without a valid token.
    Expected result: 403 Forbidden.
    """
    booking_id, _ = create_booking
    logger.info(f"\n[TC 4.2] Attempting unauthorized deletion on booking ID: {booking_id}...")
    url = f"{BASE_URL}/booking/{booking_id}"
    response = requests.delete(url)  # No token header provided
    logger.info(f"[TC 4.2] Response status: {response.status_code}")
    logger.info(f"[TC 4.2] Response text: {response.text}")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"

def test_partial_update_booking(create_booking, auth_token):
    """
    TC 5.1 - Partially update booking by modifying only the 'firstname' field.
    Validate that only the specified field is updated and others remain unchanged.
    """
    booking_id, original_payload = create_booking
    logger.info(f"\n[TC 5.1] Partially updating booking ID: {booking_id}...")
    url = f"{BASE_URL}/booking/{booking_id}"
    headers = get_headers(auth_token)
    payload = {"firstname": "Nombre Parcial"}
    response = requests.patch(url, json=payload, headers=headers)
    logger.info(f"[TC 5.1] PATCH response status: {response.status_code}")
    logger.info(f"[TC 5.1] PATCH response JSON: {response.json()}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # Retrieve to validate partial update
    get_response = requests.get(url)
    updated_data = get_response.json()
    logger.info(f"[TC 5.1] Retrieve after PATCH status: {get_response.status_code}")
    logger.info(f"[TC 5.1] Retrieve after PATCH JSON: {updated_data}")
    assert updated_data["firstname"] == payload["firstname"], "Firstname not partially updated"
    # Ensure other fields remain unchanged (for example, lastname should be the same as in original_payload)
    assert updated_data["lastname"] == original_payload["lastname"], "Lastname should not have changed"
