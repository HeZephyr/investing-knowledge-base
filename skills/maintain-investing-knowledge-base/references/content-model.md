# Content model

## Layers

| Layer | Purpose | Mutability | Public |
|---|---|---|---:|
| `raw/` | Source cards and legally permitted snapshots | Append/version; do not silently rewrite history | Yes |
| `wiki/` | Linked synthesis maintained from Raw | Update with sources and date | Yes |
| `output/` | Reproducible reports and empty templates | Derived; record command and cutoff | Only generic/demonstration content |
| `private/` | Holdings, broker records, personal research | Local owner controls | Never |

The static site may read only public layers plus site assets. Caches, `.env`, third-party clones, private research, and browser/session state must not enter the site tree.

## Raw frontmatter

Required fields:

```yaml
id: raw-<authority>-<topic>
title: Stable source title
publisher: Responsible organization
url: https://canonical.example/path
retrieved: YYYY-MM-DD
source_grade: A
markets: [全球]
usage: link-and-summarize
```

Repository cards additionally record `license` and `pinned_commit`. Use `NOASSERTION` and link-only analysis when licensing is unclear.

## Wiki frontmatter

```yaml
title: Page title
aliases: [Alternative]
category: markets
markets: [全球]
level: beginner
status: seed
sources: [raw-authority-topic]
updated: YYYY-MM-DD
```

Required body pattern: definition, importance, mechanism/measurement, market differences, example, common mistakes, checklist, related pages, and source notes. A short topic may combine sections but must preserve the substance.

## Index axes

- Region: global → country/market → access route and disclosure system.
- Asset/product: equity, fund/ETF, bond, commodity/gold, cash, FX, derivatives.
- Sector: demand, supply, pricing, costs, capital cycle, regulation, company mapping.
- Method: accounting, valuation, macro, portfolio, risk, data, backtest, behavior.

Every new topic needs one canonical home and links from all applicable axes. A site search index and graph complement, but do not replace, curated human indexes and learning routes.
