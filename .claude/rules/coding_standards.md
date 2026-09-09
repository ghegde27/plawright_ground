# Coding Standards

- Follow existing formatting and naming conventions.
- Prefer small, testable functions and explicit types for public interfaces.
- Log AI provider selection and failures without logging API keys or secrets.
- Preserve backward compatibility unless a requirement explicitly changes behavior.
- Add unit tests for provider selection, feature flags, and provider adapters.
- Do not commit `.env`, credentials, generated Allure results, caches, or browser artifacts.
