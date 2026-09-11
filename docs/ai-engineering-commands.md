# AI Engineering Commands

These commands are conventions for ChatGPT/Codex when working on this repository. They are not shell commands.

## `/implement`
Implement a requested feature. Inspect first, explain the approach, make focused changes, add/update tests, run validation, and review the diff.

Example:
```text
/implement
Add configurable Playwright tracing to the existing context fixture. Trace only when enabled and create unique artifacts for parallel workers.
```

## `/debug`
Investigate a failure and identify the root cause before changing code.

Example:
```text
/debug
This Playwright test intermittently times out while waiting for checkout. Find the root cause instead of increasing the timeout blindly.
```

## `/review`
Perform a Principal SDET code review.

Example:
```text
/review
Review the context fixture for lifecycle ownership, xdist compatibility, resource cleanup, and maintainability.
```

## `/testgen`
Convert requirements into meaningful scenarios, test cases, and automation candidates.

Example:
```text
/testgen
Generate checkout tests covering validation, payment failure, duplicate submission, session expiry, and important boundaries.
```

## `/architect`
Analyze architecture and propose alternatives before implementation.

Example:
```text
/architect
I need two independent BrowserContexts in one pytest test. Analyze the existing framework and recommend the cleanest architecture.
```

## `/refactor`
Improve existing code without changing behavior unnecessarily.

## `/explain`
Explain a technical concept from fundamentals through internals.

Example:
```text
/explain
Explain BrowserContext internals in Playwright Python and its relationship to the driver, browser process, and pytest workers.
```

## `/optimize`
Analyze execution time, fixture cost, browser/context reuse, parallelism, waits, network calls, and CI performance without sacrificing reliability.

## `/migrate`
Create and execute a migration strategy, such as Selenium → Playwright.
