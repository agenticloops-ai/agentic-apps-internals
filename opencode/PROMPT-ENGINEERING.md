# Prompt Engineering Analysis: OpenCode

## Overview

OpenCode uses a single system prompt across both modes:

| Mode | Model | Words | Characters | Lines | XML Tags | MD Headers | Bullets |
|------|-------|-------|-----------|-------|----------|-----------|---------|
| build | gpt-5.3-codex | 1,171 | 7,361 | 79 | 0 | 6 | 56 |
| plan | gpt-5.3-codex | 1,171 | 7,361 | 79 | 0 | 6 | 56 |

### Request Breakdown by Mode

| Mode | gpt-5.3-codex | Total |
|------|---------------|-------|
| Build | 7 | 7 |
| Plan | 4 | 4 |
| **Total** | **11** | **11** |

> The system prompt is **identical** across all requests in both modes — same 1,171 words, same structure. Plan mode behavior is enforced entirely through a `<system-reminder>` block injected into the user message layer, not through prompt or tool changes.

## Main System Prompt — gpt-5.3-codex

**Length:** 1,171 words (7,361 characters)

**Structure:**

- Markdown headers: 6 — organized with `##` headings
- Bullet points: 56

**6 Identifiable Sections:**

1. **Persona** — "You are OpenCode, the best coding agent on the planet" — assertive, superlative identity
2. **Editing constraints** — ASCII defaults, comment minimalism, `apply_patch` preference
3. **Tool usage** — prefer specialized tools over shell; parallel vs sequential guidance
4. **Git and workspace hygiene** — dirty worktree handling, destructive command prohibitions
5. **Frontend tasks** — anti-generic design guidance with specific aesthetic directives
6. **Presenting your work** — concise tone, question policy, final answer formatting rules

**Key Sections Identified:**

- Persona
- Tool Instructions
- Formatting
- Constraints
- Code Style

<details>
<summary>Prompt excerpt (first 1000 chars of 7,361)</summary>

```
You are OpenCode, the best coding agent on the planet.

You are an interactive CLI tool that helps users with software engineering tasks. Use the instructions below and the tools available to you to assist the user.

## Editing constraints
- Default to ASCII when editing or creating files. Only introduce non-ASCII or other Unicode characters when there is a clear justification and the file already uses them.
- Only add comments if they are necessary to make a non-obvious block easier to understand.
- Try to use apply_patch for single file edits, but it is fine to explore other options to make the edit if it does not work well. Do not use apply_patch for changes that are auto-generated (i.e. generating package.json or running a lint or format command like gofmt) or when scripting is more efficient (such as search and replacing a string across a codebase).

## Tool usage
- Prefer specialized tools over shell for file operations:
  - Use Read to view files, Edit to modify files, and Write only when needed.
  - Use Glob to find files by name and Grep to search file contents.
- Us

[...truncated — see system-prompt.md for full text]
```

</details>

## Title Generation Request

OpenCode uses the same model (gpt-5.3-codex) for title generation — request 1 in each session:

**Purpose:** Generate a short conversation title

- Same system prompt as all other requests
- No tools provided
- User message: "Generate a title for this conversation:" followed by the task text
- Returns a short phrase (e.g., "Minimal Anthropic agent loop with bash confirm")

## Mode Delta

How the system prompt changes between modes for this agent:

### Prompt Length

- **build:** 1,171 words (7,361 chars)
- **plan:** 1,171 words (7,361 chars)

Identical — the system prompt does not change between modes.

### Tool Count

- **build:** 10 tools
- **plan:** 10 tools

### Tool Differences

**build → plan:** Tool set identical across both modes

### Plan Mode Enforcement

Plan mode is enforced via a `<system-reminder>` block (228 words, 1,484 chars) injected as a second content block in the user message:

- `CRITICAL: Plan mode ACTIVE - you are in READ-ONLY phase`
- `STRICTLY FORBIDDEN: ANY file edits, modifications, or system changes`
- `This ABSOLUTE CONSTRAINT overrides ALL other instructions`
- Instructs the agent to `think, read, search, and delegate explore agents`
- Encourages asking clarifying questions and weighing tradeoffs

This means OpenCode's mode restriction is purely a **user-message-level injection** — the model receives the same system prompt and the same tools in both modes, but is told via a `<system-reminder>` block to restrict itself to read-only operations. This is similar to how Claude Code handles mode changes (via `<system-reminder>` blocks), but notably different from GitHub Copilot (which changes the tool set between modes).
