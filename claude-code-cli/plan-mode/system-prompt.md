# System Prompts — Plan Mode

> **The main system prompt is identical to agent mode.** Same 4 blocks, same 27,744 chars, same 4,332 words. The only difference is the per-request `cch=` hash in the billing header. Mode-specific behavior is enforced via a runtime `<system-reminder>` injected into the user message — see [user-prompt.md](user-prompt.md).
>
> See [../agent-mode/system-prompt.md](../agent-mode/system-prompt.md) for the full prompt text.

## Request Composition

Plan-mode session sent **15 requests**:

| Role | Model | Count |
|------|-------|------:|
| Warmup probe | haiku-4.5 | 1 |
| Title generator | haiku-4.5 | 1 |
| Title + branch generator | haiku-4.5 | 1 |
| Main planning loop | opus-4.7 | 12 |

**No security-monitor calls fired in plan mode** — consistent with the monitor's purpose (it gates *executions*, and plan mode is read-only by construction).

## Overhead Prompt #3 — Title + Branch Generator (haiku-4.5)

Plan mode adds a **third** haiku overhead role not seen in agent mode: title + git branch name generation. It fires mid-session (turn #12) right before `ExitPlanMode`, presumably to preset a branch name for the implementation that follows the plan.

**Words:** 232 | **Characters:** 1,316

```
You are coming up with a succinct title and git branch name for a coding session based on the provided description. The title should be clear, concise, and accurately reflect the content of the coding task.
You should keep it short and simple, ideally no more than 6 words. Avoid using jargon or overly technical terms unless absolutely necessary. The title should be easy to understand for anyone reading it.
Use sentence case for the title (capitalize only the first word and proper nouns), not Title Case.

The branch name should be clear, concise, and accurately reflect the content of the coding task.
You should keep it short and simple, ideally no more than 4 words. The branch should always start with "claude/" and should be all lower case, with words separated by dashes.

Return a JSON object with "title" and "branch" fields.

Example 1: {"title": "Fix login button not working on mobile", "branch": "claude/fix-mobile-login-button"}
Example 2: {"title": "Update README with installation instructions", "branch": "claude/update-readme"}
Example 3: {"title": "Improve performance of data processing script", "branch": "claude/improve-data-processing"}

Here is the session description:
<description>Refine local plan</description>
Please generate a title and branch name for this session.
```

> The session description is hard-coded as `Refine local plan` — the haiku doesn't see the user's task at this stage. Output is a deterministic-shape JSON. Branch prefix is always `claude/`.

## Other Overhead Prompts

The warmup-probe (`quota` user message, no system prompt, max_tokens=1) and the title-generator are identical to agent mode. See [../agent-mode/system-prompt.md](../agent-mode/system-prompt.md).
