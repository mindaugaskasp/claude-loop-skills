# Ledgerline: notes for coding agents

- Two packages live under `packages/`. Each has its own tools; run `make check-billing` or `make check-reports` for the one you touched.
- `reports` may import from `billing`. `billing` must never import from `reports`.
- Dates are `datetime.date`, never strings, once past the edge of the program.
- Every new public function gets a test in the same package.
- Do not add dependencies without asking.
