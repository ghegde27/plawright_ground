# Generate a Page Object

Create or extend a Page Object using the repository's existing conventions.

- Extend `BasePage`.
- Define `page_name`.
- Add locator definitions to `tests/locators/<page>.json`.
- Expose business actions.
- Use BasePage actions rather than raw Playwright calls.
- Add focused tests.
