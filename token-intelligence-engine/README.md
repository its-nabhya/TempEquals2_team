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