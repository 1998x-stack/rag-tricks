"""Shared export inventory; keep selection and validation in one place."""
from pathlib import Path

EDITION = '2026-10-07'
ARTIFACTS = ('rag-tricks-handbook.epub', 'rag-tricks-detailed.xmind')
APPENDICES = ('contradictory.md', 'SOURCE_POLICY.md', 'sources/claim-audit.md',
              'docs/project-review.md', 'docs/maintenance.md')
DEPENDENCIES = (
    'scripts/export_handbook.py', 'scripts/export_manifest.py', 'scripts/quality_check.py',
    'tools/export/xmind.cjs', 'tools/export/package.json', 'tools/export/package-lock.json',
    'requirements-dev.txt', 'assets/exports/cover.png', 'assets/exports/epub.css',
    'sources/source-map.json',
)


def source_paths(root: Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in (root/'wiki').rglob('*.md')} | set(APPENDICES)
