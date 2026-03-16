# Contributing

Thanks for your interest in contributing to Agentic Apps Internals! This repo documents AI coding agent internals through captured API traffic analysis.

## How to Contribute

### Report an Issue

Found a factual error, broken link, or inconsistency? [Open an issue](https://github.com/agenticloops-ai/agentic-apps-internals/issues/new) with:
- Which file contains the error
- What the current (incorrect) content says
- What the correct content should be, with evidence (e.g., CSV data, system prompt text)

### Add a New Agent Analysis

Want to contribute an analysis of an agent not yet covered (Cursor, Windsurf, Cline, Aider, etc.)?

1. **Capture traffic** using [AgentLens](https://github.com/agenticloops-ai/agentlens) — see `.tools/alens` for the capture setup
2. **Run all three modes** (or however many the agent supports) with a consistent test task
3. **Export session data** as JSON from AgentLens
4. **Create the directory structure:**
   ```
   agent-name/
   ├── README.md                # Agent summary + session metrics
   ├── PROMPT-ENGINEERING.md    # System prompt analysis
   ├── TOOL-USE.md              # Complete tool catalog with schemas
   ├── agent-mode/
   │   ├── system-prompt.md
   │   ├── session.md
   │   ├── transcript.md
   │   └── log/
   │       ├── session.json
   │       └── session.csv
   └── plan-mode/               # (repeat for each mode)
       └── ...
   ```
5. **Open a pull request** with your analysis

### Improve Existing Analysis

- Fix token counts or cost calculations against the raw CSV data
- Add missing observations or clarify existing ones
- Improve documentation structure or readability

## Guidelines

- All claims must be verifiable against the raw session data (CSVs and JSONs)
- Keep analysis factual — describe what the data shows, avoid speculation
- Follow the existing directory and file structure for consistency
- Keep markdown formatting consistent with existing files

## Development Setup

No build step required — this is a documentation-only repo. Just edit markdown files directly.

To run a new capture session:
```bash
./.tools/alens
```

This launches AgentLens as a MITM proxy in a tmux session. See the [AgentLens docs](https://github.com/agenticloops-ai/agentlens) for configuration details.
