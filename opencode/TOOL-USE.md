# Tool Catalog: OpenCode

## Table of Contents

- [Summary](#summary)
- [Full Tool Catalog (build mode — 10 tools)](#full-tool-catalog-build-mode--10-tools)
  - [File Operations (3 tools)](#file-operations-3-tools)
    - [`read`](#read)
    - [`glob`](#glob)
    - [`grep`](#grep)
  - [File Edit (1 tools)](#file-edit-1-tools)
    - [`apply_patch`](#apply_patch)
  - [Shell (1 tools)](#shell-1-tools)
    - [`bash`](#bash)
  - [Agents (1 tools)](#agents-1-tools)
    - [`task`](#task)
  - [Web (1 tools)](#web-1-tools)
    - [`webfetch`](#webfetch)
  - [Planning (1 tools)](#planning-1-tools)
    - [`todowrite`](#todowrite)
  - [Questions (1 tools)](#questions-1-tools)
    - [`question`](#question)
  - [Skills (1 tools)](#skills-1-tools)
    - [`skill`](#skill)
- [Mode Delta: Tool Changes](#mode-delta-tool-changes)
  - [build → plan](#build--plan)
- [Tool Invocation Patterns](#tool-invocation-patterns)
  - [build mode](#build-mode)
  - [plan mode](#plan-mode)

## Summary

| Mode | Total | File Ops | File Edit | Shell | Agents | Web | Planning | Questions | Skills |
|------|-------|----------|-----------|-------|--------|-----|----------|-----------|--------|
| build | 10 | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| plan | 10 | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

## Full Tool Catalog (build mode — 10 tools)

### File Operations (3 tools)

#### `read`

**Description:**

```
Read a file or directory from the local filesystem. If the path does not exist, an error is returned.

Usage:
- The filePath parameter should be an absolute path.
- By default, this tool returns up to 2000 lines from the start of the file.
- The offset parameter is the line number to start from (1-indexed).
- To read later sections, call this tool again with a larger offset.
- Use the grep tool to find specific content in large files or files with long lines.
- If you are unsure of the correct file path, use the glob tool to look up filenames by glob pattern.
- Contents are returned with each line prefixed by its line number as `<line>: <content>`. For example, if a file has contents "foo\n", you will receive "1: foo\n". For directories, entries are returned one per line (without line numbers) with a trailing `/` for subdirectories.
- Any line longer than 2000 characters is truncated.
- Call this tool in parallel when you know there are multiple files you want to read.
- Avoid tiny repeated slices (30 line chunks). If you need more context, read a larger window.
- This tool can read image files and PDFs and return them as file attachments.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "filePath": {
      "description": "The absolute path to the file or directory to read",
      "type": "string"
    },
    "offset": {
      "description": "The line number to start reading from (1-indexed)",
      "type": "number"
    },
    "limit": {
      "description": "The maximum number of lines to read (defaults to 2000)",
      "type": "number"
    }
  },
  "required": [
    "filePath"
  ],
  "additionalProperties": false
}
```

---

#### `glob`

**Description:**

```
- Fast file pattern matching tool that works with any codebase size
- Supports glob patterns like "**/*.js" or "src/**/*.ts"
- Returns matching file paths sorted by modification time
- Use this tool when you need to find files by name patterns
- When you are doing an open-ended search that may require multiple rounds of globbing and grepping, use the Task tool instead
- You have the capability to call multiple tools in a single response. It is always better to speculatively perform multiple searches as a batch that are potentially useful.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "description": "The glob pattern to match files against",
      "type": "string"
    },
    "path": {
      "description": "The directory to search in. If not specified, the current working directory will be used. IMPORTANT: Omit this field to use the default directory. DO NOT enter \"undefined\" or \"null\" - simply omit it for the default behavior. Must be a valid directory path if provided.",
      "type": "string"
    }
  },
  "required": [
    "pattern"
  ],
  "additionalProperties": false
}
```

---

#### `grep`

**Description:**

```
- Fast content search tool that works with any codebase size
- Searches file contents using regular expressions
- Supports full regex syntax (eg. "log.*Error", "function\s+\w+", etc.)
- Filter files by pattern with the include parameter (eg. "*.js", "*.{ts,tsx}")
- Returns file paths and line numbers with at least one match sorted by modification time
- Use this tool when you need to find files containing specific patterns
- If you need to identify/count the number of matches within files, use the Bash tool with `rg` (ripgrep) directly. Do NOT use `grep`.
- When you are doing an open-ended search that may require multiple rounds of globbing and grepping, use the Task tool instead
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "description": "The regex pattern to search for in file contents",
      "type": "string"
    },
    "path": {
      "description": "The directory to search in. Defaults to the current working directory.",
      "type": "string"
    },
    "include": {
      "description": "File pattern to include in the search (e.g. \"*.js\", \"*.{ts,tsx}\")",
      "type": "string"
    }
  },
  "required": [
    "pattern"
  ],
  "additionalProperties": false
}
```

---

### File Edit (1 tools)

#### `apply_patch`

**Description:**

```
Use the `apply_patch` tool to edit files. Your patch language is a stripped-down, file-oriented diff format designed to be easy to parse and safe to apply. You can think of it as a high-level envelope:

*** Begin Patch
[ one or more file sections ]
*** End Patch

Within that envelope, you get a sequence of file operations.
You MUST include a header to specify the action you are taking.
Each operation starts with one of three headers:

*** Add File: <path> - create a new file. Every following line is a + line (the initial contents).
*** Delete File: <path> - remove an existing file. Nothing follows.
*** Update File: <path> - patch an existing file in place (optionally with a rename).

Example patch:

*** Begin Patch
*** Add File: hello.txt
+Hello world
*** Update File: src/app.py
*** Move to: src/main.py
@@ def greet():
-print("Hi")
+print("Hello, world!")
*** Delete File: obsolete.txt
*** End Patch

It is important to remember:

- You must include a header with your intended action (Add/Delete/Update)
- You must prefix new lines with `+` even when creating a new file
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "patchText": {
      "description": "The full patch text that describes all changes to be made",
      "type": "string"
    }
  },
  "required": [
    "patchText"
  ],
  "additionalProperties": false
}
```

---

### Shell (1 tools)

#### `bash`

**Description:**

```
Executes a given bash command in a persistent shell session with optional timeout, ensuring proper handling and security measures.

All commands run in /Users/alx/Development/agenticloops-ai/agentic-apps-internals by default. Use the `workdir` parameter if you need to run a command in a different directory. AVOID using `cd <directory> && <command>` patterns - use `workdir` instead.

IMPORTANT: This tool is for terminal operations like git, npm, docker, etc. DO NOT use it for file operations (reading, writing, editing, searching, finding files) - use the specialized tools for this instead.

[...full description includes directory verification, command execution, git commit workflow, and PR creation instructions]
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "command": {
      "description": "The command to execute",
      "type": "string"
    },
    "timeout": {
      "description": "Optional timeout in milliseconds",
      "type": "number"
    },
    "workdir": {
      "description": "The working directory to run the command in. Defaults to /Users/alx/Development/agenticloops-ai/agentic-apps-internals. Use this instead of 'cd' commands.",
      "type": "string"
    },
    "description": {
      "description": "Clear, concise description of what this command does in 5-10 words.",
      "type": "string"
    }
  },
  "required": [
    "command",
    "description"
  ],
  "additionalProperties": false
}
```

---

### Agents (1 tools)

#### `task`

**Description:**

```
Launch a new agent to handle complex, multistep tasks autonomously.

Available agent types and the tools they have access to:
- general: General-purpose agent for researching complex questions and executing multi-step tasks. Use this agent to execute multiple units of work in parallel.
- explore: Fast agent specialized for exploring codebases. Use this when you need to quickly find files by patterns, search code for keywords, or answer questions about the codebase.

When using the Task tool, you must specify a subagent_type parameter to select which agent type to use.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "description": {
      "description": "A short (3-5 words) description of the task",
      "type": "string"
    },
    "prompt": {
      "description": "The task for the agent to perform",
      "type": "string"
    },
    "subagent_type": {
      "description": "The type of specialized agent to use for this task",
      "type": "string"
    },
    "task_id": {
      "description": "This should only be set if you mean to resume a previous task",
      "type": "string"
    },
    "command": {
      "description": "The command that triggered this task",
      "type": "string"
    }
  },
  "required": [
    "description",
    "prompt",
    "subagent_type"
  ],
  "additionalProperties": false
}
```

---

### Web (1 tools)

#### `webfetch`

**Description:**

```
- Fetches content from a specified URL
- Takes a URL and optional format as input
- Fetches the URL content, converts to requested format (markdown by default)
- Returns the content in the specified format
- Use this tool when you need to retrieve and analyze web content

Usage notes:
  - IMPORTANT: if another tool is present that offers better web fetching capabilities, is more targeted to the task, or has fewer restrictions, prefer using that tool instead of this one.
  - The URL must be a fully-formed valid URL
  - HTTP URLs will be automatically upgraded to HTTPS
  - Format options: "markdown" (default), "text", or "html"
  - This tool is read-only and does not modify any files
  - Results may be summarized if the content is very large
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "url": {
      "description": "The URL to fetch content from",
      "type": "string"
    },
    "format": {
      "description": "The format to return the content in (text, markdown, or html). Defaults to markdown.",
      "default": "markdown",
      "type": "string",
      "enum": [
        "text",
        "markdown",
        "html"
      ]
    },
    "timeout": {
      "description": "Optional timeout in seconds (max 120)",
      "type": "number"
    }
  },
  "required": [
    "url",
    "format"
  ],
  "additionalProperties": false
}
```

---

### Planning (1 tools)

#### `todowrite`

**Description:**

```
Use this tool to create and manage a structured task list for your current coding session. This helps you track progress, organize complex tasks, and demonstrate thoroughness to the user.

When to Use:
1. Complex multistep tasks - When a task requires 3 or more distinct steps
2. Non-trivial and complex tasks - Tasks that require careful planning
3. User explicitly requests todo list
4. User provides multiple tasks
5. After receiving new instructions
6. After completing a task
7. When you start working on a new task

Task States: pending, in_progress, completed, cancelled
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "todos": {
      "description": "The updated todo list",
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "content": {
            "description": "Brief description of the task",
            "type": "string"
          },
          "status": {
            "description": "Current status of the task: pending, in_progress, completed, cancelled",
            "type": "string"
          },
          "priority": {
            "description": "Priority level of the task: high, medium, low",
            "type": "string"
          }
        },
        "required": [
          "content",
          "status",
          "priority"
        ],
        "additionalProperties": false
      }
    }
  },
  "required": [
    "todos"
  ],
  "additionalProperties": false
}
```

---

### Questions (1 tools)

#### `question`

**Description:**

```
Use this tool when you need to ask the user questions during execution. This allows you to:
1. Gather user preferences or requirements
2. Clarify ambiguous instructions
3. Get decisions on implementation choices as you work
4. Offer choices to the user about what direction to take.

Usage notes:
- When `custom` is enabled (default), a "Type your own answer" option is added automatically; don't include "Other" or catch-all options
- Answers are returned as arrays of labels; set `multiple: true` to allow selecting more than one
- If you recommend a specific option, make that the first option in the list and add "(Recommended)" at the end of the label
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "questions": {
      "description": "Questions to ask",
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "question": {
            "description": "Complete question",
            "type": "string"
          },
          "header": {
            "description": "Very short label (max 30 chars)",
            "type": "string"
          },
          "options": {
            "description": "Available choices",
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "label": {
                  "description": "Display text (1-5 words, concise)",
                  "type": "string"
                },
                "description": {
                  "description": "Explanation of choice",
                  "type": "string"
                }
              },
              "required": [
                "label",
                "description"
              ],
              "additionalProperties": false
            }
          },
          "multiple": {
            "description": "Allow selecting multiple choices",
            "type": "boolean"
          }
        },
        "required": [
          "question",
          "header",
          "options"
        ],
        "additionalProperties": false
      }
    }
  },
  "required": [
    "questions"
  ],
  "additionalProperties": false
}
```

---

### Skills (1 tools)

#### `skill`

**Description:**

```
Load a specialized skill that provides domain-specific instructions and workflows. No skills are currently available.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "name": {
      "description": "The name of the skill from available_skills",
      "type": "string"
    }
  },
  "required": [
    "name"
  ],
  "additionalProperties": false
}
```

---

## Mode Delta: Tool Changes

### build → plan

Tool set identical across both modes.

## Tool Invocation Patterns

Tools actually called during captured sessions:

### build mode

**Call sequence:**

1. Turn 2: `read`
1. Turn 3: `apply_patch`
1. Turn 4: `apply_patch`
1. Turn 5: `read`
1. Turn 6: `bash`
1. Turn 7: TEXT (final response)

**Call frequency:**

- `apply_patch`: 2x
- `read`: 2x
- `bash`: 1x

### plan mode

**Call sequence:**

1. Turn 2: `glob`, `glob`, `glob`
1. Turn 3: `read`, `read`
1. Turn 4: TEXT (plan output)

**Call frequency:**

- `glob`: 3x
- `read`: 2x
