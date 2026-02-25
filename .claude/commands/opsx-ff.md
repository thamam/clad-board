---
description: Fast-forward — generate all remaining planning artifacts for the current change at once.
---

# /opsx:ff

Generates all remaining artifacts for the active change in sequence.
"Fast-forward" from wherever you are to fully planned.

Use after `/opsx:new` when you're ready to generate everything at once.
Also useful to resume a partially-planned change.

---

## Procedure

### 1. Identify active change
Check for changes in `openspec/changes/` that are NOT in `archive/`.

If multiple active changes exist, list them and ask which to fast-forward.
If exactly one exists, use it.
If none exist, suggest `/opsx:new <id>` first.

### 2. Check what already exists
For the active change, check which artifacts are present:
- `proposal.md` — exists?
- `specs/` — any files?
- `design.md` — exists?
- `tasks.md` — exists?

Skip existing artifacts. Generate only what's missing, in dependency order:
`proposal → specs → design → tasks`

### 3. Gather context (if proposal doesn't exist)
Ask the user: "What are we building in `<change-id>`?" and gather enough
context to write proposal.md. Read relevant existing specs and source files.

### 4. Generate missing artifacts
Follow the generation steps from `/opsx:propose` for each missing artifact.
Read existing artifacts as context before generating dependent ones.

### 5. Output
```
openspec/changes/<change-id>/
  ✓ proposal.md    (existing / created)
  ✓ specs/         (existing / created N deltas)
  ✓ design.md      (existing / created)
  ✓ tasks.md       (created — N tasks, M phases)

Ready for implementation. Run /opsx:apply to start.
```
