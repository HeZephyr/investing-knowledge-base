# Final Engineering Systems Design

**Issue:** #47

## Outcome

Close the two remaining engineering requirements without weakening the public/private boundary. The public repository gains a deterministic global-market adapter and a local-only private-research workspace generator/validator; it gains no credentials, holdings, Cookie replay, broker integration, or order execution.

## Decisions

### Global free-data adapter

- Reuse OpenBB's provider/standard-model separation as an architectural lesson, not as a runtime dependency.
- Implement an optional `YFinanceProvider` behind an injected-client boundary. The provider is a community convenience layer with no SLA and is not a statutory source.
- Require an explicit instrument registry containing canonical market, local symbol, provider symbol, currency, and exchange timezone. Never guess Korean suffixes or currency from a ticker.
- Keep raw/unadjusted and adjusted prices explicit. Do not synthesize turnover when the upstream omits it; use a missing value and disclose the limitation.
- Normalize dividends and splits into a separate company-action contract. Prices and actions must not silently substitute for each other.
- Attach request/provenance metadata and fail closed on empty responses, schema drift, duplicate dates, invalid OHLC, negative volume, ambiguous timestamps, and unsupported adjustment modes.
- Use injected offline fixtures in PR tests. Live free-provider smoke remains scheduled and non-blocking because free providers have no SLA.

### Private research workspace

- Public code may create and validate an ignored `private/` workspace, but the repository never ships a real private directory or personal example.
- Initialize four local YAML documents: policy, watchlist, positions, and decision journal. Empty positions are valid because the owner currently has no holdings.
- Use allow-listed schemas, version fields, safe YAML parsing, symlink rejection, and refusal to overwrite. Reject credential, Cookie, broker, and automatic-order fields.
- Tests operate only in temporary directories. Public reports may describe the schema and commands but never read or summarize local private content.

## Evidence and completion

`engineering-global-data` becomes `validated` only with the pinned yfinance source card, provider implementation, and offline contract tests. `engineering-private-research` becomes `validated` only with the public implementation and temporary-directory tests. The deterministic coverage report must reach 100.0%; full verification, independent review, CI, PR Policy, and fixed-SHA squash merge remain mandatory.
