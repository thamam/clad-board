---
description: Archive all completed changes at once, with spec conflict resolution.
---

# /opsx:bulk-archive

Archives all changes where tasks.md has all checkboxes complete.
Handles spec conflicts when multiple changes touch the same capability.

---

## Procedure

### 1. Find completed changes
Scan `openspec/changes/` (excluding `archive/`) for changes where:
- `tasks.md` exists AND all tasks are `- [x]`

List them:
```
Found N completed changes:
  - <change-id-1> (N tasks complete)
  - <change-id-2> (N tasks complete)
  ...
```

If none found: "No completed changes to archive."

### 2. Check for spec conflicts
Identify if multiple completed changes have delta specs for the same capability.

If conflicts exist:
```
⚠ Spec conflict: <capability>
  - <change-id-1> and <change-id-2> both modify this spec

Resolving in chronological order (by creation date):
  1. <change-id-1> (created <date>)
  2. <change-id-2> (created <date>)
```

Read the conflicting deltas and the codebase to determine a coherent merge.
The final spec should reflect the current actual system state.

### 3. Confirm with user
"Archive all N changes? (y/n)"

### 4. Archive in order
Process changes chronologically (oldest first) to ensure correct spec merge order:

For each change, follow the same procedure as `/opsx:archive`.

### 5. Final output
```
✓ Archived N changes

Specs updated:
  ✓ <capability> (merged from N changes)
  ...

All changes moved to openspec/changes/archive/
```
