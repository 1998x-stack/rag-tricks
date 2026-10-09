# CLAUDE.md

This repository is a Chinese RAG engineering knowledge base. It originated from a structured extraction of 《字节跳动 RAG 实践手册》 and is evolving into an evidence-aware engineering handbook.

## Primary goals

When editing the repository, optimize for:

1. factual traceability;
2. useful engineering decisions;
3. maintainable navigation and links;
4. explicit tradeoffs and applicability boundaries;
5. testable content quality.

Do not optimize only for prose polish.

## Evidence model

Every material technical claim should be understood as one of:

- **Source** — directly supported by an identifiable source passage.
- **Synthesis** — structured summary of one or more sources without adding a new key factual claim.
- **Derived** — engineering inference, recommendation, or design proposal.
- **External** — material from outside the original manual with an explicit source.
- **Unverified** — historical content not yet audited.

Never convert a Derived or Unverified statement into a Source statement merely by rewriting it more confidently.

High-risk claims include precise percentages, QPS, latency, cost, dates of incidents, business scale, internal component names, and statements about what a specific company “uses”, “defaults to”, or “achieved”.

See `SOURCE_POLICY.md` and `sources/source-map.json`.

## Content conventions

Existing deep-dive pages commonly follow:

```text
# <名称>
## 是什么
## 为什么重要
## 如何使用
## 常见误区
## 参见
```

This structure is no longer mandatory for every page type. Prefer the structure that fits the content:

- Concept
- Pattern
- Decision
- Playbook
- Case
- Benchmark
- Failure
- Tradeoff
- Checklist
- Glossary

For decision/tradeoff pages, explicitly include constraints, alternatives, evaluation dimensions, risks, and validation experiments when possible.

## Links

The repository currently supports two audiences:

- Obsidian users: standard relative Markdown links are supported.
- GitHub / Pages users: important navigation paths should also use standard Markdown links.

Do not assume Jekyll Cayman renders Obsidian wikilinks.

Use standard Markdown links throughout the knowledge base. Wikilinks in prose trigger the strict gate; code examples are ignored.

## Adding or changing factual content

Before adding a precise factual claim:

1. identify whether it is Source / Synthesis / Derived / External / Unverified;
2. add source details when available;
3. avoid inventing page numbers or citations;
4. include scope and measurement context for metrics;
5. distinguish illustrative examples from documented historical incidents.

If a source cannot yet be located, mark the claim as requiring verification instead of fabricating provenance.

## Quality checks

Install `requirements-dev.txt` in a Python 3.10+ virtual environment, then run:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/quality_check.py --strict
```

The parser checks local links and heading anchors (including images and references), registry types and page evidence markers, H1 titles, evidence sections and navigation reachability. CI fails on both errors and warnings. It does not verify external URLs or certify factual claims. See `docs/maintenance.md`.

Register every knowledge page in `sources/source-map.json`. Keep unresolved historical claims Unverified even after fixing links or definitions. Exact extraction markers and audit limitations are in `sources/claim-audit.md`.

## Repository structure

```text
rag-tricks/
├── README.md
├── index.md
├── SOURCE_POLICY.md
├── CONTRIBUTING.md
├── contradictory.md
├── wiki/
├── sources/
│   └── source-map.json
├── scripts/
│   └── quality_check.py
├── .github/workflows/
│   └── content-quality.yml
└── raw/
```

## Raw source material

Files under `raw/` may have independent copyright or redistribution constraints. Do not infer redistribution permission from the fact that a file is already in the repository. Do not add new third-party source files without checking provenance and permission.

## Long-term direction

The intended information architecture is:

```text
Learn  → concepts and learning paths
Build  → system design and implementation patterns
Debug  → symptom-driven troubleshooting
Decide → tradeoffs and technical decisions
Verify → provenance, evidence, and measurement context
```

Future site work should preserve Obsidian compatibility while making wikilinks, backlinks, search, and knowledge graph navigation work on the web.
