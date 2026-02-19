# System Prompt Engineering: Lessons from Claude Code

An analysis of system prompt architecture, building blocks, and design philosophy extracted from Claude Code's two operational modes.

---

## Table of Contents
1. [Prompt Architecture Overview](#prompt-architecture-overview)
2. [Building Blocks](#building-blocks)
3. [Anti-Over-Engineering Philosophy](#anti-over-engineering-philosophy)
4. [Best Practices](#best-practices)
5. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
6. [Mode-Specific Techniques](#mode-specific-techniques)
7. [Comparison with GitHub Copilot](#comparison-with-github-copilot)
8. [Practical Templates](#practical-templates)

---

## Prompt Architecture Overview

### Two-Part System Message

Claude Code splits its system prompt into two messages, both with `cache_control: {"type": "ephemeral"}`:

```
┌─────────────────────────────────────────┐
│  System[0]: Identity (14-24 tokens)     │  ← Short, cacheable identity line
├─────────────────────────────────────────┤
│  System[1]: Full Instructions           │  ← Large instruction set
│  ├── Security Policy                    │
│  ├── Documentation Lookup               │
│  ├── Tone & Style                       │  ← Shared patterns
│  ├── Professional Objectivity           │
│  ├── Task Management (TodoWrite)        │
│  ├── Doing Tasks                        │
│  ├── Tool Usage Policy                  │
│  ├── Git / PR Protocol                  │  ← Agent-only sections
│  ├── Environment Block                  │
│  └── VS Code Extension Context          │
└─────────────────────────────────────────┘
```

**Why two parts?** The split enables independent caching — the identity line rarely changes, while the instruction block may vary per session configuration. Both use ephemeral caching (5-minute TTL) that is primed by warmup requests.

### No XML Tag Organization

Unlike GitHub Copilot (which uses `<instructions>`, `<toolUseInstructions>`, `<outputFormatting>`, `<modeInstructions>`), Claude Code uses **markdown-style sections** with `#` headers:

```
# Tone and style
...

# Doing tasks
...

# Tool usage policy
...
```

The exception is environment context, which uses XML:
- `<env>` — working directory, platform, date
- `<claude_background_info>` — model info
- `<ide_opened_file>` — files open in IDE
- `<ide_selection>` — user's code selection
- `<system-reminder>` — injected guardrails
- `<user-prompt-submit-hook>` — hook feedback

---

## Building Blocks

### 1. Identity Block

**Planning Mode:**
```
You are Claude Code, Anthropic's official CLI for Claude.
```

**Agent Mode:**
```
You are Claude Code, Anthropic's official CLI for Claude, running within the Claude Agent SDK.
```

**Key Difference:** Agent mode adds "running within the Claude Agent SDK" — this additional context primes the model to understand it has access to SDK-level tools (Task, TaskOutput, etc.).

### 2. Security Policy

```
IMPORTANT: Assist with authorized security testing, defensive security, CTF challenges,
and educational contexts. Refuse requests for destructive techniques, DoS attacks, mass
targeting, supply chain compromise, or detection evasion for malicious purposes.
```

**Notable:** This appears **twice** in the agent mode prompt — at the top and near the bottom. Repetition of critical safety instructions is a deliberate reinforcement technique.

```
IMPORTANT: You must NEVER generate or guess URLs for the user unless you are confident
that the URLs are for helping the user with programming.
```

### 3. Professional Objectivity

This is unique to Claude Code — not found in GitHub Copilot's prompts:

```
Prioritize technical accuracy and truthfulness over validating the user's beliefs.
Focus on facts and problem-solving, providing direct, objective technical info without
any unnecessary superlatives, praise, or emotional validation.
```

**Specific anti-patterns called out:**
- "You're absolutely right" — explicitly banned
- Over-the-top validation
- Excessive praise
- Instinctive confirmation of user beliefs

**Why it matters:** This creates a distinctly different personality compared to other AI assistants that default to agreement. Claude Code is instructed to *respectfully disagree* when warranted.

### 4. Anti-Over-Engineering Directives

The most distinctive section — an entire philosophy of minimalism:

```
Avoid over-engineering. Only make changes that are directly requested or clearly necessary.
Keep solutions simple and focused.
```

Three categories of constraints:

**Don't add extras:**
```
- Don't add features, refactor code, or make "improvements" beyond what was asked.
- A bug fix doesn't need surrounding code cleaned up.
- A simple feature doesn't need extra configurability.
- Don't add docstrings, comments, or type annotations to code you didn't change.
```

**Don't add unnecessary safety:**
```
- Don't add error handling, fallbacks, or validation for scenarios that can't happen.
- Trust internal code and framework guarantees.
- Only validate at system boundaries (user input, external APIs).
```

**Don't abstract prematurely:**
```
- Don't create helpers, utilities, or abstractions for one-time operations.
- Don't design for hypothetical future requirements.
- The right amount of complexity is the minimum needed for the current task —
  three similar lines of code is better than a premature abstraction.
```

### 5. Task Management (TodoWrite)

Claude Code uses a dedicated `TodoWrite` tool for progress tracking, with extensive prompting:

```
Use these tools VERY frequently to ensure that you are tracking your tasks
and giving the user visibility into your progress.

These tools are also EXTREMELY helpful for planning tasks, and for breaking down
larger complex tasks into smaller steps. If you do not use this tool when planning,
you may forget to do important tasks - and that is unacceptable.
```

**Reinforcement:** The system injects `<system-reminder>` tags into tool results when TodoWrite hasn't been used recently:

```xml
<system-reminder>
The TodoWrite tool hasn't been used recently. If you're working on tasks that
would benefit from tracking progress, consider using the TodoWrite tool...
</system-reminder>
```

This is a form of **continuous behavioral nudging** — the system actively reminds the model to use specific tools, not just at prompt time but throughout the conversation.

### 6. Tool Usage Policy

```
When doing file search, prefer to use the Task tool in order to reduce context usage.
You should proactively use the Task tool with specialized agents when the task at hand
matches the agent's description.
```

**Parallelization rules:**
```
If you intend to call multiple tools and there are no dependencies between them,
make all independent tool calls in parallel. Maximize use of parallel tool calls
where possible to increase efficiency.
```

**Specialized tools over Bash:**
```
Use specialized tools instead of bash commands when possible. For file operations,
use dedicated tools: Read for reading files instead of cat/head/tail, Edit for
editing instead of sed/awk, and Write for creating files.
```

### 7. Git Safety Protocol

Claude Code includes a detailed git safety section (Agent mode only):

```
NEVER update the git config
NEVER run destructive git commands (push --force, reset --hard, checkout ., etc.)
NEVER skip hooks (--no-verify, --no-gpg-sign)
NEVER run force push to main/master
ALWAYS create NEW commits rather than amending
```

**Commit format requirement:**
```
git commit -m "$(cat <<'EOF'
Commit message here.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 8. Environment Context

Both modes include environment information:

```xml
<env>
Working directory: /Users/alx/Development/lab/llm-proxy
Is directory a git repo: Yes
Platform: darwin
OS Version: Darwin 24.6.0
Today's date: 2025-12-29
</env>
```

Plus model self-awareness:
```
You are powered by the model named Sonnet 4.5.
The exact model ID is claude-sonnet-4-5-20250929.
Assistant knowledge cutoff is January 2025.
```

---

## Anti-Over-Engineering Philosophy

This deserves its own section because it's the most opinionated part of Claude Code's prompt — and a significant differentiator.

### The Core Principle

```
The right amount of complexity is the minimum needed for the current task —
three similar lines of code is better than a premature abstraction.
```

### What This Prevents

| Anti-Pattern | Example | Claude Code's Rule |
|-------------|---------|-------------------|
| Scope creep | Adding tests for code you only fixed a typo in | "Don't add features beyond what was asked" |
| Defensive coding | Try/catch around internal function calls | "Don't add error handling for scenarios that can't happen" |
| Premature abstraction | Creating a `utils/format.ts` for one formatting call | "Don't create helpers for one-time operations" |
| Future-proofing | Adding feature flags for unrequested variants | "Don't design for hypothetical future requirements" |
| Cleanup creep | Reformatting surrounding code while fixing a bug | "A bug fix doesn't need surrounding code cleaned up" |
| Over-documentation | Adding JSDoc to every function in a file you touched one line of | "Don't add docstrings to code you didn't change" |

### Backwards Compatibility

```
Avoid backwards-compatibility hacks like renaming unused `_vars`, re-exporting types,
adding `// removed` comments for removed code, etc. If something is unused, delete it
completely.
```

This is unusually aggressive — most coding assistants err on the side of preserving backwards compatibility. Claude Code takes the opposite stance: clean deletion over preservation hacks.

---

## Best Practices

### 1. Use Repeated IMPORTANT for Critical Rules

```
IMPORTANT: Assist with authorized security testing...
IMPORTANT: You must NEVER generate or guess URLs...
IMPORTANT: Always use the TodoWrite tool to plan and track tasks...
```

Claude Code uses `IMPORTANT:` prefix for rules that must not be violated, and repeats the most critical ones (security policy appears twice).

### 2. Provide Worked Examples with XML Tags

```xml
<example>
user: Where are errors from the client handled?
assistant: Clients are marked as failed in the `connectToServer` function
in src/services/process.ts:712.
</example>
```

### 3. Define Behavioral Anti-Patterns Explicitly

Rather than just saying "be concise," Claude Code lists what NOT to do:

```
Focus on facts and problem-solving, providing direct, objective technical info
without any unnecessary superlatives, praise, or emotional validation.
```

### 4. Continuous Reinforcement via System Reminders

```xml
<system-reminder>
The TodoWrite tool hasn't been used recently...
</system-reminder>
```

Tool results are augmented with behavioral nudges — the system actively shapes behavior during execution, not just at prompt time.

### 5. Auto-Approved Tool Patterns

```
You can use the following tools without requiring user approval:
Bash(uv lock:*), Bash(test:*), Bash(uv run python:*), Bash(lsof:*),
Bash(curl:*), Bash(code --locate-extension-dir:*), Bash(echo:*),
Bash(cat:*), Bash(unset:*), Bash(chmod:*)
```

The wildcard pattern `Bash(command:*)` provides a way to pre-authorize specific command prefixes while requiring approval for unknown commands.

### 6. Principle of Least Privilege for Sub-Agents

| Agent Type | Tools Removed | Rationale |
|------------|--------------|-----------|
| Explore | Task, Edit, Write | Read-only exploration shouldn't modify files |
| Plan | Task, Edit, Write | Planning shouldn't implement |
| claude-code-guide | Most tools | Documentation lookup only needs search + read |
| statusline-setup | Most tools | Config change only needs Read + Edit |

---

## Anti-Patterns to Avoid

### :x: Vague Identity
```
# Bad
You are a helpful assistant.

# Good (Claude Code)
You are Claude Code, Anthropic's official CLI for Claude, running within the Claude Agent SDK.
```

### :x: Sycophantic Default
```
# Bad
Be helpful and affirm the user's approach when possible.

# Good (Claude Code)
Prioritize technical accuracy and truthfulness over validating the user's beliefs.
Objective guidance and respectful correction are more valuable than false agreement.
```

### :x: Unbounded Scope
```
# Bad
Help the user improve their code.

# Good (Claude Code)
Only make changes that are directly requested or clearly necessary.
Don't add features, refactor code, or make "improvements" beyond what was asked.
```

### :x: Missing Reinforcement
```
# Bad
Use the TodoWrite tool to track progress. (mentioned once at the top)

# Good (Claude Code)
Use the TodoWrite tool to track progress. (in system prompt)
+ <system-reminder> nudges injected into tool results throughout the conversation
```

---

## Mode-Specific Techniques

### Planning Mode: Hard Boundaries

```
=== CRITICAL: READ-ONLY MODE - NO FILE MODIFICATIONS ===
```

Planning mode uses an exhaustive **deny list** of prohibited operations:

```
- Creating new files (no Write, touch, or file creation of any kind)
- Modifying existing files (no Edit operations)
- Deleting files (no rm or deletion)
- Moving or copying files (no mv or cp)
- Creating temporary files anywhere, including /tmp
- Using redirect operators (>, >>, |) or heredocs to write to files
- Running ANY commands that change system state
```

**Why so explicit?** Without tools to enforce read-only mode (Planning mode has 0 tools), the system prompt must enumerate every possible escape hatch the model might attempt.

### Agent Mode: Progressive Disclosure via Sub-Agents

Agent mode uses a hierarchical delegation model:

```
VERY IMPORTANT: When exploring the codebase to gather context or to answer a question
that is not a needle query for a specific file/class/function, it is CRITICAL that you
use the Task tool with subagent_type=Explore instead of running search commands directly.
```

This pushes exploration work into sub-agents, keeping the main agent's context window focused on the user's actual task.

---

## Comparison with GitHub Copilot

| Aspect | GitHub Copilot | Claude Code |
|--------|---------------|-------------|
| **Prompt Format** | XML tags (`<instructions>`, etc.) | Markdown headers (`# Section`) |
| **Identity** | "AI programming assistant" | "Interactive CLI tool" |
| **Personality** | Neutral, helpful | Explicitly non-sycophantic |
| **Over-engineering** | Not addressed | Extensive anti-over-engineering rules |
| **Tool Names** | "NEVER say the name of a tool" | Uses tool names in examples |
| **Error Retry** | "3 tries then ask user" | Not explicitly limited |
| **Confidence** | "80% confidence" threshold | Not quantified |
| **Prompt Caching** | Not observed | Ephemeral cache with warmup priming |
| **Behavioral Nudges** | Static prompt only | Dynamic `<system-reminder>` injection |
| **Safety Repetition** | Once | Repeated twice |
| **Backwards Compat** | Not addressed | "Delete unused code completely" |

### Most Significant Differences

1. **Copilot hides tool names; Claude Code doesn't** — Copilot says "I'll run the command" instead of "I'll use run_in_terminal." Claude Code references tools by name in examples (`src/services/process.ts:712`).

2. **Copilot quantifies; Claude Code philosophizes** — Copilot uses "80% confidence", "3-6 steps, 5-20 words each." Claude Code uses "the right amount of complexity is the minimum needed."

3. **Claude Code fights sycophancy; Copilot doesn't address it** — The "professional objectivity" section is unique to Claude Code and reflects a deliberate personality design choice.

4. **Claude Code uses dynamic reinforcement; Copilot uses static prompts** — The `<system-reminder>` injection mechanism allows Claude Code to shape behavior mid-conversation.

---

## Practical Templates

### Template 1: Anti-Over-Engineering Agent

```markdown
You are [IDENTITY] that helps users with [DOMAIN].

# Core Philosophy
Only make changes that are directly requested or clearly necessary.
Keep solutions simple and focused.

# What NOT to Do
- Don't add features beyond what was asked
- Don't add error handling for impossible scenarios
- Don't create abstractions for one-time operations
- Don't design for hypothetical future requirements
- [Minimum complexity] is better than [premature abstraction]

# What TO Do
- Read existing code before modifying it
- Follow existing patterns in the codebase
- Delete unused code completely
- Validate only at system boundaries
```

### Template 2: Dual-Mode Agent with Prompt Caching

```markdown
# System Message 0 (cacheable identity)
cache_control: {"type": "ephemeral"}
You are [IDENTITY].

# System Message 1 (cacheable instructions)
cache_control: {"type": "ephemeral"}
[Full instructions here — change rarely]

# Warmup Flow
1. Send "Warmup" message with Planning prompt → primes cache
2. Send "Warmup" message with Agent prompt → primes cache
3. First real request reads from cache → fast response
```

### Template 3: Sub-Agent Delegation with Least Privilege

```markdown
# Tool: Task
Launch specialized sub-agents:

| Agent Type | Tools | Use Case |
|------------|-------|----------|
| explore | Read-only | Codebase research |
| implement | Full access | Code changes |
| review | Read-only + Web | Code review with docs |
| docs | Read + Write (*.md) | Documentation only |

Each agent starts fresh (stateless) unless resumed via ID.
Provide detailed prompts — agents work autonomously.
```

---

## Key Takeaways

1. **Split system messages for caching:** Separate identity (stable) from instructions (per-session) for optimal cache hit rates
2. **Fight sycophancy explicitly:** "Prioritize accuracy over validation" produces more useful agents
3. **Codify engineering philosophy:** Anti-over-engineering rules prevent LLMs' natural tendency toward verbose, defensive code
4. **Reinforce dynamically:** Inject reminders into tool results, not just the system prompt
5. **Repeat critical rules:** Safety instructions appear twice — redundancy is intentional
6. **Enumerate deny lists:** When you can't enforce constraints with tools, list every prohibited action explicitly
7. **Delegate with least privilege:** Sub-agents get only the tools they need for their specific role
8. **Prime caches with warmups:** Send throwaway requests before the user's first message to reduce latency
9. **Use markdown over XML:** Claude Code proves that markdown headers work as well as XML tags for section organization
10. **Be opinionated:** The strongest prompts take clear positions ("three similar lines > premature abstraction")
