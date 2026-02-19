# Claude Code - Internal Analysis

This repository contains captured API requests and responses from Claude Code (Anthropic's official CLI agent), revealing the system prompts, tool schemas, agentic loop architecture, and speculative execution patterns used under the hood.

**Model:** Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)\
**Captured:** December 29, 2025\
**Test Task:** "Validate proxy for Anthropic" (multi-file Python project)\
**Runtime:** VS Code extension (Claude Agent SDK)

---

## Modes Overview

| Mode | Tools | Purpose | Can Edit | Can Execute |
|------|-------|---------|----------|-------------|
| **Planning** | 0 | Explore codebase & design implementation plans | ❌ | ❌ |
| **Agent** | 17 | Full autonomous implementation | ✅ | ✅ |

Unlike GitHub Copilot's 4 modes (Ask/Edit/Plan/Agent), Claude Code uses a **2-mode architecture** with a sharp divide: Planning mode is strictly read-only with zero tools, while Agent mode provides full read-write-execute capabilities through 17 tools.

---

## Mode Details

### 1. Planning Mode

**Purpose:** Read-only codebase exploration and implementation plan design.

**Characteristics:**
- Zero tools in the captured requests (`"tools": []`) — yet the system prompt references Glob, Grep, Read, and Bash
- Strict "CRITICAL: READ-ONLY MODE" enforcement in system prompt
- Identity: "software architect and planning specialist"
- Required structured output ending with "Critical Files for Implementation"
- In the captured logs, only used during warmup phase to prime the prompt cache (response is discarded)

**Contradiction: prompt references tools that don't exist in the request.**
The system prompt says "Find existing patterns using Glob, Grep, and Read" and "Use Bash ONLY for read-only operations" — but the `tools` array is empty. This suggests the planning prompt is designed for the `Task` sub-agent (where `subagent_type=Plan` injects tools at runtime), but during warmup it's sent with `tools: []` since only cache priming matters. The model's warmup response confirms this — it hallucinated fake tool calls in text output that would never execute.

**System Prompt Key Points:**
- "This is a READ-ONLY planning task. You are STRICTLY PROHIBITED from creating, modifying, or deleting files"
- "You CANNOT and MUST NOT write, edit, or modify any files"
- "Use Bash ONLY for read-only operations (ls, git status, git log, git diff, find, cat, head, tail)"
- Process: Understand Requirements → Explore Thoroughly → Design Solution → Detail the Plan

**Files:** [`planning-mode/`](planning-mode/)

---

### 2. Agent Mode

**Purpose:** Full autonomous coding agent with file editing, terminal execution, sub-agent delegation, and web access.

**Characteristics:**
- 17 tools with full read-write-execute capabilities
- Identity: "interactive CLI tool that helps users with software engineering tasks"
- Multi-turn agentic loop with tool_use → tool_result cycles
- Sub-agent architecture via `Task` tool with 5 specialized agent types
- Prompt caching with `cache_control: {"type": "ephemeral"}`
- Dual-request speculative execution pattern (see [Architecture Insights](#dual-request-pattern-speculative-execution))

**System Prompt Key Points:**
- "NEVER create files unless they're absolutely necessary. ALWAYS prefer editing an existing file"
- "Prioritize technical accuracy and truthfulness over validating the user's beliefs"
- "Avoid over-engineering. Only make changes that are directly requested or clearly necessary"
- "Be careful not to introduce security vulnerabilities such as command injection, XSS, SQL injection"

**Tool Categories:**

| Category | Count | Examples |
|----------|-------|---------|
| File Operations | 4 | `Read`, `Edit`, `Write`, `NotebookEdit` |
| Search & Navigation | 2 | `Glob`, `Grep` |
| Execution | 1 | `Bash` |
| Task Management | 2 | `TodoWrite`, `AskUserQuestion` |
| Sub-Agent Delegation | 2 | `Task`, `TaskOutput` |
| Web Access | 2 | `WebFetch`, `WebSearch` |
| Mode Control | 2 | `EnterPlanMode`, `ExitPlanMode` |
| Extension | 2 | `Skill`, `KillShell` |

**Files:** [`agent-mode/`](agent-mode/)

---

## Architecture Insights

### Prompt Structure

Both modes use a **two-part system prompt** with prompt caching:

```
System Message 0 (Identity - short)
├── cache_control: {"type": "ephemeral"}
└── "You are Claude Code, Anthropic's official CLI for Claude[, running within the Claude Agent SDK]."

System Message 1 (Full Instructions - large)
├── cache_control: {"type": "ephemeral"}
└── 4K chars (Planning) or 15K chars (Agent)
    ├── Security Policy
    ├── Tone & Style
    ├── Professional Objectivity
    ├── Task Management (TodoWrite)
    ├── Tool Usage Policy
    ├── Git Commit Protocol
    ├── PR Creation Protocol
    ├── Environment Block
    └── VS Code Extension Context
```

User messages use content block arrays with special XML tags:

```
User Message (role: user)
├── content[0]: {type: "text", text: "<ide_opened_file>..."}   ← IDE context
├── content[1]: {type: "text", text: "actual user request"}    ← User prompt
└── content[N]: {type: "tool_result", tool_use_id: "..."}      ← Tool results
```

### Key Differences from GitHub Copilot

| Aspect | GitHub Copilot | Claude Code |
|--------|---------------|-------------|
| Modes | 4 (Ask/Edit/Plan/Agent) | 2 (Planning/Agent) |
| Max Tools | 68 | 17 |
| Edit Format | V4A custom diff | Exact string replacement (`old_string` → `new_string`) |
| Sub-agents | `runSubagent` (1 type) | `Task` (5 specialized types) |
| File Changes | `apply_patch` tool | `Edit` + `Write` tools |
| Task Tracking | `manage_todo_list` | `TodoWrite` with status tracking |
| Model | GPT-4.1 | Claude Sonnet 4.5 |
| MCP Support | ✅ (33 tools) | ❌ (not in captured session) |
| Prompt Caching | ❌ | ✅ (ephemeral) |
| Speculative Execution | ❌ | ✅ (dual requests) |

### Dual-Request Pattern (Speculative Execution)

The most significant architectural finding. **Every agentic turn produces TWO simultaneous API requests:**

| Aspect | Primary Request | Shadow Request |
|--------|----------------|----------------|
| **stream** | `true` | `null` |
| **temperature** | `null` (default) | `1` |
| **max_tokens** | `32000` | `21333` |
| **Messages** | Identical | Identical |
| **System** | Identical | Identical |
| **Tools** | Identical | Identical |

The primary (streaming) response is shown to the user in real-time. The shadow request uses `temperature=1` and `max_tokens=21333` (exactly 2/3 of 32000). This appears to be a **speculative execution** strategy — potentially for quality comparison, fallback generation, or A/B evaluation.

This pattern is consistent across all agentic turns and even warmup requests.

### Warmup & Prompt Cache Priming

Before the user's first request, Claude Code sends **warmup requests** to prime the prompt cache:

```
Warmup Flow:
1. Record 0: Planning mode, streaming warmup     → cache_creation_input_tokens: 1066
2. Record 1: Agent mode, streaming warmup         → cache_creation_input_tokens: 1066
3. Record 2: Planning mode, shadow warmup (t=1)   → cache_read_input_tokens: 1066
4. Record 3: Agent mode, shadow warmup (t=1)      → cache_read_input_tokens: 1066
```

The warmup message is simply `"Warmup"`. After this:
- All subsequent requests benefit from `cache_read_input_tokens` (significant cost savings on system prompt + tool schemas)
- The model responds with generic readiness messages that are discarded

### Agentic Loop

The conversation follows a strict request-response cycle:

```
Turn 1: user[text]           → assistant[text + tool_use]    (stop_reason=tool_use)
Turn 2: user[tool_result]    → assistant[text + tool_use]    (stop_reason=tool_use)
Turn 3: user[tool_result]    → assistant[text + tool_use]    (stop_reason=tool_use)
...
Turn N: user[tool_result]    → assistant[text]               (stop_reason=end_turn)
```

**Key observations:**
- Multiple tool calls are issued in parallel within a single assistant response
- Each turn, the **full conversation history** is resent (no truncation in observed session)
- Stop reason `tool_use` keeps the loop running; `end_turn` terminates it
- A `<system-reminder>` is appended to every tool result (malware scanning, TodoWrite nudges)

### Sub-Agent Architecture

The `Task` tool supports 5 specialized sub-agent types:

| Agent Type | Purpose | Available Tools |
|------------|---------|----------------|
| **general-purpose** | Complex multi-step research tasks | All tools |
| **Explore** | Fast codebase exploration (quick/medium/thorough) | All except Task, Edit, Write |
| **Plan** | Software architect for implementation planning | All except Task, Edit, Write |
| **claude-code-guide** | Official documentation lookup | Glob, Grep, Read, WebFetch, WebSearch |
| **statusline-setup** | Configure status line settings | Read, Edit |

Sub-agents are:
- **Stateless** — each invocation starts fresh (unless resumed via `resume` parameter)
- **Model-flexible** — can override model (sonnet/opus/haiku)
- **Background-capable** — can run asynchronously via `run_in_background`
- **Resumable** — previous agents can be continued via agent ID

---

## API Configuration

| Parameter | Agent Mode | Shadow Request | Planning Mode |
|-----------|-----------|----------------|---------------|
| **Model** | `claude-sonnet-4-5-20250929` | `claude-sonnet-4-5-20250929` | `claude-sonnet-4-5-20250929` |
| **max_tokens** | `32000` | `21333` | `32000` |
| **temperature** | null (default) | `1` | null (default) |
| **stream** | `true` | null | `true` |
| **top_p** | not set | not set | not set |
| **top_k** | not set | not set | not set |

### Prompt Caching

```json
{
  "cache_creation_input_tokens": 385,
  "cache_read_input_tokens": 18052,
  "cache_creation": {
    "ephemeral_5m_input_tokens": 385,
    "ephemeral_1h_input_tokens": 0
  }
}
```

Cache uses 5-minute ephemeral TTL. After warmup priming, most requests benefit from `cache_read_input_tokens` — in the observed session, 18,052 tokens were read from cache vs. only 385 created.

### Metadata

```json
{
  "metadata": {
    "user_id": "user_{hash}_account_{uuid}_session_{uuid}"
  }
}
```

The `user_id` field encodes three components: user hash, account UUID, and session UUID — enabling per-session tracking and billing.

---

## Token Usage Analysis

Estimated token consumption per mode:

| Component | Planning Mode | Agent Mode |
|-----------|--------------|------------|
| System Prompt 0 | ~14 tokens | ~24 tokens |
| System Prompt 1 | ~990 tokens | ~3,760 tokens |
| Tool Schemas | 0 | ~7,100 tokens |
| User Context | ~50 tokens | ~50 tokens |
| **Total Input (first turn)** | **~1,054** | **~10,934** |

*Token estimates based on ~4 characters per token*

### Key Insights

1. **Tool Schemas Dominate:** The 17 tools contribute ~7.1K tokens (~65% of input) in Agent mode
2. **Agent vs Planning:** Agent mode uses ~11K tokens vs Planning's ~1K — an 11x difference primarily from tools and system prompt
3. **Cache Efficiency:** After warmup, system prompt + tool schema tokens are served from cache (5-min ephemeral TTL)
4. **Per-Turn Growth:** Each additional turn adds conversation history tokens — observed session grew to 21 messages across 10 turns

### Cost Implications (Claude Sonnet 4.5 Pricing)

At $3/1M input, $15/1M output:
- **Warmup pair:** ~$0.006 (one-time, mostly cached after)
- **Single agent turn (cached):** ~$0.01-0.03 input + output
- **Full 10-turn session:** ~$0.15-0.30 (including conversation growth)
- **Shadow request overhead:** ~2x the above (every turn is doubled)

The dual-request pattern effectively doubles the API cost for every interaction.

---

## Observations

1. **Minimalist Tool Design with Maximal Descriptions:** Claude Code uses only 17 tools (vs Copilot's 68), but each tool is more general-purpose. More importantly, tool descriptions are dramatically more detailed — the `Bash` tool description alone is ~1,800 words and contains the entire git commit protocol and PR creation workflow. The `TodoWrite` tool embeds 8 worked examples. Total: ~5,400 words of behavioral instructions distributed across tool descriptions, vs Copilot's ~20 words per tool. See [TOOL-USE.md](TOOL-USE.md) for the full verbatim descriptions.

2. **Speculative Execution is Expensive:** The dual-request pattern (streaming + shadow with temp=1) doubles API costs. This trade-off suggests Anthropic values response quality or fallback reliability enough to justify the overhead.

3. **Prompt Cache Priming is Strategic:** Sending warmup requests before the user types anything ensures the first real request is fast. The 5-minute ephemeral cache means active sessions stay cached, while idle sessions gracefully expire.

4. **Professional Objectivity is Explicit:** Unlike Copilot, Claude Code's system prompt explicitly instructs the model to "prioritize technical accuracy over validating the user's beliefs" and avoid "excessive praise." This is a deliberate personality choice.

5. **Anti-Over-Engineering Philosophy:** The system prompt contains unusually detailed guidance against over-engineering: "Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements." This reflects a specific coding philosophy baked into the agent.

6. **Sub-Agent Specialization:** While Copilot has a single `runSubagent` tool, Claude Code defines 5 agent types with different tool access levels — from full-access `general-purpose` to restricted `claude-code-guide` (read-only + web search). This enables a principle-of-least-privilege delegation model.

7. **System Reminders as Guardrails:** `<system-reminder>` tags are injected into tool results to remind the model about malware scanning and TodoWrite usage. This is a form of continuous reinforcement that prevents the model from "forgetting" instructions over long conversations.

---

## Session Statistics

Data from the two captured sessions:

| Metric | Session 1 (validate proxy) | Session 2 (review README) |
|--------|---------------------------|---------------------------|
| **Duration** | ~6 minutes | ~8 minutes |
| **API Calls** | 36 records | 20 records |
| **Agentic Turns** | ~10 | ~10 |
| **Tool Calls** | Bash(14), Read(12), Write(5), Glob(3) | Edit(16), Read(14), Bash(6), Write(4), Glob(3) |
| **File** | `claude-session.jsonl` | `claude-readme.jsonl` |

---

## Deep Dive Guides

For detailed analysis, see:

- **[PROMPT-ENGINEERING.md](PROMPT-ENGINEERING.md)** — System prompt building blocks, anti-over-engineering philosophy, and comparison with Copilot
- **[TOOL-USE.md](TOOL-USE.md)** — Complete tool analysis, sub-agent architecture, parallelization rules, and token costs

---

## License

This analysis is for educational and research purposes. Claude Code is a product of Anthropic.
