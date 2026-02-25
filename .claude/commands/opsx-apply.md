---
description: Implement the tasks in tasks.md for the specified (or active) change.
---

# /opsx:apply [change-id]

Implements the tasks defined in `tasks.md` for a change, working through them
systematically, checking them off as they're completed.

---

## Inputs

`$ARGUMENTS` — optional change ID. If omitted, auto-detect from:
1. Active changes in `openspec/changes/` (non-archived, has tasks.md)
2. If multiple active changes with tasks.md exist, list them and ask which
3. If none found, suggest running `/opsx:propose` first

---

## Procedure

### 1. Load change context
Read in order:
- `openspec/changes/<id>/proposal.md` — understand the goal
- `openspec/changes/<id>/specs/` — understand the requirements
- `openspec/changes/<id>/design.md` — understand the technical approach
- `openspec/changes/<id>/tasks.md` — get the task list

### 2. Find current progress
Parse tasks.md for `- [ ]` (incomplete) vs `- [x]` (complete) checkboxes.
If some tasks are already complete, resume from the first incomplete task.

Report: "Resuming <change-id> at task <X.Y>: <task description>"

### 3. Execute tasks in order
For each incomplete task:

a. Announce: "Working on <X.Y>: <task description>"

b. Read relevant source files before making changes

c. Implement the task, following:
   - The design decisions in design.md
   - The requirements in the delta specs
   - The codebase's existing patterns and conventions

d. Mark the task complete in tasks.md:
   Change `- [ ] X.Y` to `- [x] X.Y`

e. Briefly describe what was done (1–2 sentences)

Repeat for each task. Do not skip tasks without explanation.

### 4. Handle blockers
If a task cannot be completed (missing dependency, unclear spec, etc.):
- Stop and explain the blocker clearly
- Suggest how to resolve it (update the spec, ask a question, etc.)
- Ask: "How would you like to proceed?"

### 5. Completion
When all tasks are checked off:
```
All tasks complete for <change-id>!
  ✓ <N> tasks implemented

Next steps:
  /opsx:verify    — validate implementation against spec
  /opsx:archive   — merge specs and archive this change
```

---

## Mid-Apply Corrections
If the user spots an issue during implementation:
- Stop the current task
- Apply the correction
- Update the relevant artifact (tasks.md, design.md, spec) if the correction
  changes the plan
- Resume from where you left off
