from faker import Faker
import random

fake = Faker()

def generate_random_booking():
    """Returns a dict with random booking data."""
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": random.randint(50, 500),
        "depositpaid": True,
        "bookingdates": {
            "checkin": str(fake.date_this_year()),
            "checkout": str(fake.date_this_year())
        },
        "additionalneeds": fake.sentence(nb_words=3)
    }


def get_headers(token=None):
    """Returns headers. If token is provided, includes it in the Cookie header."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Cookie"] = f"token={token}"
    return headers
