from playwright.sync_api import expect


class AssertUtils:

    @staticmethod
    def element_visible(locator, message="Element should be visible"):
        expect(locator, message).to_be_visible()

    @staticmethod
    def element_hidden(locator, message="Element should be hidden"):
        expect(locator, message).to_be_hidden()

    @staticmethod
    def element_enabled(locator, message="Element should be enabled"):
        expect(locator, message).to_be_enabled()

    @staticmethod
    def element_disabled(locator, message="Element should be disabled"):
        expect(locator, message).to_be_disabled()

    @staticmethod
    def text_equals(locator, text, message="Text mismatch"):
        expect(locator, message).to_have_text(text)

    @staticmethod
    def text_contains(locator, text, message="Text not found"):
        expect(locator, message).to_contain_text(text)

    @staticmethod
    def element_count(locator, count, message="Element count mismatch"):
        expect(locator, message).to_have_count(count)

    @staticmethod
    def page_url(page, expected_url):
        expect(page).to_have_url(expected_url)

    @staticmethod
    def page_title(page, title):
        expect(page).to_have_title(title)

    @staticmethod
    def input_value(locator, value):
        expect(locator).to_have_value(value)

    @staticmethod
    def attribute(locator, attr, value):
        expect(locator).to_have_attribute(attr, value)
