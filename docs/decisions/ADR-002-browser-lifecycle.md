# ADR-002: Browser Lifecycle

## Status
Accepted

## Context
Creating a browser instance is more expensive than creating a BrowserContext. The framework needs to balance performance with test isolation.

## Decision
The framework may reuse a Browser instance while creating isolated BrowserContexts for tests, provided lifecycle management is safe for the selected pytest execution model.

## Consequences
### Benefits
- reduced browser startup overhead
- faster execution
- context-level isolation

### Risks
- incorrect lifecycle management can leak resources
- changes must consider pytest-xdist

## Rules
- Browser ownership must be explicit.
- Context ownership must be explicit.
- Every created Context must be closed.
- Browser must be closed by its owner.
- Do not use global mutable Browser/Page state.

## Alternatives
### Browser per Test
Strong isolation but higher startup overhead.

### Shared Browser and Shared Context
Rejected because context sharing reduces test isolation.
