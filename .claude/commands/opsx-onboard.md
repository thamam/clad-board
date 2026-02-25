---
description: Interactive tutorial that walks through a complete OpenSpec workflow using the actual codebase. ~15 minutes.
---

# /opsx:onboard

Guided onboarding through the complete OpenSpec workflow. Uses your actual
codebase — finds a real small improvement to make, then walks through every
step from planning to archive.

Estimated time: 10–15 minutes.

---

## Phases

### Phase 1: Welcome
"Welcome to OpenSpec! I'll walk you through the complete workflow using your
actual codebase. We'll find something small to improve, create a proper change
for it, implement it, and archive it."

Show the workflow overview:
```
/opsx:propose → /opsx:apply → /opsx:verify → /opsx:archive
```

Ask: "Ready to start? I'll scan your codebase to find a good starter task."

### Phase 2: Codebase scan
Read the project structure. Look for:
- A small, self-contained improvement (add a missing test, fix a TODO,
  improve an error message, add a missing type, clean up dead code)
- Something that takes ~10 minutes to implement
- NOT a large feature or architectural change

Present 2–3 candidates:
```
I found a few good starter candidates:
  1. <description> — <why it's a good fit>
  2. <description>
  3. <description>

Which would you like to use for this walkthrough?
```

### Phase 3: Propose
"Great. Let's create a proper change for this."

Walk through `/opsx:propose <id>` step by step, narrating what each artifact
means and why it exists:
- "We're writing proposal.md — this captures the *why* before any code"
- "Delta specs define the requirements in testable scenarios"
- "design.md records the technical decision we're making"
- "tasks.md breaks it into steps we can track"

### Phase 4: Review artifacts
"Here's what we created. Take a moment to read through each artifact.
Does anything look off or need adjustment?"

Wait for confirmation before proceeding.

### Phase 5: Implement
"Now let's implement it. Running `/opsx:apply`..."

Run the apply workflow. Narrate each task as it's completed.

### Phase 6: Verify
"Implementation looks good. Let's verify it matches our spec."

Run `/opsx:verify`. Show the results.

### Phase 7: Archive
"Everything checks out. Let's archive this change and update the living specs."

Run `/opsx:archive`. Show the final state of `openspec/specs/`.

### Phase 8: Wrap-up
```
✓ Onboarding complete!

You just completed the full OpenSpec workflow:
  ✓ Planned before coding (/opsx:propose)
  ✓ Implemented from a spec (/opsx:apply)
  ✓ Verified against requirements (/opsx:verify)
  ✓ Updated living documentation (/opsx:archive)

For your next feature, try:
  /opsx:explore   — think through something before planning
  /opsx:propose   — jump straight to full planning
  /opsx:status    — check what's active

Full command reference: see openspec/README.md
```
