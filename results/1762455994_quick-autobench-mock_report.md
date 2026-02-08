# Benchmark Report

## Summary (by task_type × split)

| task_type   | split   |   mean_acc |   novelty |   reasoning_depth |   efficiency |   consistency_rate |
|-------------|---------|------------|-----------|-------------------|--------------|--------------------|
| causal      | test    |          0 |       0.2 |              0.1  |            1 |                  0 |
| equation    | test    |          1 |       0   |              0.14 |            1 |                  1 |
| qa          | test    |          0 |       0.1 |              0.1  |            1 |                  0 |

## First 10 Items

| id       | domain   | task_type   | split   | prediction                                   | rationale                                        |   acc |   mse | consistency_pass   |   novelty |   reasoning_depth |   efficiency |   prompt_tokens |   completion_tokens |   total_tokens |
|----------|----------|-------------|---------|----------------------------------------------|--------------------------------------------------|-------|-------|--------------------|-----------|-------------------|--------------|-----------------|---------------------|----------------|
| syn-eq-0 | physics  | equation    | test    | y = 2*x + 1  # MOCK hypothesis               | Fitted a linear model using synthetic reasoning. |     1 |     0 | True               |       0   |              0.14 |            1 |              32 |                  30 |             62 |
| syn-cg-1 | physics  | causal      | test    | {A->B, B->C}  # MOCK causal graph            | Inferred edges via mock interventions.           |     0 |   nan | False              |       0.2 |              0.1  |            1 |              22 |                  30 |             52 |
| syn-qa-2 | general  | qa          | test    | Hypothesis: variable X positively affects Y. | Based on mock literature synthesis.              |     0 |   nan | False              |       0.1 |              0.1  |            1 |               6 |                  30 |             36 |
| syn-eq-3 | physics  | equation    | test    | y = 2*x + 1  # MOCK hypothesis               | Fitted a linear model using synthetic reasoning. |     1 |     0 | True               |       0   |              0.14 |            1 |              32 |                  30 |             62 |
| syn-cg-4 | physics  | causal      | test    | {A->B, B->C}  # MOCK causal graph            | Inferred edges via mock interventions.           |     0 |   nan | False              |       0.2 |              0.1  |            1 |              22 |                  30 |             52 |
| syn-qa-5 | general  | qa          | test    | Hypothesis: variable X positively affects Y. | Based on mock literature synthesis.              |     0 |   nan | False              |       0.1 |              0.1  |            1 |               6 |                  30 |             36 |
| syn-eq-6 | physics  | equation    | test    | y = 2*x + 1  # MOCK hypothesis               | Fitted a linear model using synthetic reasoning. |     1 |     0 | True               |       0   |              0.14 |            1 |              32 |                  30 |             62 |
| syn-cg-7 | physics  | causal      | test    | {A->B, B->C}  # MOCK causal graph            | Inferred edges via mock interventions.           |     0 |   nan | False              |       0.2 |              0.1  |            1 |              22 |                  30 |             52 |
| syn-qa-8 | general  | qa          | test    | Hypothesis: variable X positively affects Y. | Based on mock literature synthesis.              |     0 |   nan | False              |       0.1 |              0.1  |            1 |               6 |                  30 |             36 |
| syn-eq-9 | physics  | equation    | test    | y = 2*x + 1  # MOCK hypothesis               | Fitted a linear model using synthetic reasoning. |     1 |     0 | True               |       0   |              0.14 |            1 |              32 |                  30 |             62 |