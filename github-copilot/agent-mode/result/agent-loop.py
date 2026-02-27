#!/usr/bin/env python3
"""Minimal Anthropic-powered agent loop with a bash tool.

Requirements:
  pip install anthropic
  export ANTHROPIC_API_KEY=...

Usage:
  python agent.py "Find Python files and count lines"
  python agent.py
"""

from __future__ import annotations

import argparse
import importlib
import os
import shlex
import subprocess
import sys
from typing import Any


SYSTEM_PROMPT = (
    "You are a helpful coding agent. "
    "Use the run_bash tool when shell execution is needed. "
    "Before each tool call, think carefully and keep commands concise."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal Anthropic agent loop with bash tool")
    parser.add_argument("task", nargs="*", help="Initial user task")
    parser.add_argument("--model", default="claude-sonnet-4-5", help="Anthropic model name")
    parser.add_argument("--max-steps", type=int, default=20, help="Maximum agent iterations")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Max tokens per model call")
    parser.add_argument(
        "--command-timeout",
        type=int,
        default=60,
        help="Timeout in seconds for each bash command",
    )
    parser.add_argument(
        "--cwd",
        default=os.getcwd(),
        help="Working directory for bash commands (default: current directory)",
    )
    return parser.parse_args()


def confirm_execution(command: str) -> bool:
    print("\n--- Tool request: run_bash ---")
    print(command)
    print("--------------------------------")
    reply = input("Execute this command? Type 'yes' to continue: ").strip().lower()
    return reply == "yes"


def run_bash(command: str, cwd: str, timeout: int) -> str:
    if not confirm_execution(command):
        return "Execution denied by human."

    try:
        completed = subprocess.run(
            command,
            shell=True,
            executable="/bin/bash",
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return f"Command timed out after {timeout}s.\nPartial output:\n{exc.stdout or ''}\n{exc.stderr or ''}"
    except Exception as exc:
        return f"Failed to execute command: {type(exc).__name__}: {exc}"

    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()

    result_parts = [f"exit_code: {completed.returncode}"]
    if stdout:
        result_parts.append(f"stdout:\n{stdout}")
    if stderr:
        result_parts.append(f"stderr:\n{stderr}")
    if not stdout and not stderr:
        result_parts.append("(no output)")

    return "\n\n".join(result_parts)


def block_to_message_param(block: Any) -> dict[str, Any]:
    if block.type == "text":
        return {"type": "text", "text": block.text}
    if block.type == "tool_use":
        return {
            "type": "tool_use",
            "id": block.id,
            "name": block.name,
            "input": block.input,
        }
    return {"type": "text", "text": f"[Unsupported block type: {block.type}]"}


def main() -> None:
    args = parse_args()

    try:
        anthropic = importlib.import_module("anthropic")
    except ImportError:
        print("Missing dependency: anthropic")
        print("Install with: pip install anthropic")
        sys.exit(1)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Missing ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)

    if not os.path.isdir(args.cwd):
        print(f"Invalid --cwd: {args.cwd}")
        sys.exit(1)

    task = " ".join(args.task).strip()
    if not task:
        task = input("Enter task: ").strip()
    if not task:
        print("No task provided.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    tools = [
        {
            "name": "run_bash",
            "description": "Run a bash command and return stdout/stderr/exit code.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Bash command to execute",
                    }
                },
                "required": ["command"],
            },
        }
    ]

    messages: list[dict[str, Any]] = [{"role": "user", "content": task}]

    for step in range(1, args.max_steps + 1):
        response = client.messages.create(
            model=args.model,
            system=SYSTEM_PROMPT,
            max_tokens=args.max_tokens,
            tools=tools,
            messages=messages,
        )

        assistant_content = [block_to_message_param(block) for block in response.content]
        messages.append({"role": "assistant", "content": assistant_content})

        print(f"\n===== Step {step} =====")
        for block in response.content:
            if block.type == "text":
                text = block.text.strip()
                if text:
                    print(text)

        tool_uses = [block for block in response.content if block.type == "tool_use"]
        if not tool_uses:
            print("\nAgent finished.")
            return

        tool_results = []
        for tool_use in tool_uses:
            if tool_use.name != "run_bash":
                result_text = f"Unknown tool: {tool_use.name}"
            else:
                command = str(tool_use.input.get("command", ""))
                if not command:
                    result_text = "Missing required input: command"
                else:
                    print(f"\nRequested command: {shlex.quote(command) if ' ' not in command else command}")
                    result_text = run_bash(
                        command=command,
                        cwd=args.cwd,
                        timeout=args.command_timeout,
                    )

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result_text,
                }
            )

        messages.append({"role": "user", "content": tool_results})

    print("\nReached max steps without final response.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
