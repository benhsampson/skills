---
name: interview-me
description: Resolve consequential ambiguity before implementation, one question at a time.
disable-model-invocation: true
---

Interview me one question at a time about anything ambiguous, prioritize questions where my answer would change the architecture.

Use **information gain** as the gate: ask only when the answer could materially change the architecture, data model, public interface, security, or an expensive-to-reverse decision.

Before asking, inspect the codebase when it can resolve the ambiguity. For each question, recommend a default and briefly explain what the answer changes.

Stop when the remaining ambiguity is cheap and reversible; proceed with reasonable assumptions.
