---
name: to-issues
description: Break a PRD into independently implementable development issues stored as local Markdown files.
---

# To Issues

Convert an existing Product Requirements Document into a set of actionable,
independently implementable issues.

All issue management must happen locally through Markdown files. Do not use
external issue trackers or services.

## Instructions

Read the PRD and identify the smallest useful vertical slices of functionality.

Each issue should deliver a meaningful, testable behavior rather than merely
completing an architectural layer.

Prefer vertical slices over horizontal tasks such as "build database", "build
API", and "build frontend".

## Planning Process

1. Read the PRD and identify its user stories and acceptance criteria.
2. Inspect the existing codebase to understand relevant architecture and
   constraints.
3. Group requirements into coherent implementation slices.
4. Identify dependencies between slices.
5. Determine which tasks require human decisions.
6. Present the proposed breakdown before creating files.
7. Ask the user to approve the granularity, ordering, and dependencies.
8. Revise the breakdown until approved.
9. Create the local issue files.

## Local File Structure

Store issues in an `issues/` folder next to the PRD, inside the feature folder:

```
ai-prds/
  <feature-slug>/
    prd.md
    issues/
      index.md
      001-initialize-feature.md
      002-implement-core-behavior.md
      003-add-integration.md
```

Use sequential, zero-padded issue IDs and descriptive kebab-case filenames.

If the project already has an established documentation structure, follow its
conventions instead.

## Issue Structure

Each issue must contain:

### Title

A concise, outcome-oriented description.

### ID

A unique local identifier, such as `001`.

### Status

One of:

- `todo`
- `in-progress`
- `blocked`
- `done`

### Type

- `HITL`: Requires human input or approval.
- `AFK`: Can be completed autonomously.

### Parent PRD

A relative Markdown link to the source PRD.

### What to Build

Describe the expected behavior, scope, and implementation boundaries.

### Acceptance Criteria

Use a checklist of objectively verifiable outcomes.

### Blocked By

List prerequisite issue IDs using relative Markdown links, or state `None`.

### User Stories Addressed

Reference the relevant stories from the PRD.

## Vertical Slice Rules

- Prefer end-to-end functionality over isolated infrastructure.
- Keep issues small enough for a focused implementation session.
- Minimize dependencies between issues.
- Avoid prescribing exact files or functions unless necessary.
- Make acceptance criteria observable and testable.
- Ensure every requirement in the PRD is covered.
- Avoid creating issues that deliver no independently verifiable value.
- Do not duplicate work across issues.

## Issue Index

Create an `index.md` containing:

- A relative link to the parent PRD.
- A table of all issues, including ID, title, status, type, and dependencies.
- A recommended implementation order.
- Any unresolved decisions or blockers.

Use relative Markdown links so the documentation remains portable.

## Progress Tracking

The local Markdown files are the source of truth.

When an issue is implemented:

1. Update its acceptance criteria checkboxes.
2. Change its status to `done` only when all acceptance criteria are satisfied.
3. Update its status in `index.md`.
4. Identify which dependent issues are now unblocked.

Never mark an issue as completed without verifying its acceptance criteria.

## Output

First, present the proposed issues in dependency order.

Wait for user approval before creating the files.

Once approved, create the local Markdown files and issue index.

Do not implement the issues during this process.

Do not modify or overwrite the parent PRD.

Do not create or interact with external issue trackers.
