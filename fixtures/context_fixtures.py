import os
import pytest
from pathlib import Path
from urllib.parse import urlparse

from core.logger import Logger

log = Logger.get_logger(__name__)


@pytest.fixture
async def context(browser, config, ensure_login):
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "main")

    # ---------------------------
    # Read config values
    # ---------------------------
    har_flag        = config.get("capture_har", False)
    trace_flag      = config.get("capture_trace", False)
    video_flag      = config.get("capture_video", False)

    locale         = config.get("locale", "en-IN")
    timezone       = config.get("timezone", "Asia/Kolkata")
    permissions    = config.get("permissions", [])           # e.g ["geolocation","notifications"]
    geolocation    = config.get("geolocation", None)         # e.g {"latitude":12.9,"longitude":77.6}

    inject_cookie  = config.get("inject_cookie_consent", True)

    log.info(f"--- Context setup started [Worker: {worker_id}] ---")
    log.info(f"Locale          : {locale}")
    log.info(f"Timezone        : {timezone}")
    log.info(f"Permissions     : {permissions}")
    log.info(f"Geolocation     : {geolocation}")
    log.info(f"Auth Enabled    : {bool(ensure_login)}")
    log.info(f"HAR Capture     : {har_flag}")
    log.info(f"Trace Capture   : {trace_flag}")
    log.info(f"Video Capture   : {video_flag}")

    # ---------------------------
    # Prepare result folders
    # ---------------------------
    Path("allure-results").mkdir(exist_ok=True)

    video_dir = f"allure-results/videos/{worker_id}"
    if video_flag:
        Path(video_dir).mkdir(parents=True, exist_ok=True)

    har_path = f"allure-results/{worker_id}_network.har" if har_flag else None

    # ---------------------------
    # Build context arguments
    # ---------------------------
    context_args = {
        "locale": locale,
        "timezone_id": timezone,
        "record_har_path": har_path,
        "record_video_dir": video_dir if video_flag else None
    }

    if permissions:
        context_args["permissions"] = permissions

    if geolocation:
        context_args["geolocation"] = geolocation

    if ensure_login:
        context_args["storage_state"] = ensure_login
        log.info(f"Using storage_state: {ensure_login}")
    else:
        log.info("No storage_state — anonymous session")

    # ---------------------------
    # Create context
    # ---------------------------
    ctx = await browser.new_context(**context_args)
    log.info("Browser context created")

    # ---------------------------
    # Inject cookie consent if enabled
    # ---------------------------
    if inject_cookie:
        domain = urlparse(config["base_url"]).hostname
        await ctx.add_cookies([{
            "name": "cookieConsent",
            "value": "true",
            "domain": domain,
            "path": "/"
        }])
        log.info("Cookie consent injected")

    # ---------------------------
    # Start tracing if enabled
    # ---------------------------
    if trace_flag:
        await ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
        log.info("Tracing started")

    yield ctx

    # ---------------------------
    # Teardown
    # ---------------------------
    if trace_flag:
        trace_path = f"allure-results/{worker_id}_trace.zip"
        await ctx.tracing.stop(path=trace_path)
        log.info(f"Tracing stopped → {trace_path}")

    await ctx.close()
    log.info(f"Context closed [Worker: {worker_id}]")
    log.info(f"--- Context teardown completed [Worker: {worker_id}] ---")
