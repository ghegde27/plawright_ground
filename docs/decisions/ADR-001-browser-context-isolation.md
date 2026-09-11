# ADR-001: BrowserContext Isolation

## Status
Accepted

## Context
Playwright BrowserContexts provide isolated browser sessions. Tests may execute sequentially or in parallel. Sharing contexts can cause authentication leakage, cookie leakage, local storage contamination, test-data interference, and race conditions.

## Decision
Independent tests will use isolated BrowserContexts. The Browser may be reused according to the framework lifecycle, but BrowserContexts must remain isolated between independent tests.

## Consequences
### Benefits
- stronger test isolation
- safer parallel execution
- independent authentication
- reduced cross-test contamination

### Trade-offs
- context creation has overhead
- fixture lifecycle requires careful cleanup

## Alternatives Considered
### Shared BrowserContext
Rejected because of isolation and concurrency risks.

### Browser per Test
Rejected because browser startup is generally more expensive than context creation.

## Implementation Guidance
Context ownership must be explicit. The fixture that creates a context is responsible for cleanup. Do not store contexts in global mutable state.
