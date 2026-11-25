# plotwatch

A small command-line tool for the Kalnu allotment association. Each plot has its own water meter. Twice a year somebody walks round, writes down the meter readings and types them into a CSV file. `plotwatch` reads that file and prints how much water each plot used and what it owes.

```
cargo run -- data/readings.csv 310
```

The second argument is the price of one cubic metre of water in cents. Every plot also pays a fixed yearly charge.

## Working on it

- Rust 1.97, no crates from outside.
- `make check` runs everything that has to pass: `cargo fmt --check`, `cargo clippy` with warnings as errors, and `cargo test`. Settings are in `rustfmt.toml` and in the `[lints]` part of `Cargo.toml`.
- The code lives on Codeberg. Woodpecker runs the same three checks on every pull request (`.woodpecker.yml`).
- We are two people, Aiste and Jonas. Each pull request is read by the other one before it is merged. Since the start of November we write down what the review found in `docs/review-findings.jsonl`, one line per finding, by hand.
- Coding agents: read `AGENTS.md` first.

## Ideas, not done

- `cargo-deny` for licence checks, once we use a crate from outside.
- A way to import readings from the photo app.
