---
description: Create a new OpenSpec change scaffold (directory only, no artifacts). Follow with /opsx:ff or /opsx:continue.
---

# /opsx:new <change-id>

Creates the change directory scaffold without generating any artifacts.
Use this when you want to build artifacts incrementally with `/opsx:continue`,
or generate them all at once with `/opsx:ff`.

---

## Inputs

`$ARGUMENTS` — the change ID (kebab-case).
If not provided, ask: "What's the change ID? (e.g., `add-dark-mode`)"

---

## Procedure

1. Check `openspec/changes/<change-id>/` — if it exists, inform the user and
   offer to resume with `/opsx:continue` or `/opsx:ff`

2. Create directory:
   ```
   openspec/changes/<change-id>/
   openspec/changes/<change-id>/specs/
   ```

3. Output:
   ```
   Created openspec/changes/<change-id>/

   Ready to plan. Choose:
     /opsx:ff          — generate all artifacts at once
     /opsx:continue    — generate one artifact at a time
   ```
