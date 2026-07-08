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