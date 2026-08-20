import json
from pathlib import Path

from locators.locator_definition import LocatorDefinition


class LocatorRepository:

    def __init__(self, locator_dir: str):

        self.locator_dir = Path(locator_dir)
        self._cache = {}

    def _load_page(self, page_name: str):

        if page_name not in self._cache:

            file = (
                    self.locator_dir
                    / f"{page_name}.json"
            )

            if not file.exists():
                raise FileNotFoundError(
                    f"Locator file not found: {file}"
                )

            with open(
                    file,
                    "r",
                    encoding="utf-8",
            ) as f:
                self._cache[page_name] = json.load(f)

        return self._cache[page_name]

    def get(
            self,
            page_name: str,
            locator_name: str,
    ) -> LocatorDefinition:

        page_locators = self._load_page(
            page_name
        )

        if locator_name not in page_locators:
            raise KeyError(
                f"Locator '{locator_name}' "
                f"not found in {page_name}.json"
            )

        data = page_locators[
            locator_name
        ]

        return LocatorDefinition(
            name=locator_name,
            strategy=data["strategy"],
            value=data["value"],
            options=data.get("options", {}),
            description=data.get("description"),
        )
