# ADR-005: Authentication and Storage State

## Status
Accepted

## Context
Many UI tests require an authenticated session. Logging in through the UI before every test can increase execution time and introduce additional failure points. Playwright supports storage state for reusable authenticated browser state.

## Decision
Use Playwright storage state where appropriate. Authentication strategy must depend on test requirements.

## When Storage State Is Appropriate
Use storage state when the test does not need to test the login flow itself.

## When UI Login Is Required
Use actual login flow for login behavior, authentication failures, session expiration, MFA, or authentication-specific functionality.

## Security
Never commit authentication state containing sensitive information. Do not expose tokens or cookies in logs.

## Parallel Execution
Authentication state must be safe for parallel workers. Tests that modify authentication state should use isolated state.

## Consequences
### Benefits
- faster tests
- reduced authentication duplication
- deterministic setup

### Trade-offs
- storage state can expire
- stale state can cause failures
- secure handling is required
