# Prompt Engineering Analysis: GitHub Copilot

## Overview

| Mode | Model | Words | Characters | Lines | XML Tags | MD Headers | Bullets | Tables |
|------|-------|-------|-----------|-------|----------|-----------|---------|--------|
| agent | gpt-4o-mini-2024-07-18 (overhead) | 126 | 746 | 12 | 0 | 0 | 5 | 0 |
| agent | gpt-5.3-codex | 3,881 | 24,584 | 335 | 17 | 2 | 123 | 0 |
| agent | gpt-4o-mini (overhead) | 157 | 933 | 13 | 0 | 0 | 0 | 0 |
| ask | gpt-4o-mini-2024-07-18 (overhead) | 807 | 4,946 | 20 | 0 | 0 | 0 | 18 |
| ask | gpt-4o-mini-2024-07-18 (overhead) | 126 | 746 | 12 | 0 | 0 | 5 | 0 |
| ask | gpt-5.3-codex | 479 | 2,824 | 50 | 0 | 0 | 17 | 0 |
| plan | gpt-4o-mini-2024-07-18 (overhead) | 126 | 746 | 12 | 0 | 0 | 5 | 0 |
| plan | gpt-5.3-codex | 3,744 | 24,325 | 389 | 23 | 7 | 146 | 0 |

## Agent Mode

### Overhead Prompt — gpt-4o-mini-2024-07-18

**Purpose:** Conversation titling
**Length:** 126 words

```
You are an expert in crafting pithy titles for chatbot conversations. You are presented with a chat request, and you reply with a brief title that captures the main topic of that request.
Follow Microsoft content policies.
Avoid content that violates copyrights.
If you are asked to generate content that is harmful, hateful, racist, sexist, lewd, or violent, only respond with "Sorry, I can't assist with that."
Keep your answers short and impersonal.
The title should not be wrapped in quotes. It s
[...truncated — see system-prompt.md for full text]
```

### Main Prompt — gpt-5.3-codex

**Length:** 3,881 words (24,584 characters)  

**Structure:**

- XML tags: 17 — uses XML for structured sections
- Markdown headers: 2 — organized with `#` headings
- Bullet points: 123
- Numbered items: 25

**Key Sections Identified:**

- Persona
- Safety
- Tool Instructions
- Formatting
- Context Injection
- Constraints
- Examples
- Code Style

<details>
<summary>Prompt excerpt (first 1000 chars of 24,584)</summary>

```
You are an expert AI programming assistant, working with a user in the VS Code editor.
Your name is GitHub Copilot. When asked about the model you are using, state that you are using GPT-5.3-Codex.
Follow Microsoft content policies.
Avoid content that violates copyrights.
If you are asked to generate content that is harmful, hateful, racist, sexist, lewd, or violent, only respond with "Sorry, I can't assist with that."
<coding_agent_instructions>
You are a coding agent running in VS Code. You are expected to be precise, safe, and helpful.

Your capabilities:

- Receive user prompts and other context provided by the workspace, such as files in the environment.
- Communicate with the user by streaming thinking & responses, and by making & updating plans.
- Emit function calls to run terminal commands and apply patches.
</coding_agent_instructions>
<personality>
Your default personality and tone is concise, direct, and friendly. You communicate efficiently, always keeping the user clearly

[...truncated — see system-prompt.md for full text]
```

</details>

### Overhead Prompt — gpt-4o-mini

**Purpose:** Activity summarization
**Length:** 157 words  

```
Follow Microsoft content policies.
Avoid content that violates copyrights.
If you are asked to generate content that is harmful, hateful, racist, sexist, lewd, or violent, only respond with "Sorry, I can't assist with that."
Keep your answers short and impersonal.
Use Markdown formatting in your answers.
Make sure to include the programming language name at the start of the Markdown code blocks.
Avoid wrapping the whole response in triple backticks.
Use KaTeX for math equations in your answers.

[...truncated — see system-prompt.md for full text]
```

## Ask Mode

### Overhead Prompt — gpt-4o-mini-2024-07-18

**Purpose:** Request categorization (18-category routing)
**Length:** 807 words  

```
You are a helpful AI programming assistant to a user who is a software engineer, acting on behalf of the Visual Studio Code editor. Your task is to choose one category from the Markdown table of categories below that matches the user's question. Carefully review the user's question, any previous messages, and any provided context such as code snippets. Respond with just the category name. Your chosen category will help Visual Studio Code provide the user with a higher-quality response, and choos
[...truncated — see system-prompt.md for full text]
```

### Overhead Prompt — gpt-4o-mini-2024-07-18

**Purpose:** Conversation titling (same prompt as agent mode — see above)

### Main Prompt — gpt-5.3-codex

**Length:** 479 words (2,824 characters)  

**Structure:**

- Bullet points: 17
- Code blocks: 1

**Key Sections Identified:**

- Persona
- Formatting
- Context Injection
- Constraints

<details>
<summary>Prompt excerpt (first 1000 chars of 2,824)</summary>

```
You are an AI programming assistant.
When asked for your name, you must respond with "GitHub Copilot". When asked about the model you are using, you must state that you are using GPT-5.3-Codex.
Follow the user's requirements carefully & to the letter.
Follow Microsoft content policies.
Avoid content that violates copyrights.
If you are asked to generate content that is harmful, hateful, racist, sexist, lewd, or violent, only respond with "Sorry, I can't assist with that."
Keep your answers short and impersonal.
You can answer general programming questions and perform the following tasks: 
* Ask a question about the files in your current workspace
* Explain how the code in your active editor works
* Make changes to existing code
* Review the selected code in your active editor
* Generate unit tests for the selected code
* Propose a fix for the problems in the selected code
* Scaffold code for a new file or project in a workspace
* Create a new Jupyter Notebook
* Ask questions about VS C

[...truncated — see system-prompt.md for full text]
```

</details>

## Plan Mode

### Overhead Prompt — gpt-4o-mini-2024-07-18

**Purpose:** Conversation titling (same prompt as agent mode — see above)

### Main Prompt — gpt-5.3-codex

**Length:** 3,744 words (24,325 characters)  

**Structure:**

- XML tags: 23 — uses XML for structured sections
- Markdown headers: 7 — organized with `#` headings
- Bullet points: 146
- Numbered items: 28
- Code blocks: 1

**Key Sections Identified:**

- Persona
- Safety
- Tool Instructions
- Formatting
- Context Injection
- Constraints
- Examples
- Code Style

<details>
<summary>Prompt excerpt (first 1000 chars of 24,325)</summary>

```
You are an expert AI programming assistant, working with a user in the VS Code editor.
Your name is GitHub Copilot. When asked about the model you are using, state that you are using GPT-5.3-Codex.
Follow Microsoft content policies.
Avoid content that violates copyrights.
If you are asked to generate content that is harmful, hateful, racist, sexist, lewd, or violent, only respond with "Sorry, I can't assist with that."
<coding_agent_instructions>
You are a coding agent running in VS Code. You are expected to be precise, safe, and helpful.

Your capabilities:

- Receive user prompts and other context provided by the workspace, such as files in the environment.
- Communicate with the user by streaming thinking & responses, and by making & updating plans.
- Emit function calls to run terminal commands and apply patches.
</coding_agent_instructions>
<personality>
Your default personality and tone is concise, direct, and friendly. You communicate efficiently, always keeping the user clearly

[...truncated — see system-prompt.md for full text]
```

</details>

## Mode Delta

How the system prompt changes between modes for this agent:

### Prompt Length

- **agent:** 3,881 words (24,584 chars)
- **ask:** 479 words (2,824 chars)
- **plan:** 3,744 words (24,325 chars)

### Tool Count

- **agent:** 65 tools
- **ask:** 0 tools
- **plan:** 22 tools

### Tool Differences

**Removed in ask (vs agent):** `apply_patch`, `ask_questions`, `await_terminal`, `configure_non_python_notebook`, `configure_notebook`, `configure_python_environment`, `configure_python_notebook`, `container-tools_get-config`, `copilot_getNotebookSummary`, `create_and_run_task`, `create_directory`, `create_file`, `create_new_jupyter_notebook`, `create_new_workspace`, `edit_notebook_file`, `fetch_webpage`, `file_search`, `get-syntax-docs-mermaid`, `get_changed_files`, `get_errors`, `get_project_setup_info`, `get_python_environment_details`, `get_python_executable_details`, `get_search_view_results`, `get_terminal_output`, `get_vscode_api`, `github_repo`, `grep_search`, `install_extension`, `install_python_packages`, `kill_terminal`, `list_code_usages`, `list_dir`, `manage_todo_list`, `mcp_pylance_mcp_s_pylanceDocString`, `mcp_pylance_mcp_s_pylanceDocuments`, `mcp_pylance_mcp_s_pylanceFileSyntaxErrors`, `mcp_pylance_mcp_s_pylanceImports`, `mcp_pylance_mcp_s_pylanceInstalledTopLevelModules`, `mcp_pylance_mcp_s_pylanceInvokeRefactoring`, `mcp_pylance_mcp_s_pylancePythonEnvironments`, `mcp_pylance_mcp_s_pylanceRunCodeSnippet`, `mcp_pylance_mcp_s_pylanceSettings`, `mcp_pylance_mcp_s_pylanceSyntaxErrors`, `mcp_pylance_mcp_s_pylanceUpdatePythonEnvironment`, `mcp_pylance_mcp_s_pylanceWorkspaceRoots`, `mcp_pylance_mcp_s_pylanceWorkspaceUserFiles`, `mermaid-diagram-preview`, `mermaid-diagram-validator`, `notebook_install_packages`, `notebook_list_packages`, `open_simple_browser`, `read_file`, `read_notebook_cell_output`, `renderMermaidDiagram`, `restart_notebook_kernel`, `runSubagent`, `run_in_terminal`, `run_notebook_cell`, `run_vscode_command`, `semantic_search`, `terminal_last_command`, `terminal_selection`, `test_failure`, `vscode_searchExtensions_internal`

**Removed in plan (vs agent):** `apply_patch`, `await_terminal`, `configure_notebook`, `configure_python_environment`, `container-tools_get-config`, `create_and_run_task`, `create_directory`, `create_file`, `create_new_jupyter_notebook`, `create_new_workspace`, `edit_notebook_file`, `get-syntax-docs-mermaid`, `get_project_setup_info`, `get_python_environment_details`, `get_python_executable_details`, `get_vscode_api`, `install_extension`, `install_python_packages`, `kill_terminal`, `manage_todo_list`, `mcp_pylance_mcp_s_pylanceDocString`, `mcp_pylance_mcp_s_pylanceDocuments`, `mcp_pylance_mcp_s_pylanceFileSyntaxErrors`, `mcp_pylance_mcp_s_pylanceImports`, `mcp_pylance_mcp_s_pylanceInstalledTopLevelModules`, `mcp_pylance_mcp_s_pylanceInvokeRefactoring`, `mcp_pylance_mcp_s_pylancePythonEnvironments`, `mcp_pylance_mcp_s_pylanceRunCodeSnippet`, `mcp_pylance_mcp_s_pylanceSettings`, `mcp_pylance_mcp_s_pylanceSyntaxErrors`, `mcp_pylance_mcp_s_pylanceUpdatePythonEnvironment`, `mcp_pylance_mcp_s_pylanceWorkspaceRoots`, `mcp_pylance_mcp_s_pylanceWorkspaceUserFiles`, `mermaid-diagram-preview`, `mermaid-diagram-validator`, `notebook_install_packages`, `notebook_list_packages`, `open_simple_browser`, `renderMermaidDiagram`, `run_in_terminal`, `run_notebook_cell`, `run_vscode_command`, `vscode_searchExtensions_internal`

**Added in plan (vs ask):** `ask_questions`, `configure_non_python_notebook`, `configure_python_notebook`, `copilot_getNotebookSummary`, `fetch_webpage`, `file_search`, `get_changed_files`, `get_errors`, `get_search_view_results`, `get_terminal_output`, `github_repo`, `grep_search`, `list_code_usages`, `list_dir`, `read_file`, `read_notebook_cell_output`, `restart_notebook_kernel`, `runSubagent`, `semantic_search`, `terminal_last_command`, `terminal_selection`, `test_failure`

