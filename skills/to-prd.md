---
name: to-prd
description: Turn an established plan into a Product Requirements Document.
---

# To PRD

Convert the current conversation, including any completed design interviews,
into a clear Product Requirements Document.

## Instructions

Do not interview the user again. Synthesize the information already available.

Do not invent requirements or silently resolve unresolved decisions.

Inspect the codebase when necessary to understand existing architecture and
constraints.

## PRD Structure

### Problem Statement

Describe the problem, who experiences it, and why solving it matters.

### Proposed Solution

Describe the intended solution at a high level, focusing on observable behavior
rather than implementation details.

### User Stories

List the user stories in the following format:

- As a [user], I want [capability], so that [benefit].

### Implementation Decisions

Record architectural decisions, important constraints, dependencies, and agreed
trade-offs.

Identify opportunities for cohesive modules with simple interfaces.

Avoid unnecessary implementation details that may become outdated.

### Testing Decisions

Describe how the solution will be validated, including:

- Expected behaviors
- Important edge cases
- Integration boundaries
- Relevant testing strategies

### Out of Scope

Explicitly list features and behaviors that will not be implemented.

### Further Notes

Include assumptions, risks, unresolved questions, and relevant references.

## Output

Produce a complete Markdown PRD.

Save it to `ai-prds/<feature-slug>/prd.md`, where `<feature-slug>` is a short
kebab-case name for the feature. Create the folder when missing.

Make sure the project's root `.gitignore` lists `ai-prds/`. Create the
`.gitignore` or append the line when missing. Do not add it twice.

Do not start implementation.

Do not create issues yet.

If essential information is missing, mark it explicitly as unresolved rather
than guessing.
