# Framework Configuration

## 1. Purpose
Configuration controls environment-specific and execution-specific behavior.

## 2. Configuration Principles
Separate configuration from test implementation.

Do not hardcode:
- URLs
- credentials
- browser settings
- proxy settings
- timeouts
- artifact locations

## 3. Typical Configuration
- Environment
- Browser
- Headless
- Base URL
- Timeouts
- Viewport
- Locale
- Timezone
- Proxy
- Permissions
- Headers
- Storage State
- Tracing
- Screenshots
- Video

## 4. Environment
Environment should be selected externally, for example:
```text
ENV=qa
```

## 5. Secrets
Never commit passwords, API keys, tokens, private certificates, or session cookies.

## 6. Browser Capabilities
Capabilities should use the existing project configuration mechanism.

## 7. Validation
Validate configuration early and fail clearly when invalid.

## 8. Defaults
Defaults should be documented, safe, and predictable.

## 9. Parallel Execution
Configuration must not create shared mutable state that breaks pytest-xdist.

## 10. Source of Truth
Configuration conventions must be documented in Git and remain consistent with implementation.
