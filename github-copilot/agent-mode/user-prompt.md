# User Prompt

> Copilot sends environment info, workspace structure, terminal state, and behavioral `<reminderInstructions>` across 2 user turns. The task is wrapped in `<userRequest>` tags. Agent mode includes terminal state in `<context>` that plan mode omits.

GitHub Copilot sends user context across multiple user turns in the main request (Request #2, after the titling overhead):

1. **Environment info** — OS, workspace folders, directory structure
2. **Context + reminder instructions** — current date, terminal state, agent behavioral instructions, and the actual user request wrapped in `<userRequest>` tags

## Environment Info

```
<environment_info>
The user's current OS is: macOS
</environment_info>
<workspace_info>
I am working in a workspace with the following folders:
- /Users/alx/Development/agenticloops-ai/agentlens/samples/copilot
I am working in a workspace that has the following structure:

This is the state of the context at this point in the conversation. The view of the workspace structure may be truncated. You can use tools to collect more context if needed.
</workspace_info>
```

## Context + Reminder Instructions

```
<context>
The current date is February 25, 2026.
Terminals:
Terminal: zsh

</context>
<reminderInstructions>
You are an agent—keep going until the user's query is completely resolved before ending your turn. ONLY stop if solved or genuinely blocked.
Take action when possible; the user expects you to do useful work without unnecessary questions.
After any parallel, read-only context gathering, give a concise progress update and what's next.
Avoid repetition across turns: don't restate unchanged plans or sections (like the todo list) verbatim; provide delta updates or only the parts that changed.
Tool batches: You MUST preface each batch with a one-sentence why/what/outcome preamble.
Progress cadence: After 3 to 5 tool calls, or when you create/edit > ~3 files in a burst, report progress.
Requirements coverage: Read the user's ask in full and think carefully. Do not omit a requirement. If something cannot be done with available tools, note why briefly and propose a viable alternative.

</reminderInstructions>
<userRequest>
Implement minimal agentic loop in Python using Anthropic API with a run bash tool and human confirmation before executing scripts. Implement as a standalone script `agent.py`
</userRequest>
```
