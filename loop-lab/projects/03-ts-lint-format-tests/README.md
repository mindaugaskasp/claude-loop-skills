# parcel-quote

Works out what it costs to send a parcel: a price by weight band, a surcharge for remote zones, and VAT on top. Used by the checkout service through the two handlers in `src/handlers`.

## Working on it

```sh
npm ci
npm run check   # lint, formatting, types, tests
```

Amounts are whole cents everywhere. Helpers for money, postcodes and weights live in `src/lib`.

## Review

Every pull request needs an approving review from a teammate before it is merged. See `CONTRIBUTING.md`.
