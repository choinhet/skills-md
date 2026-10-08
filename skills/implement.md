---
name: implement
description: Implement a local Markdown issue using test-driven development.
disable-model-invocation: true
---

# Implement

Implement one issue from `ai-prds/issues/` using test-driven development.

Work entirely with the local codebase and Markdown files. Do not interact with
external issue trackers.

## 1. Select the Issue

If the user specifies an issue, use it.

Otherwise:

1. Read `ai-prds/issues/index.md`.
2. Find the first `todo` issue whose dependencies are completed.
3. Read the issue and its parent PRD.
4. Inspect the relevant codebase.

Do not implement multiple issues in one session.

## 2. Understand the Requirements

Before modifying code:

1. Identify the acceptance criteria.
2. Identify the public interfaces affected.
3. Determine which behaviors require automated tests.
4. Identify existing tests and project conventions.

Do not reopen settled design decisions.

Ask the user only when a decision is genuinely ambiguous or blocking.

## 3. Follow the Implementation Constraints

These apply to every implementation.

### All Languages

- Never write or edit lockfiles by hand. Change dependencies only through the
  package manager (for example `uv add`, `uv remove`, `uv lock`).
- Tests never rely on local files outside the test's own temp folders. No repo
  content, home folder, or machine-specific paths. Tests create the files they
  need.

### Python

- `ruff` and `ty` are dev dependencies. Add them with `uv add --dev ruff ty`
  when missing.
- All code is fully typed: every function parameter and return value,
  including tests and fixtures.
- `ruff check`, `ruff format --check`, and `ty check` pass with no errors.

## 4. Implement Using TDD

For each behavior, follow the RED → GREEN → REFACTOR cycle.

### RED

1. Write one test describing the expected behavior.
2. Test through a public interface whenever practical.
3. Run the test and confirm it fails for the expected reason.

Never write a test that merely verifies implementation details.

### GREEN

1. Write the minimum production code necessary to pass the test.
2. Run the focused test.
3. Fix failures until it passes.
4. Run relevant existing tests to detect regressions.

Do not implement unrelated functionality.

### REFACTOR

Once the tests pass:

1. Improve code clarity and structure where useful.
2. Remove unnecessary duplication.
3. Keep public behavior unchanged.
4. Rerun the relevant tests.

Repeat the cycle for the next behavior.

Do not write all tests first and then implement everything.

## 5. Verify

After implementing all behaviors:

1. Run the relevant test suite.
2. Run type checking and linting. For Python, run `ruff check`,
   `ruff format --check`, and `ty check`.
3. Review the changes against the issue's acceptance criteria.
4. Check for regressions and unnecessary complexity.
5. Fix problems discovered during verification.

Do not claim tests passed unless they were actually executed.

## 6. Update Local Issue Tracking

After successful verification:

1. Check off satisfied acceptance criteria.
2. Set the issue status to `done`.
3. Update `ai-prds/issues/index.md`.
4. Identify the next unblocked issue.

If verification fails or the work is incomplete, leave the issue as
`in-progress` or `blocked` and document the reason.

## 7. Report

Summarize:

- What was implemented.
- Which tests were added.
- Test and type-check results.
- Any remaining limitations.
- The next available issue.

Do not automatically start the next issue.

Do not commit changes unless the user explicitly requests it.
