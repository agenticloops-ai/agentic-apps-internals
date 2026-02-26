# GitHub Copilot

**Provider(s):** github-copilot  
**Model(s):** gpt-4o-mini, gpt-4o-mini-2024-07-18, gpt-5.3-codex  
**Modes Captured:** agent, ask, plan  

## Session Metrics

| Mode | Requests | Input Tokens | Output Tokens | Total Tokens | Wall Time |
|------|----------|-------------|--------------|-------------|-----------|
| agent | 11 | 120,304 | 3,479 | 123,783 | 1m 29s |
| ask | 3 | 1,866 | 464 | 2,330 | 1m 4s |
| plan | 7 | 49,861 | 3,129 | 52,990 | 3m 54s |

## Architecture

**Multi-model pipeline:** Yes — uses gpt-4o-mini, gpt-4o-mini-2024-07-18, gpt-5.3-codex

**Overhead requests:** 8 requests (9,039 tokens) — 5 in agent (1 titling + 4 activity summarization), 2 in ask (1 categorization + 1 titling), 1 in plan (1 titling)

**Prompt caching:** Not observed

## Tool Summary

- **agent:** 65 tools
- **ask:** 0 tools
- **plan:** 22 tools

## Key Observations

- Uses gpt-4o-mini for request categorization and title generation before routing to gpt-5.3-codex for actual work
- Tool count drops from 65 (agent mode) to 22 (plan mode) — removes all write/execute tools
- Copilot's system prompt includes VS Code workspace context (folder paths, OS, editor version)
- In plan mode, spawns a subagent via `runSubagent` tool for codebase exploration

## Detailed Analysis

- [Prompt Engineering Analysis](PROMPT-ENGINEERING.md)
- [Tool Catalog](TOOL-USE.md)
- [agent mode — System Prompt](agent-mode/system-prompt.md)
- [agent mode — Session Data](agent-mode/session.md)
- [ask mode — System Prompt](ask-mode/system-prompt.md)
- [ask mode — Session Data](ask-mode/session.md)
- [plan mode — System Prompt](plan-mode/system-prompt.md)
- [plan mode — Session Data](plan-mode/session.md)
