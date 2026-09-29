#!/usr/bin/env python3
"""Static quality checks for the RAG Tricks knowledge base.

Hard failures are intentionally limited to deterministic repository integrity
problems. Historical evidence debt is reported as warnings so the repository
can migrate incrementally.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAP = ROOT / "sources" / "source-map.json"

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
STRICT_FRONTMATTER_PREFIXES = (
    "wiki/evaluation/",
    "wiki/decisions/",
    "wiki/production/",
    "wiki/cases/",
    "wiki/benchmarks/",
    "wiki/business-cases/",
)
REQUIRED_FRONTMATTER_KEYS = ("title", "type", "evidence", "verified_at")

NUMERIC_CLAIM_RE = re.compile(
    r"(?:\d+(?:\.\d+)?\s*%|\bQPS\b|\bP(?:50|95|99)\b|"
    r"\d+(?:\.\d+)?\s*(?:ms|毫秒|秒|分钟|小时|万|亿|GB|MB|TB))",
    re.IGNORECASE,
)


def markdown_files() -> list[Path]:
    return sorted(
        p for p in ROOT.rglob("*.md")
        if ".git" not in p.parts
    )


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalize_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "data:", "#")):
        return None

    # Markdown links may contain an optional quoted title after the URL.
    if " \"" in target:
        target = target.split(" \"", 1)[0]
    target = target.split("#", 1)[0].split("?", 1)[0]
    target = unquote(target)
    if not target:
        return None

    if target.startswith("/"):
        return ROOT / target.lstrip("/")
    return (source.parent / target).resolve()


def check_markdown_links(files: list[Path], errors: list[str]) -> None:
    for path in files:
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = normalize_target(path, match.group(1))
            if target is None:
                continue
            if not target.exists():
                errors.append(f"broken markdown link: {rel(path)} -> {match.group(1)}")


def resolve_wikilink(source: Path, raw: str) -> Path | None:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return None
    if not target.endswith(".md"):
        target += ".md"

    candidate = (source.parent / target).resolve()
    if candidate.exists():
        return candidate

    root_candidate = (ROOT / target).resolve()
    if root_candidate.exists():
        return root_candidate
    return None


def check_wikilinks(files: list[Path], warnings: list[str]) -> None:
    unresolved: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for match in WIKILINK_RE.finditer(text):
            raw = match.group(1)
            if resolve_wikilink(path, raw) is None:
                unresolved.append(f"{rel(path)} -> [[{raw}]]")

    if unresolved:
        preview = unresolved[:30]
        warnings.append(
            f"unresolved wikilinks: {len(unresolved)} total; first {len(preview)}:\n  "
            + "\n  ".join(preview)
        )


def check_duplicate_titles(files: list[Path], warnings: list[str]) -> None:
    titles: dict[str, list[str]] = defaultdict(list)
    for path in files:
        text = path.read_text(encoding="utf-8")
        match = H1_RE.search(text)
        if match:
            titles[match.group(1).strip()].append(rel(path))

    duplicates = {title: paths for title, paths in titles.items() if len(paths) > 1}
    for title, paths in sorted(duplicates.items()):
        warnings.append(f"duplicate H1 '{title}': {', '.join(paths)}")


def check_numeric_claims(files: list[Path], warnings: list[str]) -> None:
    flagged: list[tuple[str, int]] = []
    for path in files:
        if "wiki" not in path.parts and path.name != "contradictory.md":
            continue
        text = path.read_text(encoding="utf-8")
        count = len(NUMERIC_CLAIM_RE.findall(text))
        if count >= 3 and "## 来源与证据" not in text:
            flagged.append((rel(path), count))

    if flagged:
        flagged.sort(key=lambda x: (-x[1], x[0]))
        preview = flagged[:30]
        lines = [f"{path} ({count} numeric markers)" for path, count in preview]
        warnings.append(
            f"numerically dense pages without 来源与证据: {len(flagged)} total; "
            f"first {len(preview)}:\n  " + "\n  ".join(lines)
        )


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line.startswith((" ", "\t", "#")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def check_content_schema(files: list[Path], errors: list[str]) -> None:
    for path in files:
        relative = rel(path)
        if not relative.startswith(STRICT_FRONTMATTER_PREFIXES):
            continue
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)
        if not metadata:
            errors.append(f"missing frontmatter: {relative}")
            continue
        missing = [key for key in REQUIRED_FRONTMATTER_KEYS if not metadata.get(key)]
        if missing:
            errors.append(f"missing frontmatter keys in {relative}: {', '.join(missing)}")
        if metadata.get("type") == "case":
            if "## Case Metadata" not in text:
                errors.append(f"case missing Case Metadata section: {relative}")
            if "## 来源与证据" not in text:
                errors.append(f"case missing 来源与证据 section: {relative}")

def check_source_map(errors: list[str]) -> None:
    if not SOURCE_MAP.exists():
        errors.append("missing sources/source-map.json")
        return

    try:
        data = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid source-map JSON: {exc}")
        return

    allowed = set(data.get("statuses", []))
    if not allowed:
        errors.append("source-map statuses must not be empty")

    sources = data.get("sources", {})
    pages = data.get("pages", {})
    if not isinstance(pages, dict):
        errors.append("source-map pages must be an object")
        return

    for page, entry in pages.items():
        if not (ROOT / page).exists():
            errors.append(f"source-map references missing page: {page}")
        status = entry.get("status")
        if status not in allowed:
            errors.append(f"source-map invalid status for {page}: {status!r}")
        for ref in entry.get("source_refs", []):
            if ref not in sources:
                errors.append(f"source-map unknown source ref for {page}: {ref}")


def main() -> int:
    files = markdown_files()
    errors: list[str] = []
    warnings: list[str] = []

    check_markdown_links(files, errors)
    check_wikilinks(files, warnings)
    check_duplicate_titles(files, warnings)
    check_numeric_claims(files, warnings)
    check_content_schema(files, errors)
    check_source_map(errors)

    print(f"Checked {len(files)} Markdown files.")
    if warnings:
        print(f"\nWARNINGS ({len(warnings)} groups)")
        for item in warnings:
            print(f"- {item}")

    if errors:
        print(f"\nERRORS ({len(errors)})")
        for item in errors:
            print(f"- {item}")
        return 1

    print("\nNo blocking content-integrity errors found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
