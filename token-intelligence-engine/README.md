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