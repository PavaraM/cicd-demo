# cicd-demo

A minimal Flask API with a full CI/CD pipeline — automated testing and deployment to AWS EC2 on every push to main.

---

## What This Is

A learning project built to understand CI/CD from scratch. The app itself is simple by design — the pipeline is the point.

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
├── app.py                        # Flask app
├── test_app.py                   # pytest tests
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container definition
└── .github/
    └── workflows/
        └── ci.yml                # CI/CD pipeline
```

---

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v

# Run the app
python app.py
```

App will be available at `http://localhost:5000`

---

## Endpoints

| Method | Path | Response |
|---|---|---|
| GET | `/` | `{"status": "ok", "message": "hello from cicd-demo"}` |
| GET | `/health` | `{"healthy": true}` |

---

## CI/CD Pipeline

Defined in `.github/workflows/ci.yml`

**On every push to main:**
1. Spin up fresh Ubuntu runner
2. Install Python 3.12 + dependencies
3. Run pytest
4. If tests pass → SSH into EC2 → rebuild and redeploy Docker container

**On pull requests:**
- Tests run only — no deploy

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `EC2_HOST` | Public IP of EC2 instance |
| `EC2_USER` | SSH username (ubuntu) |
| `EC2_SSH_KEY` | Private SSH key for EC2 access |

---

## Server Setup

EC2 instance requirements:
- Ubuntu 24.04
- Docker installed and running
- Port 5000 open in security group
- Deploy key added to `~/.ssh/authorized_keys`

---

## What I Learned

- How to write a multi-stage GitHub Actions workflow
- How CI and CD are separate concerns — test first, deploy only on green
- How to securely pass credentials via GitHub secrets
- How Docker fits into a deployment pipeline
- How to debug SSH and networking issues on EC2