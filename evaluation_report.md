# CodeLens AI Evaluation Report

## Overall Metrics

- Total programs: 1000
- Overall accuracy: 0.8020
- Macro precision: 0.9531
- Macro recall: 0.8611
- Macro F1: 0.8666
- Micro precision: 0.9024
- Micro recall: 0.8438
- Micro F1: 0.8721

## Rule-wise Metrics

| Rule | Support | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| UndefinedVariable | 100 | 100 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| InfiniteLoop | 100 | 25 | 0 | 75 | 1.0000 | 0.2500 | 0.4000 |
| MissingBaseCase | 100 | 100 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| BinarySearchLogicError | 100 | 50 | 0 | 50 | 1.0000 | 0.5000 | 0.6667 |
| UnreachableCode | 100 | 100 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| UnusedVariable | 100 | 100 | 73 | 0 | 0.5780 | 1.0000 | 0.7326 |
| MissingReturn | 100 | 100 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| ShadowedVariable | 50 | 50 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| DangerousImport | 50 | 50 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |

## Top False Positives

- Program 6 (Correct Programs): UnusedVariable
- Program 10 (Correct Programs): UnusedVariable
- Program 16 (Correct Programs): UnusedVariable
- Program 20 (Correct Programs): UnusedVariable
- Program 26 (Correct Programs): UnusedVariable
- Program 30 (Correct Programs): UnusedVariable
- Program 36 (Correct Programs): UnusedVariable
- Program 40 (Correct Programs): UnusedVariable
- Program 46 (Correct Programs): UnusedVariable
- Program 50 (Correct Programs): UnusedVariable

## Top False Negatives

- Program 301 (Infinite Loop): InfiniteLoop
- Program 302 (Infinite Loop): InfiniteLoop
- Program 303 (Infinite Loop): InfiniteLoop
- Program 305 (Infinite Loop): InfiniteLoop
- Program 306 (Infinite Loop): InfiniteLoop
- Program 307 (Infinite Loop): InfiniteLoop
- Program 309 (Infinite Loop): InfiniteLoop
- Program 310 (Infinite Loop): InfiniteLoop
- Program 311 (Infinite Loop): InfiniteLoop
- Program 313 (Infinite Loop): InfiniteLoop

## Detection Rate

- Micro recall: 0.8438
- Macro recall: 0.8611

## Brief Observations

- This report is generated from deterministic benchmark labels.
- Exact-match accuracy treats every program as correct only when the predicted rule set exactly matches the expected rule set.
- Macro scores weight each rule equally; micro scores weight each individual decision equally.
