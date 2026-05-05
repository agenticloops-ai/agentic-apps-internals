# Tool Catalog: Claude Code v2.1.126

## Deferred Tool Schemas

Claude Code preloads only **8 always-available tool schemas** at session start, and exposes **117 additional tools by name only** through a `<system-reminder>` block. To call a deferred tool, the model must first invoke `ToolSearch(query="select:<name>")` to load its schema.

This keeps the always-loaded schema budget at roughly 12K characters. Most of the catalog only enters the context when the model genuinely needs it, and the savings compound across long sessions because each opus turn that doesn't touch the deferred schemas still gets cache reads on the trimmed tool definitions.

## Always-Loaded Tools (8)

These ship with every opus request:

| Tool | Category | Purpose |
|------|----------|---------|
| `Agent` | Multi-agent | Spawn a subagent; supports 6 subagent_types (claude-code-guide, codex:codex-rescue, Explore, general-purpose, Plan, statusline-setup) and a worktree isolation mode |
| `Bash` | Shell | Run shell commands; description includes the full git safety protocol and committing/PR workflows |
| `Edit` | File write | Exact string replacement in a file |
| `Read` | File read | Read file contents (text, images, PDFs, ipynb) |
| `ScheduleWakeup` | Scheduling | Schedule resumption in `/loop` dynamic mode; advice baked in about cache TTL (5 min) |
| `Skill` | Multi-agent | Invoke a named skill from the user's catalog |
| `ToolSearch` | Meta | Fetch schemas for deferred tools |
| `Write` | File write | Write a file (full content replacement) |

For broad code searches, the system prompt directs the model to use `find` and `grep` via `Bash`, or to spawn the `Explore` subagent for open-ended questions — there are no dedicated `Glob` or `Grep` tools in the always-loaded set.

## Deferred Tools (117 — by name)

Listed in the system-reminder of every initial user message. **25 built-in** + **92 MCP**.

### Built-in (25)

| Group | Tools |
|-------|-------|
| Questions | `AskUserQuestion` |
| Planning | `EnterPlanMode`, `ExitPlanMode` |
| Worktree | `EnterWorktree`, `ExitWorktree` |
| Web | `WebFetch`, `WebSearch` |
| Notebook | `NotebookEdit` |
| Cron | `CronCreate`, `CronList`, `CronDelete` |
| Notifications | `PushNotification`, `RemoteTrigger`, `SendMessage` |
| Tasks | `TaskCreate`, `TaskGet`, `TaskList`, `TaskOutput`, `TaskStop`, `TaskUpdate` |
| Teams | `TeamCreate`, `TeamDelete` |
| MCP introspection | `ListMcpResourcesTool`, `ReadMcpResourceTool` |
| Process control | `Monitor` |

### MCP (92, by service)

| Service | Count | Examples |
|---------|------:|----------|
| `claude_ai_Canva` | 32 | get-design, perform-editing-operations, export-design |
| `claude_ai_Figma` | 18 | get_design_context, get_screenshot, generate_diagram |
| `claude_ai_Gmail` | 10 | search_threads, create_draft, label_message |
| `claude_ai_Google_Calendar` | 8 | list_events, create_event, suggest_time |
| `claude_ai_Google_Drive` | 8 | search_files, read_file_content, get_file_metadata |
| `claude_ai_tldraw` | 6 | exec, search, save_checkpoint |
| `claude_ai_Excalidraw` | 5 | save_checkpoint, export_to_excalidraw |
| `claude_ai_Miro` | 2 | authenticate, complete_authentication |
| `plugin_context7_context7` | 2 | query-docs, resolve-library-id |
| `claude_ai_Mermaid_Chart` | 1 | validate_and_render_mermaid_diagram |

The MCP servers also inject a **separate** `<system-reminder>` block with usage instructions per server (Figma URL parsing rules, tldraw exec semantics, context7 documentation guidance). See [agent-mode/user-prompt.md](agent-mode/user-prompt.md) Block 2.

## Mode Delta: Tool Changes

| | Agent mode | Plan mode |
|---|---|---|
| Always-loaded count | 8 | 8 |
| Tools loaded after `ToolSearch` | varies (none in this capture) | +`AskUserQuestion`, +`ExitPlanMode` (loaded turn 7) |
| Total schemas in registry by session end | 8 | 10 |

Plan mode tools (`AskUserQuestion`, `ExitPlanMode`) ship as deferred tools that the model loads on-demand. The system prompt for plan mode is the same as agent mode — the *Plan Mode Active* system-reminder is what changes behavior. See [plan-mode/user-prompt.md](plan-mode/user-prompt.md) for the read-only enforcement reminder.

## Tool Schemas (selected)

### `ToolSearch`

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Query to find deferred tools. Use \"select:<tool_name>\" for direct selection, or keywords to search."
    },
    "max_results": {
      "type": "number",
      "description": "Maximum number of results to return (default: 5)"
    }
  },
  "required": ["query", "max_results"]
}
```

Two query modes:

- `select:Read,Edit,Grep` — fetch named tools verbatim
- `notebook jupyter` — keyword search; ranks by name + description

`+` prefix on a term forces it to appear in the tool name (e.g. `+slack send` requires "slack" in the name).

### `Agent` (subagent spawn)

The `Agent` tool description enumerates 6 subagent types directly. Two are noteworthy:

- **`Explore`** — fast read-only search agent for broad lookups. Accepts a search-breadth hint ("quick" / "medium" / "very thorough").
- **`codex:codex-rescue`** — delegates to an external Codex CLI runtime when Claude is stuck.

The schema includes optional fields for richer subagent control:

- `model` — override per-call (`sonnet` / `opus` / `haiku`)
- `name` — addressable handle for `SendMessage(to: name)` continuation
- `team_name` — team context
- `mode` — permission mode for spawned teammate (`plan`, `auto`, etc.)
- `isolation: "worktree"` — spawns into a temporary git worktree
- `run_in_background` — fire-and-notify

### `ScheduleWakeup`

Schedules the next iteration in `/loop` dynamic mode. The description encodes some unusual operational guidance:

> The Anthropic prompt cache has a 5-minute TTL. Sleeping past 300 seconds means the next wake-up reads your full conversation context uncached — slower and more expensive. So the natural breakpoints:
>
> - Under 5 minutes (60s–270s): cache stays warm
> - 5 minutes to 1 hour (300s–3600s): pay the cache miss
>
> **Don't pick 300s.** It's the worst-of-both …

This is a rare example of cache-economics being explicitly surfaced into a tool description so the model can plan around it.

### `Bash` description

The Bash description includes:

- A "use dedicated tools" preamble (Read, Edit, Write, etc.)
- A 12-bullet command-style guide (background mode, cwd persistence, find/regex tips)
- A full **git safety protocol** (no `git push --force`, no `--no-verify`, prefer new commits over amend)
- A **committing changes** workflow (4-step parallel-execution recipe with HEREDOC commit message format)
- A **creating PRs** workflow (parallel git status/diff/log → push → `gh pr create` with body HEREDOC)

This guidance lives in the tool description rather than the system prompt — it only lands in context when Bash is actually used.

## See Also

- [CHANGES-FROM-v2.1.59.md](CHANGES-FROM-v2.1.59.md) — version-to-version delta
