# Run in Scout/Sol

1. Open this repository as the writable workspace.
2. Enable shell and browser access. Permit installation or container execution of OpenFOAM, Gmsh and ParaView.
3. Optionally copy `agent/skills/mft-d1600-cfd` to `~/.copilot/skills/`.
4. Paste all of `agent/MASTER_PROMPT.md` as the root assignment.

Expected first state:

```bash
make check       # passes reduced-order/bootstrap integrity
make demo-gate   # fails with exact C1 evidence backlog
```

If the agent returns after a narrow task, respond:

> Continue the project root loop. Re-run `make status` and `make demo-gate`, select the next unsatisfied C1 criterion, and do not return until DEMO_READY or a strict BLOCKED condition is proven.
