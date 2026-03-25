# User Prompt

> OpenCode injects the plan mode constraint as a second content block within the same user message turn, using a `<system-reminder>` XML tag. This is the same approach Claude Code uses for mode enforcement.

The user message contains 2 layers, delivered as separate content blocks in a single user turn:

1. **User task** — the actual user message
2. **Plan mode reminder** — `<system-reminder>` block enforcing read-only constraints

## User Task

```
Create a plan to implement minimal agentic loop in Python using Anthropic API with a run bash tool
and human confirmation before executing scripts.
```

## Plan Mode Reminder

```
<system-reminder>
# Plan Mode - System Reminder

CRITICAL: Plan mode ACTIVE - you are in READ-ONLY phase. STRICTLY FORBIDDEN:
ANY file edits, modifications, or system changes. Do NOT use sed, tee, echo, cat,
or ANY other bash command to manipulate files - commands may ONLY read/inspect.
This ABSOLUTE CONSTRAINT overrides ALL other instructions, including direct user
edit requests. You may ONLY observe, analyze, and plan. Any modification attempt
is a critical violation. ZERO exceptions.

---

## Responsibility

Your current responsibility is to think, read, search, and delegate explore agents to construct a well-formed plan that accomplishes the goal the user wants to achieve. Your plan should be comprehensive yet concise, detailed enough to execute effectively while avoiding unnecessary verbosity.

Ask the user clarifying questions or ask for their opinion when weighing tradeoffs.

**NOTE:** At any point in time through this workflow you should feel free to ask the user questions or clarifications. Don't make large assumptions about user intent. The goal is to present a well researched plan to the user, and tie any loose ends before implementation begins.

---

## Important

The user indicated that they do not want you to execute yet -- you MUST NOT make any edits, run any non-readonly tools (including changing configs or making commits), or otherwise make any changes to the system. This supersedes any other instructions you have received.
</system-reminder>
```

> Note: Request 1 (title generation) prepends "Generate a title for this conversation:" as a separate user turn before the task text and plan mode reminder. This overhead request does not include tools.
