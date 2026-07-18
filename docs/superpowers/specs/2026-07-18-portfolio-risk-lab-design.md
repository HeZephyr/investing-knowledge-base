# Portfolio risk lab design

## Objective

Build a public, holdings-free portfolio laboratory that teaches governance before optimization and makes costs, constraints, risk contribution, stress, attribution, and process quality machine-checkable.

## Boundaries

- Public fixtures use generic asset labels and contain no user positions, account identifiers, transactions, or credentials.
- Every weight vector must be finite, nonnegative, and sum to one within explicit tolerance.
- Covariance must be finite, symmetric, and positive semidefinite; zero-volatility portfolios have no defined percentage risk contribution.
- Rebalancing reports trades, one-way turnover, and fee drag; it does not place orders.
- Attribution must reconcile to active return; residuals beyond tolerance fail closed.
- Decision journals score process completeness, never outcome profitability.

## Public API

- `validate_ips`: objectives, horizon, emergency reserve, allocation limits, decision/review dates.
- `allocation_diagnostics`: concentration, effective holdings, and weighted expected return.
- `rebalance_plan`: target values, trades, turnover, costs, and post-cost portfolio value.
- `liquidity_diagnostics`: days to liquidate under participation caps and concentration flags.
- `risk_contributions`: total volatility, marginal/component contributions, and contribution shares.
- `stress_loss` and `reverse_stress_shock`: portfolio impact and one-asset shock needed to reach a loss limit.
- `brinson_attribution`: allocation, selection, interaction, and active-return reconciliation.
- `validate_decision_journal`: preregistration and evidence-field completeness without holdings.
