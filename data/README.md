# Data

This directory contains the questions and per-question model outputs used to
verify the results reported in the paper. The questions were produced by the
scripts under [`../scripts/`](../scripts/), and the experiment outputs were
produced by the notebooks under [`../experiments/`](../experiments/).

## Questions

[`questions/So_phuc_day_du.csv`](questions/So_phuc_day_du.csv) contains the
complete Complex Numbers collection used in the study:

- 65 original questions extracted from a real high-school review document;
- 4,860 generated evaluation questions across 54 problem types;
- four answer choices, the correct answer, and a solution for each question.

The original internal dataset used codes D01 through D55. The original D54
type, containing one source question and 90 variants, was removed when the
study scope was finalized. The original D55 type was therefore renamed D54 in
the paper and in this exported dataset.

## Results

| Directory | Experiment | Contents |
|---|---|---|
| [`experiment1_65cau_khao_sat/`](results/experiment1_65cau_khao_sat/) | Experiment 1: dataset difficulty | Outputs for the 65 original questions from GPT-4o, Gemini-2.5-Flash, and Qwen3-4B |
| [`experiment2_810cau_huong_dan_giai/`](results/experiment2_810cau_huong_dan_giai/) | Experiment 2: zero-shot with a solution guide | Qwen3-4B baseline and guided outputs for 810 questions from the nine most difficult types |
| [`experiment3_4_react_calculator/`](results/experiment3_4_react_calculator/) | Experiments 3 and 4: ReAct-Calculator | Outputs for 2,160 questions from Qwen3-4B, DeepSeek-R1-Distill-Qwen-1.5B, and Llama-3.2-3B-Instruct |

### Experiment 1

[`65cau_khao_sat_GPT4o_Gemini_Qwen3-4B.csv`](results/experiment1_65cau_khao_sat/65cau_khao_sat_GPT4o_Gemini_Qwen3-4B.csv)
contains the questions, correct answers, model solutions, and C/I/U labels:

- **C**: Correct
- **I**: Incorrect
- **U**: Undetermined

The totals match the paper: GPT-4o 56/9/0, Gemini-2.5-Flash 65/0/0, and
Qwen3-4B 62/2/1.

### Experiment 2

[`810cau_zero_shot_vs_huong_dan_giai_Qwen3-4B.csv`](results/experiment2_810cau_huong_dan_giai/810cau_zero_shot_vs_huong_dan_giai_Qwen3-4B.csv)
compares the Qwen3-4B baseline with the solution-guide setting. The totals
match the paper: 234/21/555 at baseline and 665/11/134 with the guide.

### Experiments 3 and 4

Results are grouped by model under
[`experiment3_4_react_calculator/`](results/experiment3_4_react_calculator/).
Each file is named `d<NN>_<setting>_full90.csv`, where `<setting>` is
`zeroshot` or `react_calculator`. Every file contains 90 questions from one
problem type, the selected answers, the C/I/U labels, and the generated
solutions.

The Qwen3-4B directory contains only ReAct-Calculator outputs. Its baseline
results for these 24 types are included in the paper's baseline table and are
not duplicated here.
