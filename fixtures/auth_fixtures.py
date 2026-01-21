import os
import pytest
from playwright.async_api import async_playwright
from config.auth_config import AUTH_CONFIG
from core.logger import Logger

log = Logger.get_logger(__name__)


@pytest.fixture(scope="session")
async def ensure_login(request):
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
        is_valid = await _validate_storage(cfg, storage_file)

        if is_valid:
            log.info("Stored session is valid. Reusing authentication ✅")
            return storage_file
        else:
            log.warning("Stored session is expired. Removing old auth storage.")
            os.remove(storage_file)

    # No valid storage → perform fresh login
    log.info("No valid stored session found. Performing fresh login...")
    await _perform_login(cfg, site, storage_file)
    log.info("Login successful. New auth storage created ✅")

    return storage_file


async def _perform_login(cfg, site, storage_file):
    username = os.getenv(f"{site.upper()}_USER")
    password = os.getenv(f"{site.upper()}_PASS")

    if not username or not password:
        log.error("Missing credentials in environment / .env file")
        raise Exception(f"Missing credentials for {site}")

    async with async_playwright() as p:
        log.info("Launching temporary browser for login...")
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        log.info(f"Navigating to login page: {cfg['login_url']}")
        await page.goto(cfg["login_url"])

        await page.fill(cfg["username_selector"], username)
        await page.fill(cfg["password_selector"], password)
        await page.click(cfg["submit_selector"])

        log.info("Waiting for successful login redirect...")
        await page.wait_for_url(cfg["success_url"])

        await context.storage_state(path=storage_file)
        log.info(f"Auth storage saved to: {storage_file}")

        await browser.close()
        log.info("Temporary login browser closed")


async def _validate_storage(cfg, storage_file):
    async with async_playwright() as p:
        log.info("Launching temporary browser to validate stored session...")
        browser = await p.chromium.launch()
        context = await browser.new_context(storage_state=storage_file)
        page = await context.new_page()

        await page.goto(cfg["validate_url"])

        try:
            await page.wait_for_selector(cfg["validate_selector"], timeout=5000)
            log.info("Validation check passed — user is logged in")
            valid = True
        except:
            log.warning("Validation check failed — login session expired")
            valid = False

        await browser.close()
        log.info("Validation browser closed")

        return valid
