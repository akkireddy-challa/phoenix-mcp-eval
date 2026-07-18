# Security Policy

## Supported Versions

| Version | Supported |
|---------|----------|
| 0.1.x   | Yes      |

## Reporting a Vulnerability

Do **not** open a public GitHub issue for security vulnerabilities.

Please report security issues by emailing the maintainer directly via GitHub private contact, or by using [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability).

## Security Model

- API keys are read from environment variables and never logged
- No credentials are stored in code or repository
- All Phoenix API calls use HTTPS
- MCP server runs locally (stdio transport) — no network exposure by default

## Scope

In scope:
- Authentication/authorization bypass
- API key leakage via logs or error messages
- Remote code execution
- Dependency vulnerabilities with real-world impact

Out of scope:
- Issues in Arize Phoenix itself (report to Arize)
- Theoretical attacks without proof of concept

## Response Timeline

We aim to acknowledge reports within 48 hours and provide a fix within 14 days for critical issues.
