# cicd-demo

A minimal Flask API with a full CI/CD pipeline — automated testing and deployment to AWS EC2 on every push to `main`.

---

## Pipeline Overview

```
push to main
    → tests run on GitHub Actions
    → if tests pass → SSH into EC2
    → rebuild Docker image
    → redeploy container
    → app is live
```

---

## Stack

| Layer | Tool |
|---|---|
| App | Python + Flask |
| Container | Docker |
| CI/CD | GitHub Actions |
| Server | AWS EC2 (Ubuntu 24.04) |
| Tests | pytest |

---

## Project Structure

```
cicd-demo/
├── app.py                  # Flask app (CORS, error handlers, /health)
├── test_app.py             # pytest tests
├── requirements.txt        # Python dependencies (pinned)
├── Dockerfile              # Container definition (w/ HEALTHCHECK)
├── .gitignore              # Files excluded from git
├── .dockerignore           # Files excluded from Docker image
└── .github/
    └── workflows/
        └── ci.yml          # CI/CD pipeline
```

---

## Running Locally

```bash
# Create and activate a virtual environment (recommended)
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v

# Run the app
python app.py
```

App will be available at `http://localhost:5000`

### Docker

```bash
# Build
docker build -t cicd-demo .

# Run
docker run -d --name cicd-demo -p 5000:5000 cicd-demo
```

---

## Endpoints

| Method | Path | Response | Notes |
|---|---|---|---|
| GET | `/` | `{"status": "ok", "message": "hello from cicd-demo"}` | Root endpoint |
| GET | `/health` | `{"healthy": true}` | Liveness check for Docker HEALTHCHECK |
| GET | `/non-existent` | `{"error": "not found"}` | 404 — any unknown route |
| Any | `/error` | `{"error": "internal server error"}` | 500 — unhandled exceptions |

All errors return JSON instead of HTML, and CORS is enabled for cross-origin browser access.

---

## CI/CD Pipeline

Defined in `.github/workflows/ci.yml`

**On every push to `main`:**
1. Spin up fresh Ubuntu runner
2. Install Python 3.12 + dependencies
3. Run pytest
4. If tests pass → SSH into EC2 → `git fetch && reset` (no merge conflicts) → rebuild and redeploy Docker container

**On pull requests:**
- Tests run only — no deploy

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `EC2_HOST` | Public IP of EC2 instance |
| `EC2_USER` | SSH username (`ubuntu`) |
| `EC2_SSH_KEY` | Private SSH key for EC2 access |

### Key Pipeline Details

- The deploy step uses `git fetch origin main && git reset --hard origin/main` instead of `git pull` — avoids merge conflicts and dirty-state failures
- The repo URL is derived dynamically from `${{ github.repository }}`, so the pipeline works on any fork without manual edits
- Only the `test` job can trigger the `deploy` job; a PR that fails tests never reaches EC2

---

## Server Setup (EC2)

Requirements:
- Ubuntu 24.04
- Docker installed and running (`sudo apt install docker.io`)
- Port 5000 open in security group (inbound, TCP)
- GitHub deploy key (`EC2_SSH_KEY`) added to `~/.ssh/authorized_keys`

---

## Local Development

```bash
# Run tests in watch mode (requires pytest-watch)
ptw

# Lint with ruff
ruff check .
```

---

## What This Project Demonstrates

- A complete CI/CD pipeline from commit to production
- CI and CD as separate concerns — test first, deploy only on green
- Secure credential passing via GitHub secrets
- Docker as the deployment artifact
- Production awareness (HEALTHCHECK, CORS, JSON error handlers, `.dockerignore`)
- Fork-friendly workflow design (dynamic repo URL, no hardcoded usernames)
