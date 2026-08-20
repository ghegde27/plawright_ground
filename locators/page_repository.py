import importlib
import inspect
from pathlib import Path

from core.base_page import BasePage


class PageRepository:

    def __init__(
            self,
            page,
            pages_dir: str,
            locator_repository,
            ai_locator_healer=None,
    ):

        self._page = page

        self._pages_dir = Path(
            pages_dir
        )

        self._locator_repository = (
            locator_repository
        )

        self._ai_locator_healer = (
            ai_locator_healer
        )

        # ------------------------------------------------------
        # Discovered Page Classes
        # ------------------------------------------------------

        self._page_classes = {}

        # ------------------------------------------------------
        # Lazy Page Instances
        # ------------------------------------------------------

        self._page_instances = {}

        self._discover_pages()

    # ==========================================================
    # DISCOVER PAGE CLASSES
    # ==========================================================

    def _discover_pages(self):

        if not self._pages_dir.exists():
            raise FileNotFoundError(
                f"Pages directory does not exist: "
                f"{self._pages_dir}"
            )

        for file in self._pages_dir.glob(
                "*_page.py"
        ):

            module_name = file.stem

            module = importlib.import_module(
                f"pages.{module_name}"
            )

            for (
                    class_name,
                    page_class,
            ) in inspect.getmembers(
                module,
                inspect.isclass,
            ):

                # --------------------------------------------------
                # Ignore imported classes
                # --------------------------------------------------

                if (
                        page_class.__module__
                        != module.__name__
                ):
                    continue

                # --------------------------------------------------
                # Only BasePage subclasses
                # --------------------------------------------------

                if not issubclass(
                        page_class,
                        BasePage,
                ):
                    continue

                if page_class is BasePage:
                    continue

                # --------------------------------------------------
                # page_name is mandatory
                # --------------------------------------------------

                page_name = getattr(
                    page_class,
                    "page_name",
                    None,
                )

                if not page_name:
                    raise ValueError(
                        f"{class_name} must define "
                        f"'page_name'"
                    )

                # --------------------------------------------------
                # Duplicate page names
                # --------------------------------------------------

                if page_name in self._page_classes:
                    existing = (
                        self._page_classes[
                            page_name
                        ]
                    )

                    raise ValueError(
                        f"Duplicate page_name "
                        f"'{page_name}': "
                        f"{existing.__name__} and "
                        f"{class_name}"
                    )

                self._page_classes[
                    page_name
                ] = page_class

    # ==========================================================
    # GET PAGE
    # ==========================================================

    def get(
            self,
            page_name: str,
    ):

        # ------------------------------------------------------
        # Already initialized?
        # ------------------------------------------------------

        if page_name in self._page_instances:
            return self._page_instances[
                page_name
            ]

        # ------------------------------------------------------
        # Validate page
        # ------------------------------------------------------

        if page_name not in self._page_classes:
            raise AttributeError(
                f"Page '{page_name}' not found. "
                f"Available pages: "
                f"{list(self._page_classes.keys())}"
            )

        page_class = (
            self._page_classes[
                page_name
            ]
        )

        # ======================================================
        # LAZY PAGE CREATION
        # ======================================================

        # Page Object itself receives NO dependencies.
        #
        # HomePage:
        #
        # class HomePage(BasePage):
        #     page_name = "home"
        #
        # No __init__ required.
        # ======================================================

        page_instance = page_class()

        # ======================================================
        # INJECT FRAMEWORK DEPENDENCIES INTO BASE PAGE
        # ======================================================

        page_instance._initialize(
            page=self._page,
            locator_repository=(
                self._locator_repository
            ),
            ai_locator_healer=(
                self._ai_locator_healer
            ),
            page_repository=self,
        )

        # ------------------------------------------------------
        # Cache instance
        # ------------------------------------------------------

        self._page_instances[
            page_name
        ] = page_instance

        return page_instance

    # ==========================================================
    # ATTRIBUTE ACCESS
    # ==========================================================

    def __getattr__(
            self,
            name: str,
    ):

        if name.startswith("_"):
            raise AttributeError(
                name
            )

        if name in self._page_classes:
            return self.get(
                name
            )

        raise AttributeError(
            f"Page '{name}' not found. "
            f"Available pages: "
            f"{list(self._page_classes.keys())}"
        )

    # ==========================================================
    # INFORMATION
    # ==========================================================

    def available_pages(self):

        return list(
            self._page_classes.keys()
        )

    def initialized_pages(self):

        return list(
            self._page_instances.keys()
        )
