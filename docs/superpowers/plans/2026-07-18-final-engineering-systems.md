# Final Engineering Systems Plan

**Goal:** Close Issue #47 and reach evidence-backed 100.0% repository readiness.

## 1. Test-first contracts

- [ ] Add failing offline tests for global bars, actions, provenance, schema drift, invalid values, and explicit instrument mapping.
- [ ] Add failing temporary-directory tests for private workspace initialization, empty holdings, validation, overwrite refusal, symlink escape, and forbidden credential/order fields.
- [ ] Implement the minimum provider and private-workspace modules; add CLI entry points only after library contracts pass.

## 2. Sources, synthesis, and reuse

- [ ] Refresh and pin the yfinance repository card and document license, terms, supported role, and failure boundaries.
- [ ] Add global free-data and private-workspace Wiki synthesis with OpenBB/FinHack lessons, examples, failure modes, and checklists.
- [ ] Update indexes, navigation, README, maintenance log, and reusable lessons.

## 3. Coverage and delivery

- [ ] Promote only the two requirements with implementation/test evidence and regenerate the deterministic 100.0% report.
- [ ] Run full verification, independent review, CI, PR Policy, and squash merge a fixed SHA.
