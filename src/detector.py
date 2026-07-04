
import subprocess
import json
from typing import List

def run_pylint(path: str) -> List[str]:
    """
    Run pylint on a file and return list of formatted messages.
    Handles JSON parsing issues gracefully.
    """
    try:
        result = subprocess.run(
            ["pylint", path, "--output-format=json"],
            capture_output=True,
            text=True
        )
    except FileNotFoundError:
        return ["Error: Pylint not installed or not found in PATH."]

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    # If pylint throws errors in stderr
    if stderr and "Traceback" in stderr:
        return [f"Pylint internal error: {stderr}"]

    # No issues
    if stdout == "":
        return []

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        # fallback to raw text
        return stdout.splitlines()

    messages = []
    for msg in data:
        code = msg.get("message-id")
        text = msg.get("message")
        line = msg.get("line")
        messages.append(f"[{code}] Line {line}: {text}")

    return messages
