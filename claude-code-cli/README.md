# Claude Code (v2.1.126)

**Provider(s):** anthropic  
**Model(s):** claude-haiku-4-5-20251001, claude-opus-4-7 (1M context)  
**Modes Captured:** agent, plan  
**Captured:** 2026-05-04  
**CC Version:** 2.1.126

> For a version-to-version delta against the prior v2.1.59 capture, see [CHANGES-FROM-v2.1.59.md](CHANGES-FROM-v2.1.59.md). The earlier capture is preserved verbatim under [`../claude-code-cli-v2.1.59/`](../claude-code-cli-v2.1.59/).

## Session Metrics

| Mode | Requests | Billed In | Billed Out | Cache Read | Cache Create | Total Processed | Wall Time | Cost |
|------|---------:|----------:|-----------:|-----------:|-------------:|----------------:|----------:|-----:|
| agent | 10 | 978 | 2,293 | 859,014 | 186,954 | 1,049,239 | 1m 56s | $4.97 |
| plan | 15 | 899 | 4,680 | 391,714 | 46,069 | 443,362 | 4m 26s | $1.80 |

> **Note on token counts:** Billed input/output is what appears on the invoice. Total processed includes prompt-cache reads and creation — the actual byte volume the model "saw." With caching, ~96% of input on a typical mid-session turn is served from cache.

## Architecture

**Multi-stage pipeline:** Yes — 4 distinct prompt roles (main agent / security monitor / haiku title / haiku title+branch) plus a per-mode warmup probe.

**Models in play:**

- `claude-opus-4-7[1m]` — main agent (and security monitor)
- `claude-haiku-4-5-20251001` — warmup probes, session title generation, plan-mode title+branch generation

**Security Monitor:** A separate Claude opus-4-7 call that runs after select agent actions and emits `<block>yes/no</block>` based on a 30K-character classifier prompt covering ~30 BLOCK conditions and 8 ALLOW exceptions. Triggered 2× in the agent session (allowed both); 0× in plan mode. Full prompt: [SECURITY-MONITOR.md](SECURITY-MONITOR.md).

**Deferred tool schemas:** Only **8 tools** preload schemas; **117 more** are exposed by name and require a `ToolSearch(query="select:<name>")` call to load. This shifts most tool-schema bytes off the hot path. Full catalog: [TOOL-USE.md](TOOL-USE.md).

**Auto Mode:** A `<system-reminder>` block declares whether the session runs autonomously. Pairs with the Security Monitor as a safety backstop. Plan mode replaces it with a Plan Mode Active reminder.

**Memory subsystem:** Typed entries (`user`, `feedback`, `project`, `reference`) with mandatory frontmatter and a two-step save protocol. Memory directory is whitelisted by the Security Monitor; "Memory Poisoning" is one of the BLOCK categories.

## Tool Summary

- **agent:** 8 always-loaded tools (`Agent`, `Bash`, `Edit`, `Read`, `ScheduleWakeup`, `Skill`, `ToolSearch`, `Write`); 117 deferred tools (25 built-in + 92 MCP across 10 servers)
- **plan:** same baseline; loaded `AskUserQuestion` and `ExitPlanMode` mid-session via `ToolSearch`

## Key Observations

- **Main system prompt is identical between agent and plan modes** — 4,332 words, 27,744 chars, split across 4 cache-friendly content blocks. Mode behavior is enforced entirely via `<system-reminder>` blocks injected into the user message.
- **Plan mode is prompt-level enforcement, not structural** — `Edit` and `Write` remain in the always-loaded set; the Plan Mode Active reminder declares them off-limits except for the designated plan file.
- **Security Monitor + Auto Mode are co-designed** — Auto Mode lets the agent skip user confirmations for low-risk work; the Monitor catches the egregious cases. Together they enable autonomy with a safety backstop instead of a blanket "ask before risky things" pattern.
- **Heavy prompt caching** — by the end of the agent session, ~96% of input on a mid-session turn is served from cache. The 4-block system-prompt split lets the rotating billing-header hash invalidate only block 0.
- **MCP integration** — 92 tools across Canva, Figma, Gmail, Calendar, Drive, tldraw, Excalidraw, Miro, context7, Mermaid. Each MCP server can also inject usage instructions into the user-prompt layer.
- **Skills catalog: 17 skills** — including plugin-namespaced skills (`codex:*`, `frontend-design:*`, `skill-creator:*`).
- **Tool-description bloat** — git-safety, commit, and PR workflows live in the `Bash` tool description rather than the system prompt. Net effect: leaner system prompt, fatter tool description, only paid for when Bash is in scope.

## Detailed Analysis

- [Prompt Engineering Analysis](PROMPT-ENGINEERING.md) — full system-prompt structure, mode delta, multi-stage pipeline
- [Tool Catalog](TOOL-USE.md) — always-loaded vs deferred tools, schemas, deferred-tool architecture
- [Security Monitor](SECURITY-MONITOR.md) — post-action allow/block classifier
- [Changes from v2.1.59](CHANGES-FROM-v2.1.59.md) — version-to-version delta
- [agent mode — System Prompt](agent-mode/system-prompt.md)
- [agent mode — User Prompt](agent-mode/user-prompt.md)
- [agent mode — Session Data](agent-mode/session.md)
- [agent mode — Full Transcript](agent-mode/transcript.md)
- [plan mode — System Prompt](plan-mode/system-prompt.md)
- [plan mode — User Prompt](plan-mode/user-prompt.md)
- [plan mode — Session Data](plan-mode/session.md)
- [plan mode — Full Transcript](plan-mode/transcript.md)
