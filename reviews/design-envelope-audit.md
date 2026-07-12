# C1-01 independent design-envelope audit

## Scope and reviewer

An independent repository-analysis run audited the machine-readable envelope,
objectives, constraints, decisions, risks and open questions. The proposition
reviewed was deliberately limited: the values are frozen for a generic C1
computational demonstration and are not MFT product inputs or performance
claims.

## Result

**Pass — no open critical or high finding.**

- The YAML parses and uses explicit SI-derived units in field names.
- Particle weights sum to one; normal flows are ordered and the overload point
  exceeds the highest normal flow.
- D1600, water depth, pipe size/elevation, particle classes and density agree
  with `GOAL.md`.
- Passive-operation, head-loss, gap and cleaning-access constraints are
  machine-readable.
- Objectives identify direction and equal flow weighting; numerical evidence
  thresholds are explicit.
- The status and supporting prose prevent interpretation as certification,
  physical validation or a proprietary-product claim.

The original audit's only gate-blocking findings were the absent review,
evidence record and matrix status. Those bookkeeping gaps are closed with this
review and `evidence/criteria/C1-01.json`.

## Residual non-critical risk

The assumed flow envelope, head-loss limit, particle shape, manufacturing rules
and chamber details may differ from an MFT product. Any approved product input
requires a new study revision and invalidates direct reuse of candidate
rankings. This is retained as K-001 rather than hidden.
