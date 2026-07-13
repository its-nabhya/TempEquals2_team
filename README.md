# TACTIC
### Token-Aware Cognitive Task Intelligence Controller

> An intelligent hybrid routing engine that minimizes LLM inference cost by dynamically selecting between deterministic algorithms, local inference, and cloud LLMs while maintaining high task accuracy.

Built by **Team TempEquals2** for the **AMD Developer Challenge – AI Agent Track**.

---

## Overview

TACTIC is a token-efficient AI inference engine designed to solve heterogeneous NLP and reasoning tasks under strict constraints on:

- Accuracy
- Runtime
- Token usage

Instead of forwarding every request to a cloud LLM, TACTIC analyzes each task and routes it to the cheapest execution engine capable of solving it.

This significantly reduces cloud inference while preserving response quality.

---
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Fireworks AI](https://img.shields.io/badge/Fireworks-AI-orange)
![llama.cpp](https://img.shields.io/badge/llama.cpp-GGUF-green)
![Status](https://img.shields.io/badge/Status-Hackathon_Project-success)

---

## Architecture

```
                    +-------------------+
                    |   Input Task      |
                    +---------+---------+
                              |
                              v
                 +-------------------------+
                 |   Fast Task Router      |
                 +------------+------------+
                              |
                              v
               +----------------------------+
               | Feature Extraction Engine  |
               +------------+---------------+
                              |
                              v
               +----------------------------+
               | Task Classification Engine |
               +------------+---------------+
                              |
                              v
               +----------------------------+
               | Difficulty Estimation      |
               +------------+---------------+
                              |
                              v
                    Hybrid Router Decision
                              |
        +---------------------+----------------------+
        |                     |                      |
        v                     v                      v
 Symbolic Solver        Local GGUF LLM        Fireworks AI
 (Python)             (llama.cpp CPU)      (Cloud Models)
        |                     |                      |
        +---------------------+----------------------+
                              |
                              v
                      Verification Layer
                              |
                              v
                         Final Output
```

---

# Features

## Fast Deterministic Routing

Performs lightweight task identification before expensive inference.

Detects:

- Arithmetic
- Sentiment
- Summarization
- Named Entity Recognition

---

## Feature Extraction

Extracts lightweight features such as:

- Prompt length
- Word count
- Number count
- Mathematical operators
- Constraints
- Code detection
- Structured-output hints

---

## Difficulty Estimation

Tasks are categorized into:

- Easy
- Medium
- Hard

using lightweight heuristics without invoking an LLM.

---

## Hybrid Routing

TACTIC dynamically chooses between:

### Symbolic Solver

Used for deterministic tasks such as:

- Arithmetic
- Percentages
- Algebra
- Financial calculations
- Unit conversions
- Formula evaluation

Advantages:

- Instant execution
- Zero token cost
- Deterministic accuracy

---

### Local Inference

Runs a quantized GGUF model locally through llama.cpp.

Suitable for:

- Simple factual QA
- Lightweight summaries
- Basic extraction

Advantages:

- Zero API cost
- Offline execution

---

### Fireworks AI

Reserved only for tasks requiring stronger reasoning.

Supported models include:

- Minimax-M3
- Kimi-K2 Code

Used for:

- Complex reasoning
- Code generation
- Code debugging
- Long-context tasks

---

# Routing Strategy

The router combines:

- Task type
- Difficulty
- Context length
- Structured output detection
- Semantic hints

to decide the optimal execution path.

Goal:

```
Maximum Accuracy
        +
Minimum Tokens
        +
Minimum Runtime
```

---

# Technology Stack

- Python 3.11
- llama.cpp
- GGUF Models
- Fireworks AI
- OpenAI Compatible SDK
- Docker
- Regex-based Fast Routing
- Custom Symbolic Solver

---

# Repository Structure

```
analysis/
    classifier.py
    difficulty.py
    fast_router.py
    features.py
    local_engine.py

constants/

core/
    pipeline.py

inference/
    client.py
    fireworks.py

local/
    provider.py

optimization/

routing/
    registry.py
    router.py

schemas/

telemetry/

validation/

models/
    llama3.2-3b-q4.gguf
```

---

# Setup & Execution

## Prerequisites

- Python 3.11+
- Docker Desktop (Linux/amd64 support)
- Fireworks AI API Key
- Git

---

## Clone the Repository

```bash
git clone https://github.com/<username>/token-intelligence-engine.git
cd token-intelligence-engine
```

---

## Install Dependencies (Optional - Local Development)

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file in the project root.

Example:

```env
PROVIDER=fireworks

INPUT_PATH=/input/tasks.json
OUTPUT_PATH=/output/results.json

FIREWORKS_API_KEY=<YOUR_FIREWORKS_API_KEY>
FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1

ALLOWED_MODELS=accounts/fireworks/models/minimax-m3,accounts/fireworks/models/kimi-k2p7-code
```

---

## Project Structure

The benchmark expects:

```
input/
    tasks.json

output/
```

The generated results will be written to:

```
output/results.json
```

---

# Running Locally (Python)

```bash
python app.py
```

---

# Running with Docker

## Build the Docker Image

```bash
docker build -t token-intelligence .
```

---

## Run the Container

### Windows PowerShell

```powershell
docker run --rm `
-v "${PWD}\input:/input" `
-v "${PWD}\output:/output" `
-e PROVIDER=fireworks `
-e FIREWORKS_API_KEY=<YOUR_FIREWORKS_API_KEY> `
-e FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1 `
-e ALLOWED_MODELS=accounts/fireworks/models/minimax-m3,accounts/fireworks/models/kimi-k2p7-code `
token-intelligence
```

### Linux / macOS

```bash
docker run --rm \
-v "$(pwd)/input:/input" \
-v "$(pwd)/output:/output" \
-e PROVIDER=fireworks \
-e FIREWORKS_API_KEY=<YOUR_FIREWORKS_API_KEY> \
-e FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1 \
-e ALLOWED_MODELS=accounts/fireworks/models/minimax-m3,accounts/fireworks/models/kimi-k2p7-code \
token-intelligence
```

---

## Expected Output

After successful execution, the pipeline will:

- Load benchmark tasks
- Perform feature extraction
- Route each task to the appropriate execution engine
- Generate predictions
- Verify responses
- Save outputs to:

```
output/results.json
```

A runtime summary similar to the following will be displayed:

```
========================================
SUMMARY
========================================
Tasks      : 175
Symbolic   : XX
Local      : XX
Fireworks  : XX

Runtime
----------------------------------------
Symbolic   : X.XX sec
Local      : XX.XX sec
Fireworks  : XX.XX sec

Token Statistics
----------------------------------------
Prompt Tokens
Completion Tokens
Average Tokens
========================================
```

---

# Running the Benchmark

Simply replace the contents of:

```
input/tasks.json
```

with the benchmark task file and rerun the pipeline.

The generated answers will automatically be written to:

```
output/results.json
```

No code changes are required.

---

# Docker Image

Build:

```bash
docker build -t token-intelligence .
```

Tag:

```bash
docker tag token-intelligence <dockerhub-username>/token-intelligence:latest
```

Push:

```bash
docker push <dockerhub-username>/token-intelligence:latest
```

---

# Troubleshooting

### Missing Input File

```
Input file does not exist: /input/tasks.json
```

Ensure the input directory is mounted correctly.

---

### Fireworks Authentication Error

Verify:

- `FIREWORKS_API_KEY`
- `FIREWORKS_BASE_URL`

---

### Docker Architecture

Verify the image architecture:

```bash
docker inspect token-intelligence --format='{{.Architecture}}'
```

Expected:

```
amd64
```

---

### Verify Model Availability

```bash
docker run --rm --entrypoint ls token-intelligence -lh /app/models
```

The bundled GGUF model should be present inside the container.
---

# Running Locally

Build

```bash
docker build -t token-intelligence .
```

Run

```bash
docker run \
-v ./input:/input \
-v ./output:/output \
-e PROVIDER=fireworks \
-e FIREWORKS_API_KEY=<your_key> \
-e FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1 \
-e ALLOWED_MODELS=accounts/fireworks/models/minimax-m3,accounts/fireworks/models/kimi-k2p7-code \
token-intelligence
```

---

# Design Principles

TACTIC follows a hybrid inference philosophy:

> **Never spend an LLM token if deterministic logic can solve the task.**

Execution priority:

1. Symbolic Solver
2. Local LLM
3. Cloud LLM

This hierarchy minimizes cloud usage while maintaining competitive performance.

---

# Current Limitations

- Rule-based fast routing can misclassify edge cases.
- Symbolic solver currently covers a subset of mathematical reasoning tasks.
- Local inference quality depends on the selected GGUF model.
- Cloud inference remains necessary for complex reasoning problems.

---

# Future Improvements

- Learning-based router trained on benchmark traces
- Adaptive confidence estimation
- Expanded symbolic reasoning library
- Better prompt optimization
- Dynamic token budgeting
- Multi-model ensemble routing
- Automatic benchmark evaluator

---

# Team

**TempEquals2**

Built for the AMD AI Developer Challenge.

---

# License

This project was developed for the AMD AI Hackathon. Licensing may be updated after the competition concludes.


