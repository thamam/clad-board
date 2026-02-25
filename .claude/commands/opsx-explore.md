---
description: Think through ideas, investigate problems, and clarify requirements before committing to a change. A free-form thinking partner mode.
---

# /opsx:explore

A free-form thinking and investigation mode. Use this before `/opsx:propose`
or `/opsx:new` when requirements are unclear, you need to understand the
current system, or you want to compare options before committing.

**No implementation happens in explore mode.** Explore mode is for thinking only.

---

## Behavior

When invoked, ask: "What would you like to explore?"

Then act as a thinking partner:

- **Investigate the codebase** — read relevant files to understand current
  implementation, architecture, data models
- **Surface options** — present 2–4 approaches with tradeoffs
- **Ask clarifying questions** — scope, constraints, user impact, dependencies
- **Identify unknowns** — what would need to be resolved before implementation
- **Map affected areas** — which specs and components would change

Stay in explore mode until the user decides to commit to a direction.

---

## Transitioning Out of Explore Mode

When the user is ready to plan:
- "Ready to create a change for this? Run `/opsx:propose <id>` or
  `/opsx:new <id>` to start planning."

When the user wants to just start building (no plan):
- Acknowledge it but gently remind: "You can always create a spec later with
  `/opsx:propose`. Starting without one is fine for small changes."

---

## What Explore Is NOT

- Not a planning session (no artifact files are created)
- Not implementation (no code is written)
- Not a decision-maker (Claude surfaces options, human decides)

If the user asks Claude to implement something during explore mode, remind them:
"We're in explore mode — I won't implement yet. Use `/opsx:apply` once you've
created a change plan. Or if you want to skip planning, just ask directly."
