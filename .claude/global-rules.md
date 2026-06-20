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
- **When you finish a ticket** — transition it to **Done** only after all changes are merged to origin `main`. "Finished" means code is on `main`, not just committed or PR-open.
- **If you don’t know the ticket number** — you cannot proceed autonomously. Stop and ask the user to provide it or explicitly tell you to proceed without one.

---

## Standing rules (standing — applies to every Claude Code session)

These rules are non-negotiable. Do not hedge, ask permission, or make exceptions.

1. **Never force-push `main`.** Do not do this under any circumstances, even if a rebase conflict seems easier to resolve that way.

2. **Anthropic/Claude calls go through the Claude subscription, not an API key.** Do not use, request, or suggest an API key for Claude or any Anthropic model. The subscription is the only authorized path.

3. **Always rebase + squash before merging.** Never create a merge commit. Every PR lands on `main` as a single squash-merged commit.

4. **Merge only when CI is green and there are no unresolved review comments.** Do not merge early "just to unblock" anything.

5. **Never skip or disable tests.** No `--skip`, no commented-out test cases, no `skip()` or `xit()`. Tests must be brittle by design — a flaky test that hides a real failure is worse than no test.

6. **Every "for now" decision gets a tech-debt ticket.** If you defer something, open a Jira ticket before moving on. No undocumented deferrals.

7. **A subagent works exactly one ticket.** Never assign one subagent to multiple tickets. A ticket may be handled by N subagents (parallel research, multiple workers); an orchestrator may run many concurrently within a shared domain. Isolation is per-subagent, not per-session.

8. **Always create a git worktree for ticket work.** Never commit directly to `main` or to the parent session’s branch. Use `/worktree-bootstrap <ticket-id>` at the start of every ticket.

9. **Commit as `noreply@anthropic.com`.** Run `git config user.email "noreply@anthropic.com"` before the first commit in every session. No exceptions — this prevents the stop-hook from firing.

10. **Declare required GitHub repos up front.** Every orchestrator and every subagent it dispatches must state, before starting any work, which GitHub repo(s) it will read from or write to. List them in the ticket or handoff prompt so session scope can be granted first. Do not touch an undeclared repo.

11. **Label agent-authored writes; never impersonate Ryan.** MCP tools (Jira, GitHub, etc.) authenticate as Ryan, so anything an agent writes shows Ryan's name. Every agent-authored comment or decision must be explicitly labeled as agent-authored (e.g. prefix `🤖 [agent — recommendation, NOT Ryan's decision]`). Never record a decision as Ryan's unless Ryan actually made it.
