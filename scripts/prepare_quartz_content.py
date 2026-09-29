#!/usr/bin/env python3
"""Prepare the repository's publishable Markdown as a Quartz content tree."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PUBLISH_ROOT_FILES = (
    "index.md",
    "contradictory.md",
    "SOURCE_POLICY.md",
    "CONTRIBUTING.md",
)
PUBLISH_DIRS = ("wiki", "sources")


def copy_path(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True)
    elif source.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    output = args.output.resolve()

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    missing: list[str] = []
    for name in PUBLISH_ROOT_FILES:
        src = root / name
        if not src.exists():
            missing.append(name)
            continue
        copy_path(src, output / name)

    for name in PUBLISH_DIRS:
        src = root / name
        if not src.exists():
            missing.append(name)
            continue
        copy_path(src, output / name)

    # Repository maintenance metadata is useful as source material but should
    # not become part of the public knowledge garden by default. raw/ is also
    # intentionally excluded because third-party redistribution provenance is
    # still being audited.
    if missing:
        raise SystemExit("Missing publish inputs: " + ", ".join(missing))

    md_count = sum(1 for _ in output.rglob("*.md"))
    if md_count < 50:
        raise SystemExit(f"Unexpectedly small Quartz content tree: {md_count} Markdown files")

    print(f"Prepared {md_count} Markdown files under {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
