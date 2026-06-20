# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

Structured Obsidian wiki of ByteDance RAG (Retrieval-Augmented Generation) practices extracted from 《字节跳动 RAG 实践手册》(118-page PDF). 62 Markdown files across 10 category directories, all in Chinese, cross-linked with `[[wikilinks]]`.

## Content conventions

**Every deep-dive page** follows this 5-section structure:
```
# <名称>
## 是什么
## 为什么重要
## 如何使用
## 常见误区
## 参见
```

**Every main category page** follows:
```
# <类别名>
## 概述
## 详细知识 (bullet index of sub-pages with one-line descriptions)
## 核心实践 (table: 实践 | 场景 | 要点 | 参见)
```

**Language**: All content in Chinese. Preserve original technical terminology from the source PDF.

**Source**: Content paraphrased from `raw/字节跳动 RAG 实践手册.pdf` — no original author attribution needed (single-company manual, not crowdsourced tips).

## Wiki-link conventions

- Same-directory links: `[[page-name]]` (no `.md` extension)
- Cross-category links: `[[../category/page-name]]`
- Root-level links: `[[../../contradictory]]`, `[[../../index]]`
- Architecture/model/product names (`ByteVectorDB`, `Milvus`, `HNSW`, `BERT`, `ByteBM25`, `云雀`) are acceptable red links

## Adding new content

1. New deep-dive page → place in the matching category directory, follow 5-section format
2. New main category → create directory + main page, add to `index.md` nav table and `README.md`
3. New practices → add to the relevant main page under `## 核心实践` in the table format
4. New contradictions → add to `contradictory.md` following the existing entry format (table + analysis)
5. After adding pages, scan for orphan `[[wikilinks]]` and resolve them

## GitHub Pages

Site hosted at `1998x-stack.github.io/rag-tricks/` via Jekyll + Cayman theme. Config in `_config.yml`. Entry point is `index.md`. Pages rebuild on push to `main`.
