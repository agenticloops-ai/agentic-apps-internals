# User Prompt

> Claude Code injects skills and project context as `<system-reminder>` blocks alongside the user's message — 3 content blocks in a single user turn. The system prompt is identical across modes; the user prompt layer is where mode-specific context lives (skills, CLAUDE.md, git status).

The user message contains three layers, injected as separate content blocks within a single user turn:

1. **Skills reminder** — a `<system-reminder>` listing available skills (keybindings-help, claude-developer-platform, frontend-design)
2. **Project context** — a `<system-reminder>` with CLAUDE.md contents and current date
3. **User task** — the actual user message

## Skills Reminder

```
<system-reminder>
The following skills are available for use with the Skill tool:

- keybindings-help: Use when the user wants to customize keyboard shortcuts, rebind keys, add chord bindings, or modify ~/.claude/keybindings.json. Examples: "rebind ctrl+s", "add a chord shortcut", "change the submit key", "customize keybindings".
- claude-developer-platform: Build applications that call the Claude API or Anthropic SDK. Use ONLY when the code actually uses or will use the `anthropic` SDK package or Claude API endpoints.
TRIGGER when:
- Code imports `anthropic` or `@anthropic-ai/sdk` (the Anthropic SDK)
- Code imports `claude_agent_sdk` or `@anthropic-ai/claude-agent-sdk` (the Agent SDK)
- User explicitly asks to use Claude, the Anthropic API, or Anthropic SDK
- User needs an AI/LLM and no other provider's SDK is already in use
DO NOT TRIGGER when (use another skill instead):
- Code imports `openai`, `google.generativeai`, or any non-Anthropic AI SDK
- Filenames contain "openai", "gpt", "gemini" — the code uses a different provider
- The task is general programming with no LLM API calls
- The task is ML/data science (PyTorch, scikit-learn, etc.)
- Feature names like "extended thinking", "prompt caching", "tool use" appear but the code uses a NON-Anthropic SDK — those are generic concepts, not Claude-specific
CRITICAL: Check the existing code's imports FIRST. If it imports `openai` or another provider, this skill cannot help — it only contains Claude/Anthropic documentation.
- frontend-design:frontend-design: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
</system-reminder>
```

## Project Context

```
<system-reminder>
As you answer the user's questions, you can use the following context:
# claudeMd
Codebase and user instructions are shown below. Be sure to adhere to these instructions. IMPORTANT: These instructions OVERRIDE any default behavior and you MUST follow them exactly as written.

Contents of /Users/alx/Development/agenticloops-ai/agentlens/.claude/CLAUDE.md (project instructions, checked into the codebase):

# AgentLens

LLM API traffic profiler — Python MITM proxy + React web UI.

## Commands

Always use `uv run` to run Python — never bare `python` or `pytest`.

[...project-specific commands, structure, architecture, code style, testing, dependencies...]

# currentDate
Today's date is 2026-02-26.

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

## User Task

```
Implement minimal agentic loop in Python using Anthropic API with a run bash tool and human confirmation before executing scripts. Implement as a standalone script `agent-loop.py`
```
