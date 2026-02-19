# Agent Mode - Tool Definitions

17 tools available in Agent mode. Each includes the **full verbatim description** as sent in the API request.

> **Key differentiator:** Claude Code's tool descriptions are dramatically more detailed than GitHub Copilot's. Where Copilot's tool descriptions average 1-3 sentences, Claude Code embeds **entire behavioral protocols** into tool descriptions — the `Bash` tool alone contains the full git commit workflow, PR creation protocol, and command hygiene rules. The `TodoWrite` tool includes 8 worked examples with reasoning. This means a significant portion of Claude Code's "system prompt" is actually distributed across tool descriptions, not concentrated in the system message.

| Metric | Claude Code | GitHub Copilot |
|--------|------------|----------------|
| Avg description length | ~500 words | ~20 words |
| Longest tool description | `Bash` (~1,800 words) | `apply_patch` (~200 words) |
| Embedded examples | Yes (Task, TodoWrite, Bash, EnterPlanMode) | Rarely |
| Behavioral rules in tools | Git protocol, PR workflow, permission model | Minimal |
| Cross-references between tools | Frequent ("use Read instead of cat") | None |

---

## 1. Task

> Launch a new agent to handle complex, multi-step tasks autonomously.
>
> The Task tool launches specialized agents (subprocesses) that autonomously handle complex tasks. Each agent type has specific capabilities and tools available to it.
>
> Available agent types and the tools they have access to:
> - general-purpose: General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks. When you are searching for a keyword or file and are not confident that you will find the right match in the first few tries use this agent to perform the search for you. (Tools: \*)
> - statusline-setup: Use this agent to configure the user's Claude Code status line setting. (Tools: Read, Edit)
> - Explore: Fast agent specialized for exploring codebases. Use this when you need to quickly find files by patterns (eg. "src/components/\*\*/\*.tsx"), search code for keywords (eg. "API endpoints"), or answer questions about the codebase (eg. "how do API endpoints work?"). When calling this agent, specify the desired thoroughness level: "quick" for basic searches, "medium" for moderate exploration, or "very thorough" for comprehensive analysis across multiple locations and naming conventions. (Tools: All tools)
> - Plan: Software architect agent for designing implementation plans. Use this when you need to plan the implementation strategy for a task. Returns step-by-step plans, identifies critical files, and considers architectural trade-offs. (Tools: All tools)
> - claude-code-guide: Use this agent when the user asks questions ("Can Claude...", "Does Claude...", "How do I...") about: (1) Claude Code (the CLI tool) - features, hooks, slash commands, MCP servers, settings, IDE integrations, keyboard shortcuts; (2) Claude Agent SDK - building custom agents; (3) Claude API (formerly Anthropic API) - API usage, tool use, Anthropic SDK usage. **IMPORTANT:** Before spawning a new agent, check if there is already a running or recently completed claude-code-guide agent that you can resume using the "resume" parameter. (Tools: Glob, Grep, Read, WebFetch, WebSearch)
>
> When using the Task tool, you must specify a subagent_type parameter to select which agent type to use.
>
> When NOT to use the Task tool:
> - If you want to read a specific file path, use the Read or Glob tool instead of the Task tool, to find the match more quickly
> - If you are searching for a specific class definition like "class Foo", use the Glob tool instead, to find the match more quickly
> - If you are searching for code within a specific file or set of 2-3 files, use the Read tool instead of the Task tool, to find the match more quickly
> - Other tasks that are not related to the agent descriptions above
>
> Usage notes:
> - Always include a short description (3-5 words) summarizing what the agent will do
> - Launch multiple agents concurrently whenever possible, to maximize performance; to do that, use a single message with multiple tool uses
> - When the agent is done, it will return a single message back to you. The result returned by the agent is not visible to the user. To show the user the result, you should send a text message back to the user with a concise summary of the result.
> - You can optionally run agents in the background using the run_in_background parameter. When an agent runs in the background, you will need to use TaskOutput to retrieve its results once it's done. You can continue to work while background agents run.
> - Agents can be resumed using the `resume` parameter by passing the agent ID from a previous invocation. When resumed, the agent continues with its full previous context preserved. When NOT resuming, each invocation starts fresh and you should provide a detailed task description with all necessary context.
> - When the agent is done, it will return a single message back to you along with its agent ID. You can use this ID to resume the agent later if needed for follow-up work.
> - Provide clear, detailed prompts so the agent can work autonomously and return exactly the information you need.
> - Agents with "access to current context" can see the full conversation history before the tool call.
> - The agent's outputs should generally be trusted
> - Clearly tell the agent whether you expect it to write code or just to do research (search, file reads, web fetches, etc.), since it is not aware of the user's intent
> - If the agent description mentions that it should be used proactively, then you should try your best to use it without the user having to ask for it first. Use your judgement.
> - If the user specifies that they want you to run agents "in parallel", you MUST send a single message with multiple Task tool use content blocks.

```json
{
  "name": "Task",
  "input_schema": {
    "type": "object",
    "required": ["description", "prompt", "subagent_type"],
    "properties": {
      "description": {"type": "string", "description": "A short (3-5 word) description of the task"},
      "prompt": {"type": "string", "description": "The task for the agent to perform"},
      "subagent_type": {"type": "string", "description": "The type of specialized agent to use for this task"},
      "model": {"type": "string", "enum": ["sonnet", "opus", "haiku"], "description": "Optional model to use. Prefer haiku for quick tasks to minimize cost."},
      "resume": {"type": "string", "description": "Optional agent ID to resume from"},
      "run_in_background": {"type": "boolean", "description": "Set to true to run in background. Use TaskOutput to read output later."}
    }
  }
}
```

---

## 2. TaskOutput

> - Retrieves output from a running or completed task (background shell, agent, or remote session)
> - Takes a task_id parameter identifying the task
> - Returns the task output along with status information
> - Use block=true (default) to wait for task completion
> - Use block=false for non-blocking check of current status
> - Task IDs can be found using the /tasks command
> - Works with all task types: background shells, async agents, and remote sessions

```json
{
  "name": "TaskOutput",
  "input_schema": {
    "type": "object",
    "required": ["task_id"],
    "properties": {
      "task_id": {"type": "string", "description": "The task ID to get output from"},
      "block": {"type": "boolean", "default": true, "description": "Whether to wait for completion"},
      "timeout": {"type": "number", "default": 30000, "maximum": 600000, "description": "Max wait time in ms"}
    }
  }
}
```

---

## 3. Bash

The longest tool description in the entire toolkit (~1,800 words). Embeds the full **git commit protocol**, **PR creation workflow**, and **command hygiene rules** directly in the tool description.

> Executes a given bash command in a persistent shell session with optional timeout, ensuring proper handling and security measures.
>
> IMPORTANT: This tool is for terminal operations like git, npm, docker, etc. DO NOT use it for file operations (reading, writing, editing, searching, finding files) - use the specialized tools for this instead.
>
> Before executing the command, please follow these steps:
>
> 1. Directory Verification:
>    - If the command will create new directories or files, first use `ls` to verify the parent directory exists and is the correct location
>    - For example, before running "mkdir foo/bar", first use `ls foo` to check that "foo" exists and is the intended parent directory
>
> 2. Command Execution:
>    - Always quote file paths that contain spaces with double quotes (e.g., cd "path with spaces/file.txt")
>    - After ensuring proper quoting, execute the command.
>    - Capture the output of the command.
>
> Usage notes:
>   - The command argument is required.
>   - You can specify an optional timeout in milliseconds (up to 600000ms / 10 minutes). If not specified, commands will timeout after 120000ms (2 minutes).
>   - It is very helpful if you write a clear, concise description of what this command does in 5-10 words.
>   - If the output exceeds 30000 characters, output will be truncated before being returned to you.
>   - You can use the `run_in_background` parameter to run the command in the background.
>   - Avoid using Bash with the `find`, `grep`, `cat`, `head`, `tail`, `sed`, `awk`, or `echo` commands, unless explicitly instructed. Instead, always prefer using the dedicated tools:
>     - File search: Use Glob (NOT find or ls)
>     - Content search: Use Grep (NOT grep or rg)
>     - Read files: Use Read (NOT cat/head/tail)
>     - Edit files: Use Edit (NOT sed/awk)
>     - Write files: Use Write (NOT echo >/cat <<EOF)
>     - Communication: Output text directly (NOT echo/printf)
>   - When issuing multiple commands:
>     - If independent and can run in parallel, make multiple Bash tool calls in a single message.
>     - If dependent and must run sequentially, use a single Bash call with '&&' to chain them.
>     - Use ';' only when you need to run commands sequentially but don't care if earlier commands fail
>     - DO NOT use newlines to separate commands
>   - Try to maintain your current working directory throughout the session by using absolute paths.
>
> **# Committing changes with git**
>
> Only create commits when requested by the user. If unclear, ask first.
>
> Git Safety Protocol:
> - NEVER update the git config
> - NEVER run destructive/irreversible git commands (like push --force, hard reset, etc) unless the user explicitly requests them
> - NEVER skip hooks (--no-verify, --no-gpg-sign, etc) unless the user explicitly requests it
> - NEVER run force push to main/master, warn the user if they request it
> - Avoid git commit --amend. ONLY use --amend when ALL conditions are met:
>   (1) User explicitly requested amend, OR commit SUCCEEDED but pre-commit hook auto-modified files
>   (2) HEAD commit was created by you in this conversation
>   (3) Commit has NOT been pushed to remote
> - CRITICAL: If commit FAILED or was REJECTED by hook, NEVER amend - fix the issue and create a NEW commit
> - NEVER commit changes unless the user explicitly asks you to.
>
> Steps:
> 1. Run git status + git diff + git log in parallel
> 2. Analyze changes, draft commit message (focus on "why" not "what")
> 3. Add files + create commit with Co-Authored-By trailer + verify with git status
> 4. If pre-commit hook fails, fix issue and create NEW commit
>
> **# Creating pull requests**
>
> Use the gh command for ALL GitHub-related tasks.
> 1. Run git status + git diff + git log + git diff [base]...HEAD in parallel
> 2. Analyze ALL commits in PR, draft title and summary
> 3. Create branch if needed + push with -u + create PR via gh pr create
>
> **# Other common operations**
> - View comments on a Github PR: gh api repos/foo/bar/pulls/123/comments

```json
{
  "name": "Bash",
  "input_schema": {
    "type": "object",
    "required": ["command"],
    "properties": {
      "command": {"type": "string", "description": "The command to execute"},
      "timeout": {"type": "number", "description": "Optional timeout in milliseconds (max 600000)"},
      "description": {"type": "string", "description": "Clear, concise description of what this command does in 5-10 words, in active voice."},
      "run_in_background": {"type": "boolean", "description": "Run in background. Use TaskOutput to read output later."},
      "dangerouslyDisableSandbox": {"type": "boolean", "description": "Override sandbox mode and run without sandboxing."}
    }
  }
}
```

---

## 4. Glob

> - Fast file pattern matching tool that works with any codebase size
> - Supports glob patterns like "\*\*/\*.js" or "src/\*\*/\*.ts"
> - Returns matching file paths sorted by modification time
> - Use this tool when you need to find files by name patterns
> - When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead
> - You can call multiple tools in a single response. It is always better to speculatively perform multiple searches in parallel if they are potentially useful.

```json
{
  "name": "Glob",
  "input_schema": {
    "type": "object",
    "required": ["pattern"],
    "properties": {
      "pattern": {"type": "string", "description": "The glob pattern to match files against"},
      "path": {"type": "string", "description": "The directory to search in. Omit for default. DO NOT enter \"undefined\" or \"null\"."}
    }
  }
}
```

---

## 5. Grep

> A powerful search tool built on ripgrep
>
> Usage:
> - ALWAYS use Grep for search tasks. NEVER invoke `grep` or `rg` as a Bash command. The Grep tool has been optimized for correct permissions and access.
> - Supports full regex syntax (e.g., "log.\*Error", "function\\s+\\w+")
> - Filter files with glob parameter (e.g., "\*.js", "\*\*/\*.tsx") or type parameter (e.g., "js", "py", "rust")
> - Output modes: "content" shows matching lines, "files_with_matches" shows only file paths (default), "count" shows match counts
> - Use Task tool for open-ended searches requiring multiple rounds
> - Pattern syntax: Uses ripgrep (not grep) - literal braces need escaping
> - Multiline matching: By default patterns match within single lines only. For cross-line patterns, use `multiline: true`

```json
{
  "name": "Grep",
  "input_schema": {
    "type": "object",
    "required": ["pattern"],
    "properties": {
      "pattern": {"type": "string", "description": "The regular expression pattern to search for"},
      "path": {"type": "string", "description": "File or directory to search in. Defaults to cwd."},
      "glob": {"type": "string", "description": "Glob pattern to filter files (e.g. \"*.js\")"},
      "type": {"type": "string", "description": "File type to search (e.g. js, py, rust)"},
      "output_mode": {"type": "string", "enum": ["content", "files_with_matches", "count"]},
      "-B": {"type": "number", "description": "Lines to show before each match"},
      "-A": {"type": "number", "description": "Lines to show after each match"},
      "-C": {"type": "number", "description": "Context lines before and after each match"},
      "-n": {"type": "boolean", "description": "Show line numbers. Defaults to true."},
      "-i": {"type": "boolean", "description": "Case insensitive search"},
      "head_limit": {"type": "number", "description": "Limit output to first N entries"},
      "offset": {"type": "number", "description": "Skip first N entries before applying head_limit"},
      "multiline": {"type": "boolean", "description": "Enable multiline mode (rg -U --multiline-dotall)"}
    }
  }
}
```

---

## 6. Read

> Reads a file from the local filesystem. You can access any file directly by using this tool.
> Assume this tool is able to read all files on the machine. If the User provides a path to a file assume that path is valid. It is okay to read a file that does not exist; an error will be returned.
>
> Usage:
> - The file_path parameter must be an absolute path, not a relative path
> - By default, it reads up to 2000 lines starting from the beginning of the file
> - You can optionally specify a line offset and limit (especially handy for long files), but it's recommended to read the whole file by not providing these parameters
> - Any lines longer than 2000 characters will be truncated
> - Results are returned using cat -n format, with line numbers starting at 1
> - This tool allows Claude Code to read images (eg PNG, JPG, etc). When reading an image file the contents are presented visually as Claude Code is a multimodal LLM.
> - This tool can read PDF files (.pdf). PDFs are processed page by page, extracting both text and visual content for analysis.
> - This tool can read Jupyter notebooks (.ipynb files) and returns all cells with their outputs, combining code, text, and visualizations.
> - This tool can only read files, not directories. To read a directory, use an ls command via the Bash tool.
> - You can call multiple tools in a single response. It is always better to speculatively read multiple potentially useful files in parallel.
> - You will regularly be asked to read screenshots. If the user provides a path to a screenshot, ALWAYS use this tool to view the file at the path.
> - If you read a file that exists but has empty contents you will receive a system reminder warning in place of file contents.

```json
{
  "name": "Read",
  "input_schema": {
    "type": "object",
    "required": ["file_path"],
    "properties": {
      "file_path": {"type": "string", "description": "The absolute path to the file to read"},
      "offset": {"type": "number", "description": "The line number to start reading from"},
      "limit": {"type": "number", "description": "The number of lines to read"}
    }
  }
}
```

---

## 7. Edit

> Performs exact string replacements in files.
>
> Usage:
> - You must use your `Read` tool at least once in the conversation before editing. This tool will error if you attempt an edit without reading the file.
> - When editing text from Read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix. The line number prefix format is: spaces + line number + tab. Everything after that tab is the actual file content to match. Never include any part of the line number prefix in the old_string or new_string.
> - ALWAYS prefer editing existing files in the codebase. NEVER write new files unless explicitly required.
> - Only use emojis if the user explicitly requests it. Avoid adding emojis to files unless asked.
> - The edit will FAIL if `old_string` is not unique in the file. Either provide a larger string with more surrounding context to make it unique or use `replace_all` to change every instance of `old_string`.
> - Use `replace_all` for replacing and renaming strings across the file. This parameter is useful if you want to rename a variable for instance.

```json
{
  "name": "Edit",
  "input_schema": {
    "type": "object",
    "required": ["file_path", "old_string", "new_string"],
    "properties": {
      "file_path": {"type": "string", "description": "The absolute path to the file to modify"},
      "old_string": {"type": "string", "description": "The text to replace"},
      "new_string": {"type": "string", "description": "The text to replace it with (must be different from old_string)"},
      "replace_all": {"type": "boolean", "default": false, "description": "Replace all occurences of old_string"}
    }
  }
}
```

---

## 8. Write

> Writes a file to the local filesystem.
>
> Usage:
> - This tool will overwrite the existing file if there is one at the provided path.
> - If this is an existing file, you MUST use the Read tool first to read the file's contents. This tool will fail if you did not read the file first.
> - ALWAYS prefer editing existing files in the codebase. NEVER write new files unless explicitly required.
> - NEVER proactively create documentation files (\*.md) or README files. Only create documentation files if explicitly requested by the User.
> - Only use emojis if the user explicitly requests it. Avoid writing emojis to files unless asked.

```json
{
  "name": "Write",
  "input_schema": {
    "type": "object",
    "required": ["file_path", "content"],
    "properties": {
      "file_path": {"type": "string", "description": "The absolute path to the file to write (must be absolute, not relative)"},
      "content": {"type": "string", "description": "The content to write to the file"}
    }
  }
}
```

---

## 9. NotebookEdit

> Completely replaces the contents of a specific cell in a Jupyter notebook (.ipynb file) with new source. Jupyter notebooks are interactive documents that combine code, text, and visualizations, commonly used for data analysis and scientific computing. The notebook_path parameter must be an absolute path, not a relative path. The cell_number is 0-indexed. Use edit_mode=insert to add a new cell at the index specified by cell_number. Use edit_mode=delete to delete the cell at the index specified by cell_number.

```json
{
  "name": "NotebookEdit",
  "input_schema": {
    "type": "object",
    "required": ["notebook_path", "new_source"],
    "properties": {
      "notebook_path": {"type": "string", "description": "Absolute path to the Jupyter notebook"},
      "cell_id": {"type": "string", "description": "The ID of the cell to edit"},
      "new_source": {"type": "string", "description": "The new source for the cell"},
      "cell_type": {"type": "string", "enum": ["code", "markdown"]},
      "edit_mode": {"type": "string", "enum": ["replace", "insert", "delete"]}
    }
  }
}
```

---

## 10. WebFetch

> - Fetches content from a specified URL and processes it using an AI model
> - Takes a URL and a prompt as input
> - Fetches the URL content, converts HTML to markdown
> - Processes the content with the prompt using a small, fast model
> - Returns the model's response about the content
> - Use this tool when you need to retrieve and analyze web content
>
> Usage notes:
>   - IMPORTANT: If an MCP-provided web fetch tool is available, prefer using that tool instead of this one, as it may have fewer restrictions.
>   - The URL must be a fully-formed valid URL
>   - HTTP URLs will be automatically upgraded to HTTPS
>   - The prompt should describe what information you want to extract from the page
>   - This tool is read-only and does not modify any files
>   - Results may be summarized if the content is very large
>   - Includes a self-cleaning 15-minute cache for faster responses when repeatedly accessing the same URL
>   - When a URL redirects to a different host, the tool will inform you and provide the redirect URL in a special format. You should then make a new WebFetch request with the redirect URL to fetch the content.

```json
{
  "name": "WebFetch",
  "input_schema": {
    "type": "object",
    "required": ["url", "prompt"],
    "properties": {
      "url": {"type": "string", "format": "uri", "description": "The URL to fetch content from"},
      "prompt": {"type": "string", "description": "The prompt to run on the fetched content"}
    }
  }
}
```

---

## 11. WebSearch

> - Allows Claude to search the web and use the results to inform responses
> - Provides up-to-date information for current events and recent data
> - Returns search result information formatted as search result blocks, including links as markdown hyperlinks
> - Use this tool for accessing information beyond Claude's knowledge cutoff
> - Searches are performed automatically within a single API call
>
> CRITICAL REQUIREMENT - You MUST follow this:
>   - After answering the user's question, you MUST include a "Sources:" section at the end of your response
>   - In the Sources section, list all relevant URLs from the search results as markdown hyperlinks
>   - This is MANDATORY - never skip including sources in your response
>
> Usage notes:
>   - Domain filtering is supported to include or block specific websites
>   - Web search is only available in the US
>
> IMPORTANT - Use the correct year in search queries:
>   - Today's date is 2025-12-29. You MUST use this year when searching for recent information.

```json
{
  "name": "WebSearch",
  "input_schema": {
    "type": "object",
    "required": ["query"],
    "properties": {
      "query": {"type": "string", "minLength": 2, "description": "The search query to use"},
      "allowed_domains": {"type": "array", "items": {"type": "string"}, "description": "Only include results from these domains"},
      "blocked_domains": {"type": "array", "items": {"type": "string"}, "description": "Never include results from these domains"}
    }
  }
}
```

---

## 12. TodoWrite

The second-longest tool description (~1,200 words). Contains **8 worked examples** (4 when-to-use, 4 when-not-to-use) with explicit reasoning — essentially a full tutorial on task management embedded in a tool schema.

> Use this tool to create and manage a structured task list for your current coding session. This helps you track progress, organize complex tasks, and demonstrate thoroughness to the user. It also helps the user understand the progress of the task and overall progress of their requests.
>
> **When to Use This Tool:**
> 1. Complex multi-step tasks - When a task requires 3 or more distinct steps
> 2. Non-trivial and complex tasks - Tasks that require careful planning
> 3. User explicitly requests todo list
> 4. User provides multiple tasks - numbered or comma-separated lists
> 5. After receiving new instructions - Immediately capture requirements
> 6. When you start working on a task - Mark as in_progress BEFORE beginning
> 7. After completing a task - Mark as completed, add follow-up tasks
>
> **When NOT to Use:**
> 1. Single, straightforward task
> 2. Trivial task with no organizational benefit
> 3. Completable in less than 3 trivial steps
> 4. Purely conversational or informational
>
> **Examples of When to Use:** (4 detailed examples with `<reasoning>` tags)
> - Dark mode toggle implementation (multi-step feature)
> - Rename function across project (discovered scope requires tracking)
> - E-commerce features (multiple complex features from comma-separated list)
> - React optimization (analysis revealed multiple bottlenecks)
>
> **Examples of When NOT to Use:** (4 detailed examples with `<reasoning>` tags)
> - Print "Hello World" in Python (single trivial step)
> - Explain git status command (informational, no coding)
> - Add a comment to a function (single location edit)
> - Run npm install (single command execution)
>
> **Task States:** pending, in_progress, completed
> - Exactly ONE task must be in_progress at any time
> - Mark tasks complete IMMEDIATELY after finishing
> - ONLY mark completed when FULLY accomplished
> - Task descriptions require two forms: content ("Run tests") and activeForm ("Running tests")

```json
{
  "name": "TodoWrite",
  "input_schema": {
    "type": "object",
    "required": ["todos"],
    "properties": {
      "todos": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["content", "status", "activeForm"],
          "properties": {
            "content": {"type": "string", "minLength": 1},
            "status": {"type": "string", "enum": ["pending", "in_progress", "completed"]},
            "activeForm": {"type": "string", "minLength": 1}
          }
        },
        "description": "The updated todo list"
      }
    }
  }
}
```

---

## 13. AskUserQuestion

> Use this tool when you need to ask the user questions during execution. This allows you to:
> 1. Gather user preferences or requirements
> 2. Clarify ambiguous instructions
> 3. Get decisions on implementation choices as you work
> 4. Offer choices to the user about what direction to take.
>
> Usage notes:
> - Users will always be able to select "Other" to provide custom text input
> - Use multiSelect: true to allow multiple answers to be selected for a question
> - If you recommend a specific option, make that the first option in the list and add "(Recommended)" at the end of the label

```json
{
  "name": "AskUserQuestion",
  "input_schema": {
    "type": "object",
    "required": ["questions"],
    "properties": {
      "questions": {
        "type": "array",
        "minItems": 1,
        "maxItems": 4,
        "items": {
          "type": "object",
          "required": ["question", "header", "options", "multiSelect"],
          "properties": {
            "question": {"type": "string", "description": "Clear question ending with '?'"},
            "header": {"type": "string", "description": "Chip label, max 12 chars"},
            "options": {
              "type": "array",
              "minItems": 2,
              "maxItems": 4,
              "items": {
                "type": "object",
                "required": ["label", "description"],
                "properties": {
                  "label": {"type": "string", "description": "Concise, 1-5 words"},
                  "description": {"type": "string", "description": "Trade-offs or implications"},
                  "markdown": {"type": "string", "description": "Preview content (optional)"}
                }
              }
            },
            "multiSelect": {"type": "boolean"}
          }
        }
      }
    }
  }
}
```

---

## 14. EnterPlanMode

> Use this tool proactively when you're about to start a non-trivial implementation task. Getting user sign-off on your approach before writing code prevents wasted effort and ensures alignment. This tool transitions you into plan mode where you can explore the codebase and design an implementation approach for user approval.
>
> **Prefer using EnterPlanMode** when ANY of these conditions apply:
> 1. New Feature Implementation
> 2. Multiple Valid Approaches
> 3. Code Modifications affecting existing behavior
> 4. Architectural Decisions between patterns/technologies
> 5. Multi-File Changes (more than 2-3 files)
> 6. Unclear Requirements needing exploration
> 7. User Preferences Matter
>
> **When NOT to Use:** Single-line fixes, typos, obvious bugs, tasks with very specific instructions, pure research/exploration.
>
> **What Happens in Plan Mode:**
> 1. Explore codebase using Glob, Grep, Read
> 2. Understand existing patterns and architecture
> 3. Design implementation approach
> 4. Present plan for user approval
> 5. Use AskUserQuestion to clarify approaches
> 6. Exit with ExitPlanMode when ready

```json
{
  "name": "EnterPlanMode",
  "input_schema": {
    "type": "object",
    "properties": {}
  }
}
```

---

## 15. ExitPlanMode

> Use this tool when you are in plan mode and have finished writing your plan to the plan file and are ready for user approval.
>
> **How This Tool Works:**
> - You should have already written your plan to the plan file specified in the plan mode system message
> - This tool does NOT take the plan content as a parameter - it will read the plan from the file you wrote
> - This tool simply signals that you're done planning and ready for the user to review and approve
>
> **When to Use:** Only when planning implementation steps for a coding task. NOT for research tasks.
>
> **Handling Ambiguity:** If there are multiple valid approaches or unclear requirements, use AskUserQuestion first, clarify, edit plan, then use ExitPlanMode.

```json
{
  "name": "ExitPlanMode",
  "input_schema": {
    "type": "object",
    "properties": {}
  }
}
```

---

## 16. Skill

> Execute a skill within the main conversation
>
> When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.
>
> When users ask you to run a "slash command" or reference "/\<something\>" (e.g., "/commit", "/review-pr"), they are referring to a skill. Use this tool to invoke the corresponding skill.
>
> How to invoke:
> - `skill: "pdf"` - invoke the pdf skill
> - `skill: "commit", args: "-m 'Fix bug'"` - invoke with arguments
> - `skill: "review-pr", args: "123"` - invoke with arguments
> - `skill: "ms-office-suite:pdf"` - invoke using fully qualified name
>
> Important:
> - When a skill is relevant, you must invoke this tool IMMEDIATELY as your first action
> - NEVER just announce or mention a skill without actually calling this tool
> - This is a BLOCKING REQUIREMENT: invoke the relevant Skill tool BEFORE generating any other response
> - Only use skills listed in available_skills
> - Do not invoke a skill that is already running
> - Do not use this tool for built-in CLI commands (like /help, /clear, etc.)

```json
{
  "name": "Skill",
  "input_schema": {
    "type": "object",
    "required": ["skill"],
    "properties": {
      "skill": {"type": "string", "description": "The skill name, e.g. 'commit', 'review-pr', or 'pdf'"},
      "args": {"type": "string", "description": "Optional arguments for the skill"}
    }
  }
}
```

---

## 17. KillShell

> - Kills a running background bash shell by its ID
> - Takes a shell_id parameter identifying the shell to kill
> - Returns a success or failure status
> - Use this tool when you need to terminate a long-running shell
> - Shell IDs can be found using the /tasks command

```json
{
  "name": "KillShell",
  "input_schema": {
    "type": "object",
    "required": ["shell_id"],
    "properties": {
      "shell_id": {"type": "string", "description": "The ID of the background shell to kill"}
    }
  }
}
```

---

## Description Length Analysis

| Tool | Description Words | Notable Content |
|------|------------------|-----------------|
| **Bash** | ~1,800 | Git commit protocol, PR workflow, command hygiene, 6+ cross-references to other tools |
| **TodoWrite** | ~1,200 | 8 worked examples with `<reasoning>` tags, when-to/when-not-to decision framework |
| **Task** | ~600 | Sub-agent routing table (5 types), concurrency rules, resume/background patterns |
| **EnterPlanMode** | ~400 | 7 when-to-use conditions, 4 when-not-to examples, plan mode workflow |
| **ExitPlanMode** | ~250 | Ambiguity handling protocol, research vs implementation distinction |
| **Read** | ~200 | Multimodal capabilities (images, PDFs, notebooks), parallel reading guidance |
| **Grep** | ~150 | Regex syntax notes, multiline mode, output mode explanations |
| **AskUserQuestion** | ~100 | Recommendation pattern, multiSelect usage |
| **Edit** | ~100 | Uniqueness constraint, indentation preservation, Read-first enforcement |
| **Skill** | ~100 | Slash command routing, blocking requirement, available skills list |
| **WebFetch** | ~100 | 15-min cache, redirect handling, MCP preference |
| **WebSearch** | ~100 | Source citation requirement, date awareness, domain filtering |
| **Write** | ~80 | Read-first enforcement, anti-documentation-creation rule |
| **Glob** | ~60 | Parallel search recommendation, Agent tool fallback |
| **NotebookEdit** | ~50 | Cell operations (replace/insert/delete) |
| **TaskOutput** | ~50 | Blocking vs non-blocking retrieval |
| **KillShell** | ~40 | Simple termination |

**Total: ~5,400 words** of behavioral instructions embedded in tool descriptions alone — equivalent to a 10-page document that is sent with every API request.
