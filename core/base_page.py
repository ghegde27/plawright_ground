from typing import Callable

from playwright.sync_api import (
    Locator,
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from core.action_failure_classifier import FailureType, ActionFailureClassifier
from core.exceptions import (
    LocatorNotFoundError,
    LocatorResolutionError,
)
from core.logger import Logger
from core.retry import retry
from locators.locator_repository import LocatorRepository
from locators.locator_resolver import LocatorResolver


class BasePage:
    DEFAULT_TIMEOUT = 5000
    DEFAULT_RETRIES = 3
    DEFAULT_RETRY_DELAY = 1

    page_name: str | None = None

    # ==========================================================
    # FRAMEWORK INITIALIZATION
    # ==========================================================

    def _initialize(
            self,
            page: Page,
            locator_repository: LocatorRepository,
            ai_locator_healer=None,
            page_repository=None
    ):
        self.page = page
        self.repository = locator_repository
        self.resolver = LocatorResolver(page=page)
        self.ai_locator_healer = ai_locator_healer
        self.page_repository = page_repository
        self.log = Logger.get_logger(self.__class__.__name__)

        self._log(f"[PAGE] Initialized → {self.page_name}")

    # ==========================================================
    # LOGGING & HELPER METHODS
    # ==========================================================

    def _log(self, message: str):
        self.log.info(message)

    def _locator_name(self, locator: str | Locator) -> str:
        if isinstance(locator, str):
            return f"{self.page_name}.{locator}"
        return "<Playwright Locator>"

    # ==========================================================
    # LOCATOR RESOLUTION
    # ==========================================================

    def locator(self, locator_name: str) -> Locator:
        if not self.page_name:
            raise LocatorResolutionError(
                f"{self.__class__.__name__} must define page_name"
            )

        if self.repository is None:
            raise RuntimeError("LocatorRepository has not been initialized")

        self._log(f"[LOCATOR] Loading → {self.page_name}.{locator_name}")

        try:
            definition = self.repository.get(
                page_name=self.page_name,
                locator_name=locator_name,
            )
        except Exception as error:
            self._log(
                f"[LOCATOR] Repository lookup failed → "
                f"{self.page_name}.{locator_name} | {error}"
            )
            raise

        if definition is None:
            self._log(
                f"[LOCATOR] Definition not found → "
                f"{self.page_name}.{locator_name}"
            )
            raise LocatorNotFoundError(
                f"Locator '{locator_name}' not found for page '{self.page_name}'"
            )

        if self.resolver is None:
            raise RuntimeError("LocatorResolver has not been initialized")

        try:
            resolved_locator = self.resolver.resolve(definition)
            self._log(f"[LOCATOR] Resolved → {self.page_name}.{locator_name}")
            return resolved_locator
        except Exception as error:
            self._log(
                f"[LOCATOR] Resolve failed → "
                f"{self.page_name}.{locator_name} | {error}"
            )
            raise

    def _resolve(self, locator: str | Locator) -> Locator:
        if isinstance(locator, Locator):
            self._log("[LOCATOR] Existing Playwright Locator supplied")
            return locator

        if not isinstance(locator, str):
            raise TypeError("Locator must be a locator name or Playwright Locator")

        if not self.page_name:
            raise LocatorResolutionError(
                f"{self.__class__.__name__} must define page_name"
            )

        self._log(f"[LOCATOR] Resolving → {self.page_name}.{locator}")
        return self.locator(locator)

    def _is_locator_missing(self, locator: Locator) -> bool:
        try:
            count = locator.count()
            self._log(f"[LOCATOR] DOM match count → {count}")
            return count == 0
        except Exception as error:
            self._log(f"[LOCATOR] Unable to determine DOM match → {error}")
            return False

    # ==========================================================
    # AI LOCATOR HEALING
    # ==========================================================

    def _heal_locator(self, locator_name: str) -> Locator:
        if not self.ai_locator_healer:
            self._log("[AI-HEAL] Disabled")
            raise LocatorNotFoundError(
                f"Locator '{locator_name}' could not be resolved"
            )

        self._log(f"[AI-HEAL] Starting → {self.page_name}.{locator_name}")

        try:
            if self.repository is None:
                raise RuntimeError("LocatorRepository has not been initialized")

            original_definition = self.repository.get(
                page_name=self.page_name,
                locator_name=locator_name,
            )

            if original_definition is None:
                raise LocatorNotFoundError(
                    f"Original locator definition not found → "
                    f"{self.page_name}.{locator_name}"
                )

            self._log(
                f"[AI-HEAL] Original definition → "
                f"strategy={original_definition.strategy} | "
                f"value={original_definition.value} | "
                f"options={original_definition.options}"
            )

            definition = self.ai_locator_healer.heal(
                page_name=self.page_name,
                locator_name=locator_name,
                original_definition=original_definition,
            )

            self._log(
                f"[AI-HEAL] Definition generated → "
                f"strategy={definition.strategy} | "
                f"value={definition.value} | "
                f"options={definition.options}"
            )

            if self.resolver is None:
                raise RuntimeError("LocatorResolver has not been initialized")

            healed_locator = self.resolver.resolve(definition)

            if self._is_locator_missing(healed_locator):
                raise LocatorNotFoundError(
                    "AI generated locator does not match any element"
                )

            self._log(
                f"[AI-HEAL] Successful → {self.page_name}.{locator_name}"
            )
            return healed_locator

        except Exception as error:
            self._log(
                f"[AI-HEAL] Failed → {self.page_name}.{locator_name} | {error}"
            )
            raise

    # ==========================================================
    # ACTION RETRY & EXECUTION ENGINE
    # ==========================================================

    @retry(
        retries=DEFAULT_RETRIES,
        delay=DEFAULT_RETRY_DELAY,
        exceptions=(PlaywrightTimeoutError,),
    )
    def _retry_action(self, action: Callable, *args, **kwargs):
        return action(*args, **kwargs)

    def _perform(
            self,
            locator: str | Locator,
            action_name: str,
            action_builder: Callable,
    ):
        log_name = self._locator_name(locator)

        # 1. Resolve locator
        target = self._resolve(locator)
        self._log(f"[ACTION] {action_name} → {log_name}")

        # 2. Execute action with standard retry
        try:
            result = self._retry_action(action_builder(target))
            self._log(f"[ACTION] {action_name} successful → {log_name}")
            return result

        except Exception as error:
            self._log(f"[ACTION] {action_name} failed → {log_name} | {error}")

            # 3. Classify failure
            failure_type = ActionFailureClassifier.classify(
                error=error,
                locator=target,
            )
            self._log(f"[ACTION] Failure classification → {failure_type}")

            # 4. Handle genuine infrastructural / non-locator failures
            if failure_type != FailureType.LOCATOR_FAILURE:
                self._log(f"[ACTION] Genuine failure → {log_name}")
                raise

            # 5. Skip healing for direct Playwright locators
            if not isinstance(locator, str):
                self._log(
                    "[AI-HEAL] Skipped → direct Playwright Locator"
                )
                raise

            # 6. Verify locator missing in DOM
            if not self._is_locator_missing(target):
                self._log(
                    f"[ACTION] Locator exists; treating as genuine failure → {log_name}"
                )
                raise

            # 7. Attempt AI healing
            self._log(f"[AI-HEAL] Locator failure detected → {log_name}")
            healed_locator = self._heal_locator(locator)

            # 8. Retry action with healed locator
            self._log(f"[AI-HEAL] Retrying {action_name} → {log_name}")
            try:
                result = self._retry_action(action_builder(healed_locator))
                self._log(
                    f"[ACTION] {action_name} successful after healing → {log_name}"
                )
                return result
            except Exception as healed_error:
                self._log(
                    f"[ACTION] {action_name} failed after healing → "
                    f"{log_name} | {healed_error}"
                )
                raise

    # ==========================================================
    # COMMON ELEMENT ACTIONS
    # ==========================================================

    def click(self, locator: str | Locator, timeout: int = DEFAULT_TIMEOUT):
        return self._perform(
            locator=locator,
            action_name="CLICK",
            action_builder=lambda target: lambda: target.click(timeout=timeout),
        )

    def fill(
            self,
            locator: str | Locator,
            value: str,
            timeout: int = DEFAULT_TIMEOUT,
    ):
        return self._perform(
            locator=locator,
            action_name="FILL",
            action_builder=lambda target: lambda: target.fill(
                value, timeout=timeout
            ),
        )

    def press(
            self,
            locator: str | Locator,
            key: str,
            timeout: int = DEFAULT_TIMEOUT,
    ):
        return self._perform(
            locator=locator,
            action_name="PRESS",
            action_builder=lambda target: lambda: target.press(
                key, timeout=timeout
            ),
        )

    def hover(self, locator: str | Locator, timeout: int = DEFAULT_TIMEOUT):
        return self._perform(
            locator=locator,
            action_name="HOVER",
            action_builder=lambda target: lambda: target.hover(timeout=timeout),
        )

    def select_option(
            self,
            locator: str | Locator,
            value: str,
            timeout: int = DEFAULT_TIMEOUT,
    ):
        return self._perform(
            locator=locator,
            action_name="SELECT",
            action_builder=lambda target: lambda: target.select_option(
                value, timeout=timeout
            ),
        )

    def check(self, locator: str | Locator, timeout: int = DEFAULT_TIMEOUT):
        return self._perform(
            locator=locator,
            action_name="CHECK",
            action_builder=lambda target: lambda: target.check(timeout=timeout),
        )

    def uncheck(self, locator: str | Locator, timeout: int = DEFAULT_TIMEOUT):
        return self._perform(
            locator=locator,
            action_name="UNCHECK",
            action_builder=lambda target: lambda: target.uncheck(timeout=timeout),
        )

    # ==========================================================
    # WAITS
    # ==========================================================

    def wait_for_visible(
            self,
            locator: str | Locator,
            timeout: int = DEFAULT_TIMEOUT,
    ):
        log_name = self._locator_name(locator)
        self._log(f"[WAIT] VISIBLE → {log_name}")
        target = self._resolve(locator)

        try:
            target.wait_for(state="visible", timeout=timeout)
            self._log(f"[WAIT] VISIBLE successful → {log_name}")
        except PlaywrightTimeoutError as error:
            self._log(f"[WAIT] VISIBLE timeout → {log_name} | {error}")
            raise

    def wait_for_hidden(
            self,
            locator: str | Locator,
            timeout: int = DEFAULT_TIMEOUT,
    ):
        log_name = self._locator_name(locator)
        self._log(f"[WAIT] HIDDEN → {log_name}")
        target = self._resolve(locator)

        try:
            target.wait_for(state="hidden", timeout=timeout)
            self._log(f"[WAIT] HIDDEN successful → {log_name}")
        except PlaywrightTimeoutError as error:
            self._log(f"[WAIT] HIDDEN timeout → {log_name} | {error}")
            raise

    # ==========================================================
    # READ STATE & PROPERTIES
    # ==========================================================

    def get_text(self, locator: str | Locator) -> str:
        log_name = self._locator_name(locator)
        self._log(f"[READ] TEXT → {log_name}")
        target = self._resolve(locator)

        try:
            value = target.inner_text()
            self._log(f"[READ] TEXT successful → {log_name}")
            return value
        except Exception as error:
            self._log(f"[READ] TEXT failed → {log_name} | {error}")
            raise

    def get_value(self, locator: str | Locator) -> str:
        log_name = self._locator_name(locator)
        self._log(f"[READ] VALUE → {log_name}")
        target = self._resolve(locator)

        try:
            value = target.input_value()
            self._log(f"[READ] VALUE successful → {log_name}")
            return value
        except Exception as error:
            self._log(f"[READ] VALUE failed → {log_name} | {error}")
            raise

    def is_visible(self, locator: str | Locator) -> bool:
        log_name = self._locator_name(locator)
        target = self._resolve(locator)
        result = target.is_visible()
        self._log(f"[READ] VISIBLE → {log_name} = {result}")
        return result

    def is_enabled(self, locator: str | Locator) -> bool:
        log_name = self._locator_name(locator)
        target = self._resolve(locator)
        result = target.is_enabled()
        self._log(f"[READ] ENABLED → {log_name} = {result}")
        return result

    def is_checked(self, locator: str | Locator) -> bool:
        log_name = self._locator_name(locator)
        target = self._resolve(locator)
        result = target.is_checked()
        self._log(f"[READ] CHECKED → {log_name} = {result}")
        return result

    def count(self, locator: str | Locator) -> int:
        log_name = self._locator_name(locator)
        target = self._resolve(locator)
        result = target.count()
        self._log(f"[READ] COUNT → {log_name} = {result}")
        return result

    # ==========================================================
    # PAGE TRANSITIONS & NAVIGATION
    # ==========================================================

    def _page(self, page_name: str):
        if self.page_repository is None:
            raise RuntimeError("PageRepository has not been initialized")

        self._log(f"[PAGE] Loading → {page_name}")
        page = self.page_repository.get(page_name)
        self._log(f"[PAGE] Loaded → {page_name}")
        return page

    def navigate(self, url: str, timeout: int = 30000):
        self._log(f"[NAVIGATION] GOTO → {url}")
        try:
            self.page.goto(url, timeout=timeout)
            self._log(f"[NAVIGATION] GOTO successful → {url}")
        except Exception as error:
            self._log(f"[NAVIGATION] GOTO failed → {url} | {error}")
            raise

    def go_back(self):
        self._log("[NAVIGATION] BACK")
        try:
            self.page.go_back()
            self._log("[NAVIGATION] BACK successful")
        except Exception as error:
            self._log(f"[NAVIGATION] BACK failed → {error}")
            raise

    def go_forward(self):
        self._log("[NAVIGATION] FORWARD")
        try:
            self.page.go_forward()
            self._log("[NAVIGATION] FORWARD successful")
        except Exception as error:
            self._log(f"[NAVIGATION] FORWARD failed → {error}")
            raise

    def reload(self):
        self._log("[NAVIGATION] RELOAD")
        try:
            self.page.reload()
            self._log("[NAVIGATION] RELOAD successful")
        except Exception as error:
            self._log(f"[NAVIGATION] RELOAD failed → {error}")
            raise

    def wait_for_page_load(self):
        self._log("[WAIT] PAGE LOAD")
        try:
            self.page.wait_for_load_state("load")
            self._log("[WAIT] PAGE LOAD successful")
        except Exception as error:
            self._log(f"[WAIT] PAGE LOAD failed → {error}")
            raise

    def wait_for_network_idle(self):
        self._log("[WAIT] NETWORK IDLE")
        try:
            self.page.wait_for_load_state("networkidle")
            self._log("[WAIT] NETWORK IDLE successful")
        except Exception as error:
            self._log(f"[WAIT] NETWORK IDLE failed → {error}")
            raise

    # ==========================================================
    # HARDWARE & CONTEXT INTERACTIONS
    # ==========================================================

    def keyboard_press(self, key: str):
        self._log(f"[KEYBOARD] PRESS → {key}")
        try:
            self.page.keyboard.press(key)
            self._log(f"[KEYBOARD] PRESS successful → {key}")
        except Exception as error:
            self._log(f"[KEYBOARD] PRESS failed → {key} | {error}")
            raise

    def mouse_click(self, x: float, y: float):
        self._log(f"[MOUSE] CLICK → ({x}, {y})")
        try:
            self.page.mouse.click(x, y)
            self._log(f"[MOUSE] CLICK successful → ({x}, {y})")
        except Exception as error:
            self._log(f"[MOUSE] CLICK failed → ({x}, {y}) | {error}")
            raise

    def handle_new_window(self, trigger_action: Callable):
        self._log("[WINDOW] Waiting for new page")
        try:
            with self.page.context.expect_page() as page_info:
                trigger_action()
            new_page = page_info.value
            new_page.wait_for_load_state()
            self._log(f"[WINDOW] New page opened → {new_page.url}")
            return new_page
        except Exception as error:
            self._log(f"[WINDOW] Failed → {error}")
            raise

    def frame(self, selector: str):
        self._log(f"[FRAME] Access → {selector}")
        return self.page.frame_locator(selector)

    def screenshot(self, path: str, full_page: bool = False):
        self._log(f"[SCREENSHOT] Capture → {path}")
        try:
            self.page.screenshot(path=path, full_page=full_page)
            self._log(f"[SCREENSHOT] Successful → {path}")
        except Exception as error:
            self._log(f"[SCREENSHOT] Failed → {path} | {error}")
            raise
