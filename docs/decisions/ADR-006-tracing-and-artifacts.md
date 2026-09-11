# ADR-006: Tracing and Test Artifacts

## Status
Accepted

## Context
Playwright tracing provides detailed diagnostics for failed tests. Screenshots and traces are useful for CI failures, while generating every artifact can consume storage.

## Decision
Tracing and screenshots should be configurable. Failure diagnostics should retain useful artifacts without unnecessary storage cost.

## Recommended Behavior
```text
Test
 |
 +---- Pass
 |      |
 |      +---- optional artifacts
 |
 +---- Fail
        |
        +---- screenshot
        |
        +---- trace
        |
        +---- logs
```

## Artifact Location
Example:
```text
artifacts/
└── <worker>/
    └── <test-name>/
        ├── screenshot.png
        └── trace.zip
```

## Parallel Execution
Artifact paths must be unique across workers.

## Cleanup
Temporary artifacts should follow the project's retention policy.

## Security
Artifacts must not expose secrets, passwords, authentication tokens, or sensitive customer information.
