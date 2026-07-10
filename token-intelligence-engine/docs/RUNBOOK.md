# Runbook

## Local Development

1. Activate venv

2. Install requirements

3. Configure .env

4. Run

python app.py

---

## Fireworks Test

PROVIDER=fireworks

Run:

python app.py

Expected:

output/results.json

---

## Docker Build

docker build -t token-intelligence-engine .

---

## Docker Run

docker run ...

# Milestone 1

Status: ✅ Complete

The application successfully executes end-to-end using the mock inference provider.

Next milestone:

Replace the mock provider with the Fireworks provider while preserving the execution pipeline and output schema.

## Milestone 2 — Fireworks Smoke Test

Goal

Execute one successful request against Fireworks using the production inference pipeline.

Acceptance Criteria

- Configuration loads correctly.
- Fireworks API request succeeds.
- Response is written to `output/results.json`.
- Application exits with code 0.


## 404 Model Not Found

Symptoms

- HTTP 404
- "Model not found"

Cause

The Fireworks account does not recognize the supplied model identifier.

Resolution

For local development, configure `ALLOWED_MODELS` with the model identifier available to your account.

Do not hardcode these values in source code. The hackathon runtime injects its own `ALLOWED_MODELS`.


## Milestone 3 — Docker

Goal

Package the application into a Linux container that behaves identically to the hackathon judging environment.

Acceptance Criteria

- Docker image builds successfully.
- Container starts successfully.
- Reads `/input/tasks.json`.
- Writes `/output/results.json`.
- Exits with code `0`.


## Docker Environment Variables

The Docker image intentionally does not rely on `.env`.

For local testing, pass all required environment variables using `docker run -e ...`.

This mirrors the hackathon judging harness, which injects configuration at runtime.