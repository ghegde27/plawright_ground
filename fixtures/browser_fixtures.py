import json
import os
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from core.logger import Logger

log = Logger.get_logger(__name__)


# =====================================================
# Config Loader Fixture
# =====================================================
@pytest.fixture(scope="session")
def config(request):
    # Resolve environment
    env = request.config.getoption("--env") or os.getenv("ENV", "dev")
    PROJECT_ROOT = Path(__file__).parent.parent
    config_path = f"{PROJECT_ROOT}/config/config.{env}.json"

    log.info(f"Loading config: {config_path}")

    with open(config_path) as f:
        data = json.load(f)

    # Override trace flags via CLI
    if request.config.getoption("--capture-trace"):
        data["capture_trace"] = True
    if request.config.getoption("--no-capture-trace"):
        data["capture_trace"] = False

    return data


# =====================================================
# Browser Fixture
# =====================================================
@pytest.fixture(scope="function")
def browser(request, config):
    browser_cfg = config.get("browser", {})

    browser_type = browser_cfg.get("type", "chromium")
    headless = browser_cfg.get("headless", False)
    slowmo = browser_cfg.get("slowMo", 0)
    channel = browser_cfg.get("channel")
    args = browser_cfg.get("args", [])

    use_cdp = request.config.getoption("--cdp")
    cdp_url = request.config.getoption("--cdp-url")

    log.info("========== Browser Session Setup ==========")
    log.info(f"Browser Type   : {browser_type}")
    log.info(f"Headless       : {headless}")
    log.info(f"SlowMo         : {slowmo}")
    log.info(f"Channel        : {channel}")
    log.info(f"Args           : {args}")
    log.info(f"Using CDP      : {use_cdp}")

    with sync_playwright() as p:
        browser_launcher = getattr(p, browser_type)

        try:
            # --- CDP Attach Mode ---
            if use_cdp:
                if not cdp_url:
                    raise ValueError("CDP mode enabled but --cdp-url not provided")

                log.info(f"Attaching to existing browser at {cdp_url} ...")
                browser = browser_launcher.connect_over_cdp(cdp_url)
                log.info("Attached to external browser session via CDP ✅")

            # --- Normal Launch Mode ---
            else:
                log.info("Launching new browser instance...")
                browser = browser_launcher.launch(
                    headless=headless,
                    slow_mo=slowmo,
                    channel=channel,
                    args=args
                )
                log.info("Browser launched successfully ✅")

        except Exception:
            log.exception("Failed to initialize browser session ❌")
            raise

        yield browser

        # --- Cleanup ---
        if not use_cdp:
            log.info("Closing browser session...")
            browser.close()
            log.info("Browser closed successfully 🧹")
        else:
            log.info("CDP mode — skipping browser close (external session)")

    log.info("========== Browser Session Finished ==========")
