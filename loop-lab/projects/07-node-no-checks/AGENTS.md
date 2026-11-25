# Notes for coding agents

- This is plain JavaScript for Node 20 or newer, CommonJS (`require`), no build step.
- Do not add dependencies. Use what comes with Node.
- Never hard-code a path to someone's home folder or desktop. Read folders from `src/config.js`. Wrong: `'/Users/ugne/Desktop/slips'`. Right: `config.outDir`.
- Money is kept in cents as whole numbers. Format it only when it is shown.
- Texts the customer sees are in `src/texts.js`. Do not put customer-facing sentences anywhere else.
- Keep each command in `bin/kiln-desk.js` short; the work belongs in `src/`.
