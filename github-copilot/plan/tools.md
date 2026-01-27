| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `fetch_webpage` | Fetches main content from web pages for summarizing/analyzing | `urls` (array), `query` (string) |
| `file_search` | Search for files by glob pattern (e.g., `**/*.js`, `src/**`) | `query` (glob pattern) |
| `grep_search` | Fast text/regex search in workspace. Supports regex alternation | `query`, `isRegexp` |
| `get_changed_files` | Get git diffs of current file changes | None |
| `get_errors` | Get compile/lint errors in files or across workspace | None |
| `get_search_view_results` | Get results from the search view | None |
| `github_repo` | Search a GitHub repo for code snippets | `repo`, `query` |
| `list_code_usages` | List all usages/references of a symbol | `symbolName` |
| `list_dir` | List contents of a directory | `path` |
| `read_file` | Read file contents (truncates at 2000 lines) | `filePath` |
| `semantic_search` | Natural language search for code/comments in workspace | `query` |
| `test_failure` | Include test failure information in prompt | None |
| `runSubagent` | Launch autonomous agent for complex multi-step tasks | `prompt`, `description` |