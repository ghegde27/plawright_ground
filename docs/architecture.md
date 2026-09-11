# Playwright Framework Architecture

## 1. Purpose
This document describes the architecture, responsibilities, lifecycle, and engineering principles of the Playwright automation framework.

The Git repository is the authoritative source of truth for this architecture.

## 2. Technology Stack
- Python
- pytest
- Playwright
- pytest-xdist where parallel execution is required
- Git
- CI/CD platform

## 3. High-Level Architecture
```text
Test Requirements
      |
      v
Test Scenarios
      |
      v
pytest Tests
      |
      v
Page Objects
      |
      v
Page
      |
      v
BrowserContext
      |
      v
Browser
      |
      v
Playwright
      |
      v
Web Application
```

## 4. Browser Lifecycle
```text
Browser
   |
   +---- BrowserContext A
   |          |
   |          +---- Page A1
   |          +---- Page A2
   |
   +---- BrowserContext B
              |
              +---- Page B1
              +---- Page B2
```

Browser represents the browser process. BrowserContext represents an isolated browser session. Page represents a browser tab/page inside a context.

## 5. Isolation Model
Tests should use isolated BrowserContexts whenever test isolation is required. Tests should not share mutable browser state unless explicitly required.

## 6. Framework Components
### Configuration
Environment, browser, capabilities, timeouts, authentication, and artifact configuration.

### Browser Manager
Playwright initialization, browser creation, lifecycle, and shutdown.

### Context Fixture
BrowserContext creation, configuration, authentication state, tracing, screenshots, and cleanup.

### Page Objects
Page-level interactions, locators, and reusable user actions.

### Tests
Business scenarios, test data orchestration, and assertions.

### Reporting
Results, screenshots, traces, logs, and failure diagnostics.

## 7. Test Execution Flow
```text
pytest starts
   |
Fixture initialization
   |
Browser available
   |
BrowserContext created
   |
Authentication/state configured
   |
Page created
   |
Test executes
   |
Assertions
   |
Failure artifacts collected
   |
Tracing stopped
   |
Cleanup
   |
Test result reported
```

## 8. Parallel Execution
Parallel execution must consider worker isolation, BrowserContext isolation, test data, artifact naming, filesystem collisions, external-service limits, and authentication state.

## 9. Design Principles
- Reliability
- Isolation
- Maintainability
- Reusability
- Simplicity
- Configuration-driven behavior

## 10. Source of Truth
The Git repository is the authoritative source of truth for architecture, engineering standards, implementation decisions, test strategy, configuration conventions, and ADRs.

AI tools may assist with design and implementation, but important decisions must be documented in Git.

## 11. Architectural Changes
Significant architectural changes should be documented using an ADR under `docs/decisions/`.

## 12. New Engineer Principle
A new engineer should be able to understand the framework architecture without requiring access to historical AI conversations.
