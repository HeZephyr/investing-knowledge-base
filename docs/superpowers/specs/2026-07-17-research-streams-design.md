# Issue #9 Research Streams Design

## Goal

Expand the public knowledge base with three artifact-first research streams—Open Yale Courses, the AQR Data Library, and the GMO Research Library—then synthesize them into a falsifiable cross-stream evidence matrix and a reusable empirical-evidence output template.

## Scope and chosen approach

Three approaches were considered:

1. **Content only:** add three Raw cards and one Wiki page. This is the smallest change, but it leaves no reusable Output-layer workflow.
2. **Traceable content plus an empirical template (chosen):** add the cards, evidence matrix, indexes, append-only log, and a template that requires a data cutoff, point-in-time controls, conflicts, costs, and a reproduction command. This satisfies Raw → Wiki → Output without redistributing third-party data.
3. **Live downloader and parser:** automatically fetch AQR spreadsheets and GMO material. This has the highest maintenance and licensing risk because the sites do not grant a clear redistribution license and their endpoints or terms can change.

Issue #9 already defines the requested sources and acceptance criteria. The automation request authorizes selecting and implementing one bounded issue, so the Issue and pull-request review serve as the design approval gates for this unattended run.

## Content architecture

### Raw layer

Create one stable card for each public artifact:

- `raw/experts/cards/shiller-yale-financial-markets.md`
- `raw/experts/cards/aqr-data-library.md`
- `raw/experts/cards/gmo-research-library.md`

Each card records the canonical URL, retrieval date, source grade, markets, artifact scope, update frequency, publisher incentives, license or terms, limitations, and invalidation conditions. The AQR card additionally records available return-series types, monthly/daily frequency where applicable, hypothetical-portfolio status, citation request, point-in-time risks, and the distinction between frozen paper samples and updated extensions.

No course transcript, spreadsheet, forecast, chart, or article copy will be committed. Yale material is summarized and linked under its non-commercial share-alike terms; AQR and GMO material is link-and-analyze only with `NOASSERTION` where no reusable data license is stated.

### Wiki layer

Create `wiki/methods/投资研究证据矩阵.md` as the canonical synthesis. It compares:

- valuation;
- quality;
- momentum;
- behavioral mechanisms;
- macro and asset allocation.

For each stream, the page separates source facts from inferences, identifies observable variables and historical-time availability, names conflicts and implementation frictions, and defines conditions that would weaken or invalidate the claim. It links to existing pages such as `[[估值]]`, `[[因子研究]]`, `[[行为偏差]]`, `[[样本外测试]]`, and `[[换手与交易成本]]`.

### Output layer

Create `output/templates/实证证据卡.md`. A completed copy must state:

- source IDs and artifact versions;
- data provider, retrieval time, cutoff, frequency, units, row count, and content hash;
- hypothesis, benchmark, costs, lag, and point-in-time rules;
- sample split and sensitivity checks;
- conflicts, licenses or terms, limitations, failure conditions, and a literal reproduction command.

The template contains no third-party data and makes no performance promise.

## Indexing and publication

Update the expert catalog, Raw source catalog, Wiki index, dashboard, Output README, and append-only Wiki log. The site generator already discovers public-layer files recursively, so no separate navigation manifest is required. All new Wiki sources must resolve to Raw IDs and the matrix must have inbound links from both the main index and the dashboard.

## Failure handling and safety

- Treat a changed URL, revised terms, revised methodology, or missing point-in-time version as a freshness failure requiring a new Raw version or an explicit superseded relation.
- Do not use login sessions, cookies, paid material, or authenticated downloads.
- Do not present hypothetical factor portfolios, asset-class forecasts, or historical course examples as investable performance.
- Do not infer endorsement from inclusion. AQR and GMO are investment managers with product and position incentives; Yale course material is educational and dated 2011.
- If a source cannot be reproduced under its terms, retain only the canonical link, metadata, and a short analytical summary.

## Verification

Use test-first content contracts:

1. Add a failing test requiring the three cards, stable IDs, explicit conflict/terms/limitations disclosures, and AQR data-frequency/time-bias coverage.
2. Add a failing test requiring the evidence matrix and Output template to be reachable from the appropriate indexes.
3. Add the minimum content and index changes needed to pass.
4. Run Ruff lint and format check, the full test suite, Raw source audit, Wiki lint, public/private boundary audit, offline report generation, and MkDocs strict build.
5. Inspect the public diff, push only a `codex/` branch, open a PR closing Issue #9, and wait for required checks. Do not merge automatically.
