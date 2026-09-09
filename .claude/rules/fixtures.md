# Fixture Rules

- Reuse existing pytest fixtures before creating new fixtures.
- Browser, context, page, authentication, repositories, and AI services are injected through `conftest.py` and `fixtures/`.
- Keep fixture scopes intentional; do not change session/function scope without a reason.
- Never hard-code credentials. Use environment variables and existing auth configuration.
