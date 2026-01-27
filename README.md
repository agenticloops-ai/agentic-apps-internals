# AI Agents Internals

Reverse-engineering analysis of popular AI coding agents — exposing system prompts, tool architectures, and implementation patterns.

## What's Inside

This repository contains captured API requests, decoded system prompts, and detailed analysis of how different AI agents actually work under the hood. Useful for:

- **AI Engineers** building coding assistants
- **Researchers** studying LLM agent architectures
- **Developers** learning advanced prompt engineering
- **Anyone** curious about how these tools really work

## Agents Analyzed

| Agent | Status | Tools | Key Insights |
|-------|--------|-------|--------------|
| [**GitHub Copilot**](github-copilot/) | ✅ Complete | 0-68 | 4 modes with progressive capabilities; tools = 88% of token cost in Agent mode |
| **Claude Code** | 🔜 Comming soon... | - | - |
| **Cursor** | 🔜 Comming soon... | - | - |
| **Windsurf** | 🔜 Comming soon... | - | - |
| **Cline** | 🔜 Comming soon... | - | - |
| **Aider** | 🔜 Comming soon... | - | - |


## Quick Comparison

*Coming soon as more agents are analyzed*

| Aspect | Copilot | Claude Code | Windsurf | Cursor |
|--------|---------|--------|----------|-------|
| Modes | 4 (Ask/Edit/Plan/Agent) | - | - | - |
| Max Tools | 68 | - | - | - |
| Edit Format | V4A diff + 4-backtick | - | - | - |
| Sub-agents | ✅ runSubagent | - | - | - |
| MCP Support | ✅ | - | - | - |

## Methodology

Each agent analysis includes:

1. **API Capture** - Intercepted requests/responses from the IDE
2. **System Prompts** - Decoded and formatted for readability
3. **Tool Schemas** - Complete tool definitions with parameters
4. **Token Analysis** - Cost breakdown by component
5. **Best Practices** - Patterns extracted for reuse

## Disclaimer

This repository is for **educational and research purposes only**. All trademarks belong to their respective owners. The goal is to understand and learn from these systems, not to replicate proprietary services.

## Legal Notice

This analysis was conducted through observation of network traffic during normal use of publicly available software. No security measures were bypassed, no proprietary source code was accessed, and no terms of service were violated beyond what is necessary for standard interoperability research.

This is independent research and is not affiliated with, endorsed by, or connected to GitHub, Microsoft, Anthropic, or any other company analyzed.

## License

MIT - See individual agent analyses for their respective product licenses.
