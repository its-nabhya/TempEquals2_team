# Token Intelligence Engine

A lightweight token-efficient AI routing engine built for the **AMD Developer Hackathon 2026 - Track 1 (General Purpose AI Agent)**.

The system intelligently routes tasks through a hybrid inference pipeline consisting of:

- Symbolic local solvers (zero-token)
- Fireworks AI hosted models
- Modular routing architecture for future local LLM integration

The objective is to minimize Fireworks token usage while maintaining high answer quality.

---

# Features

- Task classification
- Prompt canonicalization
- Prompt optimization
- Symbolic local inference
    - Mathematical reasoning
    - Sentiment classification
    - Named Entity Recognition
- Modular routing system
- Fireworks AI integration
- Benchmark framework
- Docker support
- Detailed decision logging

---

# Project Structure

```
token-intelligence-engine/

├── analysis/
├── constants/
├── core/
├── docs/
├── evaluation/
├── inference/
├── input/
├── models/
├── output/
├── routing/
├── schemas/
├── tests/
├── utils/
├── validation/

app.py
config.py
requirements.txt
Dockerfile
README.md
```

---

# Requirements

- Python 3.11
- Docker Desktop (optional)
- Fireworks AI API Key

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd token-intelligence-engine
```

---

## Create Virtual Environment

Windows PowerShell

```powershell
python -m venv .venv
```

or

```powershell
py -3.11 -m venv .venv
```

Activate

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file in the project root.

Example

```env
LOG_LEVEL=INFO

PROVIDER=fireworks

INPUT_PATH=input/tasks.json
OUTPUT_PATH=output/results.json

REQUEST_TIMEOUT=30

FIREWORKS_API_KEY=YOUR_API_KEY

FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1

ALLOWED_MODELS=accounts/fireworks/models/minimax-m3
```

For local testing without Fireworks:

```env
PROVIDER=mock

ALLOWED_MODELS=mock-model
```

---

# Running the Project

```powershell
python app.py
```

Successful execution should produce logs similar to:

```
Application started.

Loaded 1 task(s).

Successfully processed all tasks.
```

---

# Input Format

Place the input JSON at

```
input/tasks.json
```

Example

```json
[
    {
        "task_id": "1",
        "prompt": "What is the capital of Australia?"
    }
]
```

---

# Output Format

Results are written to

```
output/results.json
```

Example

```json
[
    {
        "task_id": "1",
        "answer": "Canberra"
    }
]
```

---

# Benchmarking

Run benchmark on the default dataset

```powershell
python -m evaluation.benchmark
```

Benchmark a specific dataset

```powershell
python -m evaluation.benchmark evaluation/datasets/math.json
```

Run the complete benchmark suite

```powershell
python -m evaluation.benchmark_all
```

---

# Docker

## Build

```powershell
docker buildx build `
    --platform linux/amd64 `
    -t token-intelligence-engine:v0.1 .
```

---

## Run (Mock Provider)

```powershell
docker run --rm `
    -v "${PWD}\input:/input" `
    -v "${PWD}\output:/output" `
    -e PROVIDER=mock `
    -e ALLOWED_MODELS=mock-model `
    token-intelligence-engine:v0.1
```

---

## Run (Fireworks Provider)

```powershell
docker run --rm `
    -v "${PWD}\input:/input" `
    -v "${PWD}\output:/output" `
    -e PROVIDER=fireworks `
    -e FIREWORKS_API_KEY=<YOUR_API_KEY> `
    -e FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1 `
    -e ALLOWED_MODELS=accounts/fireworks/models/minimax-m3 `
    token-intelligence-engine:v0.1
```

---

# Environment Variables

| Variable | Description |
|-----------|-------------|
| PROVIDER | `mock` or `fireworks` |
| FIREWORKS_API_KEY | Fireworks API Key |
| FIREWORKS_BASE_URL | Fireworks inference endpoint |
| ALLOWED_MODELS | Comma-separated list of allowed model IDs |
| INPUT_PATH | Input JSON file |
| OUTPUT_PATH | Output JSON file |
| REQUEST_TIMEOUT | Request timeout (seconds) |
| LOG_LEVEL | Logging verbosity |

---

# Current Local Solvers

The following task types may be solved without calling Fireworks:

- Mathematical reasoning
- Sentiment classification
- Named Entity Recognition

If confidence is below the configured threshold, the request is automatically forwarded to Fireworks.

---

# Logging

The application logs:

- Task classification
- Selected model
- Pipeline execution
- Errors
- Benchmark metrics

---

# Development Workflow

Activate environment

```powershell
.\.venv\Scripts\Activate.ps1
```

Run application

```powershell
python app.py
```

Run benchmarks

```powershell
python -m evaluation.benchmark_all
```

Run Docker build

```powershell
docker buildx build --platform linux/amd64 -t token-intelligence-engine:v0.1 .
```

---

# Troubleshooting

## Environment variables not loading

Verify

```powershell
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('INPUT_PATH'))"
```

---

## Verify configuration

```powershell
python -c "from config import load_config; print(load_config())"
```

---

## Missing input file

Ensure

```
input/tasks.json
```

exists and contains valid JSON.

---

## Fireworks "Model not found"

Check:

- `ALLOWED_MODELS`
- `FIREWORKS_BASE_URL`
- `FIREWORKS_API_KEY`

The model must exist in your Fireworks account or be included in the hackathon environment.

---

# Future Work

- Local GGUF model inference
- Confidence-aware routing
- Adaptive prompt optimization
- Token cost estimation
- Dynamic model selection
- Fine-tuned routing policies

---

# License

Developed for the AMD Developer Hackathon 2026.












## Engineering Philosophy

TACTIC is built around the idea that **AI routing is an optimization problem, not a model selection problem**.

Rather than always selecting the most capable model, TACTIC estimates the minimum inference required to satisfy an accuracy constraint.

The framework is intentionally:

- Provider agnostic
- Model agnostic
- Token efficient
- Docker first
- Production oriented
- Extensible through progressive architecture

Every architectural decision is documented in:

- docs/ARCHITECTURE.md
- docs/ENGINEERING_DECISIONS.md

## Development Strategy

TACTIC follows an iterative development strategy:

1. Build a complete runnable baseline.
2. Integrate Fireworks inference.
3. Add routing intelligence.
4. Optimize token efficiency.

The project prioritizes correctness and testability before optimization.


## Domain Model

TACTIC communicates internally using typed domain objects instead of raw dictionaries.

Current domain objects:

- Task
- TaskContext
- TaskResult

This improves readability, maintainability and testability throughout the processing pipeline.

## Current Status

Version 1 implements the complete execution pipeline:

Input → Pipeline → Router → Provider → Output

Routing is intentionally simplistic at this stage and will be enhanced incrementally.

## Capability-Based Routing

TACTIC separates model identities from routing decisions.

Models are represented by capability profiles (e.g., code generation, reasoning, general-purpose), allowing routing policies to operate on abstract capabilities rather than specific model names.

## Zero-Token Task Classification

TACTIC performs deterministic task classification locally before any routing decision.

This enables capability-aware routing without consuming inference tokens.

## Local Symbolic Execution

Before invoking any external model, TACTIC attempts to solve supported task categories using lightweight deterministic methods.

Only tasks that cannot be solved confidently proceed to the routing stage, minimizing external token usage.

## Development Roadmap

TACTIC is developed iteratively:

1. Build a complete, valid submission.
2. Establish a baseline score.
3. Optimize routing and local execution.
4. Benchmark every improvement against the baseline.

This ensures every optimization is measurable and grounded in real evaluation results.

## Baseline Submission

Version 1 prioritizes a valid end-to-end submission.

The initial implementation establishes a measurable baseline before introducing local symbolic execution and advanced routing optimizations.

## Development Workflow

Every milestone follows this sequence:

1. Local execution
2. Runtime validation
3. Docker validation
4. Submission

This isolates packaging issues from application issues and shortens the debug cycle.


## Validation Strategy

Before containerization, TACTIC is validated through local execution using the mock provider followed by the Fireworks provider. Docker packaging is performed only after the application executes successfully in a local environment.

## Local Development vs Hackathon Runtime

During local development, `ALLOWED_MODELS` may need to contain fully qualified Fireworks model paths (for example, `accounts/fireworks/models/gemma-4-31b-it`) depending on your Fireworks account.

During hackathon evaluation, the container must use the `ALLOWED_MODELS` environment variable injected by the judging harness without modification.

## Local Development Models

The models available through a personal Fireworks account may differ from the models exposed by the hackathon evaluation environment.

Use locally available Serverless models for development. During evaluation, always rely on the injected `ALLOWED_MODELS` environment variable.

### Milestone

✅ End-to-end Fireworks inference validated.

The application has successfully executed the complete processing pipeline using the Fireworks OpenAI-compatible API and produced a valid `results.json` output.

### Prompt Optimization

Before every Fireworks API call, prompts pass through a lightweight optimization layer that:

- Normalizes whitespace
- Removes redundant polite phrases
- Applies task-specific response constraints
- Reduces estimated token usage

This optimization is deterministic and incurs no additional inference cost.

### Decision Logging

Every processed task produces a structured JSONL record in `output/decisions.jsonl` containing:

- Task type
- Routing decision
- Local solver used
- Confidence
- Selected Fireworks model
- Prompt length
- Response length

This log is used to benchmark routing quality and guide token optimization experiments.