# Locator Rules

- Locator source of truth is `tests/locators/*.json`.
- Use the supported strategies: `role`, `label`, `placeholder`, `text`, `test_id`, `alt_text`, `css`, `xpath`.
- Prefer accessibility semantics over CSS/XPath.
- Never invent a selector, attribute, role, text, or test id.
- If AI healing proposes a locator, validate it against the live page before accepting it.
- Do not persist an AI-generated locator automatically without explicit review/configuration.
