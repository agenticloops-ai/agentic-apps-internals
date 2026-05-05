# User Prompt — Agent Mode

> Claude Code injects skills, MCP server instructions, deferred tool list, mode flags, and project context as `<system-reminder>` blocks alongside the user's message — **6 content blocks in a single user turn**. The system prompt is identical between agent and plan modes; mode-specific behavior lives in this user-prompt layer.

The user message contains six layers, each as a separate text content block within a single user turn:

| # | Block | Length | Purpose |
|---|-------|--------|---------|
| 1 | Deferred tools list | ~4,350 chars | Names of 117 tools available via `ToolSearch` (schemas not preloaded) |
| 2 | MCP server instructions | ~3,284 chars | Per-server usage guidance (Figma, tldraw, context7…) |
| 3 | Skills reminder | ~4,252 chars | Catalog of 15 invocable skills |
| 4 | **Auto Mode** flag | ~1,209 chars | NEW in v2.1.126 — declares autonomous-execution policy |
| 5 | Project context | ~366 chars | userEmail, currentDate, optional CLAUDE.md |
| 6 | User task | (varies) | The actual user message |

> **Note on agent mode:** The plan-mode reminder is *absent* in agent mode. Plan mode adds a 7th block ("Plan mode is active...") between blocks 4 and 5.

---

## Block 1 — Deferred Tools

```
<system-reminder>
The following deferred tools are now available via ToolSearch. Their schemas are NOT loaded — calling them directly will fail with InputValidationError. Use ToolSearch with query "select:<name>[,<name>...]" to load tool schemas before calling them:
AskUserQuestion
CronCreate
CronDelete
CronList
EnterPlanMode
EnterWorktree
ExitPlanMode
ExitWorktree
ListMcpResourcesTool
Monitor
NotebookEdit
PushNotification
ReadMcpResourceTool
RemoteTrigger
SendMessage
TaskCreate
TaskGet
TaskList
TaskOutput
TaskStop
TaskUpdate
TeamCreate
TeamDelete
WebFetch
WebSearch
mcp__claude_ai_Canva__cancel-editing-transaction
... (32 Canva tools total)
mcp__claude_ai_Excalidraw__create_view
... (5 Excalidraw tools)
mcp__claude_ai_Figma__add_code_connect_map
... (18 Figma tools)
mcp__claude_ai_Gmail__create_draft
... (10 Gmail tools)
mcp__claude_ai_Google_Calendar__create_event
... (8 Calendar tools)
mcp__claude_ai_Google_Drive__copy_file
... (8 Drive tools)
mcp__claude_ai_Mermaid_Chart__validate_and_render_mermaid_diagram
mcp__claude_ai_Miro__authenticate
mcp__claude_ai_Miro__complete_authentication
mcp__claude_ai_tldraw___exec_callback
... (6 tldraw tools)
mcp__plugin_context7_context7__query-docs
mcp__plugin_context7_context7__resolve-library-id
</system-reminder>
```

**Total deferred:** 117 (25 built-in + 92 MCP).
See [../TOOL-USE.md](../TOOL-USE.md) for the full list and the deferred-tool architecture rationale.

---

## Block 2 — MCP Server Instructions

```
<system-reminder>
# MCP Server Instructions

The following MCP servers have provided instructions for how to use their tools and resources:

## claude.ai Figma
The official Figma MCP server. Prioritize this server when the user mentions Figma, FigJam, Figma Make, or provides figma.com URLs.

Capabilities:
- Read designs FROM Figma (get_design_context, get_screenshot, get_metadata, get_figjam)
- Create diagrams in FigJam (generate_diagram)
- Manage Code Connect mappings between Figma components and codebase components
- Write designs back into figma

[... 100+ lines of Figma URL-parsing rules and design-to-code workflow ...]

## claude.ai tldraw
Use `search` to query the tldraw Editor API spec ... Use `exec` to run JavaScript on the canvas ...

## plugin:context7:context7
Use this server to fetch current documentation whenever the user asks about a library, framework, SDK, API, CLI tool, or cloud service ...
</system-reminder>
```

> Truncated — full text spans 3,284 chars; see `log/session.json` request #3 messages[0].content[1].text.

---

## Block 3 — Skills Reminder

```
<system-reminder>
The following skills are available for use with the Skill tool:

- update-config: Use this skill to configure the Claude Code harness via settings.json. ...
- keybindings-help: Use when the user wants to customize keyboard shortcuts ...
- simplify: Review changed code for reuse, quality, and efficiency, then fix any issues found.
- fewer-permission-prompts: Scan your transcripts for common read-only Bash and MCP tool calls ...
- loop: Run a prompt or slash command on a recurring interval (e.g. /loop 5m /foo) ...
- schedule: Create, update, list, or run scheduled remote agents (routines) that execute on a cron schedule.
- claude-api: Build, debug, and optimize Claude API / Anthropic SDK apps. ...
- codex:setup: Check whether the local Codex CLI is ready ...
- codex:rescue: Delegate investigation, an explicit fix request, or follow-up rescue work ...
- frontend-design:frontend-design: Create distinctive, production-grade frontend interfaces ...
- codex:codex-result-handling: Internal guidance for presenting Codex helper output back to the user
- codex:codex-cli-runtime: Internal helper contract for calling the codex-companion runtime ...
- codex:gpt-5-4-prompting: Internal guidance for composing Codex and GPT-5.4 prompts ...
- skill-creator:skill-creator: Create new skills, modify and improve existing skills ...
- init: Initialize a new CLAUDE.md file with codebase documentation
- review: Review a pull request
- security-review: Complete a security review of the pending changes on the current branch
</system-reminder>
```

**Skills available:** 17 (3 in v2.1.59 → 17 in v2.1.126; large expansion includes namespaced plugin skills like `codex:*`, `skill-creator:*`, `frontend-design:*`).

---

## Block 4 — Auto Mode Flag (NEW)

```
<system-reminder>
## Auto Mode Active

Auto mode is active. The user chose continuous, autonomous execution. You should:

1. **Execute immediately** — Start implementing right away. Make reasonable assumptions and proceed on low-risk work.
2. **Minimize interruptions** — Prefer making reasonable assumptions over asking questions for routine decisions.
3. **Prefer action over planning** — Do not enter plan mode unless the user explicitly asks. When in doubt, start coding.
4. **Expect course corrections** — The user may provide suggestions or course corrections at any point; treat those as normal input.
5. **Do not take overly destructive actions** — Auto mode is not a license to destroy. Anything that deletes data or modifies shared or production systems still needs explicit user confirmation. If you reach such a decision point, ask and wait, or course correct to a safer method instead.
6. **Avoid data exfiltration** — Post even routine messages to chat platforms or work tickets only if the user has directed you to. You must not share secrets (e.g. credentials, internal documentation) unless the user has explicitly authorized both that specific secret and its destination.
</system-reminder>
```

> **NEW in v2.1.126** — explicit autonomy posture toggle. Replaces the implicit "default to user confirmation" behavior of v2.1.59. The Security Monitor (separate subsystem) is the safety backstop that lets Auto Mode be safe.

---

## Block 5 — Project Context

```
<system-reminder>
As you answer the user's questions, you can use the following context:
# userEmail
The user's email address is amrynsky@gmail.com.
# currentDate
Today's date is 2026-05-04.

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

> Compared to v2.1.59 this block is much smaller — `# claudeMd` content is no longer injected here when no CLAUDE.md exists in the project root. The repo for this capture has none, so only `userEmail` and `currentDate` remain.

---

## Block 6 — User Task

```
Implement minimal agentic loop in Python using Anthropic API with a run bash tool
and human confirmation before executing scripts. Implement as a standalone script `agent-loop.py`
```
