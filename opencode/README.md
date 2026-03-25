# OpenCode

**Provider(s):** openai
**Model(s):** gpt-5.3-codex
**Modes Captured:** build, plan

## Session Metrics

| Mode | Requests | Input Tokens | Output Tokens | Total Tokens | Wall Time |
|------|----------|-------------|--------------|-------------|-----------|
| build | 7 | 70,775 | 3,710 | 74,485 | 2m 8s |
| plan | 4 | 41,115 | 2,310 | 43,425 | 2m 10s |

> **Note on token counts:** No prompt caching observed. Build mode includes 1 overhead request (title generation). Plan mode includes 1 overhead request (title generation). OpenCode routes through `chatgpt.com/backend-api/codex/responses` — a ChatGPT backend endpoint, not the standard OpenAI API.

## Architecture

**Single model:** gpt-5.3-codex for all requests

**Overhead requests:** 1 per session — title generation (no tools, same model)

**Prompt caching:** Not observed — zero cache creation and cache read tokens across all requests

## Tool Summary

- **build:** 10 tools (requests 2–7; request 1 has 0)
- **plan:** 10 tools (requests 2–4; request 1 has 0)

## Key Observations

- Routes through ChatGPT backend (`chatgpt.com/backend-api/codex/responses`), not `api.openai.com`
- System prompt is **identical** across both modes — plan mode behavior is enforced via a `<system-reminder>` block injected into the user message, not by changing the system prompt or tool set
- 10-tool set is notably richer than Codex CLI (5 tools) — includes `apply_patch`, `glob`, `grep`, `read`, `bash`, `task`, `webfetch`, `todowrite`, `question`, `skill`
- Tool naming and schemas closely resemble Claude Code's tool set — suggests shared design lineage or intentional parity
- System prompt emphasizes opinionated frontend design guidance (anti-purple, anti-generic)
- Build mode used `apply_patch` for code generation (not `bash` with heredoc) — cleaner file creation pattern

## Detailed Analysis

- [Prompt Engineering Analysis](PROMPT-ENGINEERING.md)
- [Tool Catalog](TOOL-USE.md)
- [build mode — System Prompt](build-mode/system-prompt.md)
- [build mode — User Prompt](build-mode/user-prompt.md)
- [build mode — Session Data](build-mode/session.md)
- [plan mode — System Prompt](plan-mode/system-prompt.md)
- [plan mode — User Prompt](plan-mode/user-prompt.md)
- [plan mode — Session Data](plan-mode/session.md)
