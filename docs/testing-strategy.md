# Testing Strategy

## 1. Purpose
This document defines the strategy for designing and implementing automated tests.

## 2. Test Pyramid
Use the lowest practical test level for a behavior:
```text
             E2E
            /   \
       Integration
          /     \
        API / UI
          /     \
          Unit
```

## 3. Test Case Design
Consider:
- happy path
- negative path
- boundary conditions
- authentication
- dependency failures
- concurrency/race conditions

## 4. Test Independence
Tests must not depend on execution order. Each test should own its required data and state.

## 5. Determinism
Avoid arbitrary sleeps, uncontrolled random data, shared mutable state, and uncontrolled external dependencies.

## 6. Parallel Execution
Tests should be safe for pytest-xdist where supported. Consider worker IDs, data, artifacts, authentication, filesystem access, and external limits.

## 7. Failure Diagnostics
Useful diagnostics include error messages, screenshots, traces, logs, relevant test data, and environment information.

## 8. Flaky Tests
Treat flaky tests as defects until proven otherwise. Investigate synchronization, race conditions, test data, external dependencies, and environment instability.

## 9. Regression Testing
Production defects that can be automated should be considered for regression coverage.

## 10. Test Naming
Prefer behavior-oriented names such as:
```python
test_user_cannot_checkout_with_expired_card()
```

## 11. Test Review
Review correctness, assertions, isolation, determinism, maintainability, locator quality, cleanup, and parallel safety.
