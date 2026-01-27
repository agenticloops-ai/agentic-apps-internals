# GitHub Copilot Agent Mode Tools

## Core Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `apply_patch` | Edit text files using V4A diff format | `input`, `explanation` |
| `create_directory` | Create directory structure (like mkdir -p) | `dirPath` |
| `create_file` | Create new file with content | `filePath`, `content` |
| `create_new_jupyter_notebook` | Generate new Jupyter Notebook | `query` |
| `create_new_workspace` | Full project scaffolding and setup | `query` |
| `edit_notebook_file` | Edit existing Jupyter notebook cells | `filePath`, `editType`, `cellId` |
| `fetch_webpage` | Fetch and analyze web page content | `urls`, `query` |
| `file_search` | Search files by glob pattern | `query` |
| `grep_search` | Fast text/regex search in workspace | `query`, `isRegexp` |
| `get_changed_files` | Get git diffs of file changes | None |
| `get_errors` | Get compile/lint errors | None |
| `copilot_getNotebookSummary` | Get notebook cell list with metadata | `filePath` |
| `get_project_setup_info` | Get project setup info by type | `projectType` |
| `get_search_view_results` | Get results from search view | None |
| `get_vscode_api` | VS Code API documentation for extensions | `query` |
| `github_repo` | Search GitHub repo for code snippets | `repo`, `query` |
| `install_extension` | Install VS Code extension | `id`, `name` |
| `list_code_usages` | Find all usages of a symbol | `symbolName` |
| `list_dir` | List directory contents | `path` |
| `open_simple_browser` | Preview URL in VS Code browser | `url` |
| `read_file` | Read file contents (truncates at 2000 lines) | `filePath` |
| `read_notebook_cell_output` | Get notebook cell output | `filePath`, `cellId` |
| `run_notebook_cell` | Execute notebook code cell | `filePath`, `cellId` |
| `run_vscode_command` | Run VS Code command | `commandId`, `name` |
| `semantic_search` | Natural language code search | `query` |
| `test_failure` | Include test failure info | None |
| `vscode_searchExtensions_internal` | Search VS Code marketplace | None |
| `create_and_run_task` | Create/run VS Code tasks | `task`, `workspaceFolder` |
| `get_terminal_output` | Get output from terminal command | `id` |
| `manage_todo_list` | Track tasks and progress | `operation` |
| `run_in_terminal` | Execute shell commands | `command`, `explanation`, `isBackground` |
| `runSubagent` | Launch autonomous sub-agent | `prompt`, `description` |
| `runTests` | Run unit tests with optional coverage | None |
| `terminal_last_command` | Get last terminal command | None |
| `terminal_selection` | Get terminal selection | None |

## Notebook Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `configure_notebook` | Configure notebook settings | None |
| `notebook_install_packages` | Install packages for notebooks | None |
| `notebook_list_packages` | List installed packages | None |

## Python Environment Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `configure_python_environment` | Configure Python environment | None |
| `get_python_environment_details` | Get Python environment info | None |
| `get_python_executable_details` | Get Python executable info | None |
| `install_python_packages` | Install Python packages | None |

## MCP: Docker/Container Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `activate_container_management_tools` | Activate container lifecycle tools (start, stop, restart, remove) | None |
| `activate_image_management_tools` | Activate image tools (pull, remove, inspect, tag) | None |
| `activate_container_inspection_and_logging_tools` | Activate container inspection/logs tools | None |
| `activate_listing_tools_for_containers_images_and_volumes` | Activate listing tools | None |
| `mcp_copilot_conta_list_networks` | List container networks | None |
| `mcp_copilot_conta_prune` | Prune unused container resources | `pruneTarget` |

## MCP: GitKraken Git Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `mcp_gitkraken_git_add_or_commit` | Git add or commit files | `directory`, `action` |
| `mcp_gitkraken_git_blame` | Show git blame for a file | `directory`, `file` |
| `mcp_gitkraken_git_branch` | List or create branches | `directory`, `action` |
| `mcp_gitkraken_git_checkout` | Switch branches | `directory`, `branch` |
| `mcp_gitkraken_git_log_or_diff` | Show commit logs or diffs | `directory`, `action` |
| `mcp_gitkraken_git_push` | Push to remote | `directory` |
| `mcp_gitkraken_git_stash` | Stash changes | `directory` |
| `mcp_gitkraken_git_status` | Show working tree status | `directory` |
| `mcp_gitkraken_git_worktree` | List or add git worktrees | `directory`, `action` |
| `mcp_gitkraken_gitkraken_workspace_list` | List GitKraken workspaces | None |

## MCP: GitKraken Issues Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `mcp_gitkraken_issues_add_comment` | Add comment to an issue | `provider`, `issue_id`, `comment` |
| `mcp_gitkraken_issues_assigned_to_me` | Fetch issues assigned to user | `provider` |
| `mcp_gitkraken_issues_get_detail` | Get issue details | `provider`, `issue_id` |

## MCP: GitKraken Pull Request Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `mcp_gitkraken_pull_request_assigned_to_me` | Search PRs assigned to user | `provider` |
| `mcp_gitkraken_pull_request_create` | Create a new pull request | `repository_name`, `repository_organization`, `title`, `source_branch`, `target_branch`, `provider` |
| `mcp_gitkraken_pull_request_create_review` | Create a PR review | `repository_name`, `repository_organization`, `pull_request_id`, `review`, `provider` |
| `mcp_gitkraken_pull_request_get_comments` | Get PR comments | `repository_name`, `repository_organization`, `pull_request_id`, `provider` |
| `mcp_gitkraken_pull_request_get_detail` | Get PR details | `pull_request_id`, `repository_name`, `repository_organization`, `provider` |
| `mcp_gitkraken_repository_get_file_content` | Get file content from repo | `repository_name`, `repository_organization`, `ref`, `file_path`, `provider` |

## MCP: Pylance Python Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `activate_python_code_validation_and_execution` | Activate Python validation/execution tools | None |
| `activate_import_analysis_and_dependency_management` | Activate import analysis tools | None |
| `activate_python_environment_management` | Activate Python environment tools | None |
| `activate_workspace_structure_and_file_management` | Activate workspace structure tools | None |
| `mcp_pylance_mcp_s_pylanceDocuments` | Search Pylance documentation | `search` |
| `mcp_pylance_mcp_s_pylanceInvokeRefactoring` | Apply automated refactoring | `fileUri`, `name` |
| `mcp_pylance_mcp_s_pylanceRunCodeSnippet` | Execute Python code snippets | `workspaceRoot`, `codeSnippet` |
| `mcp_pylance_mcp_s_pylanceSyntaxErrors` | Validate Python syntax (snippet) | `code`, `pythonVersion` |
| `mcp_pylance_mcp_s_pylanceFileSyntaxErrors` | Check Python file for syntax errors | `workspaceRoot`, `fileUri` |

---

**Total: 68 tools** (35 core + 33 MCP/extension tools)
