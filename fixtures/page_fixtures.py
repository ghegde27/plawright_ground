import allure
import pytest

from core.logger import Logger

log = Logger.get_logger(__name__)


@pytest.fixture
def page(context, config, request):
    log.info("Creating new page...")
    page = context.new_page()
    log.info("New page created successfully")
    base_url = config.get("base_url")
    log.info(f"Navigating to base URL: {base_url}")
    page.goto(base_url)

    yield page

    # After test execution
    try:
        rep = getattr(request.node, 'rep_call', None)

        if rep and rep.failed:
            log.error(f"Test FAILED: {request.node.name}")

            if config.get("capture_screenshot", False):
                log.info("Capturing screenshot for failed test...")
                png = page.screenshot(full_page=True)
                allure.attach(
                    png,
                    name="failure-screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                log.info("Failure screenshot attached to Allure report")

        else:
            log.info(f"Test PASSED: {request.node.name}")

    except Exception as e:
        log.warning("Error while capturing failure screenshot")
        log.exception(e)

    page.close()
    log.info("Page closed successfully")
