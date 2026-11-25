# Notes for the coding agent

- Run `make check` before you say a change is finished.
- Backend code is in `backend/repaircafe`, its tests in `backend/tests`. Frontend code is in `frontend/src`.
- Dates and times go over the wire as ISO 8601 text in UTC. Never send a local time.
- Do not add a dependency without asking. The backend uses only the standard library.
- Every new backend function gets a test.
- Keep messages shown to visitors in `frontend/src/texts.js`.
