# Tool Catalog: Codex CLI

## Summary

| Mode | Total | File Write | Shell | Planning | Questions | Misc |
|------|-------|-|-|-|-|-|
| agent | 5 | 1 | 1 | 1 | 1 | 1 |
| plan | 5 | 1 | 1 | 1 | 1 | 1 |

## Full Tool Catalog (agent mode — 5 tools)

### File Write (1 tools)

#### `write_stdin`

**Description:**

```
Writes characters to an existing unified exec session and returns recent output.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "chars": {
      "type": "string",
      "description": "Bytes to write to stdin (may be empty to poll)."
    },
    "max_output_tokens": {
      "type": "number",
      "description": "Maximum number of tokens to return. Excess output will be truncated."
    },
    "session_id": {
      "type": "number",
      "description": "Identifier of the running unified exec session."
    },
    "yield_time_ms": {
      "type": "number",
      "description": "How long to wait (in milliseconds) for output before yielding."
    }
  },
  "required": [
    "session_id"
  ],
  "additionalProperties": false
}
```

---

### Shell (1 tools)

#### `exec_command`

**Description:**

```
Runs a command in a PTY, returning output or a session ID for ongoing interaction.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "cmd": {
      "type": "string",
      "description": "Shell command to execute."
    },
    "justification": {
      "type": "string",
      "description": "Only set if sandbox_permissions is \\\"require_escalated\\\".\n                    Request approval from the user to run this command outside the sandbox.\n                    Phrased as a simple question that summarizes the purpose of the\n                    command as it relates to the task at hand - e.g. 'Do you want to\n                    fetch and pull the latest version of this git branch?'"
    },
    "login": {
      "type": "boolean",
      "description": "Whether to run the shell with -l/-i semantics. Defaults to true."
    },
    "max_output_tokens": {
      "type": "number",
      "description": "Maximum number of tokens to return. Excess output will be truncated."
    },
    "prefix_rule": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Only specify when sandbox_permissions is `require_escalated`.\n                        Suggest a prefix command pattern that will allow you to fulfill similar requests from the user in the future.\n                        Should be a short but reasonable prefix, e.g. [\\\"git\\\", \\\"pull\\\"] or [\\\"uv\\\", \\\"run\\\"] or [\\\"pytest\\\"]."
    },
    "sandbox_permissions": {
      "type": "string",
      "description": "Sandbox permissions for the command. Set to \"require_escalated\" to request running without sandbox restrictions; defaults to \"use_default\"."
    },
    "shell": {
      "type": "string",
      "description": "Shell binary to launch. Defaults to the user's default shell."
    },
    "tty": {
      "type": "boolean",
      "description": "Whether to allocate a TTY for the command. Defaults to false (plain pipes); set to true to open a PTY and access TTY process."
    },
    "workdir": {
      "type": "string",
      "description": "Optional working directory to run the command in; defaults to the turn cwd."
    },
    "yield_time_ms": {
      "type": "number",
      "description": "How long to wait (in milliseconds) for output before yielding."
    }
  },
  "required": [
    "cmd"
  ],
  "additionalProperties": false
}
```

---

### Planning (1 tools)

#### `update_plan`

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
    "explanation": {
      "type": "string"
    },
    "plan": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "status": {
            "type": "string",
            "description": "One of: pending, in_progress, completed"
          },
          "step": {
            "type": "string"
          }
        },
        "required": [
          "step",
          "status"
        ],
        "additionalProperties": false
      },
      "description": "The list of steps"
    }
  },
  "required": [
    "plan"
  ],
  "additionalProperties": false
}
```

---

### Questions (1 tools)

#### `request_user_input`

**Description:**

```
Request user input for one to three short questions and wait for the response. This tool is only available in Plan mode.
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "questions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "header": {
            "type": "string",
            "description": "Short header label shown in the UI (12 or fewer chars)."
          },
          "id": {
            "type": "string",
            "description": "Stable identifier for mapping answers (snake_case)."
          },
          "options": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "description": {
                  "type": "string",
                  "description": "One short sentence explaining impact/tradeoff if selected."
                },
                "label": {
                  "type": "string",
                  "description": "User-facing label (1-5 words)."
                }
              },
              "required": [
                "label",
                "description"
              ],
              "additionalProperties": false
            },
            "description": "Provide 2-3 mutually exclusive choices. Put the recommended option first and suffix its label with \"(Recommended)\". Do not include an \"Other\" option in this list; the client will add a free-form \"Other\" option automatically."
          },
          "question": {
            "type": "string",
            "description": "Single-sentence prompt shown to the user."
          }
        },
        "required": [
          "id",
          "header",
          "question",
          "options"
        ],
        "additionalProperties": false
      },
      "description": "Questions to show the user. Prefer 1 and do not exceed 3"
    }
  },
  "required": [
    "questions"
  ],
  "additionalProperties": false
}
```

---

### Misc (1 tools)

#### `view_image`

**Description:**

```
View a local image from the filesystem (only use if given a full filepath by the user, and the image isn't already attached to the thread context within <image ...> tags).
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Local filesystem path to an image file"
    }
  },
  "required": [
    "path"
  ],
  "additionalProperties": false
}
```

---

## Mode Delta: Tool Changes

### agent → plan

Tool set identical across both modes.

## Tool Invocation Patterns

Tools actually called during captured sessions:

### agent mode

**Call sequence:**

1. Turn 1: `exec_command`
1. `exec_command`
1. Turn 2: `exec_command`
1. `exec_command`
1. Turn 4: `exec_command`
1. `exec_command`
1. Turn 5: `exec_command`
1. `exec_command`

**Call frequency:**

- `exec_command`: 8x

### plan mode

**Call sequence:**

1. Turn 1: `exec_command`
1. `exec_command`

**Call frequency:**

- `exec_command`: 2x
