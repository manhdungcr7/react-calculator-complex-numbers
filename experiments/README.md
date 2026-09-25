# Experiments

This directory contains the Kaggle notebooks used to evaluate the baseline and
ReAct-Calculator settings on 24 Complex Numbers problem types.

In the ReAct-Calculator setting, the model alternates among:

1. `Thought`: reasoning about the next step;
2. `Action: Calculator` and `Action Input`: requesting a computation;
3. `Observation`: receiving the result produced by the SymPy-based Calculator.

The process continues until the model produces a final answer or reaches the
configured limit. Detailed per-question outputs are available under
[`../data/results/experiment3_4_react_calculator/`](../data/results/experiment3_4_react_calculator/).

Only the notebooks used for the reported experiments are included. Development
notebooks, one-question debugging runs, and notebook-generated logs are
excluded.

## `Qwen3-4B/`

Qwen3-4B is the main model. Its 18 notebooks collectively cover all 24
selected problem types.

| File | Coverage |
|---|---|
| `KLTN_D<NN>_ReAct_Calculator_full90.ipynb` | Sixteen single-type notebooks, each containing 90 questions |
| `KLTN_Nhom1_D04_D14_D28_D32_D33_full90.ipynb` | D04, D14, D28, D32, and D33 in one model session |
| `KLTN_Nhom2_D34_D40_D42_D45_D46_D49_full90.ipynb` | D34, D40, D42, D45, D46, and D49 in one model session |

The grouped notebooks add the eight types not covered by the single-type
notebooks. The D55 code used in the original notebooks corresponds to D54 in
the paper. See [`../data/README.md`](../data/README.md) for the code-mapping
note.

## Cross-model evaluation

The `DeepSeek-R1-Distill-Qwen-1.5B/` and `Llama-3.2-3B-Instruct/`
directories each contain six notebooks: three type groups evaluated in two
settings.

| Type group | ReAct-Calculator | Baseline |
|---|---|---|
| D04, D38, D46, D51, D53 | `KLTN_5dang_ReAct_Calculator_full90_<model>.ipynb` | `KLTN_5dang_zeroshot_full90_<model>.ipynb` |
| D35, D36, D37, D39, D44, D45, D47, D48, D50, D52, D55 | `KLTN_11dang_ReAct_Calculator_full90_<model>.ipynb` | `KLTN_11dang_zeroshot_full90_<model>.ipynb` |
| D14, D28, D32, D33, D34, D40, D42, D49 | `KLTN_8dangMoi_ReAct_Calculator_full90_<model>.ipynb` | `KLTN_8dangMoi_zeroshot_full90_<model>.ipynb` |

`<model>` is either `DeepSeek-R1-Distill-Qwen-1.5B` or
`Llama-3.2-3B-Instruct`.

The prompt and ReAct-Calculator procedure developed for Qwen3-4B were reused
without model-specific content changes. Only the model identifier and the
generation parameters recommended for each model were changed.

## Running the notebooks

Each notebook expects a Kaggle Dataset containing its question JSON file. The
input path is configured near the beginning of the notebook through variables
such as `DATA_PATH`, `DATA_DIR`, or `MERGED_DATA_PATH`. Upload the corresponding
files from [`../data/questions/`](../data/questions/) and update these paths
before running a notebook.
