# Engineering Decisions

This document records significant architectural decisions made during development.

---

# ED-001

## Python Version

Decision

Python 3.11

Reason

- Excellent compatibility across modern AI libraries
- Mature ecosystem
- Native support for StrEnum
- Stable typing support

Rejected

Python 3.12

Reason

Some AI libraries still lag in support.

---

# ED-002

## Dependency Management

Decision

Use pip with requirements.txt.

Reason

- Universal
- Docker friendly
- Simple CI/CD integration

Rejected

Poetry

Reason

Additional tooling without meaningful benefit for this project.

---

# ED-003

## Progressive Architecture

Decision

Only introduce abstractions when required.

Reason

Avoid unnecessary complexity and premature optimization.

Guiding Principle

> Architecture should be stable. Abstractions should be earned.

---

# ED-004

## Layered Design

Decision

Use a strict layered architecture.

Application

↓

Configuration

↓

Pipeline

↓

Analysis

↓

Prompt Compilation

↓

Routing

↓

Inference

↓

Validation

Reason

Clear separation of responsibilities.

---

# ED-005

## Provider Abstraction

Decision

Inference occurs through an abstract provider interface.

Current implementations

- Mock
- Fireworks

Reason

Allows provider replacement without changing the processing pipeline.

---

# ED-006

## Provider Factory

Decision

Providers are instantiated through a factory.

Reason

Avoid conditional logic inside app.py.

---

# ED-007

## Typed Configuration

Decision

Represent configuration using a dataclass.

Reason

- type safety
- autocomplete
- single source of truth
- cleaner interfaces

---

# ED-008

## Typed Domain Objects

Decision

Represent application data using dataclasses inside schemas/.

Current objects

- Task
- TaskContext
- TaskResult

Reason

Avoid passing loosely structured dictionaries throughout the application.

---

# ED-009

## Enum Usage

Decision

Use StrEnum for finite application states.

Current usage

- ProviderType

Future

- TaskType
- Difficulty
- RoutingPolicy

Reason

Avoid magic strings.

---

# ED-010

## Mock-first Development

Decision

Develop against a MockProvider before integrating Fireworks.

Reason

- deterministic testing
- zero API cost
- offline development
- easier debugging

---

# ED-011

## Business Logic Isolation

Decision

Business logic must never appear inside

- app.py
- config.py

Reason

These files should remain orchestration-only.

---

# ED-012

## Router Independence

Decision

The router selects models but never performs inference.

Reason

Routing and inference are separate concerns.

---

# ED-013

## Fireworks Independence

Decision

The architecture never references specific models.

Reason

Models are discovered dynamically at runtime through

ALLOWED_MODELS

This satisfies the hackathon requirement while remaining future-proof.

---

# ED-014

## Optimization Objective

TACTIC optimizes

```
Minimize Expected Tokens

subject to

Expected Accuracy ≥ Required Threshold
```

rather than maximizing raw model capability.

This objective remains independent of the underlying inference provider.

---

# ED-015

## Logging

Decision

Use Python's built-in logging module.

Reason

Production standard.

Avoid print statements outside local debugging.

---

# ED-016

## Testing Strategy

Decision

Every module should be independently testable.

Reason

Improves reliability and simplifies debugging.

---

# ED-017

## Architecture Freeze

Decision

The folder structure and module responsibilities are frozen for v1.0.

Future improvements should occur inside modules rather than by reorganizing the repository.



# ED-018

## Incremental Development

Decision

Every implementation milestone must produce a runnable application.

Reason

Early integration reduces debugging complexity and keeps the project continuously testable.

---

# ED-019

## Local Symbolic First

Decision

Version 1 prioritizes symbolic local processing (Python, regex, AST, SymPy, spaCy where applicable) over bundling a local LLM.

Reason

The grading environment provides only 2 vCPUs and 4 GB RAM. Symbolic methods are deterministic, lightweight, and consume zero Fireworks tokens.


# ED-020

## Typed Pipeline State

Decision

Introduce a TaskContext object that flows through the entire pipeline.

Reason

Avoid passing multiple loosely coupled parameters between stages while keeping processing state centralized and type-safe.

---

# ED-021

## Pathlib

Decision

Use pathlib for filesystem operations.

Reason

Provides a modern, platform-independent API and improves readability over os.path.

# ED-022

## OpenAI SDK Wrapper

Decision

Wrap the OpenAI-compatible Fireworks SDK inside a FireworksClient.

Reason

Avoid coupling the pipeline to a third-party SDK.

---

# ED-023

## Mock-first Provider Development

Decision

Implement MockProvider before FireworksProvider.

Reason

Allows deterministic testing of the complete execution pipeline without consuming API credits.

---

# ED-024

## Router API

Decision

The router is responsible only for selecting a model.

Inference remains exclusively inside the provider layer.

# ED-025

## TaskContext as Pipeline State

Decision

Routing operates on the TaskContext rather than the raw prompt.

Reason

Future routing decisions require additional information such as task classification, difficulty estimation, confidence, and extracted features. Passing TaskContext avoids repeated interface changes while preserving separation between routing and inference.

# ED-026

## Provider Dependency Injection

Decision

FireworksProvider receives a FireworksClient instance instead of constructing one internally.

Reason

This separates provider logic from client construction, improves testability, and keeps SDK-specific initialization outside the provider.

# ED-027

## Capability-Based Model Registry

Decision

Represent models as structured ModelProfile objects instead of raw strings.

Reason

Allows routing policies to reason over model capabilities while remaining independent of specific model identifiers.

---

# ED-028

## Local Feature Extraction

Decision

Extract inexpensive heuristic features locally before routing.

Reason

Feature extraction incurs zero Fireworks tokens and provides useful signals for routing decisions.


# ED-029

## Deterministic Task Classification

Decision

Implement the initial task classifier using local heuristic rules instead of an LLM.

Reason

The hackathon evaluation rewards lower Fireworks token usage. Deterministic classification provides a strong routing signal at zero inference cost.

---

# ED-030

## Capability-Driven Routing

Decision

The router selects models based on task capabilities rather than prompt text.

Reason

Separating task understanding from routing simplifies both components and allows routing policies to evolve independently.

# ED-031

## Local-First Inference

Decision

Attempt deterministic local solutions before any Fireworks API call.

Reason

The hackathon scores only Fireworks token usage. Local computation is effectively free and should be exhausted before external inference.

---

# ED-032

## Solver Isolation

Decision

Implement independent symbolic solvers for each task category.

Reason

Task-specific solvers evolve independently, are reusable, and keep the Local Symbolic Engine focused solely on orchestration.

# ED-033

## Submission-First Development

Decision

Prioritize producing a fully functional submission before implementing token-saving optimizations.

Reason

A valid submission establishes a measurable baseline and minimizes integration risk. Subsequent optimization work can then be evaluated empirically against this baseline.

# ED-034

## Baseline Before Optimization

Decision

Keep the initial dependency set intentionally minimal.

Reason

Reducing moving parts improves submission reliability and provides a stable baseline for measuring future optimization work.

# ED-035

## Local Validation Before Containerization

Decision

Perform a successful local execution before building the Docker image.

Reason

Debugging Python runtime issues is significantly faster outside the container. Docker should validate packaging, not application correctness.

# ED-036

## Runtime-First Validation

Decision

Freeze feature development once the core execution pipeline is assembled and prioritize end-to-end runtime validation.

Reason

Resolving integration issues before introducing additional functionality reduces debugging complexity and establishes a stable baseline for future optimization.

# ED-037

## Incremental Local Engine

Decision

Keep the Local Symbolic Engine integrated into the architecture but disable it until task-specific solvers are implemented and validated.

Reason

This preserves the intended execution flow while minimizing integration risk for the first runnable baseline.

# ED-038

## Fail-Fast External API Handling

Decision

Wrap Fireworks SDK calls with explicit validation and error propagation.

Reason

External API failures should produce actionable runtime errors rather than ambiguous SDK exceptions, improving debugging and operational reliability.

# ED-039

## Environment-Based Configuration

Decision

Use `.env` only for local development while relying on injected environment variables in the hackathon runtime.

Reason

This preserves compatibility with the evaluation harness while providing a convenient local development experience.