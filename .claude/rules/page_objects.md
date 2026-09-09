# Page Object Rules

- Extend `BasePage`.
- Define `page_name`.
- Keep locators out of Page Object Python code unless the framework explicitly requires a direct Playwright Locator.
- Use locator names from the page repository.
- Expose business actions rather than low-level Playwright implementation details.
- Reuse existing page objects via `PageRepository` and its lazy page instances.
