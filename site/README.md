# Quartz site integration

This directory stores only RAG Tricks-specific Quartz configuration.

## Engine pin

The workflow pins Quartz v4.5.2 branch commit:

    d25a6eabf96751ffca56f8a8139272def7a65041

The engine is cloned into a temporary `.quartz-engine/` directory during CI. This keeps framework internals out of the knowledge-base repository and makes the dependency boundary explicit.

Upgrade policy:

1. choose a new upstream Quartz commit;
2. review upstream release notes and config API changes;
3. update the SHA in `.github/workflows/quartz-site.yml`;
4. update `quartz.config.ts` / `quartz.layout.ts` if required;
5. require a successful PR build before merging.

## Published content

`scripts/prepare_quartz_content.py` publishes the knowledge content and intentionally excludes `raw/`, repository automation docs, and framework files.

## Local preview

To preview with the exact CI engine:

    git clone https://github.com/jackyzha0/quartz.git .quartz-engine
    git -C .quartz-engine checkout --detach d25a6eabf96751ffca56f8a8139272def7a65041
    python3 scripts/prepare_quartz_content.py --output .quartz-engine/content
    cp site/quartz.config.ts .quartz-engine/quartz.config.ts
    cp site/quartz.layout.ts .quartz-engine/quartz.layout.ts
    cd .quartz-engine
    npm ci
    npx quartz build --serve

## GitHub Pages

After this PR is merged, GitHub Pages must use **GitHub Actions** as its source. The workflow only deploys on pushes to `main`; pull requests perform a build-only verification.
