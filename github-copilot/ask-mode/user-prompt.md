# User Prompt

> Minimal user prompt — just the task in a `<prompt>` tag. No environment info, no workspace structure, no `<reminderInstructions>`. Matches the 0-tool configuration of ask mode: pure Q&A with no agentic context.

In ask mode, the user message is minimal — no environment info, no reminder instructions, no XML wrappers. The main request (Request #3, after categorization and titling overhead) receives just a `<prompt>` tag:

## User Task

```
<prompt>
What is the difference between ReAct and plan-and-execute as agentic
design patterns? When would you choose one over the other?
</prompt>
```

> Unlike agent and plan mode, ask mode has no `<reminderInstructions>`, no `<environment_info>`, and no `<workspace_info>`. The user message is structurally simpler because ask mode has 0 tools — it's a pure Q&A interaction.
