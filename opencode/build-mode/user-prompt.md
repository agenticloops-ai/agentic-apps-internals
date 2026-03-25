# User Prompt

> OpenCode sends the user message as a single content block — no layered injection like Codex CLI or Claude Code. The task prompt is delivered as plain text in a single user turn.

The user message contains 1 layer:

1. **User task** — the actual user message

## User Task

```
Implement minimal agentic loop in Python using Anthropic API with a run bash tool
and human confirmation before executing scripts. Implement as a standalone script `agent-loop.py`
```

> Note: Request 1 (title generation) prepends "Generate a title for this conversation:" as a separate user turn before the task text. This is a title-generation overhead request and does not include tools.
