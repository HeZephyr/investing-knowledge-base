# Foundations lab design

## Objective

Complete the foundations curriculum with deterministic exercises for effect size and power, robust regression diagnostics, reproducible randomness, and sourced pathways through investment mathematics, economics, accounting, monetary transmission, and market history.

## Architecture

`src/investkb/advanced_foundations.py` owns small offline numerical contracts and a single domain error. It accepts arrays and explicit parameters, performs no network access, and never turns a statistical result into a trading instruction. Existing public evidence-case, company-reconciliation, and dependency-lock tests remain authoritative evidence where they already exercise the requirement.

## Numerical contracts

- Cohen's d uses the equal-variance pooled sample standard deviation and rejects short, non-finite, or zero-variance samples.
- Approximate two-sample power is two-sided, normal-theory, and explicit about standardized effect, per-group sample size, and alpha. It is a planning sensitivity, not the probability that a hypothesis is true.
- OLS diagnostics require a full-rank two-dimensional design matrix. They return coefficients, residuals, leverage, HC1 standard errors, and Cook's distance, while rejecting singular or underdetermined designs.
- Bootstrap means require a caller-supplied integer seed. Identical inputs and seeds must reproduce identical results; dependency versions remain locked by the project environment.

## Curriculum contracts

- Linear algebra covers vectors, matrices, covariance, rank, and quadratic forms; calculus covers derivatives, convexity, and constrained optimisation without claiming stable inputs.
- Microeconomics connects elasticity, market structure, and pricing power to falsifiable company evidence. Macroeconomics separates national accounts, inflation, labour, and cycles. Monetary policy traces instruments through rates, credit, FX, discount rates, and cash flows.
- Accounting ties the accounting equation and three-statement reconciliation to standards and a tested fixture; accrual analysis separates revenue recognition, working capital, estimates, and cash conversion.
- Crisis history uses trigger → balance-sheet amplifier → market plumbing → policy response → outcome, and avoids copying one market's dates into another market's mechanism.
- Paper replication preserves the source URL, retrieval date, data vintage, file hash, transformation, and expected statistic. Reproduction and extension are labelled separately.

## Failure boundaries

Invalid shapes, non-finite observations, singular designs, impossible power inputs, implicit stochastic state, and unverifiable replication claims are errors. HC1 does not cure omitted variables, dependence, non-linearity, or lookahead. Mathematical optimisation does not make estimated means or covariances reliable. All worked results are educational evidence, not investment advice.
