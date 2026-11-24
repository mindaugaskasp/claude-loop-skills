# Notes for coding agents

- Run `make check` before you say a change is done.
- Standard library only. Do not add a dependency to `go.mod` without asking.
- Every exported function that can block takes a `context.Context` as its first argument.
- Quantities are whole units and are never negative.
- Keep the `Store` interface small; add a method only when two callers need it.
- Tests live next to the code they test and use only the in-memory store.
