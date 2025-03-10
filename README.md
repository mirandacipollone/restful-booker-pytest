# API Automation Challenge - Pytest Test Suite + Postman Collection - Miranda Cipollone

## Overview 
This repository contains an automated API test suite for the Restful Booker API (https://restful-booker.herokuapp.com/apidoc/index.html).
Dynamic test data is generated using [Faker](https://faker.readthedocs.io/) and environment variables are managed via [python-dotenv](https://pypi.org/project/python-dotenv/). 
Detailed HTML reports can be generated using [pytest-html](https://github.com/pytest-dev/pytest-html).

## Prerequisites - 
**Python 3.7 or higher** – Verify by running:  python --version

**Virtual Environment** – Recommended for isolating dependencies.

**Git**

_**Installation**_

**1.Clone the Repository**

git clone https://github.com/mirandacipollone/restful-booker-pytest.git 

**2.Create and Activate a Virtual Environment**

python3 -m venv venv

**macOS**

source venv/bin/activate

**Windows**

venv\Scripts\activate

**3.Install Dependencies**

pip install -r requirements.txt


**Basic Test Run**

pytest --maxfail=1 --disable-warnings -q

**Detailed Run with Logging and HTML Report**

pytest -s -v --log-cli-level=INFO --html=reports/report.html --self-contained-html


**Troubleshooting**

**Module Not Found / Import Errors**: Ensure your virtual environment is activated and dependencies are installed.

**Environment Variables Not Loading**: Confirm that the .env file exists and load_dotenv() is called in config.py.

**Test Failures**: Verify that endpoints, request methods, and headers are correct. Ensure no unwanted authentication is applied to public endpoints.

**Missing Logs in HTML Report**: Run tests with --log-cli-level=INFO or configure logging via pytest.ini.


## Postman Collection

This project also includes a Postman collection for API testing of the Sauce Demo site. Follow these steps to import and use the collection:

Locate the Collection File
The collection file is located in the root directory -- postman/ directory

## Import into Postman

**Open Postman.**

1- Drag and drop the collection json file into the import window or click “Upload Files” and select it.

2- Drag and drop the environment json file into postman

3- Select the environment from the top right of Postman and verify that the variables are correctly set.

**Run the Collection**

1- Select the imported collection in the left sidebar.

2- Click the Run Collection button to open the Collection Runner.

3- Adjust any settings if necessary (such as number of iterations or delay between requests).

4-Click Start Run to execute the API tests.


Once the collection run completes, you can view detailed test results within Postman.


