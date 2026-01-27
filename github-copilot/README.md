# GitHub Copilot Chat Modes - Internal Analysis

This repository contains captured API requests and responses from GitHub Copilot's different chat modes in VS Code, revealing the system prompts, tools, and architectures used.

**Model:** GPT-4.1\
**Captured:** November 23, 2025\
**Test Task:** "Create calculator in Python, make sure it works, and write README"

---

## Modes Overview

| Mode | Tools | Purpose | Can Edit | Can Execute |
|------|-------|---------|----------|-------------|
| **Ask** | 0 | Answer questions, provide code samples | ❌ | ❌ |
| **Edit** | 0 | Suggest file changes (IDE applies them) | ❌ (suggests) | ❌ |
| **Plan** | 13 | Research codebase & create implementation plans | ❌ | ❌ |
| **Agent** | 68 | Full autonomous implementation | ✅ | ✅ |

---

## Mode Details

### 1. Ask Mode (`/ask`)

**Purpose:** Simple Q&A and code generation without tools.

**Characteristics:**
- No tool access - purely text completion
- Uses 4-backtick code blocks with `// filepath:` comments
- Lists capabilities in system prompt (explain code, generate tests, etc.)
- Relies on user to apply any code suggestions

**System Prompt Key Points:**
- "Keep your answers short and impersonal"
- Uses 4 backticks for code blocks
- Includes `// ...existing code...` markers for partial edits
- Aware of VS Code IDE context

**Files:** [`ask/`](ask/)

---

### 2. Edit Mode (`/edit`)

**Purpose:** Structured code change suggestions for IDE to apply.

**Characteristics:**
- No tool access - text completion only
- Strict output format with file headers and code blocks
- Requires user to specify files or use `#codebase`
- IDE parses response and applies changes

**System Prompt Key Points:**
- "Group your changes by file. Use the file path as the header."
- "The user is very smart and can understand how to merge your code blocks"
- "Avoid repeating existing code, instead use comments to represent regions"
- Refuses if files not specified: "Please add the files to be modified to the working set"

**Output Format:**
`````markdown
### /path/to/file.py

Summary of changes.

````python
# filepath: /path/to/file.py
# ...existing code...
{ changed code }
# ...existing code...
````
`````

**Files:** [`edit/`](edit/)

---

### 3. Plan Mode (`/plan`)

**Purpose:** Research codebase and create detailed implementation plans without making changes.

**Characteristics:**
- 13 read-only tools for exploration
- Explicit "PLANNING AGENT, NOT implementation agent" identity
- Uses `runSubagent` for deep research
- Outputs structured markdown plans

**System Prompt Key Points:**
- "STOP IMMEDIATELY if you consider starting implementation"
- "Plans describe steps for the USER or another agent to execute later"
- Research until "80% confidence you have enough context"
- Strict plan template with Steps and Further Considerations

**Tools Available (13):**

| Tool | Description |
|------|-------------|
| `fetch_webpage` | Fetch web page content |
| `file_search` | Search files by glob pattern |
| `grep_search` | Text/regex search in workspace |
| `get_changed_files` | Git diffs |
| `get_errors` | Compile/lint errors |
| `get_search_view_results` | Search view results |
| `github_repo` | Search GitHub repositories |
| `list_code_usages` | Find symbol usages |
| `list_dir` | List directory contents |
| `read_file` | Read file contents |
| `semantic_search` | Natural language code search |
| `test_failure` | Test failure info |
| `runSubagent` | Launch sub-agent for research |

**Files:** [`plan/`](plan/)

---

### 4. Agent Mode (`/agent`)

**Purpose:** Full autonomous coding agent with file editing, terminal execution, and MCP integrations.

**Characteristics:**
- 68 tools (35 core + 33 MCP/extension)
- Can create/edit files, run terminal commands, execute tests
- Uses `apply_patch` with V4A diff format for edits
- Integrates with GitKraken, Pylance, Docker via MCP
- Has `manage_todo_list` for task tracking

**System Prompt Key Points:**
- "NEVER print out a codeblock with file changes unless the user asked for it. Use the appropriate edit tool instead."
- "NEVER print out a codeblock with a terminal command to run unless the user asked for it. Use the run_in_terminal tool instead."
- "It's YOUR RESPONSIBILITY to make sure that you have done all you can to collect necessary context."
- Uses `apply_patch` tool with custom V4A diff format

**Tool Categories:**

| Category | Count | Examples |
|----------|-------|----------|
| Core Tools | 35 | `apply_patch`, `create_file`, `run_in_terminal`, `runTests` |
| Notebook Tools | 3 | `configure_notebook`, `run_notebook_cell` |
| Python Environment | 4 | `configure_python_environment`, `install_python_packages` |
| MCP: Docker | 6 | `mcp_copilot_conta_prune`, container management |
| MCP: GitKraken Git | 10 | `git_add_or_commit`, `git_push`, `git_branch` |
| MCP: GitKraken Issues | 3 | `issues_assigned_to_me`, `issues_add_comment` |
| MCP: GitKraken PRs | 6 | `pull_request_create`, `pull_request_create_review` |
| MCP: Pylance | 9 | `pylanceRunCodeSnippet`, `pylanceInvokeRefactoring` |

**Files:** [`agent/`](agent/)

---

## Architecture Insights

### Prompt Structure

All modes follow a similar message structure:

```
1. System Message (role: system)
   - Identity ("GitHub Copilot")
   - Content policies
   - Mode-specific instructions
   - Output formatting rules

2. User Context Message (role: user)
   - <environment_info> - OS, shell
   - <workspace_info> - folders, structure

3. User Request Message (role: user)
   - <context> - date, terminals
   - <reminderInstructions>
   - <userRequest> - actual prompt
```

### Key Differences

| Aspect | Ask/Edit | Plan | Agent |
|--------|----------|------|-------|
| Identity | "AI programming assistant" | "PLANNING AGENT" | "automated coding agent" |
| Tool Access | None | Read-only (13) | Full (68) |
| Output | Text + code blocks | Markdown plan | Tool calls |
| File Changes | User applies | Never | Via `apply_patch` |
| Execution | Never | Never | Via `run_in_terminal` |

### MCP (Model Context Protocol) Integration

Agent mode includes MCP tools from:
- **GitKraken** - Git operations, issues, PRs across GitHub/GitLab/Bitbucket/Azure
- **Pylance** - Python code execution, validation, refactoring
- **Docker** - Container management (via activation tools)

MCP tools use `mcp_` prefix naming convention.

---

## API Configuration

All modes use:
- **Model:** `gpt-4.1` (displayed as "GPT-4.1 (Proxy)")
- **Temperature:** 0.1
- **Top P:** 1
- **Streaming:** Enabled

---

## Token Usage Analysis

Estimated token consumption per mode (for the same "create calculator" task):

| Mode | System Prompt | User Input | Tools Schema | **Total Input** | Response | Duration |
|------|---------------|------------|--------------|-----------------|----------|----------|
| **Ask** | ~700 | ~20 | 0 | **~720** | 1,923 chars | 6.0s |
| **Edit** | ~600 | ~135 | 0 | **~735** | 2,096 chars | 6.3s |
| **Plan** | ~2,040 | ~190 | ~2,636 | **~4,865** | 812 chars | 7.0s |
| **Agent** | ~2,180 | ~270 | ~17,585 | **~20,035** | (tool calls) | 18.9s |

*Token estimates based on ~4 characters per token*

### Key Insights

1. **Tools Schema Dominates Agent Mode:** The 68 tools contribute ~17.5K tokens (~88% of input) in Agent mode
2. **Plan vs Agent:** Plan mode uses ~4.8K tokens vs Agent's ~20K - a 4x difference primarily from tools
3. **Ask/Edit are Lightweight:** Without tools, these modes use under 1K tokens total
4. **Response Efficiency:** Plan mode produces concise 812-char plans; Ask/Edit generate ~2K chars of code

### Cost Implications

For GPT-4.1 pricing (hypothetical $10/1M input, $30/1M output):
- **Ask/Edit:** ~$0.007 per request
- **Plan:** ~$0.05 per request
- **Agent:** ~$0.20+ per request (multi-turn)

Agent mode's high token count explains why it's the most expensive but most capable mode.

---

## Observations

1. **Progressive Capability Model:** Modes are designed with increasing autonomy - Ask (no tools) → Edit (suggestions) → Plan (read-only tools) → Agent (full tools)

2. **Safety Controls:** Each mode has explicit boundaries:
   - Ask/Edit: Cannot execute anything
   - Plan: "STOP IMMEDIATELY if you consider starting implementation"
   - Agent: Has tools but explicit rules about when to use them

3. **Structured Output:** All modes use consistent code block formatting (4 backticks, filepath comments, `...existing code...` markers)

4. **MCP Integration:** Agent mode extends capabilities through MCP protocol, allowing VS Code extensions to provide additional tools

5. **Sub-agent Pattern:** Both Plan and Agent modes can spawn `runSubagent` for complex research tasks, showing a recursive agent architecture

---

## Deep Dive Guides

For detailed analysis, see:

- **[PROMPT-ENGINEERING.md](PROMPT-ENGINEERING.md)** - System prompt building blocks, best practices, and templates
- **[TOOL-USE.md](TOOL-USE.md)** - Complete tool analysis across all modes, parallelization rules, token costs

---

## License

This analysis is for educational and research purposes. GitHub Copilot is a product of GitHub/Microsoft.
