from playwright.sync_api import (
    Locator,
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from core.exceptions import (
    LocatorNotFoundError,
    LocatorResolutionError,
)
from locators.locator_definition import LocatorDefinition


class LocatorResolver:

    def __init__(self, page: Page):
        self.page = page

    def resolve(self, definition: LocatorDefinition) -> Locator:
        strategy = definition.strategy
        value = definition.value
        options = definition.options or {}

        if strategy == "role":
            return self.page.get_by_role(value, **options)

        if strategy == "text":
            return self.page.get_by_text(value, **options)

        if strategy == "label":
            return self.page.get_by_label(value, **options)

        if strategy == "placeholder":
            return self.page.get_by_placeholder(value, **options)

        if strategy == "test_id":
            return self.page.get_by_test_id(value, **options)

        if strategy == "alt_text":
            return self.page.get_by_alt_text(value, **options)

        if strategy == "css":
            return self.page.locator(value)

        if strategy == "xpath":
            return self.page.locator(f"xpath={value}")

        raise LocatorResolutionError(f"Unsupported locator strategy: {strategy}")

    def validate(self, locator: Locator, timeout: int = 1000) -> bool:
        try:
            locator.wait_for(state="attached", timeout=timeout)
            return True
        except PlaywrightTimeoutError as error:
            raise LocatorNotFoundError(
                "Locator did not resolve to an attached element"
            ) from error
