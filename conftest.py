import asyncio

import pytest

from core.logger import Logger

pytest_plugins = [
    "fixtures.browser_fixtures",
    "fixtures.context_fixtures",
    "fixtures.page_fixtures",
    "fixtures.test_hooks",
    "fixtures.auth_fixtures"
]

log = Logger.get_logger(__name__)

log.info(f"========== Initiating Automation Setup ==========")


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Environment to run tests against (dev, qa). Precedence: --env > ENV var > default dev"
    )
    parser.addoption(
        "--capture-trace",
        action="store_true",
        default=None,
        help="Force enable trace capture for this run"
    )
    parser.addoption(
        "--no-capture-trace",
        action="store_true",
        default=None,
        help="Force disable trace capture for this run"
    )

    parser.addoption(
        "--site",
        action="store",
        default="linkedin",
        help="Site to authenticate (linkedin, github, etc)"
    )

    parser.addoption(
        "--use-auth",
        action="store_true",
        default=False,
        help="Use stored authentication session"
    )

    parser.addoption(
        "--refresh-auth",
        action="store_true",
        default=False,
        help="Force regenerate authentication session"
    )
    parser.addoption(
        "--cdp",
        action="store_true",
        default=False,
        help="Attach to existing browser via Chrome DevTools Protocol"
    )

    parser.addoption(
        "--cdp-url",
        action="store",
        default="http://localhost:9222",
        help="CDP endpoint URL"
    )

    def pytest_sessionfinish():
        from core.locator_report import LocatorReport
        log.info(LocatorReport.generate_report())

    # =====================================================
    # Event loop (required for session-scoped async fixtures)
    # =====================================================
    @pytest.fixture(scope="session")
    def event_loop():
        import asyncio
        loop = asyncio.new_event_loop()
        yield loop
        loop.close()
