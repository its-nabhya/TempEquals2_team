# TACTIC Architecture

## Overview

TACTIC (Token-Aware Cognitive Task Intelligence Compiler) is a modular AI inference framework designed to minimize inference token consumption while maintaining task accuracy.

Rather than maximizing reasoning capability, the framework optimizes the following objective:

```
Minimize Expected Tokens

subject to

Expected Accuracy ≥ Required Threshold
```

The architecture is intentionally provider-agnostic and model-agnostic.

No component depends on Gemma, Llama, Qwen or any other individual model.

---

# Design Philosophy

TACTIC follows four guiding principles.

## 1. Progressive Architecture

The system is designed for current requirements while remaining extensible.

Abstractions are introduced only when they solve existing problems rather than anticipated ones.

---

## 2. Single Responsibility

Each module owns exactly one responsibility.

Examples

- app.py bootstraps the application.
- router.py selects models.
- provider.py performs inference.
- compiler.py builds prompts.

No module should own more than one concern.

---

## 3. Provider Independence

The routing pipeline never communicates directly with Fireworks.

Instead, inference occurs through an abstract provider interface.

Current providers

- Mock
- Fireworks

Future providers

- Ollama
- vLLM
- OpenRouter

The remainder of the system remains unchanged.

---

## 4. Typed Domain Objects

The application communicates using strongly typed schema objects rather than dictionaries.

Current schemas

- Task
- TaskContext
- TaskResult

---

# System Layers

```
Application
      │
      ▼
Configuration
      │
      ▼
Pipeline
      │
      ▼
Analysis
      │
      ▼
Prompt Compilation
      │
      ▼
Routing
      │
      ▼
Inference
      │
      ▼
Validation
      │
      ▼
Results
```

Each layer communicates only with the next layer.

---

# Component Responsibilities

## Application

Responsible only for bootstrapping.

Owns

- startup
- dependency injection
- shutdown

Never owns

- routing
- inference
- business logic

---

## Configuration

Creates the application's Config object from environment variables and sensible defaults.

---

## Pipeline

Coordinates execution.

Responsible for moving a task through the complete processing pipeline.

Contains no routing or inference logic.

---

## Analysis

Performs local understanding of the task.

Examples

- task classification
- feature extraction
- canonicalization

No external inference calls are allowed.

---

## Prompt Compilation

Transforms analyzed tasks into optimized prompts.

Responsible only for prompt construction.

---

## Routing

Determines the most appropriate model for the current task.

Uses

- task characteristics
- available models
- optimization policy

Produces a routing decision.

---

## Inference

The only layer permitted to communicate with external AI providers.

Responsible only for executing inference.

---

## Validation

Verifies responses before returning them.

Future responsibilities include

- confidence estimation
- JSON validation
- local verification
- escalation

---

# Data Flow

```
app.py

↓

Config

↓

Task

↓

TaskContext

↓

Analysis

↓

Prompt Compiler

↓

Router

↓

Inference Provider

↓

Validation

↓

TaskResult

↓

results.json
```

---

# Dependency Rule

Dependencies always point downward.

Allowed

```
Pipeline

↓

Router

↓

Provider
```

Forbidden

```
Provider

↓

Pipeline
```

This guarantees an acyclic dependency graph and simplifies testing.

---

# Future Extensions

The architecture intentionally supports future additions without structural changes.

Examples

- Dynamic routing policies
- Bayesian optimization
- Contextual bandits
- Local model support
- Additional providers
- Fine-tuned routing models

These enhancements should occur inside existing modules rather than by reorganizing the project structure.


<!-- Changing gears -->

## Development Philosophy

The architecture is implemented incrementally. Every development milestone results in a runnable system before additional intelligence is introduced.

This ensures that optimization work is always performed on a functioning baseline rather than an incomplete prototype.


### TaskContext

Every task is wrapped inside a TaskContext object before entering the pipeline.

TaskContext serves as the shared state passed between pipeline stages, allowing each stage to enrich the task without modifying upstream components.

### Fireworks Integration

Fireworks is accessed through the official OpenAI-compatible SDK.

The SDK is wrapped by a thin FireworksClient abstraction so that external API changes remain isolated from the remainder of the codebase.


### Routing Context

The router receives the complete TaskContext rather than only the prompt.

This allows routing decisions to evolve from prompt-based heuristics to feature-based optimization without changing the routing interface.

### Provider Construction

Inference providers do not construct SDK clients directly. Client creation is delegated to the ProviderFactory, ensuring providers depend only on abstractions required for inference.

### Model Registry

The Model Registry maintains metadata for each allowed Fireworks model, including capabilities and availability.

Routing decisions query the registry rather than relying on hardcoded model identifiers.

### Task Classification

Task classification is performed locally using lightweight heuristics.

The router receives a classified TaskContext instead of the raw prompt, allowing routing decisions to focus solely on model selection.

### Local Symbolic Engine

The Local Symbolic Engine executes before model routing.

It attempts deterministic solutions for supported task categories and returns high-confidence answers directly, bypassing external inference when appropriate.