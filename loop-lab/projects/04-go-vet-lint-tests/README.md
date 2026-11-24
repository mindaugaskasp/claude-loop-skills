# Warehouse

A small stock-keeping service. It keeps a count per item, takes deliveries in, sends shipments out and lists items that are running low.

## Run

    make build
    ./bin/warehouse -addr :8080

## Endpoints

- `GET /items/{sku}` : one item
- `POST /items/{sku}/receive` : body `{"quantity": 5}`
- `POST /items/{sku}/ship` : body `{"quantity": 2}`
- `GET /low-stock` : items at or below their reorder level
- `POST /import` : CSV body, one line per item: `sku,name,quantity,reorder level`

## Checks

    make check

runs `go vet`, `golangci-lint` (settings in `.golangci.yml`) and the tests. GitLab CI runs the same three on every merge request (`.gitlab-ci.yml`).

## Working on it

Every change goes through a merge request and is read by one other person on the team. Notes for coding agents are in `AGENTS.md`.
