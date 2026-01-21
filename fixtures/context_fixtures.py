import os
import pytest
from pathlib import Path
from urllib.parse import urlparse
from core.logger import Logger

log = Logger.get_logger(__name__)


@pytest.fixture
async def context(browser, config, ensure_login):
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "main")

    har_flag = config.get("capture_har", False)
    trace_flag = config.get("capture_trace", False)
    video_flag = config.get("capture_video", False)

    log.info(f"--- Context setup started [Worker: {worker_id}] ---")
    log.info(f"Capture HAR    : {har_flag}")
    log.info(f"Capture Trace  : {trace_flag}")
    log.info(f"Capture Video  : {video_flag}")
    log.info(f"Auth Enabled   : {bool(ensure_login)}")

    # Ensure results directory exists
    Path("allure-results").mkdir(exist_ok=True)

    # Video directory per worker
    video_dir = f"allure-results/videos/{worker_id}"
    if video_flag:
        Path(video_dir).mkdir(parents=True, exist_ok=True)
        log.info(f"Video directory : {video_dir}")

    # HAR path per worker
    har_path = f"allure-results/{worker_id}_network.har" if har_flag else None
    if har_flag:
        log.info(f"HAR path        : {har_path}")

    # Build context arguments
    context_args = {
        "record_har_path": har_path,
        "record_video_dir": video_dir if video_flag else None
    }

    if ensure_login:
        context_args["storage_state"] = ensure_login
        log.info(f"Using storage_state: {ensure_login}")
    else:
        log.info("No storage_state — running anonymous session")

    # Create context
    ctx = await browser.new_context(**context_args)
    log.info("Browser context created successfully")

    # Add cookie consent
    domain = urlparse(config["base_url"]).hostname

    await ctx.add_cookies([{
        "name": "cookieConsent",
        "value": "true",
        "domain": domain,
        "path": "/"
    }])
    log.info("Cookie consent injected")

    # Start tracing if enabled
    if trace_flag:
        await ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
        log.info("Tracing started")

    yield ctx

    # Stop tracing
    if trace_flag:
        trace_path = f"allure-results/{worker_id}_trace.zip"
        await ctx.tracing.stop(path=trace_path)
        log.info(f"Tracing stopped → {trace_path}")

    # Close context
    await ctx.close()
    log.info(f"Browser context closed [Worker: {worker_id}]")
    log.info(f"--- Context teardown completed [Worker: {worker_id}] ---")
