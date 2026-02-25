# OpenSpec — Spec-Driven Development

This directory contains living specifications and change artifacts for the
Bot Monitoring Dashboard project.

## Structure

```
openspec/
├── specs/                     # Living capability specs
│   └── <capability>/
│       └── spec.md
└── changes/                   # Active and archived changes
    ├── <change-id>/
    │   ├── proposal.md
    │   ├── design.md
    │   ├── tasks.md
    │   └── specs/             # Delta specs for this change
    └── archive/
        └── <date>-<change-id>/
```

## Commands

| Command | Purpose |
|---|---|
| `/opsx:propose <id>` | Create change + all planning artifacts |
| `/opsx:apply [id]` | Implement tasks from tasks.md |
| `/opsx:verify [id]` | Validate implementation against spec |
| `/opsx:status [id]` | Show artifact completion status |
| `/opsx:archive [id]` | Merge specs, archive the change |
