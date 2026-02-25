---
description: Initialize OpenSpec in the current project. Creates the directory structure and installs slash commands.
---

# /opsx:init

Sets up OpenSpec in the current project. Run this once per project.

---

## Procedure

### 1. Check if already initialized
If `openspec/` directory exists: "OpenSpec is already initialized in this
project. Run `/opsx:status` to see active changes."

### 2. Create directory structure
```
openspec/
├── specs/
├── changes/
│   └── archive/
└── README.md
```

### 3. Write openspec/README.md
```markdown
# OpenSpec

Spec-driven development for this project.

## Structure

- `specs/` — Living capability specifications (source of truth)
- `changes/` — Active feature changes in planning or implementation
- `changes/archive/` — Completed and archived changes

## Workflow

/opsx:propose <id>   → full planning in one shot
/opsx:explore        → think before committing
/opsx:new <id>       → scaffold, then /opsx:ff or /opsx:continue
/opsx:apply [id]     → implement the tasks
/opsx:verify [id]    → validate against spec
/opsx:archive [id]   → merge specs, archive change
/opsx:status [id]    → check progress

## Spec Format

Requirements use SHALL/SHOULD/MAY language.
Scenarios use GIVEN/WHEN/THEN format.
```

### 4. Output
```
✓ OpenSpec initialized

openspec/
  specs/           — living capability specs (empty, grows as you build)
  changes/         — active changes
  changes/archive/ — completed changes

Get started:
  /opsx:onboard    — guided walkthrough using your codebase (~15 min)
  /opsx:propose <id>  — start planning a feature now
  /opsx:explore    — think through an idea first
```
