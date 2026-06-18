# Global Rules — drop-in block for your global CLAUDE.md / Global Instructions

*Paste into Global Instructions (Cowork → Global Instructions, or claude.ai → Settings → Custom Instructions). This is the full standing per-work-item requirement, assembled from your own repeated asks across May–June 2026 — including your own instruction that it "go in memory and apply to all Claude Code sessions."*

---

## Work-item / ticket requirements (standing — applies to every Claude Code session)

Whenever you scope a unit of work, a ticket, or a session launch, provide all of the following before I set you loose. Treat it as the definition of done for *proposing* work:

1. **Model recommendation** — Haiku / Sonnet / Opus / Fable, with a one-line rationale. For sub-agents, recommend the **cheapest model that will do the job effectively**; for the orchestrator/main agent, recommend the model whose judgment the task actually needs.
2. **Effort level** — one of low / medium / high / xhigh (extra-high) / max.
3. **Context window** *(when it matters)* — e.g. for Opus, call out 1M vs standard 200K and why.
4. **Token estimate** — input / output / cache.
5. **Wall-time estimate** — rounded up to the nearest 5, 10, or 15 minutes (your call) for anything under an hour; 15-minute increments above an hour.
6. **A copy-ready prompt** — a self-contained prompt written for the recommended model, complete enough to launch from on its own. When I ask for "just the prompt," reply with the prompt and nothing else (I'm often copying it on my phone).

**On long/agentic runs:** give **periodic progress updates** — accumulated tokens used and estimated time remaining — at a sensible cadence (≈ every 5 minutes for long autonomous runs).

> Interaction preferences already in my global instructions (one question at a time; brief overview then step-by-step with confirmation; acknowledge obscure-reference jokes; ask why rather than presume judgment) remain in force and aren't repeated here.

---

## Jira ticket lifecycle (standing — applies to every Claude Code session)

**You must know the Jira ticket number before doing any work.** If no ticket number has been given and the task wasn't explicitly framed as untracked work, stop and ask for it before proceeding. Do not start work, make commits, or take any action on behalf of a ticket you cannot identify.

- **When you start work on a ticket** — transition it to **In Progress** before doing anything else.
- **When you finish a ticket** — transition it to **Done** after all commits are merged and all acceptance criteria are met.
- **If you don’t know the ticket number** — you cannot proceed autonomously. Stop and ask the user to provide it or explicitly tell you to proceed without one.
