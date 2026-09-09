# AI Generation Rules

- Treat the repository as the framework knowledge base.
- The LLM proposes; deterministic code/tests validate.
- Generated code must follow existing patterns found in representative files.
- Preserve requirement-to-test traceability when requirements are supplied.
- Never fabricate business rules or application behavior.
- For locator healing, use the accessibility snapshot as the current-page evidence and the original locator only to infer intent.
- Keep provider selection behind `llm/client.py`; consumers must not contain provider-specific branches.
- Claude is selected with `AI_PROVIDER=claude`; otherwise the configured existing provider is used.
- Feature flags are independent: `AI_ENABLED`, `AI_LOCATOR_GENERATION`, `AI_LOCATOR_HEALING`, `AI_TEST_GENERATION`, `AI_FAILURE_ANALYSIS`.
