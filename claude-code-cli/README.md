# Claude Code

**Provider(s):** anthropic  
**Model(s):** claude-haiku-4-5-20251001, claude-opus-4-6  
**Modes Captured:** agent, plan  

## Session Metrics

| Mode | Requests | Input Tokens | Output Tokens | Total Tokens | Wall Time |
|------|----------|-------------|--------------|-------------|-----------|
| agent | 11 | 72,104 | 2,213 | 74,317 | 2m 4s |
| plan | 8 | 446 | 1,980 | 2,426 | 5m 1s |

> **Note on token counts:** Agent mode metrics (74K total) exclude ~595K cache_read and ~77K cache_creation tokens. Actual tokens processed per session are ~672K+.

## Architecture

**Multi-model pipeline:** Yes — uses claude-haiku-4-5-20251001, claude-opus-4-6

**Overhead requests:** 6 requests (1,576 tokens) for warmup/quota check + file path extraction (4 in agent + 2 in plan)

**Prompt caching:** 595,359 cache read tokens, 76,875 cache creation tokens

## Tool Summary

- **agent:** 24 tools
- **plan:** 24 tools

## Key Observations

- Uses claude-haiku for warmup/quota checks and file path extraction from command outputs, claude-opus-4-6 for all work
- System prompt has 8 identifiable sections (billing header, identity, System, Doing tasks, Executing actions with care, Using your tools, Tone and style, auto memory)
- Heavy use of prompt caching — significantly reduces effective per-turn input cost
- Tool set is identical across modes (24 tools in both agent and plan) — mode restriction is via system prompt instructions, not tool removal

## Detailed Analysis

- [Prompt Engineering Analysis](PROMPT-ENGINEERING.md)
- [Tool Catalog](TOOL-USE.md)
- [agent mode — System Prompt](agent-mode/system-prompt.md)
- [agent mode — Session Data](agent-mode/session.md)
- [plan mode — System Prompt](plan-mode/system-prompt.md)
- [plan mode — Session Data](plan-mode/session.md)
