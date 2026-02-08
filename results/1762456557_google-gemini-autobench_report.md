# Benchmark Report

## Summary (by task_type × split)

| task_type   | split   |   mean_acc |   novelty |   reasoning_depth |   efficiency |   consistency_rate |
|-------------|---------|------------|-----------|-------------------|--------------|--------------------|
| causal      | test    |          0 |       0.1 |              0.16 |            1 |                  0 |
| equation    | test    |          0 |       0.5 |              0.16 |            1 |                  0 |
| qa          | test    |          0 |       0.8 |              0.14 |            1 |                  0 |

## First 10 Items

| id       | domain   | task_type   | split   | prediction                                                                                                                                                                                                                           | rationale                                                       |   acc |     mse | consistency_pass   |   novelty |   reasoning_depth |   efficiency |   prompt_tokens |   completion_tokens |   total_tokens |
|----------|----------|-------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|-------|---------|--------------------|-----------|-------------------|--------------|-----------------|---------------------|----------------|
| syn-eq-0 | physics  | equation    | test    | Error: Invalid operation: The `response.text` quick accessor requires the response to contain a valid `Part`, but none were returned. The candidate's [finish_reason](https://ai.google.dev/api/generate-content#finishreason) is 2. | Failed to generate response due to API error.                   |     0 |   1e+06 | False              |       0.1 |              0.16 |            1 |               0 |                   0 |              0 |
| syn-cg-1 | physics  | causal      | test    | Error: Invalid operation: The `response.text` quick accessor requires the response to contain a valid `Part`, but none were returned. The candidate's [finish_reason](https://ai.google.dev/api/generate-content#finishreason) is 2. | Failed to generate response due to API error.                   |     0 | nan     | False              |       0.1 |              0.16 |            1 |               0 |                   0 |              0 |
| syn-qa-2 | general  | qa          | test    | Newton's Second Law of Motion.                                                                                                                                                                                                       | Generated scientific hypothesis using language model reasoning. |     0 | nan     | False              |       0.8 |              0.14 |            1 |               6 |                   5 |             11 |
| syn-eq-3 | physics  | equation    | test    | y = 2x + 1

**                                                                                                                                                                                                                       | **
The relationship is linear, as the change                    |     0 |   1e+06 | False              |       0.9 |              0.16 |            1 |              32 |                  13 |             45 |
| syn-cg-4 | physics  | causal      | test    | Error: Invalid operation: The `response.text` quick accessor requires the response to contain a valid `Part`, but none were returned. The candidate's [finish_reason](https://ai.google.dev/api/generate-content#finishreason) is 2. | Failed to generate response due to API error.                   |     0 | nan     | False              |       0.1 |              0.16 |            1 |               0 |                   0 |              0 |