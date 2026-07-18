# Research methods lab design

## Objective

Complete the research-method chain with deterministic, offline exercises for chronological validation, preregistration, time-series baselines, and event studies, then connect them to sourced causal and evidence-quality guidance.

## Architecture

`src/investkb/research_methods.py` owns pure functions and one domain error. It accepts arrays, timestamps, and plain mappings; it never fetches data or mutates a registration. Existing company point-in-time and backtest cost tests remain authoritative evidence for lookahead and cost protection instead of duplicating production paths.

## Contracts

- Walk-forward splits use half-open integer ranges. Training ends before an embargo, then testing begins; expanding and rolling modes are explicit.
- A preregistration requires hypothesis, success/failure criteria, dataset, window, method, costs, alternatives, and a timezone-aware registration timestamp strictly before result availability. Canonical JSON yields a stable SHA-256.
- Autocorrelation uses demeaned observations at a positive lag. Random-walk forecast errors use the prior observation. EWMA volatility validates `0 < lambda < 1` and returns the final annualised estimate.
- Event studies estimate `asset = alpha + beta * market` by OLS in a pre-event window, calculate abnormal returns and CAR in the event window, and reject insufficient/overlapping windows.
- Content pages distinguish prediction from diagnostics, correlation from causal identification, current constituents from point-in-time universes, and a single factor implementation from a general anomaly.

## Failure boundaries

Invalid chronology, naive timestamps, post-result registration, missing criteria, zero-variance regressors, non-finite values, overlapping events, and malformed evidence are errors. None of the outputs are described as trading signals, causal proof, or future alpha.
