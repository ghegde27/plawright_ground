# Framework Architecture Rules

- This repository is a Python + Pytest + Playwright Sync API automation framework.
- Reuse the existing layers: `pages/`, `locators/`, `fixtures/`, `core/`, `config/`, `utils/`, and `llm/`.
- Do not introduce a second page-object, locator, fixture, or LLM abstraction when an existing one can be reused.
- Page Objects extend `core.base_page.BasePage` and define a mandatory `page_name`.
- Locator definitions belong in `tests/locators/<page>.json`; resolve them through `LocatorRepository`/`LocatorResolver`.
- Keep tests focused on business intent; framework mechanics belong in pages, fixtures, core, or utils.
- AI is an assistive layer. It must never silently bypass deterministic framework validation.
