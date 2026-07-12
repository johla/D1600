# Sol/Scout D1600 separator execution contract

You have full agency within this repository to take the generic D1600 passive stormwater separator from its current reduced-order bootstrap to a reproducible, adversarially reviewed CFD design-search demonstration.

## Terminal truth

A single immutable revision must contain a computational study that independently demonstrates:

- valid parameterized D1600 geometry;
- reproducible meshes and CFD cases;
- convergence, conservation and mesh-independence;
- particle grade-efficiency at the approved flow/particle envelope;
- head-loss and overload/sediment-security evidence;
- autonomous design exploration with failed-case recovery;
- a Pareto frontier and 2–3 candidates for physical testing;
- reproducible figures/animations/report;
- no unresolved critical/high review finding.

The only project-level return gate is `make demo-gate`.

## Initial execution

Immediately:

1. Read `GOAL.md`, `SCOUT.md`, `EVIDENCE_MATRIX.md`, `ROUTES.md`, `TASKS.md`, `DECISIONS.md`, `RISKS.md`, `OPEN_QUESTIONS.md` and `evidence/evidence-matrix.json`.
2. Run `make check`, `make surrogate`, `make status` and `make demo-gate`.
3. Classify every claim as assumption, analytical calculation, reduced-order screening, CFD result, sensitivity result, review result or physical evidence.
4. Identify the earliest critical-path criterion and independent parallel work.
5. Do not return after reconnaissance.

## Search before convergence

For geometry, meshing, flow solver, turbulence model, particle model, resuspension proxy and optimizer, maintain materially different routes. Select routes by their ability to close terminal evidence, not familiarity.

The initial suggested route is:

```text
parameterized Gmsh/OpenCASCADE geometry
  -> OpenFOAM incompressible RANS baseline
  -> transient overload where needed
  -> one-way Lagrangian particle tracking
  -> Python experiment registry and multi-objective search
  -> ParaView/Python automated post-processing
```

It is a candidate, not dogma. Compare alternatives when it fails.

## Execution loop

For each transition:

1. Name the C1 criterion.
2. State current falsifying evidence.
3. Implement the smallest coherent change.
4. Execute it.
5. Check conservation, convergence and physical plausibility.
6. Use a negative control where practical.
7. Run affected regressions.
8. Launch an independent falsification review.
9. Resolve findings.
10. Update `evidence/evidence-matrix.json` and all ledgers.
11. Re-run `make status` and continue.

Do not stop after completing one task packet, one geometry, one solver run, one optimization campaign or one report.

## Non-solutions

The non-solutions in `GOAL.md` are binding. In particular, the existing surrogate is only a screening and pipeline test. It cannot satisfy any CFD result criterion.

## Strict return gate

Return `DEMO_READY` only after `make check` and `make demo-gate` pass, the release manifest is complete and the final red-team has no critical/high finding.

If genuinely blocked, return `BLOCKED` with the exact criterion, evidence, materially different routes attempted and smallest missing capability. Continue all work not dependent on that blocker.

## Mission

Do not produce a persuasive CFD story. Produce a computational experiment whose geometry, assumptions, execution, failures and evidence can be independently interrogated—and that gives MFT a credible shortlist for hydraulic testing.
