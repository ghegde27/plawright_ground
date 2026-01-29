from core.base_page import BasePage
from core.locator_helper import LocatorHelper as LH


class HomePage(BasePage):

    # Required for MCP auto-registration
    page_name = "HomePage"

    # --------------------
    # Locator Constants
    # --------------------

    CATEGORY_ELECTRONICS = "h6[data-testid='CategoryNavL0Item']:has-text('Electronics')"

    COOKIE_CONTAINER = "#truste-consent-buttons"
    COOKIE_ACCEPT_BUTTON = "#truste-consent-button"
    COOKIE_REVIEW_BUTTON = "#truste-show-consent"

    MOBILES_IMAGE = "img[alt='Mobiles & Tablets1']"

    SECTIONS = "section"
    SELECT_DROPDOWNS = "select"

    # --------------------
    # Constructor
    # --------------------

    def __init__(self, page):
        super().__init__(page)

    # --------------------
    # Page Actions
    # --------------------

    async def select_category(self, name: str):
        if not (name and name.strip()):
            raise ValueError("Invalid input: 'name' cannot be empty")

        # Hover electronics category
        await self.page.locator(self.CATEGORY_ELECTRONICS).hover()
        await self.wait_for_timeout_before_next(1000)

        # Click category link by role
        await self.click_role("link", name=name)
        await self.wait_for_timeout_before_next(1000)

    async def cookie_manage(self, option: int = 0):
        if option == 0:
            await self.wait_for_visible(self.COOKIE_CONTAINER)

            # MCP-aware selector click
            await self.click_by_selector(
                element_name="COOKIE_ACCEPT_BUTTON"
            )
        else:
            await self.click_by_selector(
                element_name="COOKIE_REVIEW_BUTTON"
            )

    async def open_link_in_new_tab(self):
        # Use MCP-aware selector click
        await self.click_by_selector(selector=self.MOBILES_IMAGE, element_name="MOBILES_IMAGE")

        await self.wait_for_timeout_before_next(2000)
        self.log.info(f"Redirected to URL → {self.page.url}")

        await self.click_text_inside_sections("Apple")
        await self.wait_for_timeout_before_next(2000)

    # --------------------
    # Utility Functions
    # --------------------

    async def list_all_selects(self):
        selects = await self.page.locator(self.SELECT_DROPDOWNS).all()
        self.log.info(f"Found {len(selects)} select elements")

        for sel in selects:
            class_name = await sel.get_attribute("class")
            self.log.info(f"Select class: {class_name}")

            options = await sel.locator("option").all()
            for opt in options:
                text = await opt.text_content()
                self.log.info(f" - {text}")

    async def list_all_sections(self):
        sections = await self.page.locator(self.SECTIONS).all()
        self.log.info(f"Found {len(sections)} Section elements")

        for idx, sec in enumerate(sections, start=1):
            class_name = await sec.get_attribute("class")
            self.log.info(f"\n--- Section {idx} ---")
            self.log.info(f"Section class: {class_name}")

            text = await sec.inner_text()
            self.log.info(text)

            if "Apple" in text:
                await self.wait_for_timeout_before_next(1000)
                await self.click_by_locator(sec)
                self.log.info("Clicked section containing 'Apple'")
                break

    async def click_text_inside_sections(self, text_to_click: str):
        sections = await self.page.locator(self.SECTIONS).all()

        for sec in sections:
            target = sec.locator(f"text={text_to_click}").first

            if await target.count() > 0:
                await target.scroll_into_view_if_needed()

                # Locator-object click (no selector string here)
                await self.click_by_locator(target)

                self.log.info(f"Clicked text → {text_to_click}")
                return True

        self.log.info(f"Text '{text_to_click}' not found in any section")
        return False
