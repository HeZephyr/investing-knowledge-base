# Asset and Product Research Lab Design

Issue #43 closes the eleven incomplete requirements on the asset axis without treating page count as completion. The lab separates legal claim, cash-flow mechanics, reference-data semantics, numerical exercises, and product suitability boundaries.

## Architecture

`src/investkb/assets.py` contains pure, offline educational contracts. It must reject ambiguous inputs and disclose assumptions; it does not fetch prices, recommend products, connect to brokers, or execute orders.

- option payoff, Black-Scholes price/Greeks, and implied-volatility inversion;
- convertible parity, premium, bond-floor and downside diagnostics;
- fund tracking difference/error and cross-currency return decomposition;
- index divisor continuity after non-market capitalization changes;
- futures curve roll decomposition using explicitly frozen contract observations;
- structured-note terminal payoff with path-dependent barrier and issuer-recovery stress.

Content-ready requirements use at least one primary source plus linked synthesis. Exercise-tested requirements additionally require implementation and boundary tests. The futures requirement uses a frozen public educational case so the contract and roll arithmetic can be reproduced without live or paid data.

## Evidence policy

Primary sources are regulators, treasury/debt offices, exchanges, index administrators, and current official tax publications. Every source card records retrieval date, jurisdiction, effective/version date where relevant, usage rights, and failure conditions. Tax material is education only and must not infer the reader's residence, treaty eligibility, beneficial-owner status, estate, or filing position.

## Safety and completion

No Cookie, token, personal holdings, broker connectivity, order routing, or performance promise enters the public tree. Promotion to 18/18 requires tests for all numerical contracts, source/synthesis lineage for every content requirement, full repository verification, and successful PR checks.
