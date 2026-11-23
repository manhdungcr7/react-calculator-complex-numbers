# Problem-type router on Complex Numbers benchmark v2

The router (Qwen3-0.6B + LoRA, the adapter that identifies all problem types in the original set correctly) was run on the 2,160 reworded questions in [`../../questions/benchmark_so_phuc_v2_24dang_2160cau.csv`](../../questions/benchmark_so_phuc_v2_24dang_2160cau.csv). The candidate list has 142 types (Exponentials and Logarithms: 1–88, Complex Numbers: 89–142). The notebook is [`../../../experiments/router/KLTN_Router_v2_Kaggle.ipynb`](../../../experiments/router/KLTN_Router_v2_Kaggle.ipynb); it was run in seven parts on Kaggle and the parts were merged here.

## Result

| Measure | Correct |
|---|---:|
| Final prediction | 1923/2160 (89.03%) |
| Step 1 (score of the prefix "Dạng N:" only) | 1385/2160 (64.12%) |

Of the 237 errors, 82 were assigned to an Exponentials and Logarithms type. The median step-1 confidence is 0.94 for correct predictions and 0.54 for errors.

| Code | Questions | Step 1 correct | Final correct |
|---|---:|---:|---:|
| D04 | 90 | 82 | 89 |
| D14 | 90 | 19 | 76 |
| D28 | 90 | 19 | 54 |
| D32 | 90 | 75 | 86 |
| D33 | 90 | 73 | 90 |
| D34 | 90 | 43 | 88 |
| D35 | 90 | 72 | 90 |
| D36 | 90 | 71 | 90 |
| D37 | 90 | 70 | 88 |
| D38 | 90 | 71 | 86 |
| D39 | 90 | 57 | 85 |
| D40 | 90 | 62 | 87 |
| D42 | 90 | 58 | 78 |
| D44 | 90 | 11 | 75 |
| D45 | 90 | 29 | 63 |
| D46 | 90 | 67 | 72 |
| D47 | 90 | 53 | 68 |
| D48 | 90 | 43 | 76 |
| D49 | 90 | 37 | 51 |
| D50 | 90 | 88 | 90 |
| D51 | 90 | 47 | 83 |
| D52 | 90 | 77 | 87 |
| D53 | 90 | 83 | 86 |
| D54 | 90 | 78 | 85 |

## Files

- `router_predictions_2160.csv`: one row per question. `so_dang` is the correct type number, `pred_v2` the final prediction, `pred_buoc1_v2` the step-1 prediction, `top3_v2` the three best types, `conf_v2` the step-1 probability of the top type, `dung_v2` whether the final prediction is correct.
- `router_errors_237.csv`: the 237 incorrect questions with the v2 question text (without answer choices).
