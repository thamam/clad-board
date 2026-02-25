---
description: Create a new OpenSpec change with all planning artifacts in one shot.
---

# /opsx:propose <change-id>

One-shot planning command. Creates the change directory and generates all four
artifacts (proposal, delta specs, design, tasks) in sequence.

Use this when you have a clear picture of what you want to build.
For exploratory/unclear requirements, use `/opsx:explore` first.

---

## Inputs

`$ARGUMENTS` — the change ID (kebab-case description of the change).
Examples: `add-dark-mode`, `fix-login-redirect`, `migrate-to-postgres`

If no argument is provided, ask the user: "What would you like to build?
Provide a short kebab-case ID (e.g., `add-user-preferences`)"

---

## Procedure

### 1. Check for existing change
If `openspec/changes/<change-id>/` already exists, ask:
"A change named `<change-id>` already exists. Continue building it,
or start fresh with a different name?"

### 2. Read context
Before generating anything:
- Check `openspec/specs/` for existing specs that this change might affect
- Scan relevant source files to understand the current implementation
- Ask clarifying questions if the request is ambiguous (scope, constraints,
  affected systems). Aim to ask all questions at once.

### 3. Create directory
```
openspec/changes/<change-id>/
openspec/changes/<change-id>/specs/
```

### 4. Generate proposal.md
Using the template from `references/artifact-templates.md`:
- Intent: Why this change, why now
- Scope: In/out of scope
- Approach: High-level direction
- Affected Specs: Which capabilities this touches
- Success Criteria: Verifiable completion checklist

Write to: `openspec/changes/<change-id>/proposal.md`

### 5. Generate delta specs
For each affected capability identified in the proposal:
- If `openspec/specs/<capability>/spec.md` exists, read it
- Write a delta spec showing ADDED/MODIFIED/REMOVED requirements
- Use SHALL/GIVEN/WHEN/THEN format (see `references/spec-format.md`)

Write to: `openspec/changes/<change-id>/specs/<capability>/spec.md`

### 6. Generate design.md
Based on proposal + delta specs + codebase context:
- Key technical decisions (with rationale and alternatives)
- Architecture/component approach
- Data model or API changes if applicable
- Risks and mitigations

Write to: `openspec/changes/<change-id>/design.md`

### 7. Generate tasks.md
Break implementation into phases and numbered tasks:
- Tasks should be atomic and implementable one at a time
- Group by phase (setup, core, polish, tests, etc.)
- Each task ID is `<phase>.<index>` (e.g., 1.1, 1.2, 2.1)

Write to: `openspec/changes/<change-id>/tasks.md`

### 8. Summary output
```
Created openspec/changes/<change-id>/
  ✓ proposal.md  — intent, scope, approach
  ✓ specs/       — <N> capability delta(s)
  ✓ design.md    — technical decisions
  ✓ tasks.md     — <N> tasks across <M> phases

Review the artifacts, then run /opsx:apply to implement.
```

---

## Quality Checks
- proposal.md has specific success criteria (not vague)
- Each delta spec identifies exactly which requirements change
- design.md has at least one decision documented with rationale
- tasks.md tasks are small enough to implement in one session
