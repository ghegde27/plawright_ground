import asyncio

from playwright.async_api import TimeoutError as PlaywrightTimeoutError, Locator

from core.locator_helper import LocatorHelper as LH
from core.locator_report import LocatorReport
from core.logger import Logger
from playwright_client.mcp_client import (
    register_page_locators,
    get_locator,
    heal_locator
)


class BasePage:
    _registered_pages = set()   # ✅ must be a set, not None
    page_name = None

    # -------------------------
    # Auto-register POM locators in MCP
    # -------------------------
    def __init_subclass__(cls):
        if not cls.page_name:
            return

        # Prevent duplicate registration per session
        if cls.page_name in BasePage._registered_pages:
            return

        BasePage._registered_pages.add(cls.page_name)

        locators = []
        for attr, value in cls.__dict__.items():
            if attr.isupper() and isinstance(value, str):
                locators.append({
                    "element_name": attr,
                    "primary_locator": value
                })

        if locators:
            register_page_locators(cls.page_name, locators)

    # -------------------------
    # Init
    # -------------------------
    def __init__(self, page):
        self.page = page
        self.log = Logger.get_logger(self.__class__.__name__)

    async def _log(self, msg: str):
        self.log.info(msg)

    # -------------------------
    # Retry helper
    # -------------------------
    async def _retry(self, func, retries=3, delay=1, action=""):
        for attempt in range(1, retries + 1):
            try:
                return await func()
            except PlaywrightTimeoutError:
                await self._log(f"Retry {attempt}/{retries} failed → {action}")
                if attempt == retries:
                    raise
                await asyncio.sleep(delay)

    # -------------------------
    # DOM Extractor (for MCP healing)
    # -------------------------
    async def extract_dom(self):
        return await self.page.evaluate("""
        () => {
          function simplify(el) {
            return {
              tag: el.tagName.toLowerCase(),
              text: el.innerText ? el.innerText.trim().slice(0,80) : null,
              children: Array.from(el.children).slice(0,5).map(simplify)
            }
          }
          return simplify(document.body)
        }
        """)

    # ======================================================
    # CLICK FUNCTIONS
    # ======================================================

    async def click_by_selector(self, selector: str = None, element_name: str = None,
                                retries=3, timeout=5000):
        """
        Primary = selector from POM
        Fallback = locator from MCP DB
        Healing only if both fail
        """

        page_name = self.page_name

        if not selector and not element_name:
            raise ValueError("Selector or element_name required")

        # 1️⃣ Try POM selector first
        if selector:
            try:
                await self._log(f"Click → POM selector: {selector}")

                async def action():
                    await self.page.wait_for_selector(selector, timeout=timeout)
                    await self.page.locator(selector).click()

                await self._retry(action, retries=retries, action=f"click {selector}")
                return

            except Exception:
                await self._log("POM locator failed → trying DB fallback")

        # 2️⃣ Try MCP stored locator
        stored_selector = None
        if page_name and element_name:
            stored_selector = get_locator(page_name, element_name)

        if stored_selector:
            try:
                await self._log(f"Click → DB selector: {stored_selector}")

                async def db_action():
                    await self.page.wait_for_selector(stored_selector, timeout=timeout)
                    await self.page.locator(stored_selector).click()

                await self._retry(db_action, retries=retries, action=f"click {stored_selector}")

                # Record outdated POM locator
                LocatorReport.mark_outdated(page_name, element_name, selector, stored_selector)
                return

            except Exception:
                await self._log("DB locator also failed → invoking healer")

        # 3️⃣ Heal via MCP
        if page_name and element_name:
            dom = await self.extract_dom()

            new_selector = heal_locator(
                page_name,
                element_name,
                dom,
                f"Find clickable element for '{element_name}'"
            )

            await self._log(f"Healed selector → {new_selector}")

            await self.page.wait_for_selector(new_selector, timeout=timeout)
            await self.page.locator(new_selector).click()

            LocatorReport.mark_outdated(page_name, element_name, selector, new_selector)
            return

        raise Exception("All locator strategies failed")

    async def click_by_locator(self, locator: Locator, retries=3, timeout=5000):
        """Click using Playwright Locator object"""

        async def action():
            await locator.wait_for(timeout=timeout)
            await locator.click()

        await self._log("Click → Locator object")
        await self._retry(action, retries=retries, action="click_by_locator")

    async def click_any(self, target, element_name=None, retries=3, timeout=5000):
        """Accepts selector string or Playwright Locator"""

        if isinstance(target, str):
            await self.click_by_selector(target, element_name, retries, timeout)
        elif isinstance(target, Locator):
            await self.click_by_locator(target, retries, timeout)
        else:
            raise ValueError("Target must be selector string or Locator")

    # ======================================================
    # FILL FUNCTION
    # ======================================================

    async def fill_by_selector(self, selector: str = None, value: str = "",
                               element_name: str = None, retries=3, timeout=5000):

        page_name = self.page_name

        if not selector and not element_name:
            raise ValueError("Selector or element_name required")

        # Try POM selector first
        if selector:
            try:
                async def action():
                    await self.page.wait_for_selector(selector, timeout=timeout)
                    await self.page.locator(selector).fill(value)

                await self._retry(action, retries=retries, action=f"fill {selector}")
                return
            except Exception:
                await self._log("POM fill failed → trying DB fallback")

        # Try DB locator
        stored = None
        if page_name and element_name:
            stored = get_locator(page_name, element_name)

        if stored:
            await self.page.wait_for_selector(stored, timeout=timeout)
            await self.page.locator(stored).fill(value)

            LocatorReport.mark_outdated(page_name, element_name, selector, stored)
            return

        # Heal if needed
        if page_name and element_name:
            dom = await self.extract_dom()
            new_selector = heal_locator(
                page_name,
                element_name,
                dom,
                f"Find input field for '{element_name}'"
            )

            await self.page.wait_for_selector(new_selector, timeout=timeout)
            await self.page.locator(new_selector).fill(value)

            LocatorReport.mark_outdated(page_name, element_name, selector, new_selector)
            return

        raise Exception("All fill locator strategies failed")

    # ======================================================
    # ROLE-BASED CLICK
    # ======================================================

    async def click_role(self, role: str, name: str = None, exact=False, **kwargs):
        selector = LH.by_role(role=role, name=name, exact=exact, **kwargs)
        await self.click_by_selector(selector)

    # ======================================================
    # HOVER
    # ======================================================

    async def hover(self, role: str, name: str, retries=3, timeout=5000):
        async def action():
            locator = self.page.get_by_role(role, name=name, exact=True)
            await locator.wait_for(timeout=timeout)
            await locator.hover()

        await self._log(f"Hover → role={role}, name={name}")
        await self._retry(action, retries=retries, action="hover")

    # ======================================================
    # BASIC UTILS
    # ======================================================

    async def get_text(self, selector: str):
        return await self.page.locator(selector).inner_text()

    async def wait_for_visible(self, selector: str, timeout=5000):
        await self.page.wait_for_selector(selector, timeout=timeout, state="visible")

    async def wait_for_hidden(self, selector: str, timeout=5000):
        await self.page.wait_for_selector(selector, timeout=timeout, state="hidden")

    async def navigate(self, url: str):
        await self._log(f"Navigate → {url}")
        await self.page.goto(url)

    async def wait_for_timeout_before_next(self, timeout=1000):
        await self.page.wait_for_timeout(timeout)

    # ======================================================
    # WINDOW / FRAME HELPERS
    # ======================================================

    async def handle_new_window(self, trigger_action):
        try:
            async with self.page.context.expect_page() as p_info:
                await trigger_action()
            new_page = await p_info.value
            await new_page.wait_for_load_state()
            await self._log(f"New window → {await new_page.title()}")
            return new_page
        except:
            await self._log("No new window detected")
            return self.page

    async def switch_to_frame(self, selector=None, index=None, name=None):
        if selector:
            return self.page.frame_locator(selector)
        if name:
            return self.page.frame(name=name)
        if index is not None:
            return self.page.frames[index]
        raise Exception("Frame selector/name/index required")
