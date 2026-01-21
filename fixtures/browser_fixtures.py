import json
import os

import pytest
from playwright.async_api import async_playwright

from core.logger import Logger

log = Logger.get_logger(__name__)


@pytest.fixture(scope="session")
def config(request):
    # 1) CLI option
    opt_env = request.config.getoption("--env")
    if opt_env:
        env = opt_env
    else:
        env = os.getenv("ENV", "dev")

    config_path = f"config/config.{env}.json"
    with open(config_path) as f:
        data = json.load(f)

    # Override capture_trace using CLI flags
    cli_trace = request.config.getoption("--capture-trace")
    cli_no_trace = request.config.getoption("--no-capture-trace")
    if cli_trace:
        data["capture_trace"] = True
    if cli_no_trace:
        data["capture_trace"] = False

    return data


@pytest.fixture(scope="function")
async def browser(request, config):
    use_cdp = request.config.getoption("--cdp")
    cdp_url = request.config.getoption("--cdp-url")

    browser_cfg = config.get("browser", {})
    browser_type = browser_cfg.get("type", "chromium")

    log.info("========== Browser Session Setup ==========")
    log.info(f"Browser type       : {browser_type}")
    log.info(f"Headless mode      : {browser_cfg.get('headless', False)}")
    log.info(f"SlowMo             : {browser_cfg.get('slowMo', 0)}")
    log.info(f"Channel            : {browser_cfg.get('channel')}")
    log.info(f"Using CDP          : {use_cdp}")

    if use_cdp:
        log.info(f"CDP Endpoint URL   : {cdp_url}")

    async with async_playwright() as p:
        browser_launcher = getattr(p, browser_type)

        try:
            if use_cdp:
                log.info("Attempting to attach to existing browser via CDP...")
                browser = await browser_launcher.connect_over_cdp(cdp_url)
                log.info("Successfully attached to existing browser session via CDP ✅")
            else:
                log.info("Launching new browser instance...")
                browser = await browser_launcher.launch(
                    headless=browser_cfg.get("headless", False),
                    slow_mo=browser_cfg.get("slowMo", 0),
                    channel=browser_cfg.get("channel"),
                    args=browser_cfg.get("args", [])
                )
                log.info("New browser launched successfully ✅")

        except Exception as e:
            log.error("Failed to initialize browser session ❌")
            log.exception(e)
            raise

        yield browser

        # Cleanup
        if not use_cdp:
            log.info("Closing browser session...")
            await browser.close()
            log.info("Browser closed successfully 🧹")
        else:
            log.info("CDP mode enabled — skipping browser close (external session)")

    log.info("========== Browser Session Finished ==========")
