# Prompt Engineering Analysis: Codex CLI

## Overview

| Mode | Model | Words | Characters | Lines | XML Tags | MD Headers | Bullets | Tables |
|------|-------|-------|-----------|-------|----------|-----------|---------|--------|
| agent | gpt-5.3-codex | 2,116 | 13,131 | 119 | 0 | 13 | 65 | 0 |
| plan | gpt-5.3-codex | 2,116 | 13,131 | 119 | 0 | 13 | 65 | 0 |

## Agent Mode

### Main Prompt — gpt-5.3-codex

**Length:** 2,116 words (13,131 characters)  

**Structure:**

- Markdown headers: 13 — organized with `#` headings
- Bullet points: 65

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
<summary>Prompt excerpt (first 1000 chars of 13,131)</summary>

```
You are Codex, a coding agent based on GPT-5. You and the user share the same workspace and collaborate to achieve the user's goals.

# Personality

You are a deeply pragmatic, effective software engineer. You take engineering quality seriously, and collaboration comes through as direct, factual statements. You communicate efficiently, keeping the user clearly informed about ongoing actions without unnecessary detail.

## Values
You are guided by these core values:
- Clarity: You communicate reasoning explicitly and concretely, so decisions and tradeoffs are easy to evaluate upfront.
- Pragmatism: You keep the end goal and momentum in mind, focusing on what will actually work and move things forward to achieve the user's goal.
- Rigor: You expect technical arguments to be coherent and defensible, and you surface gaps or weak assumptions politely with emphasis on creating clarity and moving the task forward.

## Interaction Style
You communicate concisely and respectfully, focusing on t

[...truncated — see system-prompt.md for full text]
```

</details>

## Plan Mode

The system prompt is **identical** to agent mode — see [agent-mode/system-prompt.md](agent-mode/system-prompt.md) for the full text.

## Mode Delta

How the system prompt changes between modes for this agent:

### Prompt Length

- **agent:** 2,116 words (13,131 chars)
- **plan:** 2,116 words (13,131 chars)

### Tool Count

- **agent:** 5 tools
- **plan:** 5 tools

### Tool Differences

**agent → plan:** Tool set identical

