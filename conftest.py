from pathlib import Path

import pytest

from core.logger import Logger
from llm.ai_locator_healer import AILocatorHealer
from llm.client import LLMClient
from llm.locator_generator import LocatorGenerator
from config.ai_config import AIConfig
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
def locator_generator(llm, ai_config):
    if not ai_config.enabled or not ai_config.locator_generation_enabled:
        return None
    return LocatorGenerator(llm=llm)


# ==========================================================
# AI LOCATOR HEALER
# ==========================================================

@pytest.fixture
def ai_locator_healer(
        page,
        locator_generator,
        ai_config,
):
    if not (
        ai_config.enabled
        and ai_config.locator_healing_enabled
        and locator_generator
    ):
        return None
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
def ai_config():
    return AIConfig.from_env()


@pytest.fixture(scope="session")
def llm(ai_config):
    if not ai_config.enabled:
        return None
    return LLMClient(
        provider=ai_config.provider,
        model_config=ai_config.model,
    )
