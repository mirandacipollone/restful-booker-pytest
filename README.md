# API Automation Challenge - Pytest Test Suite - Miranda Cipollone

## Overview 
This repository contains an automated API test suite for the Restful Booker API (https://restful-booker.herokuapp.com/apidoc/index.html).
Dynamic test data is generated using [Faker](https://faker.readthedocs.io/) and environment variables are managed via [python-dotenv](https://pypi.org/project/python-dotenv/). 
Detailed HTML reports can be generated using [pytest-html](https://github.com/pytest-dev/pytest-html).

## Prerequisites - 
**Python 3.7 or higher** – Verify by running:  python --version
Virtual Environment – Recommended for isolating dependencies.
Git

Installation

1.Clone the Repository 

git clone https://github.com/mirandacipollone/restful-booker-pytest.git 

2.Create and Activate a Virtual Environment

python3 -m venv venv

macOS
source venv/bin/activate

Windows
venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt


Basic Test Run

pytest --maxfail=1 --disable-warnings -q

Detailed Run with Logging and HTML Report

pytest -s -v --log-cli-level=INFO --html=reports/report.html --self-contained-html


Troubleshooting
	•	Module Not Found / Import Errors: Ensure your virtual environment is activated and dependencies are installed.
	•	Environment Variables Not Loading: Confirm that the .env file exists and load_dotenv() is called in config.py.
	•	Test Failures: Verify that endpoints, request methods, and headers are correct. Ensure no unwanted authentication is applied to public endpoints.
	•	Missing Logs in HTML Report: Run tests with --log-cli-level=INFO or configure logging via pytest.ini.
