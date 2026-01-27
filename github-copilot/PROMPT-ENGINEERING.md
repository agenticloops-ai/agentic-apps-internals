# System Prompt Engineering: Lessons from GitHub Copilot

An analysis of system prompt architecture, building blocks, and best practices extracted from GitHub Copilot's four chat modes.

---

## Table of Contents
1. [Prompt Architecture Overview](#prompt-architecture-overview)
2. [Building Blocks](#building-blocks)
3. [Best Practices](#best-practices)
4. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
5. [Mode-Specific Techniques](#mode-specific-techniques)
6. [Practical Templates](#practical-templates)

---

## Prompt Architecture Overview

### Layered Structure

GitHub Copilot uses a **layered prompt architecture** where each layer adds specificity:

```
┌─────────────────────────────────────────┐
│  Layer 1: Identity & Policies           │  ← Shared across all modes
├─────────────────────────────────────────┤
│  Layer 2: Core Instructions             │  ← Mode-specific behavior
├─────────────────────────────────────────┤
│  Layer 3: Tool Instructions             │  ← How to use tools
├─────────────────────────────────────────┤
│  Layer 4: Format Instructions           │  ← Output formatting
├─────────────────────────────────────────┤
│  Layer 5: Mode Override                 │  ← Final authority (Plan mode)
└─────────────────────────────────────────┘
```

### XML Tag Organization

All prompts use XML-style tags to organize sections:
- `<instructions>` - Core behavioral rules
- `<toolUseInstructions>` - Tool-specific guidance
- `<outputFormatting>` - Response format rules
- `<modeInstructions>` - Mode-specific overrides
- `<example>` - Concrete examples

**Why XML tags?** They create clear boundaries that the model can parse, and allow sections to reference each other (e.g., "follow `<plan_style_guide>`").

---

## Building Blocks

### 1. Identity Block

**Purpose:** Establish who the agent is and handle identity questions.

```
You are an AI programming assistant.
When asked for your name, you must respond with "GitHub Copilot".
When asked about the model you are using, you must state that you are using GPT-4.1 (Proxy).
```

**Best Practices:**
- Be explicit about identity to prevent confusion
- Handle "what model are you?" questions proactively
- Use consistent identity across all modes

### 2. Policy Block

**Purpose:** Safety guardrails and content restrictions.

```
Follow the user's requirements carefully & to the letter.
Follow Microsoft content policies.
Avoid content that violates copyrights.
If you are asked to generate content that is harmful, hateful, racist, sexist, lewd, or violent, only respond with "Sorry, I can't assist with that."
```

**Best Practices:**
- Place early in prompt (high priority)
- Provide exact refusal phrase for consistency
- Keep policies concise but comprehensive

### 3. Behavioral Directives

**Purpose:** Define how the agent should act.

```
Keep your answers short and impersonal.
Don't make assumptions about the situation- gather context first, then perform the task.
Think creatively and explore the workspace in order to make a complete fix.
Don't repeat yourself after a tool call, pick up where you left off.
```

**Directive Types:**
| Type | Example | Purpose |
|------|---------|---------|
| **Positive** | "Think creatively and explore" | Encourage desired behavior |
| **Negative** | "Don't make assumptions" | Prevent common mistakes |
| **Conditional** | "If you aren't sure, call multiple tools" | Handle edge cases |

### 4. Responsibility Assignment

**Purpose:** Make ownership explicit.

```
It's YOUR RESPONSIBILITY to make sure that you have done all you can to collect necessary context.
```

**Why it works:** Explicitly assigning responsibility prevents the model from giving up too early or deferring to the user unnecessarily.

### 5. Tool Usage Rules

**Purpose:** Guide efficient and correct tool use.

```xml
<toolUseInstructions>
No need to ask permission before using a tool.
NEVER say the name of a tool to a user. For example, instead of saying that you'll
use the run_in_terminal tool, say "I'll run the command in a terminal".
If you think running multiple tools can answer the user's question, prefer calling
them in parallel whenever possible, but do not call semantic_search in parallel.
Don't call the run_in_terminal tool multiple times in parallel. Instead, run one
command and wait for the output before running the next command.
</toolUseInstructions>
```

**Key Patterns:**
- **Permission bypass:** "No need to ask permission" - reduces latency
- **Abstraction:** Hide tool names from users for better UX
- **Parallelization rules:** Explicit guidance on what can/can't run in parallel
- **Sequential requirements:** Some tools must run sequentially (terminal)

### 6. Output Format Specification

**Purpose:** Ensure consistent, parseable output.

```xml
<outputFormatting>
Use proper Markdown formatting in your answers.
When referring to a filename or symbol in the user's workspace, wrap it in backticks.
<example>
The class `Person` is in `src/models/person.ts`.
The function `calculateTotal` is defined in `lib/utils/math.ts`.
</example>
</outputFormatting>
```

**Best Practices:**
- Provide concrete examples
- Specify exact syntax (4 backticks, filepath comments)
- Explain *why* (e.g., "so IDE can parse and apply")

### 7. Error Handling & Limits

**Purpose:** Prevent infinite loops and handle failures gracefully.

```
Do not loop more than 3 times attempting to fix errors in the same file.
If the third try fails, you should stop and ask the user what to do next.
```

**Why it matters:** Without explicit limits, agents can get stuck in retry loops. The "3 tries then ask" pattern is effective.

### 8. Context Efficiency Rules

**Purpose:** Minimize token usage and API calls.

```
When reading files, prefer reading large meaningful chunks rather than consecutive
small sections to minimize tool calls and gain better context.
You don't need to read a file if it's already provided in context.
You can use the grep_search to get an overview of a file by searching for a string
within that one file, instead of using read_file many times.
```

**Optimization Strategies:**
- Batch reads over sequential reads
- Check context before fetching
- Use search before full read

---

## Best Practices

### 1. Use NEVER for Hard Rules

```
NEVER print out a codeblock with file changes unless the user asked for it.
NEVER say the name of a tool to a user.
NEVER try to edit a file by running terminal commands unless the user specifically asks for it.
```

**Why:** Capitalized NEVER creates strong constraints that the model rarely violates.

### 2. Provide Escape Hatches

```
If the user asks you to edit a file, you can ask the user to enable editing tools
or print a codeblock with the suggested changes.
```

**Why:** When tools aren't available, the agent needs a fallback behavior rather than failing.

### 3. Use Hierarchical Overrides

Plan mode demonstrates this pattern:

```
You are currently running in "Plan" mode. Below are your instructions for this mode,
they must take precedence over any instructions above.
```

**Why:** Allows mode-specific behavior while reusing base prompts.

### 4. Define Stop Conditions

```xml
<stopping_rules>
STOP IMMEDIATELY if you consider starting implementation, switching to implementation
mode or running a file editing tool.

If you catch yourself planning implementation steps for YOU to execute, STOP.
Plans describe steps for the USER or another agent to execute later.
</stopping_rules>
```

**Why:** Explicit stop conditions prevent mode drift and scope creep.

### 5. Include Worked Examples

```xml
<example>
### /Users/someone/proj01/example.ts

Add a new property 'age' and a new method 'getAge' to the class Person.

````typescript
// filepath: /Users/someone/proj01/example.ts
class Person {
	// ...existing code...
	age: number;
	// ...existing code...
	getAge() {
		return this.age;
	}
}
````
</example>
```

**Why:** Examples are more effective than descriptions for format specification.

### 6. Quantify When Possible

```
Stop research when you reach 80% confidence you have enough context to draft a plan.
3-6 steps, 5-20 words each
1-3 Further Considerations, 5-25 words each
```

**Why:** Specific numbers constrain output better than vague terms like "a few" or "brief".

---

## Anti-Patterns to Avoid

### ❌ Vague Instructions
```
# Bad
Try to be helpful and complete tasks.

# Good
It's YOUR RESPONSIBILITY to make sure that you have done all you can to collect
necessary context. Don't give up unless you are sure the request cannot be fulfilled.
```

### ❌ Missing Fallbacks
```
# Bad
Use the apply_patch tool to edit files.

# Good
Use the apply_patch tool to edit files. If you have issues with it, you should
first try to fix your patch and continue using apply_patch.
```

### ❌ Unlimited Retries
```
# Bad
Keep trying until the error is fixed.

# Good
Do not loop more than 3 times attempting to fix errors. If the third try fails,
stop and ask the user what to do next.
```

### ❌ Ambiguous Tool Selection
```
# Bad
Use the appropriate tool.

# Good
If you don't know exactly the string or filename pattern you're looking for,
use semantic_search. You can use grep_search to get an overview of a file by
searching for a string within that one file, instead of using read_file many times.
```

---

## Mode-Specific Techniques

### Ask Mode: Capability Listing
```
You can answer general programming questions and perform the following tasks:
* Ask a question about the files in your current workspace
* Explain how the code in your active editor works
* Generate unit tests for the selected code
...
```
**Why:** Helps the model understand its scope without tools.

### Edit Mode: Refusal Pattern
```
If you need to change existing files and it's not clear which files should be changed,
then refuse and answer with "Please add the files to be modified to the working set,
or use `#codebase` in your request to automatically discover working set files."
```
**Why:** Explicit refusal text ensures consistent UX.

### Plan Mode: Workflow Definition
```xml
<workflow>
## 1. Context gathering and research:
MANDATORY: Run #runSubagent tool...

## 2. Present a concise plan to the user for iteration:
MANDATORY: Pause for user feedback...

## 3. Handle user feedback:
MANDATORY: DON'T start implementation...
</workflow>
```
**Why:** Step-by-step workflow prevents the agent from skipping phases.

### Agent Mode: Patch Format Specification
```
*** Begin Patch
*** Update File: /path/to/file.py
@@ class BaseClass
@@   def method():
[3 lines of pre-context]
-[old_code]
+[new_code]
[3 lines of post-context]
*** End Patch
```
**Why:** Custom diff format that's unambiguous and parseable by the IDE.

---

## Practical Templates

### Template 1: Basic Agent

```xml
You are [IDENTITY] that helps users with [DOMAIN].

<policies>
[Safety rules and content restrictions]
</policies>

<instructions>
[Core behavioral directives]
- Positive: what to do
- Negative: what not to do
- Conditional: how to handle edge cases
</instructions>

<tool_use>
[Tool-specific guidance]
- When to use each tool
- Parallelization rules
- Error handling
</tool_use>

<output_format>
[Format specification with examples]
</output_format>
```

### Template 2: Multi-Mode Agent

```xml
[Base prompt - shared across modes]

<mode_instructions>
You are currently running in "[MODE_NAME]" mode.
These instructions take precedence over any instructions above.

<stopping_rules>
[Mode boundaries - when to stop/refuse]
</stopping_rules>

<workflow>
[Step-by-step process for this mode]
</workflow>

<style_guide>
[Output format specific to this mode]
</style_guide>
</mode_instructions>
```

### Template 3: Tool Usage Block

```xml
<tool_use_instructions>
No need to ask permission before using a tool.

[Tool selection guidance]
- If [condition], use [tool_a]
- If [other_condition], use [tool_b]

[Parallelization rules]
- These tools CAN run in parallel: [list]
- These tools MUST run sequentially: [list]

[Error handling]
- If [error], try [recovery]
- After [N] failures, [fallback action]

[Efficiency rules]
- Prefer [efficient pattern] over [inefficient pattern]
- Don't [wasteful action] if [alternative exists]
</tool_use_instructions>
```

---

## Key Takeaways

1. **Structure matters:** Use XML tags to organize prompts into clear sections
2. **Be explicit:** Vague instructions lead to inconsistent behavior
3. **Use NEVER:** Capitalized prohibitions are strongly followed
4. **Provide examples:** Show, don't just tell
5. **Set limits:** Retry counts, confidence thresholds, word counts
6. **Define fallbacks:** What to do when the primary approach fails
7. **Assign responsibility:** "It's YOUR responsibility" prevents giving up
8. **Layer overrides:** Mode-specific instructions can override base behavior
9. **Optimize for tokens:** Guide efficient tool use to minimize costs
10. **Stop conditions:** Explicit boundaries prevent scope creep

---

## Further Reading

- [Anthropic's Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [OpenAI's Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
