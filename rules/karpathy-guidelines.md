---
name: karpathy-guidelines
description: Behavioral guidelines for writing, reviewing, or refactoring code to reduce overcomplication, hidden assumptions, unnecessary edits, and unverified results.
trigger: always_on
---

# Karpathy Guidelines

Use these guidelines when a coding task involves implementation, debugging, review, or refactoring. They bias toward caution over speed; use judgment for trivial changes.

## Think before coding

- State important assumptions before implementing.
- If the request has multiple plausible interpretations, surface them and ask when the choice materially changes the result.
- Call out confusing requirements, meaningful tradeoffs, and simpler alternatives.
- **Respect the problem, not the code:** Before modifying or removing non-obvious logic (defensive checks, workarounds, fallbacks), identify the underlying constraint it was solving.
- **Escape the patch trap:** Do not stay trapped in a timid fix-mindset. Once the core purpose is understood, feel empowered to construct novel, elegant solutions that solve the root cause rather than piling bandages onto historical accidents.
- **Novelty through simplification:** The best novel solutions don't add layers—they replace clumsy defensive hacks with clean, robust primitives that satisfy the original constraints naturally.

## Simplicity first

- Implement the minimum needed to satisfy the request.
- Avoid speculative features, abstractions for one-time use, and unrequested configurability.
- Treat unnecessary complexity as a defect: if a much smaller solution works, prefer it.

## Make surgical changes

- Touch only files and lines required by the request.
- Preserve surrounding behavior, style, comments, and formatting.
- Do not refactor unrelated code or remove pre-existing dead code.
- Remove imports, variables, or functions only when your own changes make them unused.
- Ensure every changed line has a direct reason tied to the task.

## Define and verify success

- Translate vague goals into observable success criteria.
- For bug fixes, reproduce the bug with a test or focused check before changing behavior when practical.
- For new behavior, add or update tests for the requested and important invalid cases.
- For refactors, verify behavior is unchanged with the relevant tests or checks.
- Run the narrowest meaningful validation, then report what was and was not verified.

For multi-step work, state a brief plan in this form:

```text
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```
