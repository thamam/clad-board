---
description: Validate that the implementation matches the requirements in the change's delta specs.
---

# /opsx:verify [change-id]

Validates that what was implemented actually satisfies the requirements defined
in the change's delta specs. Catches drift between plan and implementation.

---

## Inputs

`$ARGUMENTS` — optional change ID. If omitted, auto-detect active change with
a complete tasks.md (all checkboxes ticked).

---

## Procedure

### 1. Load change artifacts
Read:
- `openspec/changes/<id>/specs/` — the requirements to verify against
- `openspec/changes/<id>/tasks.md` — what was supposed to be done
- `openspec/changes/<id>/proposal.md` — success criteria

### 2. Read the implementation
Examine the relevant source files that were modified by this change.
Use git context or file timestamps if helpful to scope what changed.

### 3. Verify each requirement

For each requirement in the delta specs:
- Check if the implementation satisfies it
- Check if each GIVEN/WHEN/THEN scenario is handled

Report status per requirement:
```
✓ Requirement: <name> — satisfied
⚠ Requirement: <name> — partially satisfied (<gap>)
✗ Requirement: <name> — not implemented (<what's missing>)
```

### 4. Check success criteria
Review `proposal.md` success criteria. Mark each:
```
✓ <criterion> — met
✗ <criterion> — not yet met (<reason>)
```

### 5. Final verdict

**All passing:**
```
✓ Verification passed for <change-id>
All requirements satisfied. Ready to archive.
Run /opsx:archive to complete.
```

**Gaps found:**
```
⚠ Verification found gaps in <change-id>:
  [list of failures]

Options:
  1. Fix the gaps, then run /opsx:verify again
  2. Update the spec to reflect intentional scope reduction
  3. Archive as-is and create a follow-up change for the gaps
```
