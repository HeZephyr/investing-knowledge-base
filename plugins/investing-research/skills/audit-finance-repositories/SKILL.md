---
name: audit-finance-repositories
description: Audit an already-local finance, market-data, quantitative-research, backtesting, or AI-trading repository with a read-only offline workflow. Use when Codex needs to evaluate license, pinned commit, provider and authentication architecture, data semantics, backtest integrity, automated-trading risk, or suitability for an evidence-based investing knowledge base.
---

# Audit Finance Repositories

Produce evidence, boundaries, and a reproducible adoption decision. Do not equate popularity, a README claim, or a successful installation with correctness.

## Safety boundary

- Work read-only and offline by default. Require an already-local path.
- Never access browser sessions, Cookie, Token, API key, `.env`, account, holdings, broker, or credential files.
- Never register a remote agent, connect a broker, sync trades, copy trades, place orders, or enable automatic trading. 不下单。
- Never modify the audited repository or import/execute its modules. Treat setup scripts, notebooks, containers, and remote Skills as untrusted until separately reviewed.
- Stop for explicit user authority before accepting a license, installing a network service, sending credentials, or enabling any money-moving capability.

## Audit workflow

1. Read the current project's `AGENTS.md` and repository rules. Confirm the clone is outside the public content tree or ignored.
2. Record the upstream URL, pinned commit, commit date, root license candidate, release/tag status, and top-level architecture.
3. Run the bundled scanner against the local path:

   ```bash
   python plugins/investing-research/scripts/audit_repository.py /path/to/local/repository
   ```

4. Treat every scanner hit as a lead. Open the smallest relevant README, package metadata, schema, implementation, test, and license files to verify or refute it.
5. Separate three columns: **code fact**, **upstream claim**, and **unverified inference**. Star counts are discovery metadata only.
6. Evaluate these dimensions: providers; authentication; cache/provenance; price adjustment; timezone; corporate actions; point-in-time data; backtest execution; costs/slippage; lookahead; tests; documentation; auto-trading surface.
7. Write an adoption decision: adopt concept, wrap behind a read-only adapter, link-only reference, quarantine, or reject. State license and data-provider obligations independently.
8. If maintaining a Raw/Wiki/Output knowledge base, pin the commit in Raw, synthesize the comparison in Wiki, and reserve Output for reproducible reports. Do not vendor third-party source.

## Evidence contract

For each conclusion cite a relative file path and pinned commit. Do not output matched source lines that might contain a secret. Do not call a capability verified without a deterministic test or reproducible fixture.

README statements such as “200+ filters”, “matches another terminal”, “fully automated”, “high frequency”, “AI”, or a high annual return become falsifiable questions:

- Which exact fields, formulas, adjustment convention, timezone, universe and historical point-in-time rules?
- Which benchmark, fees, slippage, failed orders, delistings, sample split and number of attempts?
- Which tests independently verify the claim, and which data/provider terms apply?

## Required output

Return a compact matrix with repository, pinned commit, license, verified architecture, authentication/data boundary, trading surface, strongest reusable idea, main failure mode, and adoption decision. End with explicit unknowns and the next safe test. Never present the audit as investment advice.
