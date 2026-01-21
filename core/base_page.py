import asyncio

from core.logger import Logger
from core.locator_helper import LocatorHelper as LH
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class BasePage:
    def __init__(self, page):
        self.page = page
        self.log = Logger.get_logger(self.__class__.__name__)

    async def _log(self, message: str):
        self.log.info(message)

    # -------------------------------------------
    # INTERNAL UTILITIES
    # -------------------------------------------

    async def _retry(self, func, retries=3, delay=1, action=""):
        """Retry wrapper for flaky operations."""
        for attempt in range(1, retries + 1):
            try:
                await func()
                return
            except PlaywrightTimeoutError:
                await self._log(f"Retry {attempt}/{retries} failed for: {action}")
                if attempt == retries:
                    raise
                await asyncio.sleep(delay)

    # -------------------------------------------
    # BASIC ACTIONS WITH AUTO-WAIT + RETRY
    # -------------------------------------------

    async def click(self, locator: str, retries=3, timeout=5000):
        """Smart click with auto-wait, logging, retry."""

        async def action():
            await self.page.wait_for_selector(locator, timeout=timeout)
            await self.page.locator(locator).click()

        await self._log(f"Click → {locator}")
        await self._retry(action, retries=retries, action=f"click {locator}")

    async def fill(self, locator: str, value: str, retries=3, timeout=5000):
        """Smart fill with auto-wait, logging, retry."""

        async def action():
            await self.page.wait_for_selector(locator, timeout=timeout)
            await self.page.locator(locator).fill(value)

        await self._log(f"Fill → {locator} | Value: {value}")
        await self._retry(action, retries=retries, action=f"fill {locator}")

    async def type(self, locator: str, value: str, delay=50, retries=3, timeout=5000):
        """Smart type with keystroke delay + retry."""

        async def action():
            await self.page.wait_for_selector(locator, timeout=timeout)
            await self.page.locator(locator).type(value, delay=delay)

        await self._log(f"Type → {locator} | Value: {value}")
        await self._retry(action, retries=retries, action=f"type {locator}")

    async def get_text(self, locator: str, retries=2):
        """Get text from element."""

        async def action():
            return await self.page.locator(locator).inner_text()

        await self._log(f"Get Text → {locator}")
        return await self._retry(action, retries=retries, action=f"get_text {locator}")

    async def wait_for_visible(self, locator: str, timeout=5000):
        await self._log(f"Wait for Visible → {locator}")
        await self.page.wait_for_selector(locator, timeout=timeout, state="visible")

    async def wait_for_hidden(self, locator: str, timeout=5000):
        await self._log(f"Wait for Hidden → {locator}")
        await self.page.wait_for_selector(locator, timeout=timeout, state="hidden")

    async def is_visible(self, locator: str):
        return await self.page.locator(locator).is_visible()

    async def navigate(self, url: str):
        await self._log(f"Navigate → {url}")
        await self.page.goto(url)

    # -------------------------------------------
    # ROLE-BASED CLICK / FILL (using LocatorHelper)
    # -------------------------------------------

    async def click_role(
            self,
            role: str,
            name: str = None,
            exact: bool = False,
            checked: bool = None,
            disabled: bool = None,
            expanded: bool = None,
            include_hidden: bool = False,
            level: int = None,
            pressed: bool = None,
            selected: bool = None,
    ):
        locator = LH.by_role(
            role=role,
            name=name,
            exact=exact,
            checked=checked,
            disabled=disabled,
            expanded=expanded,
            include_hidden=include_hidden,
            level=level,
            pressed=pressed,
            selected=selected,
        )
        await self.click(locator)

    # Add this inside BasePage class

    async def hover(self, locator: str, retries=3, timeout=5000):
        """Smart hover with auto-wait, logging, retry."""
        async def action():
            await self.page.wait_for_selector(locator, timeout=timeout)
            await self.page.locator(locator).hover()

        await self._log(f"Hover → {locator}")
        await self._retry(action, retries=retries, action=f"hover {locator}")

    async def wait_for_timeout_before_next(self, timeout=10):
        await self.page.wait_for_timeout(timeout=timeout)


    # -----------------------------
#  WINDOW HANDLING
# -----------------------------

async def handle_new_window(self, trigger_action):
    """
    Waits for a new window/tab created by any action.
    Example: await handle_new_window(lambda: self.click(selector))
    """
    async with self.page.context.expect_page() as p_info:
        await trigger_action()
    new_page = await p_info.value
    await self._log(f"New window detected: {await new_page.title()}")
    return new_page


async def switch_to_window(self, title=None, url_contains=None, index=None):
    """
    Switch to a specific window by title, URL, or index.
    """
    pages = self.page.context.pages
    await self._log(f"Available windows: {[await p.title() for p in pages]}")

    # Switch by index
    if index is not None:
        await pages[index].bring_to_front()
        await self._log(f"Switched to window index: {index}")
        return pages[index]

    # Switch by title
    if title:
        for p in pages:
            if title in await p.title():
                await p.bring_to_front()
                await self._log(f"Switched to window with title: {await p.title()}")
                return p

    # Switch by URL
    if url_contains:
        for p in pages:
            if url_contains in p.url:
                await p.bring_to_front()
                await self._log(f"Switched to window with url containing: {url_contains}")
                return p

    raise Exception("Window not found!")


async def close_other_windows(self):
    """
    Closes all windows except the first one.
    """
    pages = self.page.context.pages
    main = pages[0]

    for p in pages[1:]:
        await p.close()

    await main.bring_to_front()
    await self._log("Closed all other windows and returned to main window.")
    return main


# -----------------------------
#  POPUP HANDLING (JS POPUPS)
# -----------------------------
async def handle_popup(self, trigger_action):
    """
    Handles popup windows (window.open, JS popups).
    """
    async with self.page.expect_popup() as popup_info:
        await trigger_action()

    popup = await popup_info.value
    await self._log(f"Popup opened with title: {await popup.title()}")
    return popup


# -----------------------------
#  FRAME HANDLING
# -----------------------------
async def switch_to_frame(self, selector=None, index=None, name=None):
    """
    Switch inside an iframe by selector, name, or index.
    """
    if selector:
        frame = self.page.frame_locator(selector)
        await self._log(f"Switched to frame: {selector}")
        return frame

    if name:
        frame = self.page.frame(name=name)
        await self._log(f"Switched to frame by name: {name}")
        return frame

    if index is not None:
        frame = self.page.frames[index]
        await self._log(f"Switched to frame by index: {index}")
        return frame

    raise Exception("Frame selector/name/index required.")


async def switch_to_main_frame(self):
    """
    Switch back to the main document frame.
    """
    await self._log("Switching to main frame.")
    return self.page.main_frame
