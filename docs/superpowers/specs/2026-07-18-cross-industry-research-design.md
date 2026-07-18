# Cross-Industry Research Systems Design

Issue #45 completes the six remaining sector requirements by separating classification, physical/contractual operating units, accounting recognition, financing, and market valuation.

## Architecture

`src/investkb/sectors.py` contains pure offline bridges that can be hand checked:

- insurance combined ratio, reserve development, and solvency coverage;
- wafer good-die output across fabrication yield and packaging/test yield;
- industrial backlog reconciliation and capacity utilization;
- property project cash bridge, net leverage, and interest coverage;
- mining contained/recovered metal and unit cash-cost bridges;
- industry classification records with explicit scheme, revision, effective date, and primary activity.

The functions do not value securities or generate recommendations. A company can span several activities, so classification is an index into research—not a substitute for segment disclosure.

## Evidence

Primary evidence uses UNSD ISIC, IFRS 17/IAIS, NIST/SEC filings, U.S. Census manufacturing and housing methods, and USGS/SEC mining disclosure. Official aggregates are never mapped directly to company revenue without a documented unit bridge. Company filings illustrate disclosure fields but are not universal industry truth.

## Completion

Each content-ready requirement needs a primary source and linked synthesis. Cross-industry numerical bridges additionally receive boundary tests. No proprietary classification database, paid estimates, personal holdings, credentials, or live order capability enters the public tree.
