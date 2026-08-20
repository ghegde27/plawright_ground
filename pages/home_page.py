from playwright.sync_api import expect

from core.base_page import BasePage


class HomePage(BasePage):
    page_name = "home"

    def search_objects(
            self,
            search_text: str,
    ):

        if not search_text:
            raise ValueError(
                "Search text not provided"
            )

        self.click(
            "search_trigger"
        )

        self.wait_for_visible(
            "search_box"
        )

        results = (
            self.fetch_typeahead_search_results()
        )

        for result in results:
            print(result)

        self.fill(
            "search_box",
            search_text,
        )

        self.press(
            "search_box",
            "Enter",
        )

    def fetch_typeahead_search_results(self):

        return self.locator(
            "typeahead_results"
        ).all_inner_texts()

    def upload_prescription(self):

        self.locator(
            "upload_link"
        ).first.click()

        self.locator(
            "upload_button"
        ).click()

    def login(self):
        pass

    def move_to_lab_test(self):

        self.hover(
            "lab_tests")

        self.click(
            "all_tests"
        )

        expect(
            self.page
        ).to_have_url(
            "https://pharmeasy.in/diagnostics/all-tests"
        )
