# Playwright Framework — Claude Instructions

## Mission

You are working inside an existing Python/Pytest/Playwright automation framework. Extend and maintain the framework; do not replace its architecture with a generic Playwright solution.

## Repository Map

- `core/`: framework primitives, BasePage, retry, logging, failure classification.
- `fixtures/`: browser/context/page/auth pytest fixtures.
- `pages/`: Page Objects; all should extend `BasePage` and define `page_name`.
- `locators/`: locator definitions, repositories, resolver, page discovery.
- `tests/`: business-facing automation tests and locator JSON.
- `llm/`: provider-neutral LLM client, prompts, locator generation, AI healing.
- `config/`: environment and AI runtime configuration.

## Non-negotiable behavior

1. Reuse existing framework abstractions before creating new ones.
2. Do not place raw selectors in tests if a repository locator can represent them.
3. Do not bypass `BasePage` for normal UI actions.
4. Do not invent selectors, business rules, credentials, or application behavior.
5. Keep LLM providers behind `LLMClient`/`BaseLLMProvider`.
6. Claude is a runtime provider, not a second framework. Select it with `AI_PROVIDER=claude`.
7. If `AI_PROVIDER` is not `claude`, preserve the existing provider behavior via `LLM_PROVIDER` (defaulting to Groq for backward compatibility).
8. Feature flags must allow AI capabilities to be disabled independently.
9. AI output is untrusted input and must be schema/behavior validated before use.
10. Make the smallest safe change and add/update tests.

## Runtime provider flags

```text
AI_ENABLED=true
AI_PROVIDER=claude
AI_MODEL=claude-sonnet-4
ANTHROPIC_API_KEY=<secret>

AI_LOCATOR_GENERATION=true
AI_LOCATOR_HEALING=true
AI_TEST_GENERATION=true
AI_FAILURE_ANALYSIS=true
```

Fallback to the existing provider:

```text
AI_PROVIDER=groq
GROQ_API_KEY=<secret>
```

## Workflow

Before editing:
- inspect the relevant implementation and its tests;
- identify existing reusable abstractions;
- make a minimal change.

After editing:
- run focused tests first;
- run the full unit suite when practical;
- report failures honestly;
- never claim an external PR was created unless the push/PR operation actually succeeded.
