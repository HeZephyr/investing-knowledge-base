---
name: maintain-investing-knowledge-base
description: Build and maintain a public, Obsidian-friendly investing knowledge base with traceable Raw sources, linked Wiki synthesis, reusable research outputs, free-data code, indexes, safety boundaries, and GitHub PR automation. Use when Codex is asked to add or update investment markets, assets, funds, sectors, experts, repositories, data providers, quant research, source cards, Wiki pages, indexes, or publishing workflows.
---

# Maintain an Investing Knowledge Base

Maintain evidence lineage and public reuse before maximizing page count. Treat markets, assets/products, sectors, and methods as orthogonal indexes.

## Start safely

1. Read the repository `AGENTS.md`, `docs/INDEX.md`, `wiki/index.md`, `config/knowledge-coverage.yaml`, and the nearest relevant index.
2. Confirm the working branch is not `main` or `master`. Create or link an Issue before material work.
3. Run the repository's baseline verification. Preserve unrelated user changes.
4. Keep holdings, accounts, costs, broker exports, Cookie, Token, personal assets, caches, and paid-source copies in the ignored private layer.

Read [content-model.md](references/content-model.md) before changing schemas or placement. Read [source-evaluation.md](references/source-evaluation.md) before collecting experts, repositories, current rules, or external data. Read [research-expansion.md](references/research-expansion.md) when adding a new market, asset, sector, or provider.

## Choose the workflow

- **Current fact, rule, fee, API, product, expert, or repository**: browse first; prefer primary/official sources and record the retrieval date.
- **New knowledge topic**: create Raw source cards first, then synthesize Wiki, then update all affected indexes.
- **Code or provider change**: write a failing test first; implement explicit validation, provenance, timeouts, and failure behavior.
- **Research output**: start from a public template, disclose data cutoff, assumptions, benchmark, costs, limitations, and reproduction command.
- **Publishing/governance change**: preserve least privilege, fork safety, public/private isolation, and PR-only `main`.

## Ingest sources

1. Search official regulators, exchanges, filing systems, standard setters, fund documents, papers, and maintained upstream repositories.
2. Evaluate authority, method transparency, conflicts, license, freshness, stability, and whether the material is fact, interpretation, or marketing.
3. Create one stable Raw card per source. Use `scripts/scaffold_source_card.py` when the repository follows the standard schema.
4. Summarize; do not reproduce long copyrighted text. Pin repository commits and record licenses. Treat Star counts only as discovery signals.
5. For authenticated sources, use only authorized local credentials. Never commit or publish credentials, reverse-engineered access bypasses, or session material.

## Synthesize knowledge

1. State definitions and mechanisms before opinions.
2. Separate source facts, calculations, and inferences. Label unresolved conflicts `disputed`.
3. Cover market-specific differences, examples, failure modes, a checklist, related pages, and source IDs.
4. Link the page across every relevant axis: region, asset/product, sector, and method. Avoid duplicating the same fact in multiple pages.
5. Update the learning route, Wiki index, Raw catalog, repository catalog, site navigation, and append-only maintenance log where applicable.
6. Update `config/knowledge-coverage.yaml` with the actual evidence, status, verification date, and remaining gap. Never promote an item merely because a page exists.
7. When work exposes a failed hypothesis, data accident, licensing rejection, CI failure, or repeated mistake, append the reusable pattern to `[[经验与失败教训]]` and add a regression check where possible.

Map each change to one atomic capability stage instead of treating a topic page as complete:

- `content-ready`: validate only with an authoritative `source` plus a maintained `synthesis`.
- `exercise-tested`: validate only with `implementation + test` or `synthesis + test`.
- `case-validated`: validate only with a frozen public `source + report + test`, including negative results where relevant.
- `maintenance-live`: validate only with a scheduled or protected `workflow + test`.

`status` and `stage` answer different questions. Keep an explicit gap for every missing, seed, or reviewed capability; never upgrade an unrelated stage because another stage passed.

## Validate code and data

- Use adjusted/unadjusted prices deliberately and document the convention.
- Enforce next-tradable-time execution; reject same-bar lookahead.
- Record provider, endpoint, parameters, retrieval time, version, row count, and content hash.
- Fail on empty responses, schema drift, duplicate keys, nonpositive prices, invalid OHLC, and timezone ambiguity.
- Backtests must include benchmark, fees, slippage, untradeable states, out-of-sample evidence, and sensitivity analysis.
- Free providers have no SLA. Keep live smoke checks scheduled and separate from deterministic PR tests.

## Publish through review

1. Run formatting, unit tests, `coverage validate`, Raw/Wiki integrity, public-boundary audit, offline research smoke, and strict site build.
2. Inspect the public diff for personal material, secrets, generated caches, copyright problems, and broken indexes.
3. Commit conventionally on a topic branch and push it.
4. Open a PR that closes its Issue and records sources, data cutoff, tests, risks, and public-boundary checks.
5. Do not bypass required checks, conversations, linear history, or branch protection. Merge only after the protected workflow passes.

## Stop conditions

Stop and request authority when work requires buying data, accepting a license, publishing private material, sharing credentials, connecting a broker, placing trades, or changing repository/account security beyond the stated task. Do not stop merely because a free provider is flaky; isolate it, document it, and continue with other verifiable work.
