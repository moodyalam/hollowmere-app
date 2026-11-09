# Hollowmere Festival app

The phone app of **Hollowmere**, a made-up three-day music festival in a field in
Somerset. It shows the line-up and what your wristband lets you into. It is the
system you are on call for in **Lecture 7: Deploy, observe, respond** of
*Mastering CS Technical Competencies* (University of Bath).

All names, artists and people are made up for teaching.

## How this repository works (like a real team's)

| Branch or tag | What it is | How things get there |
|---|---|---|
| `dev` (default) | Work in progress: the next release | Pull requests from `feature/...` branches, after CI passes |
| `production` | What is live at the festival | A pull request from `dev`, when the team decides to release |
| `v1.0`, `v1.1`, ... | Releases: fixed points on `production` | A tag; CI then publishes the image `ghcr.io/novastack-hq/hollowmere-app:<version>` |
| `feature/FEST-42-vip-backstage` | One piece of work (one ticket) | Branched from `dev`, merged back by pull request |

**Deploying** means running a published image with a version tag (see
`ops/compose.yaml`), never "whatever is on my laptop". **Rolling back** means
running the previous tag again.

## Run it

With Docker (the way the festival runs it):

```bash
cd ops
docker compose up -d
```

- <http://localhost:8000>: the phone app (get a wristband, see the line-up)
- <http://localhost:8000/crew>: the crew screen
- <http://localhost:9090>: Prometheus

Without Docker, for developing (needs [uv](https://docs.astral.sh/uv/)):

```bash
uv sync
uv run python app.py
```

Tests and lint, as CI runs them:

```bash
uv run ruff check .
uv run pytest
```

## What's inside

| Path | What |
|---|---|
| `app.py` | The app: line-up, wristbands, `/health`, `/version`, `/metrics`, JSON logs with a request ID |
| `lineup.json` | Saturday's sets |
| `templates/`, `static/` | The phone pages and the crew screen |
| `tests/` | The tests CI runs |
| `ops/` | The "on site" stack: the app, pretend festival-goers (`tools/traffic.py`) and Prometheus with one alert |
| `.github/workflows/ci.yml` | CI: tests and Ruff on every pull request; publishes the image for every release tag |

## Privacy

The app deals random three-digit wristband numbers and keeps them in a cookie.
It asks for no name and stores nothing about you. Its logs record the wristband
number, never your IP address.
