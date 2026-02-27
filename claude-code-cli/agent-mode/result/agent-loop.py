#!/usr/bin/env python3
"""Minimal agentic loop with a bash tool and human confirmation."""

from __future__ import annotations

import subprocess
import sys

import anthropic

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096

SYSTEM_PROMPT = """\
You are a helpful assistant with access to a bash tool. \
Use it to answer questions, explore the filesystem, run scripts, and accomplish tasks. \
Always explain what you intend to do before invoking a command.\
"""

TOOLS = [
    {
        "name": "run_bash",
        "description": (
            "Execute a bash command and return its stdout and stderr. "
            "The command runs in the user's shell. Use this for file operations, "
            "running scripts, installing packages, querying system info, etc."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute",
                },
            },
            "required": ["command"],
        },
    }
]


def run_bash(command: str) -> str:
    """Execute a bash command and return combined output."""
    result = subprocess.run(
        ["bash", "-c", command],
        capture_output=True,
        text=True,
        timeout=120,
    )
    output_parts = []
    if result.stdout:
        output_parts.append(result.stdout)
    if result.stderr:
        output_parts.append(f"[stderr]\n{result.stderr}")
    output_parts.append(f"[exit code: {result.returncode}]")
    return "\n".join(output_parts)


def confirm(command: str) -> bool:
    """Ask the user to confirm before running a command."""
    print(f"\n{'─' * 60}")
    print(f"  Tool call: run_bash")
    print(f"  Command:   {command}")
    print(f"{'─' * 60}")
    while True:
        answer = input("  Run this command? [y/n]: ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatch a tool call, gated by human confirmation."""
    if name != "run_bash":
        return f"Error: unknown tool '{name}'"

    command = tool_input["command"]
    if not confirm(command):
        return "User declined to run this command."

    try:
        return run_bash(command)
    except subprocess.TimeoutExpired:
        return "Error: command timed out after 120 seconds."
    except Exception as e:
        return f"Error: {e}"


def agent_loop(user_message: str) -> None:
    """Run the agentic loop until Claude stops calling tools."""
    client = anthropic.Anthropic()
    messages: list[dict] = [{"role": "user", "content": user_message}]

    while True:
        print("\n... thinking", end="", flush=True)

        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
            response = stream.get_final_message()

        print()

        if response.stop_reason == "end_turn":
            break

        # Extract tool_use blocks
        tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
        if not tool_use_blocks:
            break

        # Append assistant response (preserves tool_use blocks)
        messages.append({"role": "assistant", "content": response.content})

        # Execute each tool and collect results
        tool_results = []
        for tool in tool_use_blocks:
            result = execute_tool(tool.name, tool.input)
            print(f"\n{result}")
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool.id,
                    "content": result,
                }
            )

        messages.append({"role": "user", "content": tool_results})


def main() -> None:
    if len(sys.argv) > 1:
        user_message = " ".join(sys.argv[1:])
        agent_loop(user_message)
        return

    print("Agent Loop (type 'quit' to exit)\n")
    while True:
        try:
            user_message = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_message or user_message.lower() in ("quit", "exit"):
            break
        agent_loop(user_message)


if __name__ == "__main__":
    main()
