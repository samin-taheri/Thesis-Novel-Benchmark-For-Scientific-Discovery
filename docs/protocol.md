# Evaluation Protocol (v1)

- **Determinism**: temperature=0.0 (and 0.2 for robustness), fixed seeds.
- **Tools**: Closed-book unless scenario explicitly allows calculator/code.
- **Prompts**: Use `prompts/base.txt` plus scenario-specific instructions.
- **Retries**: Only on API/network errors (≤2). No retries for accuracy.
- **Scoring**: Prefer **programmatic verifiers** (numeric equivalence, causal metrics, unit checks).
- **Metrics**: Accuracy, Novelty, Generalization (IID vs OOD), Scientific Consistency, Reasoning Depth, Efficiency.
- **Reporting**: CSV summaries + Markdown report.
- **Ethics**: Avoid proprietary data; document any human-in-the-loop judgments.
