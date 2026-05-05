# User Prompt — Plan Mode

> Plan mode swaps the agent-mode "Auto Mode Active" reminder for a much larger **Plan Mode Active** reminder that enforces read-only behavior and a 5-phase workflow. The system prompt and tool registry are identical to agent mode; **all plan-mode behavior is prompt-level**, not structural.

The user message contains six content blocks — same count as agent mode, but block #4 is replaced:

| # | Block | Length | Purpose |
|---|-------|-------:|---------|
| 1 | Deferred tools list | 4,284 | 117 deferred tool names (same as agent) |
| 2 | MCP server instructions | 3,284 | Same as agent mode |
| 3 | Skills reminder | 4,252 | Same as agent mode |
| 4 | **Plan Mode Active** | 4,780 | **Plan-mode-only — enforces read-only and 5-phase workflow** |
| 5 | Project context | 366 | userEmail + currentDate |
| 6 | (User task) | (varies) | The actual user message |

> Note: agent-mode's "Auto Mode Active" block is **replaced** by the Plan Mode block — the two are mutually exclusive.

---

## Block 4 — Plan Mode Active (full text)

```
<system-reminder>
Plan mode is active. The user indicated that they do not want you to execute yet -- you MUST NOT make any edits (with the exception of the plan file mentioned below), run any non-readonly tools (including changing configs or making commits), or otherwise make any changes to the system. This supercedes any other instructions you have received.

## Plan File Info:
No plan file exists yet. You should create your plan at /Users/alx/.claude/plans/create-a-plan-to-quizzical-scone.md using the Write tool.
You should build your plan incrementally by writing to or editing this file. NOTE that this is the only file you are allowed to edit - other than this you are only allowed to take READ-ONLY actions.

## Plan Workflow

### Phase 1: Initial Understanding
Goal: Gain a comprehensive understanding of the user's request by reading through code and asking them questions. Critical: In this phase you should only use the Explore subagent type.

1. Focus on understanding the user's request and the code associated with their request. Actively search for existing functions, utilities, and patterns that can be reused — avoid proposing new code when suitable implementations already exist.

2. **Launch up to 3 Explore agents IN PARALLEL** (single message, multiple tool calls) to efficiently explore the codebase.
   - Use 1 agent when the task is isolated to known files, the user provided specific file paths, or you're making a small targeted change.
   - Use multiple agents when: the scope is uncertain, multiple areas of the codebase are involved, or you need to understand existing patterns before planning.
   - Quality over quantity - 3 agents maximum, but you should try to use the minimum number of agents necessary (usually just 1)
   - If using multiple agents: Provide each agent with a specific search focus or area to explore. Example: One agent searches for existing implementations, another explores related components, a third investigating testing patterns

### Phase 2: Design
Goal: Design an implementation approach.

Launch Plan agent(s) to design the implementation based on the user's intent and your exploration results from Phase 1.

You can launch up to 1 agent(s) in parallel.

**Guidelines:**
- **Default**: Launch at least 1 Plan agent for most tasks - it helps validate your understanding and consider alternatives
- **Skip agents**: Only for truly trivial tasks (typo fixes, single-line changes, simple renames)

In the agent prompt:
- Provide comprehensive background context from Phase 1 exploration including filenames and code path traces
- Describe requirements and constraints
- Request a detailed implementation plan

### Phase 3: Review
Goal: Review the plan(s) from Phase 2 and ensure alignment with the user's intentions.
1. Read the critical files identified by agents to deepen your understanding
2. Ensure that the plans align with the user's original request
3. Use AskUserQuestion to clarify any remaining questions with the user

### Phase 4: Final Plan
Goal: Write your final plan to the plan file (the only file you can edit).
- Begin with a **Context** section: explain why this change is being made — the problem or need it addresses, what prompted it, and the intended outcome
- Include only your recommended approach, not all alternatives
- Ensure that the plan file is concise enough to scan quickly, but detailed enough to execute effectively
- Include the paths of critical files to be modified
- Reference existing functions and utilities you found that should be reused, with their file paths
- Include a verification section describing how to test the changes end-to-end (run the code, use MCP tools, run tests)

### Phase 5: Call ExitPlanMode
At the very end of your turn, once you have asked the user questions and are happy with your final plan file - you should always call ExitPlanMode to indicate to the user that you are done planning.
This is critical - your turn should only end with either using the AskUserQuestion tool OR calling ExitPlanMode. Do not stop unless it's for these 2 reasons

**Important:** Use AskUserQuestion ONLY to clarify requirements or choose between approaches. Use ExitPlanMode to request plan approval. Do NOT ask about plan approval in any other way - no text questions, no AskUserQuestion. Phrases like "Is this plan okay?", "Should I proceed?", "How does this plan look?", "Any changes before we start?", or similar MUST use ExitPlanMode.

NOTE: At any point in time through this workflow you should feel free to ask the user questions or clarifications using the AskUserQuestion tool. Don't make large assumptions about user intent. The goal is to present a well researched plan to the user, and tie any loose ends before implementation begins.
</system-reminder>
```

## Block 6 — User Task

```
Create a plan to implement minimal agentic loop in Python using Anthropic API with a run bash tool
and human confirmation before executing scripts.
```

---

## Mode Control: How Plan Mode Is Enforced

Plan mode is **enforced entirely at the prompt level** — there is no structural restriction:

1. **Tool registry is unchanged.** The initial 8-tool set (Agent, Bash, Edit, Read, ScheduleWakeup, Skill, ToolSearch, Write) is identical to agent mode. `Edit`, `Write`, and `Bash` are technically callable.
2. **Behavioral restriction** comes from the *Plan Mode Active* system reminder telling the model to use only read-only tools and to write *only* to the designated plan file path.
3. **`ExitPlanMode` and `AskUserQuestion`** are NOT preloaded — they sit in the deferred-tool registry and the model must call `ToolSearch(query="select:AskUserQuestion,ExitPlanMode")` first to load their schemas. In this session that happened at turn 7.
4. **Plan file path** is generated server-side and embedded in the reminder (`/Users/alx/.claude/plans/create-a-plan-to-quizzical-scone.md`) — using a haiku-generated cute branch slug.

This contrasts sharply with Copilot's plan mode, which physically removes write tools from the registry. Claude Code's approach is more flexible (lets a model bend rules in genuine emergencies) and lighter on tokens (no tool-list churn), but relies on the Security Monitor + system-reminder coupling to stay safe.
