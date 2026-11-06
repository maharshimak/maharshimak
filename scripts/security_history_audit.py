from __future__ import annotations

import re
import subprocess
from pathlib import Path

PATTERNS = {
    "private key": rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "GitHub token": rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})",
    "OpenAI key": rb"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{25,}",
    "AWS access key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "Anthropic key": rb"\bsk-ant-[A-Za-z0-9_-]{20,}",
    "Hugging Face token": rb"\bhf_[A-Za-z0-9]{30,}\b",
    "Google API key": rb"\bAIza[0-9A-Za-z_-]{35}\b",
    "Stripe live secret": rb"\bsk_live_[0-9A-Za-z]{16,}\b",
    "Slack token": rb"\bxox[baprs]-[A-Za-z0-9-]{20,}\b",
    "npm token": rb"\bnpm_[A-Za-z0-9]{30,}\b",
    "GitLab token": rb"\bglpat-[A-Za-z0-9_-]{20,}\b",
    "Groq key": rb"\bgsk_[A-Za-z0-9]{20,}\b",
    "credential URL": rb"https?://[^\s/:@]+:[^\s/@]+@",
    "assigned secret": (
        rb"(?im)(?:password|secret|api[_-]?key|token)\s*[=:]\s*"
        rb"[\"'][A-Za-z0-9_+/=-]{20,}[\"']"
    ),
}

# Exact immutable false positives only. Keep this narrow: matching any other
# label/blob/path combination must still fail the audit.
ALLOWLISTED_FINDINGS = {
    (
        "credential URL",
        "ff0a3252c87a349bc6ed267391cc50df8db31e30",
        "tests/test_specialists.py",
    ): (
        "Synthetic URL-embedded credentials in makma-ai-os's negative test "
        "for rejecting HTTP adapter URLs with userinfo. This exception is "
        "limited to the reviewed immutable test fixture blob."
    ),
    (
        "credential URL",
        "e48b003899c301ead95e90263435fc0e06cac3d3",
        "tests/test_specialists.py",
    ): (
        "Earlier immutable version of the same makma-ai-os negative test, "
        "which verifies that the HTTP adapter rejects URL-embedded credentials."
    ),
    (
        "assigned secret",
        "73555f8035a9a4de97b9000e9fd77ac13a0a36cc",
        "tests/test_api_contracts.py",
    ): "Synthetic bearer-auth fixture in mlops-control-plane API contract tests.",
    (
        "assigned secret",
        "b9c094b63587b022a0c642d11f93487edbcfeb3b",
        "tests/test_api_contracts.py",
    ): "Earlier immutable synthetic bearer-auth fixture in mlops-control-plane.",
    (
        "assigned secret",
        "1d12945fa3bec01cee7d226f99332e35b74e2bde",
        "tests/test_api_contracts.py",
    ): "Earlier immutable synthetic bearer-auth fixture in mlops-control-plane.",
    (
        "assigned secret",
        "1d08dcc8cf9bc1ed99eda5070159715365525c68",
        "tests/test_deployment_http.py",
    ): (
        "Synthetic bearer token in mlops-control-plane's disposable loopback "
        "HTTP controller test; not an operational credential."
    ),
    (
        "credential URL",
        "e2f5d39824a251970c16008c5a303af9205386db",
        "tests/test_deployments.py",
    ): "Synthetic embedded-credentials rejection fixture in mlops-control-plane PR #11.",
    (
        "assigned secret",
        "1846bdcdab6d27e5c0dc4dcf8cfa0b8bf0d235e2",
        "README.md",
    ): (
        "Historical secure-data-copilot README bash example assigning "
        "a non-credential, human-readable 'your...' token placeholder. "
        "This exception is restricted to this one immutable blob."
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
                finding = (label, sha, path)
                if finding in ALLOWLISTED_FINDINGS:
                    continue
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
