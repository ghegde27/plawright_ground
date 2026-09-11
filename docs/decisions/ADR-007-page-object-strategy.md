# ADR-007: Page Object Strategy

## Status
Accepted

## Context
UI automation becomes difficult to maintain when locators and interaction logic are duplicated across tests. Page Objects can encapsulate page interactions.

## Decision
Use Page Objects where they provide meaningful reuse and separation of concerns.

Page Objects should encapsulate:
- locators
- page interactions
- reusable UI actions

Tests should focus on:
- business scenarios
- test data
- assertions

## Responsibilities
### Page Object
Locators, UI interaction, reusable page-level behavior.

### Test
Scenario orchestration, business intent, assertions.

## Anti-Pattern
Avoid very large Page Objects containing unrelated workflows. Split them into logical components when necessary.

## Locators
Prefer role, label, test ID, and stable attributes. Avoid fragile DOM structures.

## Consequences
### Benefits
- reduced locator duplication
- easier maintenance
- readable tests
- centralized UI interaction logic

### Trade-offs
- additional abstraction
- poorly designed Page Objects can become difficult to maintain

## Principle
Use Page Objects to improve maintainability, not simply because every test must have one.
