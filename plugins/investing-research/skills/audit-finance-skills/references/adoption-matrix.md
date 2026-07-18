# Finance Skill adoption matrix

Use the most restrictive applicable decision. Evaluate code license, copied-content license, data terms, authentication and execution authority independently.

| Decision | Minimum evidence | Default action | Promotion test |
|---|---|---|---|
| `adopt` | License clear; idea can be independently implemented; no required secret, network or order authority | Reimplement the smallest concept with local fixtures and tests | Compare formulas/schema against an authoritative source and frozen fixture |
| `optional` | License clear; read-only use; dependency and provider terms documented; secrets supplied only by the user at runtime | User installs outside default CI; wrap behind explicit adapter | Offline contract test plus user-authorized sandbox query with redacted provenance |
| `link-only` | Useful public reference, but root/nested license, copied documentation rights or quality remains unresolved | Store URL, pinned commit and original analysis only | Upstream license clarification and per-resource provenance audit |
| `quarantine` | Cookie/password flow, proprietary terminal, broker/order/transfer function, remote execution, or broad system mutation | Do not install, load or run in the default plugin | Separate threat model, zero-money sandbox, least privilege and human confirmation |
| `reject` | Authentication bypass, secret exfiltration, hidden persistence, policy override, unreviewable binary, or order execution without confirmation | Do not use | No automatic promotion; require a new security review |

## Evidence rules

- Record exact relative paths and pinned commit, never secret-bearing source lines.
- Treat README statements as upstream claims until implementation and tests corroborate them.
- Treat `setup.py`, build hooks, shell commands, plugin hooks and agent instructions as executable surfaces even if the audit never runs them.
- Record `NOASSERTION` when a root license is absent or ambiguous. Do not infer MIT from package popularity or a README footer.
- Audit nested license and provenance for copied official docs, examples, images, templates and imported Skills.
- A missing match for timezone, lookahead, prompt injection or order keywords is an unknown, not proof of absence.
