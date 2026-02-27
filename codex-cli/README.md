# Codex CLI

**Provider(s):** openai  
**Model(s):** gpt-5.3-codex  
**Modes Captured:** agent, plan  

## Session Metrics

| Mode | Requests | Input Tokens | Output Tokens | Total Tokens | Wall Time |
|------|----------|-------------|--------------|-------------|-----------|
| agent | 5 | 54,572 | 4,909 | 59,481 | 3m 20s |
| plan | 2 | 21,312 | 2,157 | 23,469 | 3m 18s |

## Architecture

**Single model:** gpt-5.3-codex

**Overhead requests:** None

**Prompt caching:** Not observed

## Tool Summary

- **agent:** 5 tools
- **plan:** 5 tools

## Key Observations

- Uses a single model (gpt-5.3-codex) for everything — no overhead requests
- Minimal tool set (5 tools) — relies heavily on exec_command for everything
- System prompt emphasizes pragmatic engineering personality with explicit values (Clarity, Pragmatism, Rigor)
- Tool set identical across modes (5 tools) — same as Claude's approach

## Detailed Analysis

- [Prompt Engineering Analysis](PROMPT-ENGINEERING.md)
- [Tool Catalog](TOOL-USE.md)
- [agent mode — System Prompt](agent-mode/system-prompt.md)
- [agent mode — User Prompt](agent-mode/user-prompt.md)
- [agent mode — Session Data](agent-mode/session.md)
- [plan mode — System Prompt](plan-mode/system-prompt.md)
- [plan mode — User Prompt](plan-mode/user-prompt.md)
- [plan mode — Session Data](plan-mode/session.md)
