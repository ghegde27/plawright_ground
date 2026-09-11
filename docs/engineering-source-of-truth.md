# Engineering Source of Truth

The Git repository is the authoritative source of truth for this engineering project.

The repository should contain and version-control:
- source code
- automated tests
- architecture documentation
- engineering standards
- Playwright guidelines
- configuration documentation
- Architecture Decision Records (ADRs)
- implementation decisions
- migration plans
- troubleshooting documentation
- CI/CD conventions
- AI/Codex engineering instructions

ChatGPT Project instructions provide working context and engineering guidance, but they must not become the only place where important engineering decisions exist.

When an important architectural or implementation decision is made:
1. Discuss and reason about it.
2. Implement it.
3. Document the final decision in the Git repository.
4. Commit the documentation together with the relevant code when appropriate.

If an AI assistant's understanding conflicts with the repository's documented architecture, treat the repository as authoritative and flag the conflict.

The repository should remain understandable to a new engineer without requiring access to ChatGPT or Codex conversation history.
