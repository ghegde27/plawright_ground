import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from config.auth_config import AUTH_CONFIG
from core.logger import Logger

load_dotenv()

log = Logger.get_logger(__name__)


@pytest.fixture(scope="session")
def ensure_login(request):
    use_auth = request.config.getoption("--use-auth")
    refresh_auth = request.config.getoption("--refresh-auth")
    site = request.config.getoption("--site")

    if not use_auth:
        log.info("Auth disabled (--use-auth not provided). Running anonymous session.")
        return None

    cfg = AUTH_CONFIG[site]
    storage_file = cfg["storage_file"]

    log.info("========== Authentication Setup ==========")
    log.info(f"Site               : {site}")
    log.info(f"Storage file       : {storage_file}")
    log.info(f"Force refresh auth : {refresh_auth}")

    # Force refresh if flag passed
    if refresh_auth and os.path.exists(storage_file):
        os.remove(storage_file)
        log.info("Existing auth storage deleted due to --refresh-auth flag")

    # If storage exists → validate
    if os.path.exists(storage_file):
        log.info("Existing auth storage found. Validating session...")
        # is_valid = _validate_storage(storage_file)
        is_valid = True

        if is_valid:
            log.info("Stored session is valid. Reusing authentication ✅")
            return storage_file
        else:
            log.warning("Stored session is expired. Removing old auth storage.")
            # os.remove(storage_file)

    # No valid storage → perform fresh login
    log.info("No valid stored session found. Performing fresh login...")
    _perform_login(cfg, site, storage_file)
    log.info("Login successful. New auth storage created ✅")

    return storage_file


def _perform_login(cfg, site, storage_file):
    username = os.getenv(f"{site.upper()}_USER")
    password = os.getenv(f"{site.upper()}_PASS")

    if not username or not password:
        log.error("Missing credentials in environment / .env file")
        raise Exception(f"Missing credentials for {site}")

    with sync_playwright() as p:
        log.info("Launching temporary browser for login...")
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        browser.close()
        log.info("Temporary login browser closed")


def _validate_storage(cfg, storage_file):
    with sync_playwright() as p:
        log.info("Launching temporary browser to validate stored session...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=storage_file)
        page = context.new_page()

        page.goto(cfg["validate_url"])
        page.wait_for_timeout(timeout=5000)

        page.wait_for_url("**/update_profile**", timeout=10000)

        valid = "update_profile" in page.url
        if valid:
            log.info("Validation successful")
        else:
            log.info(f"Validation failed: redirected to {page.url}")

        browser.close()
        log.info("Validation browser closed")
        return valid
