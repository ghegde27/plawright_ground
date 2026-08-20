# Playwright Pytest Automation Framework

A scalable Playwright + Pytest automation framework supporting:

- UI automation with Playwright sync API
- Config-driven environment setup
- Optional authentication reuse (storage state)
- CDP attachment to existing browser
- Tracing, HAR, Video, Screenshot capture
- Allure reporting
- Structured logging
- .env based credential management

---

## Tech Stack

- Python 3.9+
- Playwright (Sync API)
- Pytest
- Allure Reports
- Python-dotenv
- Custom Logging
- Config JSON based environments

---

## Project Structure

play_right/
│
├── config/
│   ├── config.dev.json
│   ├── config.qa.json
│   └── auth_config.py
│
├── core/
│   └── logger.py
│
├── fixtures/
│   ├── browser_fixtures.py
│   ├── context_fixtures.py
│   ├── page_fixtures.py
│   └── auth_fixtures.py
│
├── tests/
│   └── test_sample.py
│
├── logs/
├── allure-results/
├── .env
├── .gitignore
├── pytest.ini
└── README.md

---

## Installation

### 1) Clone repository

git clone https://github.com/ghegde27/play_right.git  
cd play_right

### 2) Create virtual environment

python -m venv venv  
source venv/bin/activate      # Mac/Linux  
venv\Scripts\activate         # Windows

### 3) Install dependencies

pip install -r requirements.txt

### 4) Install Playwright browsers

playwright install

---

## Environment Configuration

Environment configs are stored in:

config/config.dev.json  
config/config.qa.json

Example:

{
  "base_url": "https://www.linkedin.com",
  "capture_trace": false,
  "capture_har": false,
  "capture_video": false,
  "capture_screenshot": true,

  "browser": {
    "type": "chromium",
    "headless": false,
    "slowMo": 0,
    "channel": "chrome",
    "args": []
  }
}

Select environment:

pytest --env=dev  
pytest --env=qa

---

## Credential Management (.env)

Create a .env file in project root:

LINKEDIN_USER=your_email@example.com  
LINKEDIN_PASS=your_password

.env is ignored by Git for security.

---

## Authentication Reuse

Run with saved authentication:

pytest --use-auth --site=linkedin

Force regenerate login session:

pytest --use-auth --refresh-auth --site=linkedin

Run without authentication:

pytest

---

## Attach to Existing Browser (CDP Mode)

Launch Chrome manually:

google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile

Then run:

pytest --cdp --cdp-url=http://localhost:9222

---

## Reports

Generate Allure report:

pytest  
allure serve allure-results

---

## Logging

Logs are stored in:

logs/automation.log

---

## Parallel Execution

Use pytest-xdist workers:

pytest -n 4

---

## Author

Gopalkrishna Hegde
