# Heal a Failed Test

1. Inspect the failure and classify it as locator, application, environment, or test/framework failure.
2. Do not use AI for non-locator failures.
3. For locator failures, inspect the original locator and current accessibility evidence.
4. Generate one stable replacement using the framework's supported strategies.
5. Validate the candidate against the live page.
6. Prefer the smallest change; do not regenerate unrelated code.
7. Do not silently persist a healed locator unless explicitly requested.
