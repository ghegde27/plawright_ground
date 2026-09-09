# Playwright Rules

- Use Playwright Sync API because that is the framework's established execution model.
- Prefer framework methods such as `click`, `fill`, `press`, `hover`, `wait_for_visible`, `get_text`, etc.
- Do not put raw `page.locator()` calls into tests when a repository locator can be used.
- Prefer semantic Playwright locators: role, label, placeholder, text, test id, then CSS/XPath only when necessary.
- Do not add arbitrary sleeps. Prefer Playwright state-based waits and the framework wait methods.
- Preserve tracing, screenshots, video, HAR, Allure, and structured logging conventions.
