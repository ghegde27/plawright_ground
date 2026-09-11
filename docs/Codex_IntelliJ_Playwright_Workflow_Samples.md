# Codex + IntelliJ IDEA — Playwright SDET Workflow Samples

This file is a practical sample of how to use Codex inside IntelliJ IDEA for a Playwright + Python + pytest framework.

> **Important:** `/explain`, `/architect`, `/implement`, `/debug`, `/review`, `/testgen`, `/refactor`, `/optimize`, and `/migrate` are command conventions. If the Codex IntelliJ UI does not treat them as built-in slash commands, paste the full prompt normally.

---

## 1. Repository structure

Open the Playwright framework repository in IntelliJ IDEA.

Recommended structure:

```text
playwright_framework/
├── .codex/
│   └── instructions.md
├── docs/
│   ├── architecture.md
│   ├── playwright-guidelines.md
│   ├── testing-strategy.md
│   ├── configuration.md
│   ├── ai-engineering-commands.md
│   └── decisions/
├── tests/
├── conftest.py
├── pyproject.toml
└── ...
```

The key file is:

```text
.codex/instructions.md
```

It contains the persistent engineering rules that Codex should follow.

---

# 2. Start with `/explain`

Use this first when working with an unfamiliar repository.

```text
/explain

Analyze this Playwright framework and explain:

1. Overall architecture
2. pytest fixture hierarchy
3. Browser/BrowserContext/Page lifecycle
4. Configuration flow
5. Test execution flow
6. Authentication strategy
7. Trace and screenshot handling
8. Parallel execution support
9. Existing architectural decisions

Do not modify any files.

Reference the relevant repository files while explaining.
```

### Purpose

This is a read-only repository analysis.

Use it before making changes so Codex understands the existing architecture.

---

# 3. Use `/architect` before a significant change

Example: adding a reusable BrowserContext fixture.

```text
/architect

I want to introduce a reusable Playwright BrowserContext fixture.

Requirements:
- Browser can be reused
- Each test gets an isolated BrowserContext
- Context capabilities come from configuration
- Trace should be configurable
- Screenshots should be captured on failure
- Fixture must work with pytest
- It must support parallel execution

Analyze the existing framework first.

Do not implement yet.

Provide:
1. Current architecture
2. Proposed design
3. Files that need modification
4. Fixture lifecycle
5. Configuration changes
6. Risks
7. Testing strategy
8. Relevant ADRs
```

### Purpose

`/architect` should answer:

> What should we build and why?

before asking Codex to change the repository.

---

# 4. Implement with `/implement`

After reviewing the architecture/design:

```text
/implement

Implement the BrowserContext fixture design we just discussed.

Before changing anything:
1. Re-read the relevant repository documentation.
2. Inspect the existing fixtures and configuration.
3. Follow existing framework conventions.
4. Do not introduce unnecessary abstractions.

Requirements:
- BrowserContext isolation per test
- Capabilities from configuration
- Configurable tracing
- Screenshot on failure
- Proper cleanup
- pytest compatible
- xdist compatible

After implementation:
1. Run relevant tests.
2. Run lint/type checks if configured.
3. Review the changes.
4. Report modified files.
5. Report test results.
6. Identify any remaining risks.
```

### Purpose

`/implement` is the main development workflow.

Codex should inspect → design → implement → test → validate → report.

---

# 5. Debug failures with `/debug`

Example failure:

```text
playwright._impl._errors.TimeoutError:
locator.click: Timeout 30000ms exceeded
```

Use:

```text
/debug

This test is failing with:

playwright._impl._errors.TimeoutError:
locator.click: Timeout 30000ms exceeded

Investigate the root cause.

Steps:
1. Inspect the failing test.
2. Inspect the locator.
3. Inspect the Page Object.
4. Inspect relevant fixtures.
5. Check whether the element is actually available.
6. Check synchronization/waiting behavior.
7. Determine whether this is:
   - locator problem
   - timing problem
   - fixture problem
   - application behavior
   - test-data problem
   - environment problem

Do not increase timeout unless evidence shows timeout is actually the problem.

Explain the root cause before modifying code.
```

### Important

Avoid using a larger timeout as the default fix.

Bad approach:

```python
timeout=120000
```

unless there is evidence that the timeout itself is the problem.

---

# 6. Review code with `/review`

After implementation:

```text
/review

Review the current changes as a Principal SDET.

Check:

### Playwright
- BrowserContext isolation
- locator quality
- auto-waiting
- synchronization
- Page lifecycle
- resource cleanup

### pytest
- fixture scope
- fixture dependencies
- teardown
- parametrization
- parallel execution

### Framework
- maintainability
- coupling
- abstraction quality
- configuration
- extensibility

### Reliability
- flaky-test risks
- race conditions
- shared state
- test-data collisions

### Security
- credentials
- tokens
- storage state
- logs
- screenshots
- traces

Do not modify code.

Categorize findings as:
CRITICAL
HIGH
MEDIUM
LOW

For each finding provide:
- file
- problem
- why it matters
- recommended fix
```

### Purpose

Use `/review` as a quality gate before committing.

---

# 7. Generate tests with `/testgen`

Example requirement:

```text
Users should be able to reset their password using the
"Forgot Password" flow.
```

Prompt:

```text
/testgen

Generate tests for this requirement:

Users should be able to reset their password using
the "Forgot Password" flow.

First identify:
1. Business rules
2. Positive scenarios
3. Negative scenarios
4. Boundary cases
5. Validation cases
6. Authentication/security cases
7. API/backend considerations
8. UI automation candidates

Then classify each test as:
- UI
- API
- Integration
- Unit

For UI candidates, generate Playwright + pytest tests
following this repository's conventions.

Do not duplicate existing tests.
```

### Purpose

The desired flow is:

```text
Requirement
    ↓
Business rules
    ↓
Test scenarios
    ↓
Test cases
    ↓
Automation candidates
    ↓
Playwright tests
```

---

# 8. Refactor with `/refactor`

Example: authentication code has duplication.

```text
/refactor

Review the authentication implementation.

Goal:
Reduce duplication without changing behavior.

Requirements:
- Preserve existing test behavior
- Preserve fixture contracts
- Preserve public APIs
- Do not introduce unnecessary abstractions
- Follow the existing architecture
- Update tests if required

Before modifying:
1. Identify duplication.
2. Explain the proposed refactoring.
3. Identify risks.

Then implement and validate.
```

### Purpose

Refactor for maintainability without changing intended behavior.

---

# 9. Optimize with `/optimize`

Example: Playwright suite is slow.

```text
/optimize

Analyze Playwright test execution performance.

Investigate:

1. Browser startup
2. BrowserContext creation
3. Page creation
4. Authentication
5. Storage state
6. Fixtures
7. Test data setup
8. Parallel execution
9. Trace/video collection
10. Unnecessary waits

Do not optimize blindly.

Measure or identify evidence first.

Provide:
- current bottlenecks
- expected impact
- risks
- recommended changes

Do not modify code yet.
```

### Purpose

Optimize based on evidence rather than assumptions.

---

# 10. Migrate with `/migrate`

Example: Selenium → Playwright.

```text
/migrate

Analyze the existing Selenium framework and propose
a migration to Playwright + Python + pytest.

Map:

Selenium WebDriver
→ Playwright Browser

WebDriver session
→ BrowserContext

WebDriver page
→ Page

Explicit waits
→ Playwright auto-waiting

ExpectedConditions
→ Locator assertions / web-first assertions

PageFactory
→ Playwright Page Objects

ThreadLocal
→ pytest fixture/context isolation

Selenium Grid
→ Playwright workers / browser execution

Do not implement yet.

Produce a phased migration plan with risks.
```

---

# 11. Recommended complete workflow

For a normal framework change, use:

```text
/explain
    ↓
/architect
    ↓
Review design
    ↓
/implement
    ↓
Run tests
    ↓
/debug       ← only if failures occur
    ↓
/review
    ↓
git diff
    ↓
git commit
```

Visualized:

```text
           ┌─────────────┐
           │   Explain   │
           └──────┬──────┘
                  ↓
           ┌─────────────┐
           │  Architect  │
           └──────┬──────┘
                  ↓
           ┌─────────────┐
           │  Implement  │
           └──────┬──────┘
                  ↓
           ┌─────────────┐
           │    Test     │
           └──────┬──────┘
                  ↓
          ┌───────┴────────┐
          ↓                ↓
       PASS             FAILURE
          ↓                ↓
       Review            /debug
          ↓                │
       Git commit ←────────┘
```

---

# 12. Quick command reference

| Command | Use it for | Modifies code? |
|---|---|---:|
| `/explain` | Understand repository/code | No |
| `/architect` | Design a solution | No |
| `/implement` | Implement a change | Yes |
| `/debug` | Investigate and fix failures | Usually yes |
| `/review` | Principal SDET code review | No |
| `/testgen` | Generate test scenarios/tests | Depends |
| `/refactor` | Improve structure without changing behavior | Yes |
| `/optimize` | Performance analysis/optimization | Depends |
| `/migrate` | Framework/technology migration | Depends |

---

# 13. Example: Complete real-world task

Suppose you need to add authentication using Playwright storage state.

### Step 1 — Understand

```text
/explain

Analyze the current authentication implementation.

Do not modify files.

Explain:
- current login flow
- authentication fixtures
- browser/context lifecycle
- storage state usage
- configuration
- secrets handling
- relevant ADRs
```

### Step 2 — Design

```text
/architect

Design a Playwright authentication strategy using storage state.

Goals:
- Avoid UI login for every test
- Keep tests isolated
- Support parallel execution
- Never commit credentials
- Allow auth state to be refreshed
- Preserve tests that specifically validate login

Do not implement.

Provide the proposed architecture and file changes.
```

### Step 3 — Implement

```text
/implement

Implement the approved authentication architecture.

Follow:
- repository documentation
- existing fixture conventions
- ADRs
- security requirements

Do not expose credentials or secrets.

Run relevant tests after implementation.
```

### Step 4 — Debug if needed

```text
/debug

Authentication tests are failing after the storage-state change.

Investigate the root cause.

Do not modify code until the root cause is identified.
```

### Step 5 — Review

```text
/review

Review the authentication implementation.

Pay special attention to:
- storage state isolation
- secrets
- fixture scope
- parallel execution
- token leakage
- artifact leakage
- authentication reliability

Do not modify code.
```

### Step 6 — Commit

After the review is clean:

```bash
git status
git diff
git add .
git commit -m "feat: add Playwright authentication storage state"
```

---

# 14. Golden rules for Codex

Always prefer:

```text
Understand → Design → Implement → Test → Review
```

rather than:

```text
Ask AI → Generate code → Hope it works
```

For Playwright specifically:

- Prefer `BrowserContext` isolation.
- Let Playwright auto-wait.
- Avoid arbitrary `time.sleep()`.
- Prefer resilient locators.
- Keep fixtures focused.
- Avoid global mutable `Page` or `BrowserContext`.
- Keep test assertions in tests.
- Keep reusable UI interaction logic in Page Objects.
- Make parallel execution safe.
- Keep credentials and tokens out of source control.
- Capture diagnostics deterministically.
- Document important architectural decisions as ADRs.

---

# 15. Source-of-truth principle

The engineering hierarchy should be:

```text
Git repository
      ↓
Code + tests + docs + ADRs
      ↓
.codex/instructions.md
      ↓
Codex
      ↓
IntelliJ IDEA
```

The **Git repository is the authoritative source of truth**.

Chat history should not be required to understand why the framework works the way it does.

When an important architectural decision is made:

```text
Decision
   ↓
Implement
   ↓
Document
   ↓
ADR
   ↓
Git commit
```

This makes the framework maintainable even when the original developer, ChatGPT, or Codex is no longer involved.

---

## Recommended first command

When you open the repository in IntelliJ IDEA, start with:

```text
/explain

Analyze this repository and explain its architecture.

Do not modify anything.
```

Then move to `/architect` for the first change.
