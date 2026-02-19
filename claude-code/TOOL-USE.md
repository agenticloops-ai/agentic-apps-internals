# Tool Use Analysis: Claude Code

A comprehensive analysis of tool availability, schemas, sub-agent architecture, and usage patterns in Claude Code.

---

## Tool Distribution Overview

| Mode | Tools Defined | Read | Write | Execute | Sub-Agents | Token Cost |
|------|---------------|------|-------|---------|------------|------------|
| **Planning** | 0 | ❌ | ❌ | ❌ | ❌ | 0 |
| **Agent** | 17 | ✅ | ✅ | ✅ | ✅ | ~7,100 |

Planning mode sends an **empty tools array** — no tools are available to the model. The system prompt references tools (Glob, Grep, Read, Bash), but these exist only in text; the model cannot invoke them. See [Planning Mode](#planning-mode-zero-tools) below for the full explanation.

---

## Planning Mode: Zero Tools

### No Tools Are Defined

Planning mode requests are sent with `"tools": []` — a completely empty array. **The model has no tools available.** It cannot call Read, Glob, Grep, Bash, or any other tool.

```json
{
  "tools": [],
  "system": [
    {"text": "You are Claude Code, Anthropic's official CLI for Claude.", "cache_control": {"type": "ephemeral"}},
    {"text": "You are a software architect and planning specialist...", "cache_control": {"type": "ephemeral"}}
  ],
  "messages": [{"role": "user", "content": [{"type": "text", "text": "Warmup"}]}]
}
```

### System Prompt References Tools That Don't Exist

Despite `tools: []`, the system prompt references tools by name:

> "Find existing patterns and conventions using Glob, Grep, and Read"
> "Use Bash ONLY for read-only operations (ls, git status, git log, git diff, find, cat, head, tail)"

**This is a contradiction.** The most likely explanation: this planning prompt is designed for the `Task` sub-agent system, where `subagent_type=Plan` injects tools at runtime. In the captured logs, planning mode only appears in **warmup requests** (where `tools: []` is fine because the response is discarded — only cache priming matters). During actual planning tasks spawned via the `Task` tool, the Plan agent likely receives read-only tools.

The model's warmup response confirms the disconnect — with no real tools available, it **hallucinated fake tool calls as plain text** that could never execute:

```
<invoke name="read_file">
<parameter name="path">/Users/alx/Development/lab/llm-proxy/README.md</parameter>
</invoke>
```

These are NOT `tool_use` content blocks — they are raw text in the assistant's response.

### Comparison with Copilot's Plan Mode

| Aspect | Copilot Plan Mode | Claude Code Planning |
|--------|-------------------|----------------------|
| Tools defined | 13 read-only tools | **0 tools** (`tools: []`) |
| Can read files | ✅ via `read_file` tool | ❌ no tools available |
| Can search code | ✅ via `grep_search` tool | ❌ no tools available |
| Can run commands | ❌ | ❌ |
| Can edit files | ❌ | ❌ |
| Enforcement | Tool-level restrictions | No tools = nothing to restrict |
| Tool token cost | ~2,636 tokens | 0 tokens |

### What the System Prompt Would Allow (If Tools Were Present)

The system prompt defines permitted and prohibited operations. These rules would apply if the Plan sub-agent receives tools at runtime via the `Task` tool:

**Allowed read operations:**
```
ls, git status, git log, git diff, find, cat, head, tail
```

**Prohibited operations:**
```
mkdir, touch, rm, cp, mv, git add, git commit, npm install, pip install,
or any file creation/modification
```

---

## Agent Mode: 17 Full-Access Tools

### Tool Categories

| Category | Count | Token Cost* | Purpose |
|----------|-------|-------------|---------|
| **File Operations** | 4 | ~2,200 | Read, Edit, Write, NotebookEdit |
| **Search & Navigation** | 2 | ~1,400 | Glob, Grep |
| **Execution** | 1 | ~800 | Bash |
| **Task Management** | 2 | ~600 | TodoWrite, AskUserQuestion |
| **Sub-Agent Delegation** | 2 | ~1,200 | Task, TaskOutput |
| **Web Access** | 2 | ~500 | WebFetch, WebSearch |
| **Mode Control** | 2 | ~200 | EnterPlanMode, ExitPlanMode |
| **Extension** | 2 | ~200 | Skill, KillShell |

*Estimated tokens for tool schema definitions*

### Complete Tool Reference

#### File Operations

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **Read** | Read files with line numbers (`cat -n` format) | `file_path` (required), `offset`, `limit` |
| **Edit** | Exact string replacement in files | `file_path`, `old_string`, `new_string` (required), `replace_all` |
| **Write** | Create or overwrite files | `file_path`, `content` (required) |
| **NotebookEdit** | Edit Jupyter notebook cells | `notebook_path`, `new_source` (required), `cell_id`, `edit_mode` |

**Key Rules:**
- `Read` must be called before `Edit` or `Write` on existing files
- `Edit` fails if `old_string` is not unique — must provide more context
- `Write` overwrites entirely — prefer `Edit` for modifications
- `NotebookEdit` supports replace, insert, and delete modes

#### Search & Navigation

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **Glob** | File pattern matching | `pattern` (required), `path` |
| **Grep** | Content search (ripgrep-based) | `pattern` (required), `path`, `glob`, `output_mode`, context flags |

**Grep output modes:**
- `files_with_matches` (default) — file paths only
- `content` — matching lines with context
- `count` — match counts per file

#### Execution

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **Bash** | Execute shell commands | `command` (required), `timeout`, `description`, `run_in_background` |

**Bash constraints:**
- 120-second default timeout (max 600 seconds)
- Output truncated at 30,000 characters
- `dangerouslyDisableSandbox` flag available but restricted
- Background execution supported via `run_in_background`

#### Task Management

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **TodoWrite** | Structured task list management | `todos` array with `content`, `status`, `activeForm` |
| **AskUserQuestion** | Ask user questions with options | `questions` array with `question`, `header`, `options`, `multiSelect` |

**TodoWrite statuses:** `pending`, `in_progress`, `completed`\
**AskUserQuestion:** 1-4 questions, 2-4 options each, supports preview markdown

#### Sub-Agent Delegation

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **Task** | Launch specialized sub-agents | `description`, `prompt`, `subagent_type` (required), `model`, `resume`, `run_in_background` |
| **TaskOutput** | Retrieve output from background tasks | `task_id` (required), `block`, `timeout` |

#### Web Access

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **WebFetch** | Fetch URL and process with AI | `url`, `prompt` (required) |
| **WebSearch** | Web search with AI processing | `query` (required), `allowed_domains`, `blocked_domains` |

#### Mode Control

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **EnterPlanMode** | Switch to planning mode | No required params |
| **ExitPlanMode** | Signal plan ready for review | No required params |

#### Extension

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **Skill** | Execute slash commands | `skill` (required), `args` |
| **KillShell** | Terminate background shells | `shell_id` (required) |

---

## The `Task` Tool: Sub-Agent Architecture

The most architecturally significant tool. Unlike GitHub Copilot's single `runSubagent`, Claude Code defines **5 specialized agent types** with different capability levels.

### Agent Type Comparison

| Agent Type | Purpose | Tools Available | Tools Removed |
|------------|---------|----------------|---------------|
| **general-purpose** | Complex multi-step tasks | All tools | None |
| **Explore** | Fast codebase exploration | All read/search tools | Task, Edit, Write, NotebookEdit |
| **Plan** | Implementation planning | All read/search tools | Task, Edit, Write, NotebookEdit |
| **claude-code-guide** | Documentation lookup | Glob, Grep, Read, WebFetch, WebSearch | All write/execute tools |
| **statusline-setup** | Config changes | Read, Edit | Everything else |

### Capability Matrix

```
                    Read  Edit  Write  Bash  Glob  Grep  Web  Task  Todo
general-purpose      ✅    ✅    ✅     ✅    ✅    ✅   ✅    ✅    ✅
Explore              ✅    ❌    ❌     ✅    ✅    ✅   ✅    ❌    ✅
Plan                 ✅    ❌    ❌     ✅    ✅    ✅   ✅    ❌    ✅
claude-code-guide    ✅    ❌    ❌     ❌    ✅    ✅   ✅    ❌    ❌
statusline-setup     ✅    ✅    ❌     ❌    ❌    ❌   ❌    ❌    ❌
```

### Key Design Decisions

1. **Principle of Least Privilege:** Each agent type gets only the tools needed for its role
2. **No Recursive Task Spawning:** Explore and Plan agents cannot call `Task` — prevents infinite agent chains
3. **Model Override:** Sub-agents can use different models (`sonnet`/`opus`/`haiku`) for cost optimization
4. **Background Execution:** `run_in_background` enables parallel sub-agent work
5. **Resumability:** Agents can be resumed via ID, preserving their full context

### Throughness Levels (Explore Agent)

The Explore agent supports explicit thoroughness control:

```
"quick"        — basic searches
"medium"       — moderate exploration
"very thorough" — comprehensive analysis across multiple locations and naming conventions
```

### Sub-Agent Invocation Pattern

```json
{
  "type": "tool_use",
  "name": "Task",
  "input": {
    "description": "Find error handling patterns",
    "prompt": "Explore the codebase at /path/to/project and identify all error handling patterns. Look for try/catch blocks, error middleware, and custom error classes.",
    "subagent_type": "Explore",
    "model": "haiku"
  }
}
```

---

## The `Edit` Tool: String Replacement vs Diffs

Claude Code's file editing approach is fundamentally different from GitHub Copilot's:

### Comparison

| Aspect | Claude Code `Edit` | Copilot `apply_patch` |
|--------|-------------------|----------------------|
| **Format** | Exact string match + replace | V4A custom diff format |
| **Granularity** | Any text substring | Line-level with context |
| **Scope markers** | None needed | `@@` class/function markers |
| **Batch edits** | One replacement per call | Multiple regions per patch |
| **Uniqueness** | `old_string` must be unique in file | Context lines disambiguate |
| **replace_all** | Optional flag for global replace | Not applicable |

### Edit Tool Rules

```
- You must Read a file before editing it (enforced)
- old_string must be unique in the file (or use replace_all)
- Preserve exact indentation (tabs/spaces)
- Never include line number prefixes in old_string/new_string
```

**Why string replacement?** It's simpler and less error-prone than diff formats. The model doesn't need to generate correct line numbers, context lines, or scope markers. The trade-off is that each Edit call handles only one replacement, requiring multiple calls for multi-site changes.

---

## Tool Use Instructions Analysis

### Permission Model

Claude Code uses a **hybrid permission model:**

1. **Auto-approved tools:** Read, Glob, Grep, TodoWrite, etc. (always allowed)
2. **Pattern-approved Bash:** `Bash(uv lock:*)`, `Bash(test:*)`, etc. (pre-approved patterns)
3. **User-approved tools:** Write, Edit, Bash (general) — require user confirmation

```
You can use the following tools without requiring user approval:
Bash(uv lock:*), Bash(test:*), Bash(uv run python:*), Bash(lsof:*),
Bash(curl:*), Bash(code --locate-extension-dir:*), Bash(echo:*),
Bash(cat:*), Bash(unset:*), Bash(chmod:*)
```

This is more granular than Copilot's "No need to ask permission before using a tool" — Claude Code distinguishes between safe and potentially dangerous operations.

### Parallelization Rules

```
If you intend to call multiple tools and there are no dependencies between them,
make all independent tool calls in parallel. Maximize use of parallel tool calls
where possible to increase efficiency.
```

**Parallel-safe tools:** Read, Glob, Grep, WebFetch, WebSearch, Task\
**Sequential-required:** Edit (must read first), Write (must read first), Bash (may have side effects)

| Pattern | OK? | Reason |
|---------|-----|--------|
| Read + Read | ✅ | Independent file reads |
| Glob + Grep | ✅ | Independent searches |
| Read → Edit | Sequential | Edit depends on Read |
| Task + Task | ✅ | Independent sub-agents |
| Bash + Bash | Depends | Parallel if independent, sequential if stateful |

### Specialized Tools Over Bash

```
Use specialized tools instead of bash commands when possible:
- Read instead of cat/head/tail
- Edit instead of sed/awk
- Write instead of cat with heredoc or echo redirection
- Glob instead of find or ls
- Grep instead of grep or rg
```

**Why?** Specialized tools provide:
1. Better user experience (structured output)
2. Permission tracking (user can approve/deny)
3. Consistent formatting (line numbers, etc.)
4. Error messages the model understands (e.g., "File has not been read yet")

---

## Tool Error Handling

### Error Responses

When tools fail, results use a special XML format:

```xml
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

Observed error patterns:
- **Write without Read:** "File has not been read yet"
- **Edit non-unique string:** `old_string` not unique in file — provide more context
- **Bash timeout:** Command exceeded timeout limit

### System Reminders in Tool Results

Every tool result is augmented with `<system-reminder>` tags:

```xml
<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware...
</system-reminder>
```

```xml
<system-reminder>
The TodoWrite tool hasn't been used recently...
</system-reminder>
```

These serve as **mid-conversation guardrails** — continuously reinforcing important behaviors without requiring the model to remember from the initial prompt.

---

## Token Cost Analysis

### Tool Schema Overhead

| Tool | Estimated Schema Tokens | Complexity |
|------|------------------------|------------|
| Task | ~800 | High (5 agent types, many params) |
| Bash | ~600 | Medium (multiple params, descriptions) |
| Grep | ~550 | Medium (many search flags) |
| Read | ~400 | Medium (file reading options) |
| Edit | ~350 | Medium (string replacement) |
| AskUserQuestion | ~350 | Medium (questions with options) |
| TodoWrite | ~300 | Medium (todo list management) |
| Write | ~250 | Low (file + content) |
| Glob | ~200 | Low (pattern + path) |
| NotebookEdit | ~200 | Low (cell editing) |
| WebFetch | ~200 | Low (url + prompt) |
| WebSearch | ~200 | Low (query + filters) |
| TaskOutput | ~200 | Low (task_id + options) |
| EnterPlanMode | ~100 | Minimal (no params) |
| ExitPlanMode | ~100 | Minimal (no params) |
| Skill | ~100 | Minimal (skill name) |
| KillShell | ~100 | Minimal (shell_id) |
| **Total** | **~5,000-7,100** | |

### Comparison with GitHub Copilot

| Metric | Claude Code (Agent) | Copilot (Agent) | Ratio |
|--------|-------------------|-----------------|-------|
| Tool count | 17 | 68 | 1:4 |
| Schema tokens | ~7,100 | ~17,585 | 1:2.5 |
| Tokens per tool | ~418 | ~259 | 1.6:1 |
| % of input tokens | ~65% | ~88% | — |

Claude Code uses fewer tools but each tool schema is dramatically more detailed. Where Copilot averages ~20 words per tool description, Claude Code averages ~500 words — embedding entire behavioral protocols (git workflow, task management tutorials, planning decision trees) directly into tool descriptions. Copilot has 4x more tools but many are simple MCP wrappers with minimal schemas. See [agent-mode/tools.md](agent-mode/tools.md) for the full verbatim descriptions.

---

## Design Patterns

### 1. Fewer, More General Tools

```
Claude Code: 17 tools (Read/Edit/Write/Bash cover most operations)
Copilot:     68 tools (dedicated tools for each operation type)
```

Claude Code's approach:
- `Bash` replaces 5+ Copilot terminal tools
- `Edit` replaces Copilot's `apply_patch` + `create_file`
- `Task` replaces `runSubagent` with 5 specialized types
- `Grep` replaces `grep_search` + `semantic_search`

**Trade-off:** Fewer tools = lower token overhead, but each tool must handle more use cases.

### 2. Delegation Over Direct Execution

```
VERY IMPORTANT: When exploring the codebase to gather context, it is CRITICAL that you
use the Task tool with subagent_type=Explore instead of running search commands directly.
```

Claude Code actively pushes work into sub-agents to:
- Reduce main context window pollution
- Enable parallel exploration
- Allow model-flexible execution (use cheaper models for simple searches)

### 3. Read-Before-Write Enforcement

```
You must use your Read tool at least once in the conversation before editing.
This tool will error if you attempt an edit without reading the file.
```

This is **programmatically enforced**, not just suggested:
```xml
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

### 4. Hybrid Permission Model

Three tiers of tool permissions:
1. **Always allowed:** Read, Glob, Grep (safe reads)
2. **Pattern-matched:** `Bash(test:*)`, `Bash(curl:*)` (pre-approved commands)
3. **User-approved:** Write, Edit, general Bash (potentially destructive)

---

## Key Takeaways

1. **Less is more:** 17 well-designed tools outperform 68 narrow tools — lower token cost, simpler mental model
2. **Sub-agents enable least privilege:** 5 agent types with graduated tool access prevent over-privileged delegation
3. **String replacement beats custom diffs:** Simpler edit format reduces model errors vs Copilot's V4A diff
4. **Read-before-write is enforceable:** Programmatic enforcement (error on write without read) is stronger than prompt-only instructions
5. **Dynamic reminders work:** `<system-reminder>` injection keeps behavior on track over long conversations
6. **Hybrid permissions balance safety and speed:** Auto-approve safe operations, require confirmation for risky ones
7. **Tool schemas are expensive:** ~7K tokens per request just for tool definitions — cache them aggressively
