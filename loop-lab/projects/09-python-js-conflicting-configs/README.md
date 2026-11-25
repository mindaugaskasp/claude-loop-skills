# Repair café bookings

Small booking tool for the Saturday repair café at the neighbourhood centre.

- `backend/` : Python. Keeps the list of repair slots and bookings in a JSON file and serves them over HTTP.
- `frontend/` : plain JavaScript. A widget for the centre's website that shows free slots and takes a booking.

## Working on it

    pip install -r requirements-dev.txt
    npm ci
    make check

`make check` runs everything that the build on GitHub runs: Ruff and pytest for the backend, ESLint for the frontend.

Run the backend locally with `make serve` (port 8040).

## History

The project started in 2021 as a Python-only script on Travis CI and got its frontend and a GitHub Actions build in 2024. Some files from the early days are still lying around.
