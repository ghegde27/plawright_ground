import allure
import pytest

from core.logger import Logger

log = Logger.get_logger(__name__)


@pytest.mark.home
@allure.feature("Homepage")
def test_verify_home_page(pages):

    log.info("Started Home page tests")

    with allure.step("Navigate to Lab Tests"):
        pages.home.move_to_lab_test()

# HomePage().searchResults(SearchResultsPage).selctProduct(ProductDetailsPage).review(ReviewPage)
