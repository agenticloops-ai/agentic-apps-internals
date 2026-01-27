# Tool Use Analysis: GitHub Copilot Modes

A comprehensive analysis of tool availability, usage patterns, and design decisions across GitHub Copilot's four chat modes.

---

## Tool Distribution Overview

```
Ask Mode      ████████████████████████████████████████  0 tools
Edit Mode     ████████████████████████████████████████  0 tools
Plan Mode     ████████████████████████████████████████  13 tools (read-only)
Agent Mode    ████████████████████████████████████████  68 tools (full access)
```

| Mode | Tools | Read | Write | Execute | Token Cost |
|------|-------|------|-------|---------|------------|
| **Ask** | 0 | ❌ | ❌ | ❌ | ~0 |
| **Edit** | 0 | ❌ | ❌ | ❌ | ~0 |
| **Plan** | 13 | ✅ | ❌ | ❌ | ~2,636 |
| **Agent** | 68 | ✅ | ✅ | ✅ | ~17,585 |

---

## Ask & Edit Modes: Zero Tools

### Why No Tools?

Ask and Edit modes operate as **pure text completion** without tool access. This is intentional:

1. **Simplicity:** Answer questions without API overhead
2. **Speed:** No tool call latency
3. **Cost:** Minimal token usage (~700 tokens total)
4. **Control:** User applies changes manually

### Fallback Behavior

When tools would be needed, these modes use text output:

```
# Edit mode - when files not specified:
"Please add the files to be modified to the working set, or use `#codebase`
in your request to automatically discover working set files."

# Ask mode - code suggestions:
````python
# filepath: /path/to/file.py
# ...existing code...
def new_function():
    pass
````
```

---

## Plan Mode: 13 Read-Only Tools

### Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| **Search** | 4 | Find files and code |
| **Read** | 3 | Read files and directories |
| **Analysis** | 3 | Errors, diffs, usages |
| **External** | 2 | Web, GitHub repos |
| **Delegation** | 1 | Sub-agent |

### Complete Tool List

| Tool | Description | Use Case |
|------|-------------|----------|
| `file_search` | Glob pattern search | Find files by name pattern |
| `grep_search` | Text/regex search | Find code by content |
| `semantic_search` | Natural language search | Find code by meaning |
| `list_dir` | List directory contents | Explore structure |
| `read_file` | Read file contents | Understand implementation |
| `list_code_usages` | Find symbol references | Impact analysis |
| `get_changed_files` | Git diffs | Understand recent changes |
| `get_errors` | Compile/lint errors | Identify issues |
| `get_search_view_results` | VS Code search results | Use existing searches |
| `test_failure` | Test failure info | Debug failing tests |
| `fetch_webpage` | Fetch web content | Research documentation |
| `github_repo` | Search GitHub repos | Find external examples |
| `runSubagent` | Launch sub-agent | Deep research tasks |

### Why Read-Only?

Plan mode is explicitly a **PLANNING AGENT**:

```
You are a PLANNING AGENT, NOT an implementation agent.

<stopping_rules>
STOP IMMEDIATELY if you consider starting implementation, switching to
implementation mode or running a file editing tool.
</stopping_rules>
```

Read-only tools allow:
- ✅ Research codebase structure
- ✅ Understand existing patterns
- ✅ Identify files to modify
- ❌ Make any changes
- ❌ Execute commands

### Search Strategy

Plan mode uses a **hierarchical search approach**:

```
1. semantic_search  → Find relevant areas by meaning
2. file_search      → Narrow down to specific files
3. grep_search      → Find exact code patterns
4. read_file        → Read full implementation
```

**Prompt guidance:**
```
Research the user's task comprehensively using read-only tools.
Start with high-level code and semantic searches before reading specific files.
Stop research when you reach 80% confidence you have enough context.
```

---

## Agent Mode: 68 Full-Access Tools

### Tool Categories

| Category | Count | Token Cost | Purpose |
|----------|-------|------------|---------|
| **Core** | 35 | ~12,000 | Essential operations |
| **Notebook** | 3 | ~800 | Jupyter support |
| **Python Env** | 4 | ~600 | Python configuration |
| **MCP: Docker** | 6 | ~1,200 | Container management |
| **MCP: GitKraken Git** | 10 | ~1,500 | Git operations |
| **MCP: GitKraken Issues** | 3 | ~500 | Issue tracking |
| **MCP: GitKraken PRs** | 6 | ~1,200 | Pull requests |
| **MCP: Pylance** | 9 | ~1,000 | Python tooling |

### Core Tools (35)

#### File Operations
| Tool | Description |
|------|-------------|
| `read_file` | Read file contents (truncates at 2000 lines) |
| `create_file` | Create new file with content |
| `apply_patch` | Edit files using V4A diff format |
| `create_directory` | Create directory structure |
| `list_dir` | List directory contents |

#### Search & Navigation
| Tool | Description |
|------|-------------|
| `file_search` | Search files by glob pattern |
| `grep_search` | Text/regex search in workspace |
| `semantic_search` | Natural language code search |
| `list_code_usages` | Find all symbol references |
| `get_search_view_results` | Get VS Code search results |

#### Terminal & Execution
| Tool | Description |
|------|-------------|
| `run_in_terminal` | Execute shell commands |
| `get_terminal_output` | Get output from terminal |
| `terminal_last_command` | Get last terminal command |
| `terminal_selection` | Get terminal selection |
| `runTests` | Run unit tests with coverage |

#### Git & Version Control
| Tool | Description |
|------|-------------|
| `get_changed_files` | Get git diffs |

#### Error & Diagnostics
| Tool | Description |
|------|-------------|
| `get_errors` | Get compile/lint errors |
| `test_failure` | Get test failure info |

#### Workspace & Project
| Tool | Description |
|------|-------------|
| `create_new_workspace` | Full project scaffolding |
| `get_project_setup_info` | Get project setup by type |
| `create_and_run_task` | Create/run VS Code tasks |
| `manage_todo_list` | Track tasks and progress |

#### VS Code Integration
| Tool | Description |
|------|-------------|
| `run_vscode_command` | Run VS Code command |
| `install_extension` | Install VS Code extension |
| `vscode_searchExtensions_internal` | Search marketplace |
| `get_vscode_api` | VS Code API docs |
| `open_simple_browser` | Preview URL in browser |

#### Notebooks
| Tool | Description |
|------|-------------|
| `create_new_jupyter_notebook` | Create new notebook |
| `edit_notebook_file` | Edit notebook cells |
| `run_notebook_cell` | Execute notebook cell |
| `read_notebook_cell_output` | Get cell output |
| `copilot_getNotebookSummary` | Get notebook summary |

#### External
| Tool | Description |
|------|-------------|
| `fetch_webpage` | Fetch web page content |
| `github_repo` | Search GitHub repos |

#### Delegation
| Tool | Description |
|------|-------------|
| `runSubagent` | Launch autonomous sub-agent |

### MCP Tools (33)

#### Docker/Container (6)
| Tool | Description |
|------|-------------|
| `activate_container_management_tools` | Enable start/stop/restart/remove |
| `activate_image_management_tools` | Enable pull/remove/inspect/tag |
| `activate_container_inspection_and_logging_tools` | Enable inspect/logs |
| `activate_listing_tools_for_containers_images_and_volumes` | Enable listing |
| `mcp_copilot_conta_list_networks` | List container networks |
| `mcp_copilot_conta_prune` | Prune unused resources |

#### GitKraken Git (10)
| Tool | Description |
|------|-------------|
| `mcp_gitkraken_git_add_or_commit` | Git add or commit |
| `mcp_gitkraken_git_blame` | Show git blame |
| `mcp_gitkraken_git_branch` | List/create branches |
| `mcp_gitkraken_git_checkout` | Switch branches |
| `mcp_gitkraken_git_log_or_diff` | Show logs or diffs |
| `mcp_gitkraken_git_push` | Push to remote |
| `mcp_gitkraken_git_stash` | Stash changes |
| `mcp_gitkraken_git_status` | Show working tree status |
| `mcp_gitkraken_git_worktree` | Manage worktrees |
| `mcp_gitkraken_gitkraken_workspace_list` | List workspaces |

#### GitKraken Issues (3)
| Tool | Description |
|------|-------------|
| `mcp_gitkraken_issues_add_comment` | Add issue comment |
| `mcp_gitkraken_issues_assigned_to_me` | Get assigned issues |
| `mcp_gitkraken_issues_get_detail` | Get issue details |

#### GitKraken Pull Requests (6)
| Tool | Description |
|------|-------------|
| `mcp_gitkraken_pull_request_assigned_to_me` | Get assigned PRs |
| `mcp_gitkraken_pull_request_create` | Create new PR |
| `mcp_gitkraken_pull_request_create_review` | Create PR review |
| `mcp_gitkraken_pull_request_get_comments` | Get PR comments |
| `mcp_gitkraken_pull_request_get_detail` | Get PR details |
| `mcp_gitkraken_repository_get_file_content` | Get file from repo |

#### Pylance Python (9)
| Tool | Description |
|------|-------------|
| `activate_python_code_validation_and_execution` | Enable validation |
| `activate_import_analysis_and_dependency_management` | Enable import analysis |
| `activate_python_environment_management` | Enable env management |
| `activate_workspace_structure_and_file_management` | Enable structure tools |
| `mcp_pylance_mcp_s_pylanceDocuments` | Search Pylance docs |
| `mcp_pylance_mcp_s_pylanceInvokeRefactoring` | Apply refactoring |
| `mcp_pylance_mcp_s_pylanceRunCodeSnippet` | Execute Python code |
| `mcp_pylance_mcp_s_pylanceSyntaxErrors` | Validate syntax |
| `mcp_pylance_mcp_s_pylanceFileSyntaxErrors` | Check file syntax |

---

## Tool Use Instructions Analysis

### Permission Model

```
No need to ask permission before using a tool.
```

**Why:** Reduces latency by eliminating confirmation dialogs.

### Tool Name Abstraction

```
NEVER say the name of a tool to a user. For example, instead of saying
that you'll use the run_in_terminal tool, say "I'll run the command in a terminal".
```

**Why:** Better UX - users don't need to know internal tool names.

### Parallelization Rules

```
If you think running multiple tools can answer the user's question,
prefer calling them in parallel whenever possible, but do not call
semantic_search in parallel.

Don't call the run_in_terminal tool multiple times in parallel.
Instead, run one command and wait for the output before running the next command.
```

| Tool Type | Parallel OK? | Reason |
|-----------|--------------|--------|
| `file_search` | ✅ | Independent queries |
| `grep_search` | ✅ | Independent queries |
| `read_file` | ✅ | Independent reads |
| `semantic_search` | ❌ | Resource intensive |
| `run_in_terminal` | ❌ | Sequential dependencies |

### Efficiency Patterns

```
When reading files, prefer reading large meaningful chunks rather than
consecutive small sections to minimize tool calls and gain better context.

You can use the grep_search to get an overview of a file by searching
for a string within that one file, instead of using read_file many times.

You don't need to read a file if it's already provided in context.
```

**Optimization Strategy:**
1. Check context first (avoid redundant reads)
2. Use grep for targeted searches
3. Batch reads over sequential reads
4. Read large chunks for better context

### Error Handling

```
Do not loop more than 3 times attempting to fix errors in the same file.
If the third try fails, you should stop and ask the user what to do next.
```

**Why:** Prevents infinite retry loops on unfixable errors.

### Tool Availability Awareness

```
Tools can be disabled by the user. You may see tools used previously in
the conversation that are not currently available. Be careful to only
use the tools that are currently available to you.
```

**Why:** Users can disable dangerous tools; agent must handle gracefully.

---

## The `apply_patch` Tool: Deep Dive

Agent mode uses a custom diff format called **V4A** for file edits:

### Format Structure

```
*** Begin Patch
*** Update File: [file_path]
@@ class ClassName
@@   def method_name():
[3 lines of pre-context]
-[old_code]
+[new_code]
[3 lines of post-context]
*** End Patch
```

### Key Rules

| Rule | Description |
|------|-------------|
| **Context lines** | 3 lines before and after each change |
| **@@ operator** | Indicates class/function scope when context insufficient |
| **Multiple @@** | Can chain for deeply nested code |
| **Indentation** | Must match original (tabs vs spaces) |
| **Multiple regions** | Repeat `*** Update File:` header |

### Why Custom Format?

1. **Unambiguous:** No confusion with unified diff
2. **Scope markers:** `@@` helps locate code in large files
3. **IDE integration:** VS Code can parse and apply reliably
4. **Error recovery:** "If you have issues, try to fix your patch"

---

## The `runSubagent` Tool: Recursive Agents

Both Plan and Agent modes can spawn sub-agents:

```json
{
  "name": "runSubagent",
  "parameters": {
    "prompt": "Detailed task description",
    "description": "3-5 word summary"
  }
}
```

### Characteristics

- **Stateless:** Each invocation starts fresh
- **Synchronous:** Caller waits for result
- **Autonomous:** Sub-agent works without user feedback
- **Single response:** Returns one final message

### Use Cases

| Mode | Sub-agent Use |
|------|---------------|
| **Plan** | Deep research before planning |
| **Agent** | Complex multi-step research tasks |

### Prompt Guidance

```
Each agent invocation is stateless. You will not be able to send additional
messages to the agent. Therefore, your prompt should contain a highly detailed
task description for the agent to perform autonomously.
```

---

## Token Cost Analysis

### Tool Schema Overhead

| Mode | Tool Count | Schema Tokens | % of Total Input |
|------|------------|---------------|------------------|
| Ask | 0 | 0 | 0% |
| Edit | 0 | 0 | 0% |
| Plan | 13 | ~2,636 | 54% |
| Agent | 68 | ~17,585 | 88% |

### Per-Tool Token Cost (Estimates)

| Tool Type | Avg Tokens | Notes |
|-----------|------------|-------|
| Simple (no params) | ~50 | `test_failure`, `get_errors` |
| Medium (few params) | ~150 | `read_file`, `grep_search` |
| Complex (many params) | ~300 | `apply_patch`, MCP tools |
| With enum values | ~400+ | Docker activation tools |

### Optimization Strategies

1. **Tool pruning:** Remove unused tools to reduce overhead
2. **Lazy loading:** Only include tools when needed
3. **Tool groups:** MCP "activation" tools load others on demand
4. **Mode selection:** Use Ask/Edit when tools aren't needed

---

## Design Patterns

### 1. Progressive Disclosure

```
Ask (0 tools) → Edit (0 tools) → Plan (13 read-only) → Agent (68 full)
```

Each mode adds capabilities incrementally.

### 2. Activation Tools

Docker MCP uses "activation" tools that enable other tools:

```
activate_container_management_tools → enables start, stop, restart, remove
activate_image_management_tools    → enables pull, remove, inspect, tag
```

**Why:** Reduces initial token overhead by loading tools on demand.

### 3. Tool Abstraction

User-facing language hides tool names:
- "I'll run the command" not "I'll use run_in_terminal"
- "Let me search" not "I'll call grep_search"

### 4. Graceful Degradation

When tools unavailable:
```
You don't currently have any tools available for editing files. If the user
asks you to edit a file, you can ask the user to enable editing tools or
print a codeblock with the suggested changes.
```

---

## Key Takeaways

1. **Tools have significant token cost:** 68 tools = ~17.5K tokens per request
2. **Read-only tools enable safe exploration:** Plan mode can research without risk
3. **Parallelization improves speed:** But some tools must run sequentially
4. **Custom formats aid reliability:** V4A diff format is unambiguous
5. **Sub-agents enable recursion:** Complex tasks can spawn helper agents
6. **Activation patterns reduce overhead:** Load tools only when needed
7. **Graceful fallbacks are essential:** Handle missing tools elegantly
