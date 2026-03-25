#!/usr/bin/env python3
"""Minimal agentic loop using the Anthropic API and a confirmed bash tool."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from typing import Any

try:
    from anthropic import Anthropic  # type: ignore[import-not-found]
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: anthropic. Install with `pip install anthropic`."
    ) from exc


SYSTEM_PROMPT = (
    "You are a helpful coding assistant. "
    "When useful, call the run_bash tool to inspect or run commands. "
    "Always explain your reasoning briefly and avoid destructive commands."
)

TOOLS: list[dict[str, Any]] = [
    {
        "name": "run_bash",
        "description": "Run a bash command on the local machine.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute.",
                }
            },
            "required": ["command"],
        },
    }
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal Anthropic agentic loop")
    parser.add_argument("prompt", nargs="*", help="Initial user prompt")
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-5",
        help="Anthropic model name (default: claude-sonnet-4-5)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="Max tokens per model response",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Seconds before bash command timeout",
    )
    return parser.parse_args()


def prompt_user_for_command(command: str) -> bool:
    print("\nTool request: run_bash")
    print(f"Command: {command}")
    choice = input("Execute this command? [y/N]: ").strip().lower()
    return choice in {"y", "yes"}


def run_bash(command: str, timeout_seconds: int) -> str:
    try:
        completed = subprocess.run(
            ["bash", "-lc", command],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout_seconds} seconds."
    except Exception as exc:  # pragma: no cover
        return f"Execution failed: {exc}"

    output = (
        f"Exit code: {completed.returncode}\n"
        f"--- STDOUT ---\n{completed.stdout or '(empty)'}\n"
        f"--- STDERR ---\n{completed.stderr or '(empty)'}"
    )
    max_len = 12_000
    if len(output) > max_len:
        output = output[:max_len] + "\n[output truncated]"
    return output


def serialize_block(block: Any) -> dict[str, Any]:
    if block.type == "text":
        return {"type": "text", "text": block.text}
    if block.type == "tool_use":
        return {
            "type": "tool_use",
            "id": block.id,
            "name": block.name,
            "input": block.input,
        }
    return {"type": block.type}


def main() -> int:
    args = parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        return 1

    initial_prompt = " ".join(args.prompt).strip()
    if not initial_prompt:
        initial_prompt = input("User prompt: ").strip()
    if not initial_prompt:
        print("No prompt provided.", file=sys.stderr)
        return 1

    client = Anthropic(api_key=api_key)
    messages: list[dict[str, Any]] = [{"role": "user", "content": initial_prompt}]

    while True:
        response = client.messages.create(
            model=args.model,
            max_tokens=args.max_tokens,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        assistant_content = [serialize_block(block) for block in response.content]
        messages.append({"role": "assistant", "content": assistant_content})

        tool_uses = [block for block in response.content if block.type == "tool_use"]

        for block in response.content:
            if block.type == "text" and block.text.strip():
                print(f"\nAssistant: {block.text}")

        if not tool_uses:
            break

        tool_results: list[dict[str, Any]] = []
        for tool_use in tool_uses:
            if tool_use.name != "run_bash":
                result = f"Unsupported tool: {tool_use.name}"
            else:
                command = str(tool_use.input.get("command", "")).strip()
                if not command:
                    result = "Invalid input: missing command"
                elif not prompt_user_for_command(command):
                    result = "Command not executed: user denied confirmation."
                else:
                    result = run_bash(command, timeout_seconds=args.timeout)
                    print(f"\nTool output:\n{result}")

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result,
                }
            )

        messages.append({"role": "user", "content": tool_results})

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
