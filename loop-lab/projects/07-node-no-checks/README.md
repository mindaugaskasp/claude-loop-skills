# kiln-desk

Small command-line helper for the pottery studio. It reads the order export from the webshop (a CSV file) and makes two things:

- packing slips, one HTML page per order, ready to print
- the kiln plan for the week: which pieces go into which firing

It also sends the "your order is packed" email through the mail service the webshop already uses.

## Use

    nvm use
    npm run slips     # packing slips for the sample export, written to out/slips
    npm run plan      # kiln plan for the sample export
    node bin/kiln-desk.js notify data/sample-orders.csv   # send the "packed" emails

There is nothing to install: the tool uses only what comes with Node.

Settings come from environment variables, see `src/config.js`.

## How we work

Two of us work on this, Ugne and Rasa, mostly with a coding agent (its notes are in `AGENTS.md`). Every change goes through a pull request on GitHub and the other person reads it before it is merged.

There are no automated checks of any kind: no linter, no formatter, no tests, and nothing runs on GitHub when a pull request is opened. `npm test` is the placeholder npm puts there. The `.editorconfig` file only tells editors how to indent.

Since the end of September Ugne copies the review comments into `docs/review-findings.jsonl`, one line per comment, with a note on whether the comment led to a fix.
