import pytest
import allure

from core.logger import Logger
from pages.home_page import HomePage

log = Logger.get_logger(__name__)


@pytest.mark.asyncio
@allure.feature("Homepage")
async def test_verify_home_page(page):
    home = HomePage(page)
    await home.open_link_in_new_tab()


