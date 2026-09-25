from __future__ import annotations

import re
import subprocess
from pathlib import Path

PATTERNS = {
    "private key": rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "GitHub token": rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})",
    "OpenAI key": rb"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{25,}",
    "AWS access key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "credential URL": rb"https?://[^\s/:@]+:[^\s/@]+@",
    "assigned secret": (
        rb"(?im)(?:password|secret|api[_-]?key|token)\s*[=:]\s*"
        rb"[\"'][A-Za-z0-9_+/=-]{20,}[\"']"
    ),
}


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def audit(repo: Path) -> int:
    """Inspect every reachable Git blob without printing potential secret values."""
    count = 0
    for row in run("git", "rev-list", "--objects", "--all", cwd=repo).splitlines():
        sha, _, path = row.partition(" ")
        if run("git", "cat-file", "-t", sha, cwd=repo) != "blob":
            continue
        count += 1
        data = subprocess.check_output(
            ["git", "cat-file", "blob", sha],
            cwd=repo,
        )
        for label, pattern in PATTERNS.items():
            if re.search(pattern, data):
                raise RuntimeError(
                    f"Review required: {label}, blob {sha}, path {path}"
                )
        if (
            re.search(
                r"(^|/)(\.env(?:\.[^/]+)?|id_rsa|credentials|.*\.(?:db|sqlite|pem|key))$",
                path,
            )
            and not path.endswith(".env.example")
        ):
            raise RuntimeError(
                f"Review sensitive filename in history: {path}, blob {sha}"
            )
    return count
