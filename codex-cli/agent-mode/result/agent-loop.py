#!/usr/bin/env python3
"""
Minimal agentic loop using Anthropic's Messages API with a bash tool.

Features:
- Single standalone script (stdlib only)
- `run_bash` tool exposed to the model
- Human confirmation required before executing any command
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any


ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

RUN_BASH_TOOL = {
    "name": "run_bash",
    "description": (
        "Run a bash command on the local machine. "
        "Use for inspecting files, running scripts, and performing shell tasks."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Bash command to execute (run with `bash -lc`).",
            },
            "cwd": {
                "type": "string",
                "description": "Optional working directory for the command.",
            },
            "timeout_seconds": {
                "type": "integer",
                "minimum": 1,
                "maximum": 600,
                "description": "Optional timeout in seconds. Defaults to 60.",
            },
        },
        "required": ["command"],
        "additionalProperties": False,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Minimal Anthropic agent loop with a confirm-before-run bash tool."
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Task prompt for the agent. If omitted, you'll be prompted interactively.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
        help="Anthropic model name (default: %(default)s or $ANTHROPIC_MODEL).",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=1024,
        help="Max tokens per Anthropic response (default: %(default)s).",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=12,
        help="Max assistant turns before aborting (default: %(default)s).",
    )
    parser.add_argument(
        "--tool-output-chars",
        type=int,
        default=12000,
        help="Max characters from each tool result returned to the model (default: %(default)s).",
    )
    parser.add_argument(
        "--system",
        default=(
            "You are a CLI agent. Use the run_bash tool when needed. "
            "Be concise. Explain what you are doing before risky actions."
        ),
        help="System prompt.",
    )
    return parser.parse_args()


def anthropic_messages_create(
    *,
    api_key: str,
    model: str,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    max_tokens: int,
    system: str | None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "tools": tools,
    }
    if system:
        payload["system"] = system

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=data,
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body = "<failed to read error body>"
        raise RuntimeError(f"Anthropic API HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to reach Anthropic API: {exc}") from exc


def render_assistant_output(blocks: list[dict[str, Any]]) -> None:
    text_parts: list[str] = []
    tool_uses: list[dict[str, Any]] = []

    for block in blocks:
        if block.get("type") == "text":
            text = block.get("text", "")
            if text:
                text_parts.append(text)
        elif block.get("type") == "tool_use":
            tool_uses.append(block)

    if text_parts:
        print("\nAssistant:\n")
        print("".join(text_parts).strip())

    for block in tool_uses:
        print(f"\nAssistant requested tool: {block.get('name')} ({block.get('id')})")
        print(json.dumps(block.get("input", {}), indent=2))


def confirm(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} [y/N]: ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"", "n", "no"}:
            return False
        print("Please answer y or n.")


def truncate_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    head = max_chars // 2
    tail = max_chars - head
    return (
        text[:head]
        + "\n\n...[truncated]...\n\n"
        + text[-tail:]
    )


def run_bash_tool(
    tool_input: dict[str, Any],
    *,
    tool_output_chars: int,
) -> tuple[bool, str]:
    command = tool_input.get("command")
    cwd = tool_input.get("cwd")
    timeout_seconds = int(tool_input.get("timeout_seconds", 60))

    if not isinstance(command, str) or not command.strip():
        result = {"ok": False, "error": "Missing or invalid `command`."}
        return False, json.dumps(result)

    if cwd is not None and not isinstance(cwd, str):
        result = {"ok": False, "error": "Invalid `cwd`; expected string."}
        return False, json.dumps(result)

    if timeout_seconds < 1 or timeout_seconds > 600:
        result = {"ok": False, "error": "`timeout_seconds` must be between 1 and 600."}
        return False, json.dumps(result)

    print("\nTool request: run_bash")
    print(f"Command: {command}")
    if cwd:
        print(f"CWD: {cwd}")
    print(f"Timeout: {timeout_seconds}s")

    if not confirm("Execute this command?"):
        result = {"ok": False, "error": "User denied command execution."}
        return False, json.dumps(result)

    started = time.time()
    try:
        completed = subprocess.run(
            ["bash", "-lc", command],
            cwd=cwd or None,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        duration = time.time() - started
        result = {
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "duration_seconds": round(duration, 3),
            "stdout": truncate_text(completed.stdout or "", tool_output_chars),
            "stderr": truncate_text(completed.stderr or "", tool_output_chars),
        }
        return completed.returncode == 0, json.dumps(result)
    except subprocess.TimeoutExpired as exc:
        duration = time.time() - started
        result = {
            "ok": False,
            "error": "Command timed out.",
            "duration_seconds": round(duration, 3),
            "stdout": truncate_text((exc.stdout or ""), tool_output_chars),
            "stderr": truncate_text((exc.stderr or ""), tool_output_chars),
        }
        return False, json.dumps(result)
    except Exception as exc:
        result = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        return False, json.dumps(result)


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: set ANTHROPIC_API_KEY in the environment.", file=sys.stderr)
        return 1

    prompt = " ".join(args.prompt).strip()
    if not prompt:
        prompt = input("User prompt: ").strip()
    if not prompt:
        print("Error: prompt is required.", file=sys.stderr)
        return 1

    messages: list[dict[str, Any]] = [{"role": "user", "content": prompt}]

    for turn in range(1, args.max_turns + 1):
        print(f"\n=== Turn {turn} ===")

        response = anthropic_messages_create(
            api_key=api_key,
            model=args.model,
            messages=messages,
            tools=[RUN_BASH_TOOL],
            max_tokens=args.max_tokens,
            system=args.system,
        )

        content = response.get("content", [])
        if not isinstance(content, list):
            print("Error: unexpected Anthropic response format.", file=sys.stderr)
            return 1

        render_assistant_output(content)
        messages.append({"role": "assistant", "content": content})

        tool_uses = [b for b in content if b.get("type") == "tool_use"]
        if not tool_uses:
            print("\nDone.")
            return 0

        tool_results: list[dict[str, Any]] = []
        for block in tool_uses:
            tool_name = block.get("name")
            tool_id = block.get("id")
            tool_input = block.get("input", {})

            if tool_name != "run_bash":
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "is_error": True,
                        "content": json.dumps(
                            {"ok": False, "error": f"Unknown tool: {tool_name}"}
                        ),
                    }
                )
                continue

            ok, result_content = run_bash_tool(
                tool_input if isinstance(tool_input, dict) else {},
                tool_output_chars=args.tool_output_chars,
            )
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "is_error": not ok,
                    "content": result_content,
                }
            )

        messages.append({"role": "user", "content": tool_results})

    print(f"\nStopped after max turns ({args.max_turns}).", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
