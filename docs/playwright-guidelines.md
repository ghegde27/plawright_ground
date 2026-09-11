# Playwright Engineering Guidelines

## 1. Purpose
These guidelines define how Playwright should be used within the automation framework.

## 2. Browser vs BrowserContext vs Page
```text
Browser
   |
   +---- BrowserContext
             |
             +---- Page
```

Browser is the browser instance/process. BrowserContext is an isolated browser session. Page is a browser tab/page.

## 3. BrowserContext Isolation
Prefer a separate BrowserContext for independent tests. Do not share authentication state unintentionally. Avoid global Context or Page objects.

## 4. Locators
Preferred order:
1. `get_by_role()`
2. `get_by_label()`
3. `get_by_test_id()`
4. stable application attributes
5. CSS
6. XPath when justified

Example:
```python
page.get_by_role("button", name="Submit")
```

## 5. Synchronization
Prefer Playwright auto-waiting and condition-based synchronization. Avoid arbitrary `time.sleep()`.

## 6. Assertions
Assertions should verify meaningful business behavior.
```python
expect(page.get_by_text("Order confirmed")).to_be_visible()
```

Do not weaken assertions simply to reduce failures.

## 7. Authentication
Use the framework authentication strategy. Where appropriate, use storage state. Never hardcode credentials or print tokens.

## 8. Tracing
Tracing should be configurable. Prefer retaining useful trace artifacts on failures.

## 9. Screenshots
Capture screenshots on failure or at explicit diagnostic points. Avoid excessive artifacts.

## 10. Network Interception
Use mocking/interception for deterministic external dependencies, failure simulation, or unavailable third-party services. Do not mock the system under test unnecessarily.

## 11. Page Objects
Page Objects should encapsulate locators and reusable page interactions. Avoid turning them into large business-logic classes.

## 12. Test Data
Test data should be deterministic, isolated, environment-aware, and safe for parallel execution.

## 13. Anti-Patterns
Avoid arbitrary sleeps, global Page/Context state, hardcoded credentials/URLs, brittle XPath, blind retries, huge Page Objects, and duplicate fixtures.

## 14. Reliability Principle
Synchronize with application behavior, not arbitrary elapsed time.

## 15. Version Awareness
Distinguish documented Playwright API behavior from implementation details that may change between versions.
