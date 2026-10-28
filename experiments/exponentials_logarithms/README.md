# Exponentials and Logarithms experiments

`KLTN_mulogarit_zeroshot_full90_Qwen3-4B.ipynb` evaluates the 8,010 generated variants using 10 groups. It expects the JSON file in [`../../data/questions/exponentials_logarithms/`](../../data/questions/exponentials_logarithms/), configured for the Kaggle environment.

[`react/`](react/) contains the initial G01–G10 and D79 notebooks and the H/R rerun notebooks. [`react/prompts/`](react/prompts/) contains the initial and revised type-specific prompt texts. For the exact run used for each of the 32 result files, see [`react_final_runs.csv`](../../data/results/experiment5_exponentials_logarithms/react_final_runs.csv). The final files use G/D79, H, R01 or R04 as appropriate; other notebooks are retained to make the revision history understandable.

The notebooks use Qwen3-4B, vLLM and a SymPy-based Calculator. They require the JSON dataset and GPU/model access; input paths and group settings must be adapted to the environment. The linked [main research repository](https://github.com/manhdungcr7/slm-highschool-math-tutoring) contains the notebook builders and broader development history.

The original notebooks also set `presence_penalty=1.2`; this parameter is not listed in the paper's Qwen3-4B parameter table. Consult the notebook configuration for the complete settings.
