# Prompt Engineering Analysis: Claude Code

## Overview

Claude Code uses two distinct prompts across its modes:

| Prompt | Model | Words | Characters | Lines | XML Tags | MD Headers | Bullets | Reused Across |
|--------|-------|-------|-----------|-------|----------|-----------|---------|---------------|
| Main system prompt | claude-opus-4-6 | 2,345 | 15,107 | 135 | 4 | 11 | 64 | All 14 opus requests (7 agent + 7 plan) |
| Overhead prompt | claude-haiku-4-5-20251001 | 179 | 1,181 | 25 | 5 | 0 | 0 | All 6 haiku requests (3 agent + 3 plan, but 2 types — see below) |

### Request Breakdown by Mode

| Mode | Opus (main) | Haiku (overhead) | Total |
|------|-------------|------------------|-------|
| Agent | 7 | 4 | 11 |
| Plan | 6 | 2 | 8 |
| **Total** | **13** | **6** | **19** |

> The main system prompt is **identical** across all opus requests in both modes — same 2,345 words, same structure. Mode-specific behavior is controlled entirely through `<system-reminder>` tags injected into conversation turns (see [Mode Delta](#mode-delta)).

## Main System Prompt — claude-opus-4-6

**Length:** 2,345 words (15,107 characters)

**Structure:**

- XML tags: 4 — uses XML for structured sections
- Markdown headers: 11 — organized with `#` headings
- Bullet points: 64

**8 Identifiable Sections:**

1. **Billing header** — `x-anthropic-billing-header` with version, entrypoint, and cache hash
2. **Identity** — "You are Claude Code, Anthropic's official CLI for Claude"
3. **System** — Display rules, permission modes, tag handling, hooks
4. **Doing tasks** — Task execution guidelines, anti-over-engineering rules, security awareness
5. **Executing actions with care** — Reversibility checks, blast radius assessment, confirmation requirements
6. **Using your tools** — Tool selection preferences, dedicated tools vs Bash, sub-agent guidelines
7. **Tone and style** — Concise responses, no emojis, code reference format
8. **Auto memory** — Persistent memory directory, what to save/not save

**Key Sections Identified:**

- Persona
- Safety
- Tool Instructions
- Formatting
- Context Injection
- Constraints
- Examples
- Code Style

<details>
<summary>Prompt excerpt (first 1000 chars of 15,107)</summary>

```
x-anthropic-billing-header: cc_version=2.1.59.a37; cc_entrypoint=cli; cch=dba19;

You are Claude Code, Anthropic's official CLI for Claude.


You are an interactive agent that helps users with software engineering tasks. Use the instructions below and the tools available to you to assist the user.

IMPORTANT: Assist with authorized security testing, defensive security, CTF challenges, and educational contexts. Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise, or detection evasion for malicious purposes. Dual-use security tools (C2 frameworks, credential testing, exploit development) require clear authorization context: pentesting engagements, CTF competitions, security research, or defensive use cases.
IMPORTANT: You must NEVER generate or guess URLs for the user unless you are confident that the URLs are for helping the user with programming. You may use URLs provided by the user in their messages or local files.

# System
 - All text yo

[...truncated — see system-prompt.md for full text]
```

</details>

## Overhead Prompts — claude-haiku-4-5-20251001

Claude Code uses haiku for two distinct overhead purposes:

### 1. Warmup / Quota Check

**Purpose:** Verify API connectivity and quota availability before the main session begins.

- Appears once at the start of each mode session (1 in agent, 1 in plan)
- Sends only 8 input tokens, receives 1 token back
- `stop_reason: max_tokens` — intentionally truncated; the response content doesn't matter
- Acts as a lightweight API health check

### 2. File Path Extraction

**Purpose:** Extract file paths from command outputs for context tracking.

- Appears after tool executions that produce file-related output
- Uses the prompt: *"Extract any file paths that this command reads or modifies..."*
- 2 requests in agent mode, 1 in plan mode
- ~340-395 input tokens per request, ~32 output tokens

**There is no categorization or titling** — unlike Copilot, Claude Code's overhead model is never used for request routing or title generation.

```
x-anthropic-billing-header: cc_version=2.1.59.20c; cc_entrypoint=cli; cch=48ea8;

You are Claude Code, Anthropic's official CLI for Claude.

Extract any file paths that this command reads or modifies. For commands like "git diff" and "cat", include the paths of files being shown. Use paths verbatim -- don't add any slashes or try to resolve them. Do not try to infer paths that were not explicitly listed in the command output.

IMPORTANT: Commands that do not display the contents of the files sho
[...truncated — see system-prompt.md for full text]
```

## Mode Delta

How the system prompt changes between modes for this agent:

### Prompt Length

- **agent:** 2,345 words (15,107 chars)
- **plan:** 2,345 words (15,107 chars)

The base system prompt is **identical** across both modes.

### Tool Count

- **agent:** 24 tools
- **plan:** 24 tools

### Tool Differences

**agent → plan:** Tool set identical

### Plan Mode Behavioral Control

While the system prompt and tool set are identical, plan mode behavior is controlled through a `<system-reminder>` tag injected into the `EnterPlanMode` tool result. This runtime injection contains detailed instructions including:

- **"Plan mode is active... you MUST NOT make any edits"** — enforces read-only behavior
- **Plan file path** — specifies a unique file path where the plan should be written (the only file the agent is allowed to edit)
- **5-phase workflow** — Initial Understanding → Design → Review → Final Plan → ExitPlanMode
- **Agent spawning limits** — up to 3 Explore agents in Phase 1, up to 1 Plan agent in Phase 2

This means Claude Code's mode restriction is entirely a prompt-level control — the agent *could* use any of its 24 tools, but the injected instructions tell it not to. This contrasts with Copilot's structural approach of physically removing tools.
