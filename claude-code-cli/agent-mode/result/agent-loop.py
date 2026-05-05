#!/usr/bin/env python3
"""Minimal agentic loop using the Anthropic API with a bash tool.

Usage:
    export ANTHROPIC_API_KEY=...
    python agent-loop.py "list the files in the current directory"
"""
from __future__ import annotations

import subprocess
import sys

import anthropic

MODEL = "claude-opus-4-7"
SYSTEM = (
    "You are a helpful assistant with access to a `run_bash` tool that executes "
    "shell commands on the user's machine. Use it when needed to answer the user's "
    "request. Be concise."
)

TOOLS = [
    {
        "name": "run_bash",
        "description": (
            "Execute a bash command on the user's local machine and return its "
            "stdout, stderr, and exit code. The user will be asked to confirm "
            "before the command runs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute.",
                },
            },
            "required": ["command"],
        },
    }
]


def confirm(command: str) -> bool:
    print(f"\n\033[33m[agent wants to run]\033[0m {command}")
    answer = input("Approve? [y/N] ").strip().lower()
    return answer in ("y", "yes")


def run_bash(command: str) -> tuple[str, bool]:
    if not confirm(command):
        return ("Command rejected by user.", True)
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return ("Command timed out after 120s.", True)
    output = (
        f"exit_code: {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    return (output, result.returncode != 0)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: agent-loop.py <prompt>", file=sys.stderr)
        sys.exit(1)
    user_prompt = " ".join(sys.argv[1:])

    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": user_prompt}]

    while True:
        with client.messages.stream(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        ) as stream:
            for event in stream:
                if (
                    event.type == "content_block_start"
                    and event.content_block.type == "tool_use"
                ):
                    print(f"\n\033[36m[tool_use]\033[0m {event.content_block.name}")
                elif event.type == "content_block_delta":
                    if event.delta.type == "text_delta":
                        print(event.delta.text, end="", flush=True)
            response = stream.get_final_message()

        print()  # newline after streaming text

        if response.stop_reason == "end_turn":
            return

        if response.stop_reason != "tool_use":
            print(f"\n[stopped: {response.stop_reason}]", file=sys.stderr)
            return

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            if block.name == "run_bash":
                output, is_error = run_bash(block.input["command"])
                print(f"\033[90m{output}\033[0m")
            else:
                output, is_error = (f"Unknown tool: {block.name}", True)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                    "is_error": is_error,
                }
            )

        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    main()
