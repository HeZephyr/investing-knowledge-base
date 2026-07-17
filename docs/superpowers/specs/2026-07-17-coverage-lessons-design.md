# Auditable Coverage and Lessons System Design

## Goal and approval

Issue #11 turns the user's “100%” objective into evidence-backed requirements. The user explicitly requested continuous autonomous completion and emphasized experience and lessons, so the active goal and Issue serve as this batch's approval gate.

The system must reveal incomplete work rather than optimize the score. A 100% report means every declared requirement has current evidence under the repository's schema; it does not mean markets are predictable, profits are guaranteed, or the knowledge base will never need maintenance.

## Approaches considered

1. **Markdown roadmap only:** easy to edit, but status, evidence paths and freshness can silently diverge.
2. **Versioned YAML manifest + Python validator + generated Markdown report (chosen):** reviewable in Git, deterministic in CI, readable from Obsidian and Pages, and small enough for the current architecture.
3. **Database and web admin UI:** supports richer workflows but adds migrations, authentication and hosting before the content model is stable.

## Coverage model

Create `config/knowledge-coverage.yaml` with schema version, an `as_of` date and requirements grouped into five axes:

- `markets`: market structure, disclosure and trading rules;
- `assets`: products and asset-class mechanics;
- `sectors`: repeatable sector research plus at least one evidence-backed case;
- `methods`: valuation, accounting, risk, empirical and portfolio methods;
- `engineering`: data, testing, publication, security and maintenance.

Each requirement has a unique ID, title, status, last verification date, evidence paths and a concise gap. Allowed states are:

- `missing`: required but no adequate artifact;
- `seed`: an indexed outline exists;
- `reviewed`: sources and synthesis passed repository audits;
- `validated`: reviewed evidence plus a reproducible Output, automated test, or runtime/CI proof appropriate to the requirement.

The validator rejects duplicate IDs, unknown axes or states, future dates, missing paths, non-Markdown evidence outside allowed project files, and `validated` entries without at least two independent evidence kinds. Seed/reviewed entries remain visible as incomplete; they are never promoted because of page count.

## Report and CLI

Add `investkb.coverage` with typed immutable records, YAML parsing, validation and Markdown rendering. Add `investkb coverage report --config ... --output ...` to write `output/reports/knowledge-coverage.md`.

The report includes counts by axis and state, an evidence-weighted readiness percentage, every incomplete requirement and its next gap. The score weights `missing=0`, `seed=0.25`, `reviewed=0.65`, `validated=1.0`; it is explicitly labeled repository readiness, not expected return. Rendering is deterministic for CI.

## Experience and lessons model

Create `wiki/methods/经验与失败教训.md` with a stable incident structure:

- event and evidence;
- root cause;
- impact;
- repair;
- prevention;
- re-verification.

Initial lessons come from repository evidence: exact Action-version assertions breaking Dependabot, a source's deep-link restriction discovered in review, revised factor histories creating point-in-time bias, SSE heartbeat messages being mistaken for quote payloads, and negative research results needing retention.

Create `output/templates/研究事故与教训.md` for future incidents. It must prohibit credentials and personal data, distinguish observation from inference, and require a regression test or explicit manual re-verification when automation is impossible.

## Indexing and CI

Link the lessons page and generated coverage report from Wiki/dashboard, docs index, Output README and MkDocs navigation. Add a deterministic coverage validation command to the existing Raw/Wiki integrity CI job. The generated report is committed because it is a public audit artifact and must be reproducible byte-for-byte.

## Testing and safety

Use TDD for parsing, duplicate IDs, future dates, missing evidence, invalid promotion, scoring, deterministic rendering and CLI exit behavior. The public-boundary scanner remains authoritative for credentials. No Cookie, Token, holdings, account details, cached quotes or private incident data enter the public lessons ledger.

## Completion evidence

This batch is complete only when focused tests first fail, then pass; the full suite, coverage validator, Raw/Wiki audits, public-boundary audit, offline backtest and MkDocs strict build pass; the PR is reviewed by required checks and merged. The report is expected to show substantial gaps after launch—that honesty is the feature.
