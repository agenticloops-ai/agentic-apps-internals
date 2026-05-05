# Claude Code: v2.1.59 → v2.1.126

> **Captured:** v2.1.59 on 2026-02-26 → v2.1.126 on 2026-05-04 (≈ 67 days apart).
>
> The earlier capture is preserved verbatim under [`../claude-code-cli-v2.1.59/`](./.archive/claude-code-cli-v2.1.59/). This document summarizes what changed.

## Headline Changes

| | v2.1.59 | v2.1.126 | Direction |
|---|---|---|---|
| Default opus model | claude-opus-4-6 | claude-opus-4-7 (1M context) | upgrade |
| Knowledge cutoff | May 2025 | January 2026 | newer |
| Main system prompt size | 2,345 words | 4,332 words | +85% |
| Tools always loaded | 24 | 8 | −67% |
| Tools deferred (loadable) | 0 | 117 | new |
| MCP integration | none captured | 92 tools / 10 servers | new |
| Skills available | 3 | 17 | +5× |
| System-prompt blocks | 1 | 4 (cache-friendly split) | new structure |
| Distinct prompt types | 2 (main + path-extract) | 4 (main + monitor + 2 haiku) | +2 |
| Security Monitor | absent | present (BLOCK/ALLOW classifier) | new |
| Auto Mode | absent | present (autonomy posture flag) | new |
| Memory subsystem | 28 lines, free-form | typed entries, frontmatter, two-step save | overhaul |
| Haiku overhead per session | 2–3 path-extract calls | 1 title + (plan: 1 title+branch) | replaced |
| User-prompt blocks | 3 (skills + project + task) | 6–7 (deferred tools, MCP, skills, mode flag, project, task) | +3–4 |

## 1. Multi-Stage Pipeline (NEW)

v2.1.59 had a simple two-prompt design:

```
[ haiku: file-path-extraction (after Bash) ]
[ opus: main agent ]
```

v2.1.126 has four prompt roles:

```
[ haiku: warmup probe        ]      one-token API health check
[ haiku: title generator     ]      session naming
[ haiku: title+branch        ]      plan-mode only, mid-session
[ opus: main agent           ]      core loop
[ opus: SECURITY MONITOR     ]      post-action allow/block classifier
```

The path-extraction haiku is **gone** — file-path tracking is now derived directly from the Read/Write/Edit tool arguments instead of an LLM-mediated extraction.

## 2. Security Monitor — A New Subsystem

v2.1.126 adds a **30,452-character system prompt** for an independent classifier that runs after select agent actions. It has no tools, uses `</block>` as its stop sequence, and emits a one-line verdict (`<block>no` or `<block>yes</block><reason>…</reason>`).

In the captured agent-mode session it fired 2 times and approved both. See [SECURITY-MONITOR.md](SECURITY-MONITOR.md) for the full prompt and analysis.

The monitor enables **Auto Mode** to be safer than v2.1.59's blanket "ask before risky actions" pattern — most things execute immediately, but a separate process gates ~30 categories of high-risk behavior (Production Deploy, Cloud Storage Mass Delete, Memory Poisoning, Credential Exploration, etc.).

## 3. Deferred Tool Schemas

v2.1.59 preloaded all 24 tool schemas in every opus request. v2.1.126 preloads 8 and exposes the rest by name only:

**Always loaded (8):** `Agent`, `Bash`, `Edit`, `Read`, `ScheduleWakeup`, `Skill`, `ToolSearch`, `Write`

**Deferred (117):** all `Task*`, `Team*`, `Cron*`, `WebFetch`/`WebSearch`, `NotebookEdit`, `EnterPlanMode`/`ExitPlanMode`, `AskUserQuestion`, `EnterWorktree`, `Monitor`, `SendMessage`, MCP tools (Canva, Figma, Gmail, Calendar, Drive, tldraw, Excalidraw, Miro, context7, Mermaid)…

The deferred-tool catalog ships in a `<system-reminder>` at the top of every initial user message. To use one, the model calls `ToolSearch(query="select:<name>")` to load schemas. See [TOOL-USE.md](TOOL-USE.md).

**Effect:** with cache, the always-loaded schemas (~12K vs ~20K) reduce cache pressure on every turn, while the much larger total catalog only costs anything when actually accessed. The plan-mode session in this capture invoked `ToolSearch(select:AskUserQuestion,ExitPlanMode)` exactly once at turn 7.

## 4. Tools Removed Entirely

`Glob` and `Grep` are gone from the tool registry. The system prompt now says:

> For broad codebase exploration or research that'll take more than 3 queries, spawn Agent with subagent_type=Explore. Otherwise use `find` or `grep` via the Bash tool directly.

Searching is now either Bash (precise targets) or the Explore subagent (open-ended). This reduces the always-loaded surface and unifies search semantics.

## 5. Auto Mode Flag (NEW)

A 6-rule `<system-reminder>` block declares whether the session is "auto mode":

> Auto mode is active. The user chose continuous, autonomous execution.
> 1. Execute immediately
> 2. Minimize interruptions
> 3. Prefer action over planning
> 4. Expect course corrections
> 5. Do not take overly destructive actions (still requires confirmation for prod / shared / data deletion)
> 6. Avoid data exfiltration

This **replaces v2.1.59's implicit posture** ("default to confirmation"). It is mutually exclusive with Plan Mode — agent mode includes the Auto Mode reminder; plan mode includes the Plan Mode Active reminder.

## 6. Memory System Overhaul

v2.1.59 had a 28-line memory section with simple "save your stable patterns" guidance.

v2.1.126 dedicates ~5,000 characters to memory and introduces:

- **4 typed memory entries:** `user`, `feedback`, `project`, `reference`
- **Mandatory frontmatter:** `name`, `description`, `type` per file
- **Structured body** for `feedback`/`project`: rule + `**Why:**` + `**How to apply:**` lines
- **Two-step save:** write the memory file *and* index it in `MEMORY.md`
- **Verification before recommending:** "a memory naming a file is a claim it existed when written — grep for it before recommending"
- **`MEMORY.md` is an index, not a memory** — entries one line, < 150 chars; lines after 200 truncated

The memory directory is also explicitly **whitelisted** in the Security Monitor's ALLOW exceptions ("Memory Directory: routine writes are intended persistence"), with **Memory Poisoning** as a BLOCK condition guarding against memories that would function as future permission grants.

## 7. Tool Description Bloat

Material that used to live in the system prompt has migrated into tool descriptions:

| | v2.1.59 | v2.1.126 |
|---|---|---|
| Bash description | ~600 chars | ~3,800 chars |
| Includes git safety protocol | system prompt | Bash description |
| Includes PR creation workflow | system prompt | Bash description |
| Includes commit message HEREDOC | system prompt | Bash description |
| Agent description includes subagent catalog | no | yes (6 subagent types listed) |

This shifts cost: the always-loaded system prompt is leaner; tool descriptions only land in context when their tools are exposed (and Bash's expanded text is paid every turn since Bash is always loaded).

## 8. New Always-Loaded Tools

| Tool | Purpose |
|------|---------|
| `ScheduleWakeup` | Self-pace `/loop` dynamic mode iterations (with explicit cache-TTL economics in the description) |
| `ToolSearch` | Load schemas for deferred tools — the meta-tool that makes the deferred catalog work |

Both are net-new in v2.1.126. (`Skill` is also always-loaded, but it was already present in v2.1.59 — included here in earlier drafts by mistake.)

## 9. User-Prompt Layer Restructured

v2.1.59 user message had **3 content blocks**:

1. Skills reminder (3 skills)
2. Project context (CLAUDE.md + currentDate)
3. User task

v2.1.126 user message has **6 (agent) or 7 (plan) content blocks**:

1. Deferred tools list (117)
2. MCP server instructions (10 servers)
3. Skills reminder (17 skills)
4. **Auto Mode** *or* **Plan Mode Active** flag
5. (plan only) Plan File Info + 5-phase workflow
6. Project context (userEmail + currentDate; CLAUDE.md only when present)
7. User task

## 10. Plan Mode Workflow Made Explicit

v2.1.59 plan mode had a "you MUST NOT make any edits" reminder. v2.1.126 expands this into a **5-phase workflow**:

- **Phase 1: Initial Understanding** — up to 3 `Explore` agents in parallel
- **Phase 2: Design** — up to 1 `Plan` agent
- **Phase 3: Review** — read critical files, AskUserQuestion as needed
- **Phase 4: Final Plan** — write to the designated plan file (Context section, recommended approach, verification section)
- **Phase 5: ExitPlanMode** — exit explicitly; no text-based "Is this OK?" questions

The plan-file path is generated server-side from a haiku-derived branch slug. The model is allowed to edit only that file.

## 11. New System-Prompt Sections

| Section | Purpose |
|---------|---------|
| **Text output** | What user-facing text should look like (concise, no narration of internal deliberation, end-of-turn summary 1–2 sentences) |
| **System reminders** | How to interpret `<system-reminder>` blocks (instructions to the model, not user messages); when to think more vs. less |
| **Session-specific guidance** | The `!` shell prefix for interactive commands, when to use Agent vs. find/grep, ultrareview info |
| **Context management** | Brief note about saving important info in responses since tool results may be cleared |

## 12. Skills Catalog Growth

v2.1.59: 3 skills (`keybindings-help`, `claude-developer-platform`, `frontend-design`)

v2.1.126: 17 skills, including:
- Plugin-namespaced: `codex:setup`, `codex:rescue`, `codex:codex-result-handling`, `codex:codex-cli-runtime`, `codex:gpt-5-4-prompting`, `frontend-design:frontend-design`, `skill-creator:skill-creator`
- New built-ins: `update-config`, `simplify`, `fewer-permission-prompts`, `loop`, `schedule`, `claude-api`, `init`, `review`, `security-review`

## 13. Cost Profile

| | v2.1.59 agent | v2.1.126 agent |
|---|---|---|
| Wall time | 2m 4s | 1m 56s |
| Requests | 11 | 10 |
| Billed input tokens | 72,104 | 978 |
| Cache read | 595K | 859K |
| Cache creation | 77K | 187K |
| Total processed | ~745K | ~1,049K |
| Estimated cost | ~$1.10 (excl. cache) → likely ~$3+ effective | $4.97 |

The v2.1.126 session is **more expensive** despite being slightly faster, primarily due to:

- Two security-monitor calls (~$0.36)
- Larger system prompt (~85% more text)
- Higher cache-creation in the first turn (the 4-block split + 6 user-prompt blocks need to be cached fresh)

In a long session, the cache-friendliness pays off (subsequent turns are nearly free); in a short session, the v2.1.126 startup overhead dominates.

## What Stayed the Same

- Single-provider design (Anthropic) — no multi-provider routing
- Tone and style rules (concise responses, no emojis, file:line refs)
- "Don't over-engineer" / "don't add backwards-compatibility hacks" core ethos (now articulated more precisely)
- Anti-prompt-injection wariness (now reinforced by the Security Monitor)
- Mode-as-prompt-control: tools aren't physically removed in plan mode; behavior is enforced via the system-reminder

## Capture Notes

- v2.1.126 captures live in [`agent-mode/log/session.json`](agent-mode/log/session.json) and [`plan-mode/log/session.json`](plan-mode/log/session.json) — full request/response payloads.
- Original capture timestamps: `2026-05-04T08-58-35` (agent) and `2026-05-04T08-53-00` (plan); also preserved in `../results/`.
- v2.1.59 captures live in [`../claude-code-cli-v2.1.59/`](../claude-code-cli-v2.1.59/) — preserved unchanged from the prior analysis.
