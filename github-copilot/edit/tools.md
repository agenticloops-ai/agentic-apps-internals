# GitHub Copilot Edit Mode Tools

## Tools Available

**None** - Edit mode has no tools.

Edit mode is a **text-only completion mode** that returns code suggestions in a specific format using 4 backticks with filepath comments. The IDE is responsible for parsing and applying the changes.

## How Edit Mode Works

1. User provides a request (with files in working set or `#codebase`)
2. Copilot generates structured text response
3. VS Code parses the response format
4. IDE applies the suggested changes to files

## Output Format

```markdown
### /path/to/file.ext

Brief description of changes.

````languageId
// filepath: /path/to/file.ext
// ...existing code...
{ changed code }
// ...existing code...
````
```

## Comparison with Other Modes

| Mode | Tools | Can Edit Files | Can Execute |
|------|-------|----------------|-------------|
| **Ask** | 0 | ❌ | ❌ |
| **Edit** | 0 | ❌ (suggests only) | ❌ |
| **Plan** | 13 | ❌ | ❌ |
| **Agent** | 68 | ✅ | ✅ |
