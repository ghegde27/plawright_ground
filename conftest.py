import os
from pathlib import Path

import pytest

from core.logger import Logger
from llm.ai_locator_healer import AILocatorHealer
from llm.client import LLMClient
from llm.locator_generator import LocatorGenerator
from llm.models import DEFAULT_MODEL
from llm.provider import Provider
from locators.locator_repository import LocatorRepository
from locators.page_repository import PageRepository

pytest_plugins = [
    "fixtures.browser_fixtures",
    "fixtures.context_fixtures",
    "fixtures.page_fixtures",
    "fixtures.test_hooks",
    "fixtures.auth_fixtures",
]

log = Logger.get_logger(__name__)

log.info(
    "========== Initiating Automation Setup =========="
)

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).parent

PAGES_DIR = (
        PROJECT_ROOT / "pages"
)

LOCATORS_DIR = (
        PROJECT_ROOT / "tests" / "locators"
)


# ==========================================================
# PYTEST OPTIONS
# ==========================================================

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help=(
            "Environment to run tests against "
            "(dev, qa). Precedence: "
            "--env > ENV var > default dev"
        ),
    )

    parser.addoption(
        "--capture-trace",
        action="store_true",
        default=None,
        help="Force enable trace capture for this run",
    )

    parser.addoption(
        "--no-capture-trace",
        action="store_true",
        default=None,
        help="Force disable trace capture for this run",
    )

    parser.addoption(
        "--site",
        action="store",
        default="moneycontrol",
        help=(
            "Site to authenticate "
            "(linkedin, github, etc)"
        ),
    )

    parser.addoption(
        "--use-auth",
        action="store_true",
        default=False,
        help="Use stored authentication session",
    )

    parser.addoption(
        "--refresh-auth",
        action="store_true",
        default=False,
        help=(
            "Force regenerate authentication session"
        ),
    )

    parser.addoption(
        "--cdp",
        action="store_true",
        default=False,
        help=(
            "Attach to existing browser via "
            "Chrome DevTools Protocol"
        ),
    )

    parser.addoption(
        "--cdp-url",
        action="store",
        default="http://localhost:9222",
        help="CDP endpoint URL",
    )


# ==========================================================
# LOCATOR REPOSITORY
# ==========================================================

@pytest.fixture(scope="session")
def locator_repository():
    return LocatorRepository(
        locator_dir=str(
            LOCATORS_DIR
        )
    )


# ==========================================================
# LLM LOCATOR GENERATOR
# ==========================================================

@pytest.fixture(scope="session")
def locator_generator(llm):
    return LocatorGenerator(
        llm=llm
    )


# ==========================================================
# AI LOCATOR HEALER
# ==========================================================

@pytest.fixture
def ai_locator_healer(
        page,
        locator_generator,
):
    return AILocatorHealer(
        page=page,
        locator_generator=locator_generator,
    )


# ==========================================================
# PAGE REPOSITORY
# ==========================================================
@pytest.fixture
def pages(
        page,
        locator_repository,
        ai_locator_healer,
):
    return PageRepository(
        page=page,
        pages_dir=str(PAGES_DIR),
        locator_repository=locator_repository,
        ai_locator_healer=ai_locator_healer,
    )


# ==========================================================
# SESSION FINISH
# ==========================================================

def pytest_sessionfinish(
        session,
        exitstatus,
):
    pass


@pytest.fixture(scope="session")
def llm():
    return LLMClient(
        provider=Provider.GROQ,
        api_key=os.getenv(""),
        model_config=DEFAULT_MODEL
    )
