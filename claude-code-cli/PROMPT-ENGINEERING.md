# Prompt Engineering Analysis: Claude Code v2.1.126

## Overview

Claude Code v2.1.126 uses **four distinct system prompts** across its modes:

| Prompt | Model | Words | Characters | Lines | Purpose | Reused Across |
|--------|-------|------:|-----------:|------:|---------|---------------|
| Main system prompt | claude-opus-4-7 | 4,332 | 27,744 | 238 | Core agent behavior | All 18 main opus requests (6 agent + 12 plan) |
| Security monitor | claude-opus-4-7 | ~5,200 | 30,452 | 165 | Independent allow/block classifier | Triggered after select agent actions |
| Title generator | claude-haiku-4-5-20251001 | 116 | 700 | 17 | Session title from user message | Per-session-start (1 per mode) |
| Title+branch generator (plan-only) | claude-haiku-4-5-20251001 | 232 | 1,316 | 20 | Title + git branch slug | Mid-session in plan mode (1 call) |

> The main system prompt is **identical** across both modes — same 4,332 words. Mode-specific behavior is controlled entirely through `<system-reminder>` blocks injected into the user message (see [Mode Delta](#mode-delta)).

### Request Breakdown by Mode

| Mode | Main opus | Security monitor | Haiku overhead | Total |
|------|----------:|----------------:|---------------:|------:|
| Agent | 6 | 2 | 2 (warmup + title) | 10 |
| Plan | 12 | 0 | 3 (warmup + title + title+branch) | 15 |
| **Total** | **18** | **2** | **5** | **25** |

## Main System Prompt Structure

The main prompt is sent as **4 separate content blocks** so different sections cache independently:

| # | Length | Content |
|---|-------:|---------|
| 0 | 81 chars | `x-anthropic-billing-header: cc_version=2.1.126.<hash>; cc_entrypoint=cli; cch=<hash>;` (rotates per request — breaks cache) |
| 1 | 57 chars | Identity line |
| 2 | 9,925 chars | Core rules: System / Doing tasks / Executing actions / Using your tools / Tone and style |
| 3 | 17,678 chars | Text output / System reminders / Session-specific guidance / Auto memory (huge) / Environment / gitStatus |

**Block 3 is by far the largest** and is dominated by the **auto memory** subsystem — see [Memory System](#memory-system).

### Identifiable Sections (10)

1. **Billing header** — `x-anthropic-billing-header` with version, entrypoint, cache hash
2. **Identity** — "You are Claude Code, Anthropic's official CLI for Claude"
3. **System** — display rules, permission modes, hooks, context-compression note
4. **Doing tasks** — execution guidelines, anti-over-engineering rules, frontend-testing requirement, comment policy
5. **Executing actions with care** — reversibility checks, blast radius, examples of risky actions
6. **Using your tools** — dedicated-tool preference, parallel tool calls
7. **Tone and style** — concise responses, no emojis, file:line references, no colons before tool calls
8. **Text output** — explicit guidance on what user-facing text should look like
9. **Session-specific guidance** — `!` shell prefix, Agent vs find/grep, Skill invocation, ultrareview info
10. **Auto memory** — persistent typed-memory system

**Plus** non-section structural text: Environment block, Context management note, gitStatus snapshot.

## Multi-Stage Prompt Architecture

```
                          USER MESSAGE
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
         haiku: warmup   haiku: title    haiku: title+branch
         (1 token)       (~20 tokens)    (plan-only, mid-session)
                              │
                              ▼
                        opus: main turn ─────► tool calls
                              │                    │
                              │                    ▼
                              │            opus: SECURITY MONITOR
                              │            (after select actions)
                              │                    │
                              │              <block>yes/no
                              ▼                    │
                        next opus turn  ◄──────────┘
```

The **security monitor** is a separate Claude opus-4-7 call invoked after select agent actions. It uses `</block>` as a stop sequence and emits a 9-char verdict (`<block>no` or `<block>yes…`). Full prompt and analysis in [SECURITY-MONITOR.md](SECURITY-MONITOR.md).

## Auto Mode

A 6-rule `<system-reminder>` block in agent mode declares whether the session is "auto mode" (continuous autonomous execution). Behavior:

- Lets the agent make low-risk decisions immediately
- Keeps high-stakes guardrails ("not a license to destroy")
- Pairs with the **Security Monitor** as the safety backstop

Agent mode includes the Auto Mode block; plan mode includes a **Plan Mode Active** block instead. They are mutually exclusive.

## Tool Description Bloat

Tool descriptions absorb material that would otherwise sit in the system prompt:

- **Bash** description carries the full git-safety protocol and PR-creation workflow
- **Agent** description carries the explicit subagent catalog and prompt-writing examples
- **ScheduleWakeup** documents prompt-cache TTL economics in its own description

This shifts cost: tool descriptions are only paid when relevant tools are exposed. See [TOOL-USE.md](TOOL-USE.md).

## Mode Delta

How the prompt environment changes between agent and plan modes:

### Prompt Length

- **Main system prompt:** identical (4,332 words / 27,744 chars in both modes)
- **User-prompt blocks:** agent has 6 blocks (1 Auto Mode reminder); plan has 7 blocks (replaces Auto Mode with Plan Mode reminder + Plan File Info)
- **Plan-mode reminder:** 4,780 chars detailing read-only restrictions, plan file path, and a 5-phase workflow (Initial Understanding → Design → Review → Final Plan → ExitPlanMode)

### Tool Count

- **Agent:** 8 always-loaded; 117 deferred
- **Plan:** 8 always-loaded; 117 deferred (same registry); model loaded `AskUserQuestion` and `ExitPlanMode` mid-session via `ToolSearch`, ending with 10 schemas

### Plan Mode Behavioral Control

Plan mode behavior is enforced **entirely at the prompt layer**:

- The injected `<system-reminder>` says "you MUST NOT make any edits (with the exception of the plan file)…"
- The plan-file path is generated server-side using a haiku-derived branch slug (`/Users/alx/.claude/plans/create-a-plan-to-quizzical-scone.md`)
- The 5-phase workflow tells the model to use **Explore** subagents in Phase 1 (parallelizable, up to 3) and a **Plan** subagent in Phase 2 (up to 1)
- `ExitPlanMode` is the only blessed exit; "Is this plan okay?" text questions are explicitly disallowed

The model *could* still call `Edit` or `Write` (they're in the always-loaded set), but the reminder makes that a violation. The Security Monitor would catch egregious cases — though in this capture it never fired in plan mode (no executions happened).

## Caching Behavior

The 4-block split lets each cache independently:

| Block | Caches across | Reason |
|-------|---------------|--------|
| 0 (billing header) | never (rotates per request) | The `cch=` hash is unique per call |
| 1 (identity) | every opus request | Static |
| 2 (core rules) | every opus request | Static |
| 3 (text/memory/env/git) | every opus request *with same env* | Static within session |
| User prompt blocks 1–5 | every opus request *after the first* | Static within session |

In the agent-mode session, **request #6 reads 198K cache tokens** vs only 1 fresh input token. By the end of the session, ~96% of input is served from cache — making the per-turn marginal cost extremely small.

## Memory System

The memory section is the largest single block of the system prompt. Key directives:

> **Each memory has typed frontmatter** (`name`, `description`, `type ∈ {user, feedback, project, reference}`).

> **For feedback/project memories: rule/fact, then `**Why:**` line, then `**How to apply:**` line.** Knowing why lets you judge edge cases instead of blindly following the rule.

> **Don't save** code patterns, file paths, project structure, debugging recipes, or anything in CLAUDE.md — those can be derived. Memory is for things that *can't* be re-derived from the repo.

> **Verify before recommending.** "The memory says X exists" is not the same as "X exists now." If a memory names a function/flag, grep for it before recommending.

> **`MEMORY.md` is an index, not a memory.** Lines after 200 are truncated. Each entry one line, < 150 chars.

The memory store is a typed knowledge base with versioning discipline: write the memory file *and* index it in `MEMORY.md`, then verify before recall.

## See Also

- [SECURITY-MONITOR.md](SECURITY-MONITOR.md) — the post-action allow/block classifier
- [TOOL-USE.md](TOOL-USE.md) — full tool catalog with deferred-tool architecture
- [CHANGES-FROM-v2.1.59.md](CHANGES-FROM-v2.1.59.md) — version-to-version delta
- [agent-mode/system-prompt.md](agent-mode/system-prompt.md) — full system prompt text
- [agent-mode/user-prompt.md](agent-mode/user-prompt.md) — 6-block user prompt structure
- [plan-mode/user-prompt.md](plan-mode/user-prompt.md) — plan-mode reminder + 5-phase workflow
