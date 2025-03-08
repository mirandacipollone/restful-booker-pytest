import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
WRONG_USERNAME = os.getenv("WRONG_USERNAME")
WRONG_PASSWORD = os.getenv("WRONG_PASSWORD")

