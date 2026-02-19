<div align="center">

# Agentic Apps Internals

**Reverse-engineering analysis of popular AI coding agents**\
Exposing system prompts, tool architectures, and implementation patterns.

[![Website](https://img.shields.io/badge/Website-agenticloops.ai-green?style=for-the-badge&logo=googlechrome&logoColor=white)](https://agenticloops.ai)
[![Substack](https://img.shields.io/badge/Substack-Blogs_&_Newsletter-orange?style=for-the-badge&logo=substack&logoColor=white)](https://agenticloopsai.substack.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/agenticloops-ai)
[![Follow @agenticloops_ai](https://img.shields.io/badge/Follow%20%40agenticloops__ai-black?style=for-the-badge&logo=x&logoColor=white)](https://x.com/agenticloops_ai)

</div>

## 🔍 What's Inside

This repository contains captured API requests, decoded system prompts, and detailed analysis of how different AI agents actually work under the hood. Useful for:

- **AI Engineers** building coding assistants
- **Researchers** studying LLM agent architectures
- **Developers** learning advanced prompt engineering
- **Anyone** curious about how these tools really work

## 🤖 Agents Analyzed

| Agent | Status | Tools | Key Insights |
|-------|--------|-------|--------------|
| [**GitHub Copilot**](github-copilot/) | ![complete](https://img.shields.io/badge/complete-brightgreen) | 0-68 | 4 modes with progressive capabilities; tools = 88% of token cost in Agent mode |
| [**Claude Code**](claude-code/) | ![complete](https://img.shields.io/badge/complete-brightgreen) | 0-17 | 2-mode architecture with speculative dual-request execution; anti-over-engineering philosophy |
| **Cursor** | ![coming soon](https://img.shields.io/badge/coming%20soon-orange) | - | - |
| **Windsurf** | ![coming soon](https://img.shields.io/badge/coming%20soon-orange) | - | - |
| **Cline** | ![coming soon](https://img.shields.io/badge/coming%20soon-orange) | - | - |
| **Aider** | ![coming soon](https://img.shields.io/badge/coming%20soon-orange) | - | - |

## ⚡ Quick Comparison

| Aspect | Copilot | Claude Code | Windsurf | Cursor |
|--------|---------|-------------|----------|--------|
| Modes | 4 (Ask/Edit/Plan/Agent) | 2 (Planning/Agent) | - | - |
| Max Tools | 68 | 17 | - | - |
| Edit Format | V4A diff + 4-backtick | String replacement | - | - |
| Sub-agents | ✅ runSubagent (1 type) | ✅ Task (5 types) | - | - |
| MCP Support | ✅ (33 tools) | Not in captured session | - | - |
| Prompt Caching | ❌ | ✅ (ephemeral) | - | - |
| Speculative Exec | ❌ | ✅ (dual requests) | - | - |

## 🔬 Methodology

Each agent analysis includes:

1. **API Capture** - Intercepted requests/responses from the IDE
2. **System Prompts** - Decoded and formatted for readability
3. **Tool Schemas** - Complete tool definitions with parameters
4. **Token Analysis** - Cost breakdown by component
5. **Best Practices** - Patterns extracted for reuse

## ⚠️ Disclaimer

This repository is for **educational and research purposes only**. All trademarks belong to their respective owners. The goal is to understand and learn from these systems, not to replicate proprietary services.

## 📜 Legal Notice

This analysis was conducted through observation of network traffic during normal use of publicly available software. No security measures were bypassed, no proprietary source code was accessed, and no terms of service were violated beyond what is necessary for standard interoperability research.

This is independent research and is not affiliated with, endorsed by, or connected to GitHub, Microsoft, Anthropic, or any other company analyzed.

## ⚖️ License

MIT - See individual agent analyses for their respective product licenses.
