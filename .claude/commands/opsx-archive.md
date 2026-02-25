---
description: Merge delta specs into the living specs and archive the completed change.
---

# /opsx:archive [change-id]

Merges the change's delta specs into the living specs in `openspec/specs/`,
then moves the change to the archive directory. This is the final step of
the OpenSpec workflow.

---

## Inputs

`$ARGUMENTS` — optional change ID. If omitted, auto-detect the change with
all tasks complete (all `- [x]`).

---

## Procedure

### 1. Pre-flight checks
- Confirm all tasks in tasks.md are checked off
- If tasks are incomplete, warn: "tasks.md has unchecked items. Archive anyway?
  (tasks will be marked as skipped)"

### 2. Merge delta specs into living specs

For each file in `openspec/changes/<id>/specs/<capability>/spec.md`:

a. Check if `openspec/specs/<capability>/spec.md` exists
   - If yes: merge the delta into the existing spec
   - If no: this is a new capability — copy the delta as the initial spec

b. **Merging rules:**
   - ADDED requirements: append to the relevant section in the living spec
   - MODIFIED requirements: replace the old requirement text
   - REMOVED requirements: delete from the living spec
   - Remove delta-notation markers (ADDED/MODIFIED/REMOVED) — the merged spec
     should read as a clean, current spec

c. After merging, the living spec should accurately describe the current
   system state, with no delta markers remaining

### 3. Move change to archive

```
openspec/changes/archive/<YYYY-MM-DD>-<change-id>/
```

Move the entire `openspec/changes/<id>/` directory to the archive location
with today's date prefix.

### 4. Output
```
✓ Archived <change-id>

Specs updated:
  ✓ openspec/specs/<capability>/spec.md  (merged N requirements)
  ...

Moved to: openspec/changes/archive/<date>-<change-id>/

Ready for the next feature.
```

---

## Notes

- Archive does not delete anything — all history is preserved in git
- Archived changes are out of scope for `/opsx:apply` and `/opsx:ff`
- If a capability spec doesn't exist yet and the delta has MODIFIED or REMOVED
  items, warn the user — this likely indicates a spec that was never written
