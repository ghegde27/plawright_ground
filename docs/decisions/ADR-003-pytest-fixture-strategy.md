# ADR-003: pytest Fixture Strategy

## Status
Accepted

## Context
Playwright resources have setup and teardown requirements. pytest fixtures provide lifecycle management and dependency injection.

## Decision
pytest fixtures are the primary mechanism for managing Playwright initialization, Browser lifecycle, BrowserContext lifecycle, Page lifecycle, authentication state, and test artifacts.

## Principles
Fixtures should have one clear responsibility. Fixture scope should match resource lifecycle. Prefer fixture composition over large fixtures.

## Example Lifecycle
```text
Playwright fixture
       ↓
Browser fixture
       ↓
Context fixture
       ↓
Page fixture
       ↓
Test
       ↓
Page teardown
       ↓
Context teardown
       ↓
Browser teardown
```

## Consequences
### Benefits
- deterministic lifecycle
- dependency injection
- reusable setup
- centralized teardown

### Risks
Poor fixture scopes can cause shared state, performance issues, and resource leaks.

Every non-obvious fixture lifecycle should document ownership and teardown behavior.
