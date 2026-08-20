from playwright.sync_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
)


class FailureType:
    LOCATOR_FAILURE = "LOCATOR_FAILURE"
    ACTION_FAILURE = "ACTION_FAILURE"
    UNKNOWN = "UNKNOWN"


class ActionFailureClassifier:

    @staticmethod
    def classify(error: Exception, locator) -> str:
        # 1. Timeout
        if isinstance(error, PlaywrightTimeoutError):
            return FailureType.LOCATOR_FAILURE

        # 2. Playwright errors
        if isinstance(error, PlaywrightError):
            message = str(error).lower()

            # Locator-related failures
            locator_errors = (
                "strict mode violation",
                "locator resolved to",
                "waiting for locator",
                "element(s) not found",
                "failed to find element",
                "no element found",
                "element is not attached",
            )

            if any(text in message for text in locator_errors):
                return FailureType.LOCATOR_FAILURE

            # Genuine action/browser failures
            action_errors = (
                "browser has been closed",
                "page has been closed",
                "target page",
                "target closed",
                "context has been closed",
                "connection closed",
            )

            if any(text in message for text in action_errors):
                return FailureType.ACTION_FAILURE

        # 3. Unknown
        return FailureType.UNKNOWN
