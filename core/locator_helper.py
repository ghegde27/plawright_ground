# locator_helper.py

class LocatorHelper:

    # -------------------------------------------
    # FULL get_by_role() with ALL Playwright options
    # -------------------------------------------
    @staticmethod
    def by_role(
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
        locator = f"role={role}"

        filters = []

        if name is not None:
            if exact:
                filters.append(f"name=\"{name}\"")
            else:
                filters.append(f"name=/{name}/")

        if checked is not None:
            filters.append(f"checked={str(checked).lower()}")

        if disabled is not None:
            filters.append(f"disabled={str(disabled).lower()}")

        if expanded is not None:
            filters.append(f"expanded={str(expanded).lower()}")

        if include_hidden:
            filters.append("include-hidden=true")

        if level is not None:
            filters.append(f"level={level}")

        if pressed is not None:
            filters.append(f"pressed={str(pressed).lower()}")

        if selected is not None:
            filters.append(f"selected={str(selected).lower()}")

        # Append filters to the base role selector
        if filters:
            locator += "[" + " ".join(filters) + "]"

        return locator

    # -------------------------------------------
    # Additional locators (as before)
    # -------------------------------------------

    @staticmethod
    def by_id(id: str):
        return f"#{id}"

    @staticmethod
    def by_class(class_name: str):
        return f".{class_name}"

    @staticmethod
    def by_css(selector: str):
        return selector

    @staticmethod
    def by_xpath(xpath: str):
        return f"xpath={xpath}"

    @staticmethod
    def by_text(text: str):
        return f"text={text}"

    @staticmethod
    def by_exact_text(text: str):
        return f"text=\"{text}\""

    @staticmethod
    def button_with_text(text: str):
        return f"button:has-text('{text}')"

    @staticmethod
    def by_data_testid(testid: str):
        return f"[data-testid='{testid}']"

    @staticmethod
    def by_placeholder(placeholder: str):
        return f"input[placeholder='{placeholder}']"

    @staticmethod
    def nth(selector: str, index: int):
        return f"{selector} >> nth={index}"
