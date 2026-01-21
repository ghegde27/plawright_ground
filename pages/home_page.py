import time

from core.base_page import BasePage
from core.locator_helper import LocatorHelper as LH


class HomePage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    '''
        :name - select the category
        '''

    async def select_category(self, name: str = None):
        if not (name and name.strip()):
            raise ValueError("Invalid input: 'name' cannot be empty or None")
        await self.hover(locator="h6[data-testid='CategoryNavL0Item']:has-text('Electronics')")
        await self.wait_for_timeout_before_next(timeout=10000)
        await self.click_role("link", name=name)
        await self.wait_for_timeout_before_next(timeout=10000)

    async def cookie_manage(self, option: int = 0):
        if option == 0:

            await self.wait_for_visible(LH.by_css("#truste-consent-buttons"))
            await self.click("#truste-consent-button")

        else:

            await self.page.locator("#truste-show-consent").click()  # Review details
