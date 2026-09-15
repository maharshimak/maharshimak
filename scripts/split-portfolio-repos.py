"""Prepare verified history-preserving splits; optionally publish with GitHub CLI.

Run from the profile repository on a clean main branch. No source is removed.
Requires Python 3.12+, git-filter-repo, Git, and Docker; --publish also needs gh.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PATTERNS = {
    "private key": rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "GitHub token": rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})",
    "OpenAI key": rb"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{25,}",
    "AWS access key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "credential URL": rb"https?://[^\s/:@]+:[^\s/@]+@",
    "assigned secret": rb"""(?im)(?:password|secret|api[_-]?key|token)\s*[=:]\s*["'][A-Za-z0-9_+/=-]{20,}["']""",
}


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def audit(repo: Path) -> int:
    """Inspect every reachable blob without printing potential credential values."""
    count = 0
    for row in run("git", "rev-list", "--objects", "--all", cwd=repo).splitlines():
        sha, _, path = row.partition(" ")
        if run("git", "cat-file", "-t", sha, cwd=repo) != "blob":
            continue
        count += 1
        data = subprocess.check_output(["git", "cat-file", "blob", sha], cwd=repo)
        for label, pattern in PATTERNS.items():
            if re.search(pattern, data):
                raise RuntimeError(f"Review required: {label}, blob {sha}, path {path}")
        if re.search(
            r"(^|/)(\.env(?:\.[^/]+)?|id_rsa|credentials|.*\.(?:db|sqlite|pem|key))$",
            path,
        ) and not path.endswith(".env.example"):
            raise RuntimeError(f"Review sensitive filename in history: {path}, blob {sha}")
    return count


def validate(repo: Path) -> None:
    """Run in an isolated virtual environment, including a real container build."""
    run(sys.executable, "-m", "venv", ".venv", cwd=repo)
    python = (
        repo
        / ".venv"
        / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    )
    run(str(python), "-m", "pip", "install", "-e", ".[dev]", cwd=repo)
    run(str(python), "-m", "ruff", "check", ".", cwd=repo)
    run(str(python), "-m", "pytest", "-q", cwd=repo)
    run(str(python), "-m", "pip", "wheel", "--no-deps", ".", "-w", "dist", cwd=repo)
    run("docker", "build", "-t", f"{repo.name}:migration-check", ".", cwd=repo)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="maharshimak")
    parser.add_argument("--output", type=Path, default=Path("../portfolio-split"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", args.owner):
        parser.error("Invalid GitHub owner")
    source = Path(run("git", "rev-parse", "--show-toplevel")).resolve()
    metadata = json.loads((source / "docs/portfolio-repositories.json").read_text())
    source_sha = run("git", "rev-parse", "HEAD", cwd=source)
    if source_sha != run("git", "rev-parse", "refs/heads/main", cwd=source):
        raise RuntimeError("Check out main before preparing the migration")
    if run("git", "status", "--porcelain", cwd=source):
        raise RuntimeError("Source working tree must be clean")
    origin = run("git", "remote", "get-url", "origin", cwd=source)
    if origin not in (
        "https://github.com/maharshimak/maharshimak.git",
        "git@github.com:maharshimak/maharshimak.git",
    ):
        raise RuntimeError("Source origin must be maharshimak/maharshimak")
    if run("git", "rev-parse", "--is-shallow-repository", cwd=source) != "false":
        raise RuntimeError("A full clone is required to preserve history")
    print(f"Source commit: {source_sha}")
    for name in metadata:
        if not (source / "portfolio-projects" / name / "pyproject.toml").is_file():
            raise RuntimeError(f"Missing project: {name}")
        print(
            f"{name}: split history, scan, install, lint, test, build wheel/container"
        )
    if args.dry_run:
        print("Dry run: no filesystem or GitHub changes made")
        return
    for executable in ("git", "docker", *(["gh"] if args.publish else [])):
        if not shutil.which(executable):
            raise RuntimeError(f"Required executable is missing: {executable}")
    run(sys.executable, "-m", "git_filter_repo", "--version")
    if args.publish:
        run("gh", "auth", "status")
        if run("gh", "api", "user", "--jq", ".login") != args.owner:
            raise RuntimeError("Authenticated GitHub account does not match --owner")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    records = []
    # Prepare and validate ALL projects before the first public write.
    for name in metadata:
        dest = output / name
        run(
            "git",
            "clone",
            "--no-local",
            "--single-branch",
            "--branch",
            "main",
            str(source),
            str(dest),
        )
        run(
            sys.executable,
            "-m",
            "git_filter_repo",
            "--subdirectory-filter",
            f"portfolio-projects/{name}",
            cwd=dest,
        )
        actual = run("git", "rev-parse", "HEAD^{tree}", cwd=dest)
        expected = run(
            "git", "rev-parse", f"{source_sha}:portfolio-projects/{name}", cwd=source
        )
        if actual != expected:
            raise RuntimeError(f"Tree mismatch for {name}")
        blobs = audit(dest)
        validate(dest)
        records.append(
            {
                "name": name,
                "source": source_sha,
                "split": run("git", "rev-parse", "HEAD", cwd=dest),
                "blobs_scanned": blobs,
            }
        )
        (output / "verification.json").write_text(json.dumps(records, indent=2))
    if not args.publish:
        print(
            f"Prepared and validated {len(records)} splits in {output}; no public changes"
        )
        return
    for record in records:
        name = record["name"]
        repo = f"{args.owner}/{name}"
        url = f"https://github.com/{repo}.git"
        check = subprocess.run(
            ["gh", "api", f"repos/{repo}"], capture_output=True, text=True, check=False
        )
        if check.returncode:
            if "HTTP 404" not in check.stderr:
                raise RuntimeError(
                    f"Cannot inspect destination {repo}; refusing to infer absence"
                )
            run(
                "gh",
                "repo",
                "create",
                repo,
                "--public",
                "--description",
                metadata[name]["description"],
            )
        else:
            remote = json.loads(check.stdout)
            if remote.get("private"):
                raise RuntimeError(f"Refusing to change visibility of existing {repo}")
        # Query refs, never repository size. Never force-push or overwrite existing work.
        if run("git", "ls-remote", url):
            raise RuntimeError(f"Destination {repo} has refs; refusing to overwrite")
        run("git", "push", url, "main:main", cwd=output / name)
        if (
            run("git", "ls-remote", url, "refs/heads/main").split()[0]
            != record["split"]
        ):
            raise RuntimeError(f"Remote verification failed for {repo}")
        topic_args = [
            arg for topic in metadata[name]["topics"] for arg in ("--add-topic", topic)
        ]
        run(
            "gh",
            "repo",
            "edit",
            repo,
            "--default-branch",
            "main",
            "--description",
            metadata[name]["description"],
            "--homepage",
            "https://maharshipatel-portfolio.vercel.app/",
            *topic_args,
        )
        print(f"Published and verified {repo}; check its Actions before source cleanup")
    print(
        "Original folders retained. Cleanup requires verified public repositories and passing Actions."
    )


if __name__ == "__main__":
    main()
