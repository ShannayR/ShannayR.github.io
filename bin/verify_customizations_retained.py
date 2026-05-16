#!/usr/bin/env python3

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

DEFAULT_PATHS = [
    "_pages/**",
    "_projects/**",
    "_posts/**",
    "_bibliography/**",
    "assets/pdf/**",
    "assets/img/**",
    "assets/bibliography/**",
    "_data/cv.yml",
    "_data/socials.yml",
]


def run_git(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout


def file_matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def parse_changed_files(diff_output: str) -> list[str]:
    files: list[str] = []
    for line in diff_output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]

        # rename/copy entries: R100 old new / C100 old new
        if status.startswith(("R", "C")) and len(parts) >= 3:
            files.append(parts[2])
            continue

        # normal entries: A/M/D/etc path
        if len(parts) >= 2:
            if status == "D":
                # Deletions are paths removed in previous_ref and should not be
                # required to exist in current_ref.
                continue
            files.append(parts[1])

    return sorted(set(files))


def exists_at_ref(repo: Path, ref: str, path: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{ref}:{path}"],
        text=True,
        capture_output=True,
    )
    return completed.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify that customization files from a previous customized ref are retained "
            "after an upstream rebase/update."
        )
    )
    parser.add_argument("--repo", default=".", help="Path to the git repository (default: current directory)")
    parser.add_argument("--upstream-base", required=True, help="Upstream base ref used before customizations")
    parser.add_argument("--previous-ref", required=True, help="Previous customized ref before update/rebase")
    parser.add_argument("--current-ref", default="HEAD", help="Updated ref to verify (default: HEAD)")
    parser.add_argument(
        "--paths",
        nargs="*",
        default=DEFAULT_PATHS,
        help="Glob patterns that define retained customization scope",
    )

    args = parser.parse_args()
    repo = Path(args.repo).resolve()

    try:
        diff_output = run_git(
            repo,
            [
                "diff",
                "--name-status",
                "--find-renames",
                args.upstream_base,
                args.previous_ref,
            ],
        )
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr)
        return exc.returncode

    candidates = [p for p in parse_changed_files(diff_output) if file_matches(p, args.paths)]

    missing = [p for p in candidates if not exists_at_ref(repo, args.current_ref, p)]

    print(f"Scope patterns: {', '.join(args.paths)}")
    print(f"Candidates from {args.previous_ref} vs {args.upstream_base}: {len(candidates)}")

    if missing:
        print(f"Missing in {args.current_ref}: {len(missing)}")
        for path in missing:
            print(f"  - {path}")
        return 1

    print(f"All scoped customization files are retained in {args.current_ref}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
