---
description: Show artifact completion status and next actions for a change.
---

# /opsx:status [change-id]

Displays the current state of a change — which artifacts exist, which tasks
are complete, and what the next step is.

---

## Inputs

`$ARGUMENTS` — optional change ID. If omitted, shows status of all active
(non-archived) changes.

---

## Output Format

For each change:

```
Change: <change-id>
──────────────────────────────────
Artifacts:
  ✓ proposal.md
  ✓ specs/ (N capabilities)
  ✓ design.md
  ◆ tasks.md — N/M tasks complete

Progress: [████████░░] 80%

Next: /opsx:apply to finish remaining M tasks
      or /opsx:verify to check implementation
```

Status symbols:
- `✓` — artifact exists
- `◆` — exists, partially complete (for tasks.md)
- `○` — not yet created

If no active changes:
```
No active changes. Start with /opsx:propose <change-id>
```
