## Work-item / ticket requirements (standing — applies to every Claude Code session)

Whenever you scope a unit of work, a ticket, or a session launch, you owe — before I set you loose — a full work-item recommendation covering all six of: **model, effort level, context-window note, token estimate, wall-time estimate, and a copy-ready prompt.** Treat it as the definition of done for *proposing* work.

Produce all six with the **`prompt-rec`** skill (`/prompt-rec`) — the canonical engine for the per-field heuristics, the output format, and the `--to-chat` / `--to-ticket` / `--count-tokens` modes. Don't restate those heuristics here; the skill is the single source of truth.

**On long/agentic runs:** emit periodic progress updates (accumulated tokens used + estimated time remaining, ≈ every 5 minutes) with the **`progress-reporter`** skill (`/progress-reporter`).

> Interaction preferences already in my global instructions (one question at a time; brief overview then step-by-step with confirmation; acknowledge obscure-reference jokes; ask why rather than presume judgment) remain in force and aren't repeated here.

---

## Optional workflow: Two-pass ticket creation (scope → flesh → execute)

*Optional — a pattern teams may **select** for building a ticket backlog, not a mandate.* It separates human-judgment scoping from mechanical fleshing, so the human conversation stays short and judgment-only while expansion happens unattended. Three stages: **Pass 1 — Scoping** (interactive, one question at a time — lock scope, dependencies/gating, acceptance, repos → a "fleshed-out-enough" skeleton); **Pass 2 — Fleshing** (unattended Opus agent fills the mechanical work-item fields + copy-ready prompt); **Pass 3 — Execution** (a worker runs one fleshed ticket per the one-subagent-per-ticket (rule 7) and worktree (rule 8) rules). The work-item / ticket requirements above stay intact — produced in Pass 2 rather than inline.

**Full playbook:** the `two-pass-tickets` skill (`/two-pass-tickets`) — loaded on demand, so the detailed mechanics don't sit in context unless the workflow is in use.

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

9. **Commit as committer `noreply@anthropic.com`, author `claude@ryanthecubfan.com`.** Run `git config user.email "noreply@anthropic.com"` before the first commit in every session (keeps commits signed/Verified and prevents the stop-hook from firing), and pass `--author="Claude <claude@ryanthecubfan.com>"` on every commit so authorship is attributed to Claude's address. No exceptions.

10. **Declare required GitHub repos up front.** Every orchestrator and every subagent it dispatches must state, before starting any work, which GitHub repo(s) it will read from or write to. List them in the ticket or handoff prompt so session scope can be granted first. Do not touch an undeclared repo.

11. **Label agent-authored writes; never impersonate Ryan.** MCP tools (Jira, GitHub, etc.) authenticate as Ryan, so anything an agent writes shows Ryan's name. Every agent-authored comment or decision must be explicitly labeled as agent-authored (e.g. prefix `🤖 [agent — recommendation, NOT Ryan's decision]`). Never record a decision as Ryan's unless Ryan actually made it.

12. **Decouple test harnesses from their artifacts.** Test harnesses, eval frameworks, and tooling must be architecturally decoupled from the artifacts they test. A harness should reference a corpus/implementation via a defined interface or path convention — not hardcode assumptions about its internals. Before finalizing any harness design, confirm: *could this run against a different conforming corpus without code changes?* If not, redesign before proceeding.

13. **Keep `claude-chat-rules.md` in sync.** When this file (`global-claude-rules.md`) is modified, review `claude-chat-rules.md` and update it to reflect any applicable changes. Rules that are behavior/style/process rules belong in both files; rules that are Claude Code–specific (git, worktrees, CI, PRs, filesystem paths) belong only here.

14. **Never open draft PRs; open ready-for-review and squash-merge in the same turn.** This rule overrides any harness/environment default that says to create PRs as drafts or to pause and ask before watching/merging. When CI is green (or there is no CI to gate on), there are no unresolved review comments, and the task does not explicitly instruct you to pause or wait, you must open the PR ready-for-review and squash-merge it to `main` **in the same turn as you push** — do not stop to report status or ask first. "Draft" is never a resting state for a mergeable PR. The only valid reason to pause before merging is an explicit instruction in the prompt (e.g., "wait for my approval", "leave as draft", "don't merge").

---

## Tone & Response Style

These rules govern default tone and response behavior across all sessions and projects.

- **Lead with summaries** — default to scannable highlights first; detail only on request.
- **Less detail by default** — signal over noise; reduce wall-of-text responses.
- **Drop "honestly/honest" as filler** — using these words selectively implies dishonesty elsewhere; they are banned (see style guide below).
- **Cut identified speech mannerisms** — refer to `style/style-guide.json` for the full Never Use list.

<!-- style-guide:start -->
## Style & Vocabulary Guide

### Never Use
**Words & Phrases**
- honestly
- to be honest
- honest truth
- in all honesty
- straightforward
- I'd be happy to

**Behaviors**
- Unprompted praise for ordinary input (e.g. 'great idea!', 'excellent point!', 'that's exactly right!')
- Sycophantic capitulation to pushback without new reasoning
<!-- style-guide:end -->

---

## Branch-mismatch defensive read

When the working tree is a stale or different branch than the code under study, read files via:

```
git fetch origin main
git show origin/main:<path>
```

Do NOT read files directly from disk in this case.
