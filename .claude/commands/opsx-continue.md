---
description: Generate the next planning artifact for the current change (incremental, one at a time).
---

# /opsx:continue

Generates the single next artifact in sequence for the active change.
Use this to review and refine each artifact before moving to the next.

Artifact dependency order: `proposal → specs → design → tasks`

---

## Procedure

### 1. Identify active change
Same logic as `/opsx:ff` — find the active (non-archived) change.

### 2. Determine next artifact
Check what exists:
- No `proposal.md` → generate proposal
- Has proposal, no `specs/` content → generate delta specs
- Has specs, no `design.md` → generate design
- Has design, no `tasks.md` → generate tasks
- All exist → "All planning artifacts are complete. Run `/opsx:apply` to implement."

### 3. Generate the next artifact
Read all existing artifacts as context. Read relevant codebase files.
Follow generation instructions from `/opsx:propose` for the specific artifact.

### 4. Output
```
✓ Created <artifact-name>

Next: /opsx:continue to create <next-artifact>, or review this artifact first.
```

Prompt the user to review before continuing, unless they've asked for automatic
progression.
