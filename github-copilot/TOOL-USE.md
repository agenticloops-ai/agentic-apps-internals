# Tool Catalog: GitHub Copilot

## Table of Contents

- [Summary](#summary)
- [Full Tool Catalog (agent mode — 65 tools)](#full-tool-catalog-agent-mode-65-tools)
  - [File Read (7 tools)](#file-read-7-tools)
    - [`file_search`](#file_search)
    - [`grep_search`](#grep_search)
    - [`list_code_usages`](#list_code_usages)
    - [`list_dir`](#list_dir)
    - [`read_file`](#read_file)
    - [`read_notebook_cell_output`](#read_notebook_cell_output)
    - [`semantic_search`](#semantic_search)
  - [File Write (4 tools)](#file-write-4-tools)
    - [`apply_patch`](#apply_patch)
    - [`create_directory`](#create_directory)
    - [`create_file`](#create_file)
    - [`edit_notebook_file`](#edit_notebook_file)
  - [Shell (7 tools)](#shell-7-tools)
    - [`await_terminal`](#await_terminal)
    - [`create_and_run_task`](#create_and_run_task)
    - [`get_terminal_output`](#get_terminal_output)
    - [`kill_terminal`](#kill_terminal)
    - [`run_in_terminal`](#run_in_terminal)
    - [`terminal_last_command`](#terminal_last_command)
    - [`terminal_selection`](#terminal_selection)
  - [Web (2 tools)](#web-2-tools)
    - [`fetch_webpage`](#fetch_webpage)
    - [`open_simple_browser`](#open_simple_browser)
  - [Planning (1 tools)](#planning-1-tools)
    - [`manage_todo_list`](#manage_todo_list)
  - [Questions (1 tools)](#questions-1-tools)
    - [`ask_questions`](#ask_questions)
  - [Multi Agent (1 tools)](#multi-agent-1-tools)
    - [`runSubagent`](#runsubagent)
  - [Vscode (10 tools)](#vscode-10-tools)
    - [`create_new_workspace`](#create_new_workspace)
    - [`get_changed_files`](#get_changed_files)
    - [`get_errors`](#get_errors)
    - [`get_project_setup_info`](#get_project_setup_info)
    - [`get_search_view_results`](#get_search_view_results)
    - [`get_vscode_api`](#get_vscode_api)
    - [`install_extension`](#install_extension)
    - [`run_vscode_command`](#run_vscode_command)
    - [`test_failure`](#test_failure)
    - [`vscode_searchExtensions_internal`](#vscode_searchextensions_internal)
  - [Mcp (13 tools)](#mcp-13-tools)
    - [`mcp_pylance_mcp_s_pylanceDocString`](#mcp_pylance_mcp_s_pylancedocstring)
    - [`mcp_pylance_mcp_s_pylanceDocuments`](#mcp_pylance_mcp_s_pylancedocuments)
    - [`mcp_pylance_mcp_s_pylanceFileSyntaxErrors`](#mcp_pylance_mcp_s_pylancefilesyntaxerrors)
    - [`mcp_pylance_mcp_s_pylanceImports`](#mcp_pylance_mcp_s_pylanceimports)
    - [`mcp_pylance_mcp_s_pylanceInstalledTopLevelModules`](#mcp_pylance_mcp_s_pylanceinstalledtoplevelmodules)
    - [`mcp_pylance_mcp_s_pylanceInvokeRefactoring`](#mcp_pylance_mcp_s_pylanceinvokerefactoring)
    - [`mcp_pylance_mcp_s_pylancePythonEnvironments`](#mcp_pylance_mcp_s_pylancepythonenvironments)
    - [`mcp_pylance_mcp_s_pylanceRunCodeSnippet`](#mcp_pylance_mcp_s_pylanceruncodesnippet)
    - [`mcp_pylance_mcp_s_pylanceSettings`](#mcp_pylance_mcp_s_pylancesettings)
    - [`mcp_pylance_mcp_s_pylanceSyntaxErrors`](#mcp_pylance_mcp_s_pylancesyntaxerrors)
    - [`mcp_pylance_mcp_s_pylanceUpdatePythonEnvironment`](#mcp_pylance_mcp_s_pylanceupdatepythonenvironment)
    - [`mcp_pylance_mcp_s_pylanceWorkspaceRoots`](#mcp_pylance_mcp_s_pylanceworkspaceroots)
    - [`mcp_pylance_mcp_s_pylanceWorkspaceUserFiles`](#mcp_pylance_mcp_s_pylanceworkspaceuserfiles)
- [Mode Delta: Tool Changes](#mode-delta-tool-changes)
  - [agent → ask](#agent-ask)
  - [agent → plan](#agent-plan)
  - [ask → plan](#ask-plan)
- [Tool Invocation Patterns](#tool-invocation-patterns)
  - [agent mode](#agent-mode)
  - [ask mode](#ask-mode)
  - [plan mode](#plan-mode)

## Summary

| Mode | Total | File Read | File Write | Shell | Web | Planning | Questions | Multi Agent | Notebook | Python Env | Vscode | Github | Mcp | Mermaid | Container |
|------|-------|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
| agent | 65 | 7 | 4 | 7 | 2 | 1 | 1 | 1 | 9 | 4 | 10 | 1 | 13 | 4 | 1 |
| ask | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plan | 22 | 7 | 0 | 3 | 1 | 0 | 1 | 1 | 4 | 0 | 4 | 1 | 0 | 0 | 0 |

## Full Tool Catalog (agent mode — 65 tools)

### File Read (7 tools)

#### `file_search`

**Description:**

```
Search for files in the workspace by glob pattern. This only returns the paths of matching files. Use this tool when you know the exact filename pattern of the files you're searching for. Glob patterns match from the root of the workspace folder. Examples:
- **/*.{js,ts} to match all js/ts files in the workspace.
- src/** to match all files under the top-level src folder.
- **/foo/**/*.js to match all js files under any foo folder in the workspace.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search for files with names or paths matching this glob pattern."
    },
    "maxResults": {
      "type": "number",
      "description": "The maximum number of results to return. Do not use this unless necessary, it can slow things down. By default, only some matches are returned. If you use this and don't see what you're looking for, you can try again with a more specific query or a larger maxResults."
    }
  },
  "required": [
    "query"
  ]
}
```

#### `grep_search`

**Description:**

```
Do a fast text search in the workspace. Use this tool when you want to search with an exact string or regex. If you are not sure what words will appear in the workspace, prefer using regex patterns with alternation (|) or character classes to search for multiple potential words at once instead of making separate searches. For example, use 'function|method|procedure' to look for all of those words at once. Use includePattern to search within files matching a specific pattern, or in a specific file, using a relative path. Use 'includeIgnoredFiles' to include files normally ignored by .gitignore, other ignore files, and `files.exclude` and `search.exclude` settings. Warning: using this may cause the search to be slower, only set it when you want to search in ignored folders like node_modules or build outputs. Use this tool when you want to see an overview of a particular file, instead of using read_file many times to look for code within a file.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The pattern to search for in files in the workspace. Use regex with alternation (e.g., 'word1|word2|word3') or character classes to find multiple potential words in a single search. Be sure to set the isRegexp property properly to declare whether it's a regex or plain text pattern. Is case-insensitive."
    },
    "isRegexp": {
      "type": "boolean",
      "description": "Whether the pattern is a regex."
    },
    "includePattern": {
      "type": "string",
      "description": "Search files matching this glob pattern. Will be applied to the relative path of files within the workspace. To search recursively inside a folder, use a proper glob pattern like \"src/folder/**\". Do not use | in includePattern."
    },
    "maxResults": {
      "type": "number",
      "description": "The maximum number of results to return. Do not use this unless necessary, it can slow things down. By default, only some matches are returned. If you use this and don't see what you're looking for, you can try again with a more specific query or a larger maxResults."
    },
    "includeIgnoredFiles": {
      "type": "boolean",
      "description": "Whether to include files that would normally be ignored according to .gitignore, other ignore files and `files.exclude` and `search.exclude` settings. Warning: using this may cause the search to be slower. Only set it when you want to search in ignored folders like node_modules or build outputs."
    }
  },
  "required": [
    "query",
    "isRegexp"
  ]
}
```

#### `list_code_usages`

**Description:**

```
Request to list all usages (references, definitions, implementations etc) of a function, class, method, variable etc. Use this tool when 
1. Looking for a sample implementation of an interface or class
2. Checking how a function is used throughout the codebase.
3. Including and updating all usages when changing a function, method, or constructor
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "symbolName": {
      "type": "string",
      "description": "The name of the symbol, such as a function name, class name, method name, variable name, etc."
    },
    "filePaths": {
      "type": "array",
      "description": "One or more file paths which likely contain the definition of the symbol. For instance the file which declares a class or function. This is optional but will speed up the invocation of this tool and improve the quality of its output.",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "symbolName"
  ]
}
```

#### `list_dir`

**Description:**

```
List the contents of a directory. Result will have the name of the child. If the name ends in /, it's a folder, otherwise a file
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "The absolute path to the directory to list."
    }
  },
  "required": [
    "path"
  ]
}
```

#### `read_file`

**Description:**

```
Read the contents of a file.

You must specify the line range you're interested in. Line numbers are 1-indexed. If the file contents returned are insufficient for your task, you may call this tool again to retrieve more content. Prefer reading larger ranges over doing many small reads.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "filePath": {
      "description": "The absolute path of the file to read.",
      "type": "string"
    },
    "startLine": {
      "type": "number",
      "description": "The line number to start reading from, 1-based."
    },
    "endLine": {
      "type": "number",
      "description": "The inclusive line number to end reading at, 1-based."
    }
  },
  "required": [
    "filePath",
    "startLine",
    "endLine"
  ]
}
```

#### `read_notebook_cell_output`

**Description:**

```
This tool will retrieve the output for a notebook cell from its most recent execution or restored from disk. The cell may have output even when it has not been run in the current kernel session. This tool has a higher token limit for output length than the runNotebookCell tool.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "filePath": {
      "type": "string",
      "description": "An absolute path to the notebook file with the cell to run, or the URI of a untitled, not yet named, file, such as `untitled:Untitled-1.ipynb"
    },
    "cellId": {
      "type": "string",
      "description": "The ID of the cell for which output should be retrieved."
    }
  },
  "required": [
    "filePath",
    "cellId"
  ]
}
```

#### `semantic_search`

**Description:**

```
Run a natural language search for relevant code or documentation comments from the user's current workspace. Returns relevant code snippets from the user's current workspace if it is large, or the full contents of the workspace if it is small.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The query to search the codebase for. Should contain all relevant context. Should ideally be text that might appear in the codebase, such as function names, variable names, or comments."
    }
  },
  "required": [
    "query"
  ]
}
```

---

### File Write (4 tools)

#### `apply_patch`

**Description:**

```
Edit text files. Do not use this tool to edit Jupyter notebooks. `apply_patch` allows you to execute a diff/patch against a text file, but the format of the diff specification is unique to this task, so pay careful attention to these instructions. To use the `apply_patch` command, you should pass a message of the following structure as "input":

*** Begin Patch
[YOUR_PATCH]
*** End Patch

Where [YOUR_PATCH] is the actual content of your patch, specified in the following V4A diff format.

*** [ACTION] File: [/absolute/path/to/file] -> ACTION can be one of Add, Update, or Delete.
An example of a message that you might pass as "input" to this function, in order to apply a patch, is shown below.

*** Begin Patch
*** Update File: /Users/someone/pygorithm/searching/binary_search.py
@@class BaseClass
@@    def search():
-        pass
+        raise NotImplementedError()

@@class Subclass
@@    def search():
-        pass
+        raise NotImplementedError()

*** End Patch
Do not use line numbers in this diff format.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "input": {
      "type": "string",
      "description": "The edit patch to apply."
    },
    "explanation": {
      "type": "string",
      "description": "A short description of what the tool call is aiming to achieve."
    }
  },
  "required": [
    "input",
    "explanation"
  ]
}
```

#### `create_directory`

**Description:**

```
Create a new directory structure in the workspace. Will recursively create all directories in the path, like mkdir -p. You do not need to use this tool before using create_file, that tool will automatically create the needed directories.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "dirPath": {
      "type": "string",
      "description": "The absolute path to the directory to create."
    }
  },
  "required": [
    "dirPath"
  ]
}
```

#### `create_file`

**Description:**

```
This is a tool for creating a new file in the workspace. The file will be created with the specified content. The directory will be created if it does not already exist. Never use this tool to edit a file that already exists.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "filePath": {
      "type": "string",
      "description": "The absolute path to the file to create."
    },
    "content": {
      "type": "string",
      "description": "The content to write to the file."
    }
  },
  "required": [
    "filePath",
    "content"
  ]
}
```

#### `edit_notebook_file`

**Description:**

```
This is a tool for editing an existing Notebook file in the workspace. Generate the "explanation" property first.
The system is very smart and can understand how to apply your edits to the notebooks.
When updating the content of an existing cell, ensure newCode preserves whitespace and indentation exactly and does NOT include any code markers such as (...existing code...).
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "filePath": {
      "type": "string",
      "description": "An absolute path to the notebook file to edit, or the URI of a untitled, not yet named, file, such as `untitled:Untitled-1."
    },
    "cellId": {
      "type": "string",
      "description": "Id of the cell that needs to be deleted or edited. Use the value `TOP`, `BOTTOM` when inserting a cell at the top or bottom of the notebook, else provide the id of the cell after which a new cell is to be inserted. Remember, if a cellId is provided and editType=insert, then a cell will be inserted after the cell with the provided cellId."
    },
    "newCode": {
      "anyOf": [
        {
          "type": "string",
          "description": "The code for the new or existing cell to be edited. Code should not be wrapped within <VSCode.Cell> tags. Do NOT include code markers such as (...existing code...) to indicate existing code."
        },
        {
          "type": "array",
          "items": {
            "type": "string",
            "description": "The code for the new or existing cell to be edited. Code should not be wrapped within <VSCode.Cell> tags"
          }
        }
      ]
    },
    "language": {
      "type": "string",
      "description": "The language of the cell. `markdown`, `python`, `javascript`, `julia`, etc."
    },
    "editType": {
      "type": "string",
      "enum": [
        "insert",
        "delete",
        "edit"
      ],
      "description": "The operation peformed on the cell, whether `insert`, `delete` or `edit`.\nUse the `editType` field to specify the operation: `insert` to add a new cell, `edit` to modify an existing cell's content, and `delete` to remove a cell."
    }
  },
  "required": [
    "filePath",
    "editType",
    "cellId"
  ]
}
```

---

### Shell (7 tools)

#### `await_terminal`

**Description:**

```
Wait for a background terminal command to complete. Returns the output, exit code, or timeout status.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "The ID of the terminal to await (returned by run_in_terminal when isBackground=true)."
    },
    "timeout": {
      "type": "number",
      "description": "Timeout in milliseconds. If the command does not complete within this time, returns the output collected so far with a timeout indicator. Use 0 for no timeout."
    }
  },
  "required": [
    "id",
    "timeout"
  ]
}
```

#### `create_and_run_task`

**Description:**

```
Creates and runs a build, run, or custom task for the workspace by generating or adding to a tasks.json file based on the project structure (such as package.json or README.md). If the user asks to build, run, launch and they have no tasks.json file, use this tool. If they ask to create or add a task, use this tool.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "workspaceFolder": {
      "type": "string",
      "description": "The absolute path of the workspace folder where the tasks.json file will be created."
    },
    "task": {
      "type": "object",
      "description": "The task to add to the new tasks.json file.",
      "properties": {
        "label": {
          "type": "string",
          "description": "The label of the task."
        },
        "type": {
          "type": "string",
          "description": "The type of the task. The only supported value is 'shell'.",
          "enum": [
            "shell"
          ]
        },
        "command": {
          "type": "string",
          "description": "The shell command to run for the task. Use this to specify commands for building or running the application."
        },
        "args": {
          "type": "array",
          "description": "The arguments to pass to the command.",
          "items": {
            "type": "string"
          }
        },
        "isBackground": {
          "type": "boolean",
          "description": "Whether the task runs in the background without blocking the UI or other tasks. Set to true for long-running processes like watch tasks or servers that should continue executing without requiring user attention. When false, the task will block the terminal until completion."
        },
        "problemMatcher": {
          "type": "array",
          "description": "The problem matcher to use to parse task output for errors and warnings. Can be a predefined matcher like '$tsc' (TypeScript), '$eslint - stylish', '$gcc', etc., or a custom pattern defined in tasks.json. This helps VS Code display errors in the Problems panel and enables quick navigation to error locations.",
          "items": {
            "type": "string"
          }
        },
        "group": {
          "type": "string",
          "description": "The group to which the task belongs."
        }
      },
      "required": [
        "label",
        "type",
        "command"
      ]
    }
  },
  "required": [
    "task",
    "workspaceFolder"
  ]
}
```

#### `get_terminal_output`

**Description:**

```
Get the output of a terminal command previously started with run_in_terminal
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "The ID of the terminal to check."
    }
  },
  "required": [
    "id"
  ]
}
```

#### `kill_terminal`

**Description:**

```
Kill a terminal by its ID. Use this to clean up terminals that are no longer needed (e.g., after stopping a server or when a long-running task completes). The terminal ID is returned by run_in_terminal when isBackground=true.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "The ID of the background terminal to kill (returned by run_in_terminal when isBackground=true)."
    }
  },
  "required": [
    "id"
  ]
}
```

#### `run_in_terminal`

**Description:**

```
This tool allows you to execute shell commands in a persistent zsh terminal session, preserving environment variables, working directory, and other context across multiple commands.

Command Execution:
- Use && to chain simple commands on one line
- Prefer pipelines | over temporary files for data flow
- Never create a sub-shell (eg. bash -c "command") unless explicitly asked

Directory Management:
- Prefer relative paths when navigating directories, only use absolute when the path is far away or the current cwd is not expected
- Remember when isBackground=false is specified, that shell and cwd is reused until it is moved to the background
- Use $PWD for current directory references
- Consider using pushd/popd for directory stack management
- Supports directory shortcuts like ~ and -

Program Execution:
- Supports Python, Node.js, and other executables
- Install packages via package managers (brew, apt, etc.)
- Use which or command -v to verify command availability

Background Processes:
- For long-running tasks (e.g., servers), set isBackground=true
- Returns a terminal ID for checking status and runtime later

Output Management:
- Output is automatically truncated if longer than 60KB to prevent context overflow
- Use head, tail, grep, awk to filter and limit output size
- For pager commands, disable paging: git --no-pager or add | cat
- Use wc -l to count lines before displaying large outputs

Best Practices:
- Quote variables: "$var" instead of $var to handle spaces
- Use find with -exec or xargs for file operations
- Be specific with commands to avoid excessive output
- Avoid printing credentials unless absolutely required
- Use type to check command type (builtin, function, alias)
- Use jobs, fg, bg for job control
- Use [[ ]] for conditional tests instead of [ ]
- Prefer $() over backticks for command substitution
- Use setopt errexit for strict error handling
- Take advantage of zsh globbing features (**, extended globs)
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "description": "The command to run in the terminal."
    },
    "explanation": {
      "type": "string",
      "description": "A one-sentence description of what the command does. This will be shown to the user before the command is run."
    },
    "goal": {
      "type": "string",
      "description": "A short description of the goal or purpose of the command (e.g., \"Install dependencies\", \"Start development server\")."
    },
    "isBackground": {
      "type": "boolean",
      "description": "Whether the command starts a background process.\n\n- If true, a new shell will be spawned where the cwd is the workspace directory and will run asynchronously in the background and you will not see the output.\n\n- If false, a single shell is shared between all non-background terminals where the cwd starts at the workspace directory and is remembered until that terminal is moved to the background, the tool call will block on the command finishing and only then you will get the output.\n\nExamples of background processes: building in watch mode, starting a server. You can check the output of a background process later on by using get_terminal_output."
    },
    "timeout": {
      "type": "number",
      "description": "An optional timeout in milliseconds. When provided, the tool will stop tracking the command after this duration and return the output collected so far. Be conservative with the timeout duration, give enough time that the command would complete on a low-end machine. Use 0 for no timeout. If it's not clear how long the command will take then use 0 to avoid prematurely terminating it, never guess too low."
    }
  },
  "required": [
    "command",
    "explanation",
    "goal",
    "isBackground",
    "timeout"
  ]
}
```

#### `terminal_last_command`

**Description:**

```
Get the last command run in the active terminal.
```

#### `terminal_selection`

**Description:**

```
Get the current selection in the active terminal.
```

---

### Web (2 tools)

#### `fetch_webpage`

**Description:**

```
Fetches the main content from a web page. This tool is useful for summarizing or analyzing the content of a webpage. You should use this tool when you think the user is looking for information from a specific webpage.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "urls": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "An array of URLs to fetch content from."
    },
    "query": {
      "type": "string",
      "description": "The query to search for in the web page's content. This should be a clear and concise description of the content you want to find."
    }
  },
  "required": [
    "urls",
    "query"
  ]
}
```

#### `open_simple_browser`

**Description:**

```
Preview a website or open a URL in the editor's Simple Browser. Useful for quickly viewing locally hosted websites, demos, or resources without leaving the coding environment.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "url": {
      "type": "string",
      "description": "The website URL to preview or open in the Simple Browser inside the editor. Must be either an http or https URL"
    }
  },
  "required": [
    "url"
  ]
}
```

---

### Planning (1 tools)

#### `manage_todo_list`

**Description:**

```
Updates the task plan.
Provide an optional explanation and a list of plan items, each with a step and status.
At most one step can be in_progress at a time.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "todoList": {
      "type": "array",
      "description": "Complete array of all todo items. Must include ALL items - both existing and new.",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "number",
            "description": "Unique identifier for the todo. Use sequential numbers starting from 1."
          },
          "title": {
            "type": "string",
            "description": "Concise action-oriented todo label (3-7 words). Displayed in UI."
          },
          "status": {
            "type": "string",
            "enum": [
              "not-started",
              "in-progress",
              "completed"
            ],
            "description": "not-started: Not begun | in-progress: Currently working (max 1) | completed: Fully finished with no blockers"
          }
        },
        "required": [
          "id",
          "title",
          "status"
        ]
      }
    }
  },
  "required": [
    "todoList"
  ]
}
```

---

### Questions (1 tools)

#### `ask_questions`

**Description:**

```
Ask the user questions to clarify intent, validate assumptions, or choose between implementation approaches. Prefer proposing a sensible default so users can confirm quickly.

Only use this tool when the user's answer provides information you cannot determine or reasonably assume yourself. This tool is for gathering information, not for reporting status or problems. If a question has an obvious best answer, take that action instead of asking.

When to use:
- Clarify ambiguous requirements before proceeding
- Get user preferences on implementation choices
- Confirm decisions that meaningfully affect outcome

When NOT to use:
- The answer is determinable from code or context
- Asking for permission to continue or abort
- Confirming something you can reasonably decide yourself
- Reporting a problem (instead, attempt to resolve it)

Question guidelines:
- NEVER use `recommended` for quizzes or polls. Recommended options are PRE-SELECTED and visible to users, which would reveal answers
- Batch related questions into a single call (max 4 questions, 2-6 options each; omit options for free text input)
- Provide brief context explaining what is being decided and why
- Only mark an option as `recommended` to suggest YOUR preferred implementation choice
- Keep options mutually exclusive for single-select; use `multiSelect: true` only when choices are additive and phrase the question accordingly

After receiving answers:
- Incorporate decisions and continue without re-asking unless requirements change

An "Other" option is automatically shown to users—do not add your own.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "questions": {
      "type": "array",
      "description": "Array of 1-4 questions to ask the user",
      "minItems": 1,
      "maxItems": 4,
      "items": {
        "type": "object",
        "properties": {
          "header": {
            "type": "string",
            "description": "A short label (max 12 chars) displayed as a quick pick header, also used as the unique identifier for the question",
            "maxLength": 12
          },
          "question": {
            "type": "string",
            "description": "The complete question text to display"
          },
          "multiSelect": {
            "type": "boolean",
            "description": "Allow multiple selections",
            "default": false
          },
          "options": {
            "type": "array",
            "description": "0-6 options for the user to choose from. If empty or omitted, shows a free text input instead.",
            "minItems": 0,
            "maxItems": 6,
            "items": {
              "type": "object",
              "properties": {
                "label": {
                  "type": "string",
                  "description": "Option label text"
                },
                "description": {
                  "type": "string",
                  "description": "Optional description for the option"
                },
                "recommended": {
                  "type": "boolean",
                  "description": "Mark this option as recommended"
                }
              },
              "required": [
                "label"
              ]
            }
          },
          "allowFreeformInput": {
            "type": "boolean",
            "description": "When true, allows user to enter free-form text in addition to selecting options. Use when the user's opinion or custom input would be valuable.",
            "default": false
          }
        },
        "required": [
          "header",
          "question"
        ]
      }
    }
  },
  "required": [
    "questions"
  ]
}
```

---

### Multi Agent (1 tools)

#### `runSubagent`

**Description:**

```
Launch a new agent to handle complex, multi-step tasks autonomously. This tool is good at researching complex questions, searching for code, and executing multi-step tasks. When you are searching for a keyword or file and are not confident that you will find the right match in the first few tries, use this agent to perform the search for you.

- Agents do not run async or in the background, you will wait for the agent's result.
- When the agent is done, it will return a single message back to you. The result returned by the agent is not visible to the user. To show the user the result, you should send a text message back to the user with a concise summary of the result.
- Each agent invocation is stateless. You will not be able to send additional messages to the agent, nor will the agent be able to communicate with you outside of its final report. Therefore, your prompt should contain a highly detailed task description for the agent to perform autonomously and you should specify exactly what information the agent should return back to you in its final and only message to you.
- The agent's outputs should generally be trusted
- Clearly tell the agent whether you expect it to write code or just to do research (search, file reads, web fetches, etc.), since it is not aware of the user's intent
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "prompt": {
      "type": "string",
      "description": "A detailed description of the task for the agent to perform"
    },
    "description": {
      "type": "string",
      "description": "A short (3-5 word) description of the task"
    }
  },
  "required": [
    "prompt",
    "description"
  ]
}
```

---

### Vscode (10 tools)

#### `create_new_workspace`

**Description:**

```
Get comprehensive setup steps to help the user create complete project structures in a VS Code workspace. This tool is designed for full project initialization and scaffolding, not for creating individual files.

When to use this tool:
- User wants to create a new complete project from scratch
- Setting up entire project frameworks (TypeScript projects, React apps, Node.js servers, etc.)
- Initializing Model Context Protocol (MCP) servers with full structure
- Creating VS Code extensions with proper scaffolding
- Setting up Next.js, Vite, or other framework-based projects
- User asks for "new project", "create a workspace", "set up a [framework] project"
- Need to establish complete development environment with dependencies, config files, and folder structure

When NOT to use this tool:
- Creating single files or small code snippets
- Adding individual files to existing projects
- Making modifications to existing codebases
- User asks to "create a file" or "add a component"
- Simple code examples or demonstrations
- Debugging or fixing existing code

This tool provides complete project setup including:
- Folder structure creation
- Package.json and dependency management
- Configuration files (tsconfig, eslint, etc.)
- Initial boilerplate code
- Development environment setup
- Build and run instructions

Use other file creation tools for individual files within existing projects.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The query to use to generate the new workspace. This should be a clear and concise description of the workspace the user wants to create."
    }
  },
  "required": [
    "query"
  ]
}
```

#### `get_changed_files`

**Description:**

```
Get git diffs of current file changes in a git repository. Don't forget that you can use run_in_terminal to run git commands in a terminal as well.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "repositoryPath": {
      "type": "string",
      "description": "The absolute path to the git repository to look for changes in. If not provided, the active git repository will be used."
    },
    "sourceControlState": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "staged",
          "unstaged",
          "merge-conflicts"
        ]
      },
      "description": "The kinds of git state to filter by. Allowed values are: 'staged', 'unstaged', and 'merge-conflicts'. If not provided, all states will be included."
    }
  }
}
```

#### `get_errors`

**Description:**

```
Get any compile or lint errors in a specific file or across all files. If the user mentions errors or problems in a file, they may be referring to these. Use the tool to see the same errors that the user is seeing. If the user asks you to analyze all errors, or does not specify a file, use this tool to gather errors for all files. Also use this tool after editing a file to validate the change.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "filePaths": {
      "description": "The absolute paths to the files or folders to check for errors. Omit 'filePaths' when retrieving all errors.",
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

#### `get_project_setup_info`

**Description:**

```
Do not call this tool without first calling the tool to create a workspace. This tool provides a project setup information for a Visual Studio Code workspace based on a project type and programming language.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "projectType": {
      "type": "string",
      "description": "The type of project to create. Supported values are: 'python-script', 'python-project', 'mcp-server', 'model-context-protocol-server', 'vscode-extension', 'next-js', 'vite' and 'other'"
    }
  },
  "required": [
    "projectType"
  ]
}
```

#### `get_search_view_results`

**Description:**

```
The results from the search view
```

#### `get_vscode_api`

**Description:**

```
Get comprehensive VS Code API documentation and references for extension development. This tool provides authoritative documentation for VS Code's extensive API surface, including proposed APIs, contribution points, and best practices. Use this tool for understanding complex VS Code API interactions.

When to use this tool:
- User asks about specific VS Code APIs, interfaces, or extension capabilities
- Need documentation for VS Code extension contribution points (commands, views, settings, etc.)
- Questions about proposed APIs and their usage patterns
- Understanding VS Code extension lifecycle, activation events, and packaging
- Best practices for VS Code extension development architecture
- API examples and code patterns for extension features
- Troubleshooting extension-specific issues or API limitations

When NOT to use this tool:
- Creating simple standalone files or scripts unrelated to VS Code extensions
- General programming questions not specific to VS Code extension development
- Questions about using VS Code as an editor (user-facing features)
- Non-extension related development tasks
- File creation or editing that doesn't involve VS Code extension APIs

CRITICAL usage guidelines:
1. Always include specific API names, interfaces, or concepts in your query
2. Mention the extension feature you're trying to implement
3. Include context about proposed vs stable APIs when relevant
4. Reference specific contribution points when asking about extension manifest
5. Be specific about the VS Code version or API version when known

Scope: This tool is for EXTENSION DEVELOPMENT ONLY - building tools that extend VS Code itself, not for general file creation or non-extension programming tasks.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The query to search vscode documentation for. Should contain all relevant context."
    }
  },
  "required": [
    "query"
  ]
}
```

#### `install_extension`

**Description:**

```
Install an extension in VS Code. Use this tool to install an extension in Visual Studio Code as part of a new workspace creation process only.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "The ID of the extension to install. This should be in the format <publisher>.<extension>."
    },
    "name": {
      "type": "string",
      "description": "The name of the extension to install. This should be a clear and concise description of the extension."
    }
  },
  "required": [
    "id",
    "name"
  ]
}
```

#### `run_vscode_command`

**Description:**

```
Run a command in VS Code. Use this tool to run a command in Visual Studio Code as part of a new workspace creation process only.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "commandId": {
      "type": "string",
      "description": "The ID of the command to execute. This should be in the format <command>."
    },
    "name": {
      "type": "string",
      "description": "The name of the command to execute. This should be a clear and concise description of the command."
    },
    "args": {
      "type": "array",
      "description": "The arguments to pass to the command. This should be an array of strings.",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "commandId",
    "name"
  ]
}
```

#### `test_failure`

**Description:**

```
Includes test failure information in the prompt.
```

#### `vscode_searchExtensions_internal`

**Description:**

```
This is a tool for browsing Visual Studio Code Extensions Marketplace. It allows the model to search for extensions and retrieve detailed information about them. The model should use this tool whenever it needs to discover extensions or resolve information about known ones. To use the tool, the model has to provide the category of the extensions, relevant search keywords, or known extension IDs. Note that search results may include false positives, so reviewing and filtering is recommended.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "category": {
      "type": "string",
      "description": "The category of extensions to search for",
      "enum": [
        "AI",
        "Azure",
        "Chat",
        "Data Science",
        "Debuggers",
        "Extension Packs",
        "Education",
        "Formatters",
        "Keymaps",
        "Language Packs",
        "Linters",
        "Machine Learning",
        "Notebooks",
        "Programming Languages",
        "SCM Providers",
        "Snippets",
        "Testing",
        "Themes",
        "Visualization",
        "Other"
      ]
    },
    "keywords": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "The keywords to search for"
    },
    "ids": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "The ids of the extensions to search for"
    }
  }
}
```

---

### Mcp (13 tools)

#### `mcp_pylance_mcp_s_pylanceDocString`

**Description:**

```
Get the docstring/documentation for a Python symbol. Returns the docstring content for functions, classes, methods, or variables. Use when: you need to understand what a symbol does, check documentation before using a function, explain code behavior to users, or validate symbol purpose. Example: To understand foo_bar function, provide its file URI and symbol name "foo_bar".
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "fileUri": {
      "type": "string",
      "description": "The uri of the file containing the symbol."
    },
    "symbolName": {
      "type": "string",
      "description": "The name of the symbol (function, class, method, variable) to get the docstring for. This should be the exact symbol name as it appears in the code."
    }
  },
  "required": [
    "fileUri",
    "symbolName"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceDocuments`

**Description:**

```
Search Pylance documentation for Python language server help, configuration guidance, feature explanations, and troubleshooting. Returns comprehensive answers about Pylance settings, capabilities, and usage. Use when users ask: How to configure Pylance? What features are available? How to fix Pylance issues?
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "search": {
      "type": "string",
      "description": "Detailed question in natural language. Think of it as a prompt for an LLM. Do not use keyword search terms."
    }
  },
  "required": [
    "search"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceFileSyntaxErrors`

**Description:**

```
Check Python file for syntax errors. Returns detailed error list with line numbers, messages, and error types. Use when: users report syntax problems, validating files before processing, debugging parse errors.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "workspaceRoot": {
      "type": "string",
      "description": "The root directory uri of the workspace."
    },
    "fileUri": {
      "type": "string",
      "description": "The uri of the file to check for syntax errors. Must be a user file in the workspace."
    }
  },
  "required": [
    "workspaceRoot",
    "fileUri"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceImports`

**Description:**

```
Analyze imports across workspace user files. Returns all top-level module names imported, including resolved and unresolved imports. Use for: finding missing dependencies, understanding project dependencies, analyzing import patterns.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "workspaceRoot": {
      "type": "string",
      "description": "The root directory uri of the workspace."
    }
  },
  "required": [
    "workspaceRoot"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceInstalledTopLevelModules`

**Description:**

```
Get available top-level modules from installed Python packages in environment. Shows what can be imported. Use for: checking if packages are installed, verifying import availability, helping users understand available modules.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "workspaceRoot": {
      "type": "string",
      "description": "The root directory uri of the workspace."
    },
    "pythonEnvironment": {
      "type": "string",
      "description": "The Python environment to use. Must be a value returned by the pylancePythonEnvironments tool. If pythonEnvironment is missing, the python environment of the workspace will be used."
    }
  },
  "required": [
    "workspaceRoot"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceInvokeRefactoring`

**Description:**

```
Apply automated code refactoring to Python files. Returns refactored content (does not modify original file) unless mode is "update". Use for: extracting functions, organizing imports, improving code structure, applying refactoring patterns.  Optional "mode" parameter: "update" updates the file, "edits" returns a WorkspaceEdit, "string" returns updated content as string. If mode is not specified, "update" will be used as the default. The "edits" mode is helpful for determining if a file needs changes (for example, to remove unused imports or fix import formatting) without making any modifications; if no changes are needed, the result will be either an empty WorkspaceEdit or a message indicating that no text edits were found. Available refactorings: source.unusedImports: - Removes all unused import statements from a Python file. Use when imports are imported but never referenced in the code. Requires fileUri parameter pointing to a Python file with unused imports.
source.convertImportFormat: - Converts import statements between absolute and relative formats according to python.analysis.importFormat setting. Use when import format consistency is needed. Requires fileUri parameter pointing to a Python file with imports to convert.
source.convertImportStar: - Converts all wildcard imports (from module import *) to explicit imports listing all imported symbols. Use when explicit imports are preferred for better code clarity and IDE support. Requires fileUri parameter pointing to a Python file with wildcard imports.
source.convertImportToModule: - Converts `from module import name1, name2` (including wildcard imports) into `import module` and rewrites references to `module.name1`, `module.name2`. Use when you want module-qualified references. Requires fileUri parameter pointing to a Python file with `from ... import ...` statements.
source.renameShadowedStdlibImports: - Renames imported user modules that shadow standard library module names (e.g. a local calendar.py). Use to avoid import shadowing bugs. Requires fileUri parameter pointing to the importing Python file.
source.addTypeAnnotation: - Adds type annotations to all variables and functions in a Python file that can be inferred from their usage. Use when type hints are needed for better type checking and code clarity. Requires fileUri parameter pointing to a Python file with unannotated variables or functions.
source.fixAll.pylance: - Applies all available automatic code fixes from python.analysis.fixAll setting. Use when multiple code issues need to be addressed simultaneously. Requires fileUri parameter pointing to a Python file with fixable issues.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "fileUri": {
      "type": "string",
      "description": "The uri of the file to invoke the refactoring."
    },
    "name": {
      "type": "string",
      "description": "The name of the refactoring to invoke. This must be one of these [source.unusedImports, source.convertImportFormat, source.convertImportStar, source.convertImportToModule, source.renameShadowedStdlibImports, source.addTypeAnnotation, source.fixAll.pylance]"
    },
    "mode": {
      "type": "string",
      "enum": [
        "update",
        "edits",
        "string"
      ],
      "description": "Determines the output mode: \"update\" updates the file directly, \"edits\" returns a WorkspaceEdit, \"string\" returns the updated content as a string. If omitted, \"update\" will be used as the default. The \"edits\" mode is especially useful for checking if any changes are needed (such as unused imports or import formatting issues) without modifying the file, as it will return a WorkspaceEdit only if edits are required."
    }
  },
  "required": [
    "fileUri",
    "name"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylancePythonEnvironments`

**Description:**

```
Get Python environment information for workspace: current active environment and all available environments. Use for: Python environment issues, switching environments, understanding Python setup.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "workspaceRoot": {
      "type": "string",
      "description": "The root directory uri of the workspace."
    }
  },
  "required": [
    "workspaceRoot"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceRunCodeSnippet`

**Description:**

```
Execute Python code snippets directly in the workspace environment. PREFERRED over terminal commands for running Python code. This tool automatically uses the correct Python interpreter configured for the workspace, eliminates shell escaping/quoting problems that plague terminal execution, and provides clean, properly formatted output with stdout/stderr correctly interleaved. Use this instead of `python -c "code"` or terminal commands when running Python snippets. Ideal for: testing code, running quick scripts, validating Python expressions, checking imports, and any Python execution within the workspace context. No temporary files needed - code runs directly in memory.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "workspaceRoot": {
      "type": "string",
      "description": "The root directory uri of the workspace."
    },
    "codeSnippet": {
      "type": "string",
      "description": "The code snippet to run."
    },
    "workingDirectory": {
      "type": "string",
      "description": "The working directory to use for the code snippet. If the code snippet is pulled from a file, this should be the directory for the file. Especially if the snippet has imports."
    },
    "timeout": {
      "type": "number",
      "minimum": 0,
      "description": "The timeout for the code snippet execution."
    }
  },
  "required": [
    "workspaceRoot",
    "codeSnippet"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceSettings`

**Description:**

```
Get current Python analysis settings and configuration for a workspace. Returns all "python.analysis.*" settings with default vs user-configured indicators. Use for: troubleshooting configuration, checking current settings, diagnosing analysis issues.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "workspaceRoot": {
      "type": "string",
      "description": "The root directory uri of the workspace."
    }
  },
  "required": [
    "workspaceRoot"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceSyntaxErrors`

**Description:**

```
Validate Python code snippets for syntax errors without saving to file. Returns syntax error details with line numbers and descriptions. Use for: validating generated code, checking user code snippets, pre-execution validation.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "code": {
      "type": "string",
      "description": "The Python code to check for syntax errors."
    },
    "pythonVersion": {
      "type": "string",
      "description": "The version of Python to use for the syntax check. Must be a valid Python version string. ex) \"3.10\" or \"3.11.4\"."
    }
  },
  "required": [
    "code",
    "pythonVersion"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceUpdatePythonEnvironment`

**Description:**

```
Switch active Python environment for workspace to different Python installation or virtual environment. Updates settings and ensures subsequent operations use new environment. Use for: changing Python versions, switching to virtual environments, resolving environment issues.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "workspaceRoot": {
      "type": "string",
      "description": "The root directory uri of the workspace."
    },
    "pythonEnvironment": {
      "type": "string",
      "description": "The Python environment to use. Must be either a value returned by the pylancePythonEnvironments tool or the absolute path to a Python executable."
    }
  },
  "required": [
    "workspaceRoot",
    "pythonEnvironment"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceWorkspaceRoots`

**Description:**

```
Get workspace root directories. Returns workspace root for specific file or all workspace roots if no file provided. Use for: understanding workspace structure, getting paths for other operations.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "fileUri": {
      "type": "string",
      "description": "The uri of the file to check its workspace"
    }
  },
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

#### `mcp_pylance_mcp_s_pylanceWorkspaceUserFiles`

**Description:**

```
Get list of all user Python files in workspace (excludes library/dependency files). Respects python.analysis.include/exclude settings. Use for: analyzing user code, searching project files, operating on user-created Python files.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "workspaceRoot": {
      "type": "string",
      "description": "The root directory uri of the workspace."
    }
  },
  "required": [
    "workspaceRoot"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

---

## Mode Delta: Tool Changes

### agent → ask

**Removed (65):** `apply_patch`, `ask_questions`, `await_terminal`, `configure_non_python_notebook`, `configure_notebook`, `configure_python_environment`, `configure_python_notebook`, `container-tools_get-config`, `copilot_getNotebookSummary`, `create_and_run_task`, `create_directory`, `create_file`, `create_new_jupyter_notebook`, `create_new_workspace`, `edit_notebook_file`, `fetch_webpage`, `file_search`, `get-syntax-docs-mermaid`, `get_changed_files`, `get_errors`, `get_project_setup_info`, `get_python_environment_details`, `get_python_executable_details`, `get_search_view_results`, `get_terminal_output`, `get_vscode_api`, `github_repo`, `grep_search`, `install_extension`, `install_python_packages`, `kill_terminal`, `list_code_usages`, `list_dir`, `manage_todo_list`, `mcp_pylance_mcp_s_pylanceDocString`, `mcp_pylance_mcp_s_pylanceDocuments`, `mcp_pylance_mcp_s_pylanceFileSyntaxErrors`, `mcp_pylance_mcp_s_pylanceImports`, `mcp_pylance_mcp_s_pylanceInstalledTopLevelModules`, `mcp_pylance_mcp_s_pylanceInvokeRefactoring`, `mcp_pylance_mcp_s_pylancePythonEnvironments`, `mcp_pylance_mcp_s_pylanceRunCodeSnippet`, `mcp_pylance_mcp_s_pylanceSettings`, `mcp_pylance_mcp_s_pylanceSyntaxErrors`, `mcp_pylance_mcp_s_pylanceUpdatePythonEnvironment`, `mcp_pylance_mcp_s_pylanceWorkspaceRoots`, `mcp_pylance_mcp_s_pylanceWorkspaceUserFiles`, `mermaid-diagram-preview`, `mermaid-diagram-validator`, `notebook_install_packages`, `notebook_list_packages`, `open_simple_browser`, `read_file`, `read_notebook_cell_output`, `renderMermaidDiagram`, `restart_notebook_kernel`, `runSubagent`, `run_in_terminal`, `run_notebook_cell`, `run_vscode_command`, `semantic_search`, `terminal_last_command`, `terminal_selection`, `test_failure`, `vscode_searchExtensions_internal`

### agent → plan

**Removed (43):** `apply_patch`, `await_terminal`, `configure_notebook`, `configure_python_environment`, `container-tools_get-config`, `create_and_run_task`, `create_directory`, `create_file`, `create_new_jupyter_notebook`, `create_new_workspace`, `edit_notebook_file`, `get-syntax-docs-mermaid`, `get_project_setup_info`, `get_python_environment_details`, `get_python_executable_details`, `get_vscode_api`, `install_extension`, `install_python_packages`, `kill_terminal`, `manage_todo_list`, `mcp_pylance_mcp_s_pylanceDocString`, `mcp_pylance_mcp_s_pylanceDocuments`, `mcp_pylance_mcp_s_pylanceFileSyntaxErrors`, `mcp_pylance_mcp_s_pylanceImports`, `mcp_pylance_mcp_s_pylanceInstalledTopLevelModules`, `mcp_pylance_mcp_s_pylanceInvokeRefactoring`, `mcp_pylance_mcp_s_pylancePythonEnvironments`, `mcp_pylance_mcp_s_pylanceRunCodeSnippet`, `mcp_pylance_mcp_s_pylanceSettings`, `mcp_pylance_mcp_s_pylanceSyntaxErrors`, `mcp_pylance_mcp_s_pylanceUpdatePythonEnvironment`, `mcp_pylance_mcp_s_pylanceWorkspaceRoots`, `mcp_pylance_mcp_s_pylanceWorkspaceUserFiles`, `mermaid-diagram-preview`, `mermaid-diagram-validator`, `notebook_install_packages`, `notebook_list_packages`, `open_simple_browser`, `renderMermaidDiagram`, `run_in_terminal`, `run_notebook_cell`, `run_vscode_command`, `vscode_searchExtensions_internal`

### ask → plan

**Added (22):** `ask_questions`, `configure_non_python_notebook`, `configure_python_notebook`, `copilot_getNotebookSummary`, `fetch_webpage`, `file_search`, `get_changed_files`, `get_errors`, `get_search_view_results`, `get_terminal_output`, `github_repo`, `grep_search`, `list_code_usages`, `list_dir`, `read_file`, `read_notebook_cell_output`, `restart_notebook_kernel`, `runSubagent`, `semantic_search`, `terminal_last_command`, `terminal_selection`, `test_failure`

## Tool Invocation Patterns

Tools actually called during captured sessions:

### agent mode

**Call sequence:**

1. Turn 2: `list_dir`
1. Turn 4: `create_file`
1. Turn 6: `get_errors`
1. Turn 8: `apply_patch`
1. Turn 9: `get_errors`

**Call frequency:**

- `get_errors`: 2x
- `list_dir`: 1x
- `create_file`: 1x
- `apply_patch`: 1x

### ask mode

*No tool calls observed.*

### plan mode

**Call sequence:**

1. Turn 2: `runSubagent`
1. Turn 3: `list_dir`
1. `file_search`
1. Turn 4: `list_dir`
1. `list_dir`
1. `file_search`
1. `file_search`
1. Turn 6: `ask_questions`

**Call frequency:**

- `list_dir`: 3x
- `file_search`: 3x
- `runSubagent`: 1x
- `ask_questions`: 1x
