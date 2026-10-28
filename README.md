# ReAct-Calculator for High-School Mathematics

This repository accompanies the SOICT 2026 camera-ready paper **"Improving Small Language Model Performance on High-School Mathematics Using ReAct: A Case Study on Complex Numbers."** The main research and graduation-thesis repository is [slm-highschool-math-tutoring](https://github.com/manhdungcr7/slm-highschool-math-tutoring).

The study evaluates Qwen3-4B on known multiple-choice problem types, using manually written solution guides and ReAct examples together with a SymPy-based Calculator. The main case study is Complex Numbers; the camera-ready evaluation also includes Exponentials and Logarithms and questions collected from the Internet.

## Results reported in the paper

| Evaluation | Baseline | Guided/ReAct-Calculator |
|---|---:|---:|
| Complex Numbers: all 4,860 variants, 54 types | Qwen3-4B: 85.7%; Gemini-2.5-Flash: 98.5% | — |
| Complex Numbers: 810 variants in nine difficult types | Qwen3-4B: 28.9% | Solution guide: 82.1% |
| Complex Numbers: 2,160 variants in 24 selected types | Qwen3-4B: 67.8% | ReAct-Calculator: 100% |
| Exponentials and Logarithms: 2,880 variants in 32 selected types | Qwen3-4B: 69.0% | ReAct-Calculator: 100% |
| Internet questions: 77 questions in 41 known types | 43/43 baseline-prompt questions | 30/34 ReAct-prompt questions; 73/77 overall (94.8%) |

The full Exponentials and Logarithms set contains 8,010 generated variants across 89 types, derived from 107 original questions; the regraded baseline result is 7,118/8,010 (88.86%). Reusing the Complex Numbers prompts and procedure on Llama-3.2-3B-Instruct changed accuracy from 20.7% to 53.5%; DeepSeek-R1-Distill-Qwen-1.5B changed from 40.3% to 38.9%.

The generated variants generally preserve the original question structure and vary numeric values. The Internet set is limited to known types, and the approach did not answer all of those questions correctly. The study does not establish performance on unseen problem types or free-response questions, nor does it isolate the effects of the Calculator and the ReAct example.

## Repository contents

| Path | Contents |
|---|---|
| [`appendix/`](appendix/) | Codes and names of the 54 Complex Numbers types in the paper |
| [`data/questions/`](data/questions/) | Complex Numbers and Exponentials and Logarithms questions |
| [`data/results/`](data/results/) | Per-question outputs and result summaries, including Experiments 5 and 6 |
| [`experiments/`](experiments/) | Baseline and ReAct-Calculator notebooks and prompts |
| [`scripts/`](scripts/) | Extraction, generation and result-verification scripts |

Start with [`data/README.md`](data/README.md) for the precise data files, selection procedure, regrading, and final-run provenance. [`experiments/exponentials_logarithms/README.md`](experiments/exponentials_logarithms/README.md) explains which notebooks produced the final results. Questions and model outputs are in Vietnamese. The original review PDF is not distributed here.

To check the counts in Experiments 5 and 6 using the included CSV files:

```bash
python scripts/verify_camera_ready_results.py
```

Some experiment notebooks require Kaggle datasets, GPU resources, model access, and paths configured by the user. See the directory READMEs. The 100% results on the selected generated variants include type-specific prompts refined after inspecting earlier failures; they should not be interpreted as an independent held-out evaluation.

## Appendix: 54 Problem Types (Complex Numbers)

The following codes are used in the paper's result tables. A machine-readable
version is available at
[`appendix/problem_types_54.csv`](appendix/problem_types_54.csv).

| Code | Problem type |
|---|---|
| D01 | Given $z=a+bi$, find both the real and imaginary parts of $z$ |
| D02 | Given $z=a+bi$, find the real part of $z$ |
| D03 | Given $z=a+bi$, find the imaginary part of $z$ |
| D04 | Given $z=a+bi$, find the real and imaginary parts of its conjugate |
| D05 | Given two complex numbers, find the real part of their sum |
| D06 | Given two complex numbers, find the imaginary part of the first plus the conjugate of the second |
| D07 | Given two complex numbers, find the real or imaginary part of their product |
| D08 | Given $z$, find the real or imaginary part of $z^2$ |
| D09 | Given the real and imaginary parts, write the corresponding complex number |
| D10 | Given several complex numbers, identify the purely imaginary numbers |
| D11 | Given $z=a+bi$, find its conjugate |
| D12 | Given a complex number as an expression, find its conjugate |
| D13 | Given $z=a+bi$, compute $\lvert z\rvert$ |
| D14 | Given two complex numbers, compute the modulus of their sum or difference |
| D15 | Compute $\lvert z\rvert$ when the conjugate of $z$ equals a product of two complex numbers |
| D16 | Compute the modulus of a product containing a complex number and the conjugate of another |
| D17 | Compute the modulus of the product of two given complex numbers |
| D18 | Given $z=a+bi$, find the coordinates of the point representing $z$ |
| D19 | Find the point representing $z^2$ |
| D20 | Find the point representing $w=iz$ |
| D21 | Find the point representing a linear combination of two complex numbers |
| D22 | Given the representing point $M(p;q)$, find $z$ |
| D23 | Given the representing point $M(p;q)$, find the real part of $z$ |
| D24 | Given two complex numbers, find their sum |
| D25 | Given two complex numbers, find their difference |
| D26 | Given $z$ and a real number $k$, compute $kz$ |
| D27 | Given $z$, compute an expression that combines several operations on $z$ |
| D28 | Solve a linear equation containing only $z$ or only its conjugate, then compute $\lvert z\rvert$ |
| D29 | Solve a linear equation containing only $z$ or only its conjugate, then find a component of $z$ |
| D30 | Solve a linear equation containing only $z$ or only its conjugate, then find the conjugate of $z$ |
| D31 | Solve an equation containing both $z$ and its conjugate, then add the real and imaginary parts |
| D32 | Solve an equation containing both $z$ and its conjugate, then compute $\lvert z\rvert$ |
| D33 | Given an equation containing $\lvert z\rvert$, find $z$ by matching real and imaginary parts |
| D34 | Given a circle condition and the condition that $z^2$ is purely imaginary, count the solutions |
| D35 | Given a circle condition and a purely imaginary quotient condition, count the solutions |
| D36 | Given a modulus equation and a perpendicular-bisector condition, count the solutions |
| D37 | Given an equation containing $\lvert z\rvert$ in several places, determine the interval containing $\lvert z\rvert$ |
| D38 | Given an equation containing $\lvert z\rvert$ in several places, count the solutions |
| D39 | Given conditions involving the modulus and conjugate, count the solutions |
| D40 | Given $\lvert z-z_0\rvert=R$, identify the locus representing $z$ |
| D41 | Given that a product is purely imaginary, find the center of the resulting circle |
| D42 | Given that a product is purely imaginary, find the radius of the resulting circle |
| D43 | Given $w=az+b$ with fixed $\lvert z\rvert$, find the locus representing $w$ |
| D44 | Given a fractional linear expression in $z$ with fixed $\lvert z\rvert$, find the locus representing $w$ |
| D45 | For a parameterized quadratic equation, count parameter values for which the roots have equal modulus |
| D46 | For a parameterized quadratic equation, count parameter values for which the sum of the root moduli equals a given value |
| D47 | For a parameterized quadratic equation, count parameter values for which a root with a given modulus exists |
| D48 | For a quadratic equation with two parameters, count parameter pairs satisfying a condition on the roots |
| D49 | Given two conjugate complex roots, write the quadratic equation having those roots |
| D50 | Given that the point representing $z$ lies on a line segment, find the extrema of a modulus |
| D51 | Given that $z$ lies on a circle, maximize a difference of squared distances |
| D52 | Given a condition involving $\lvert z^2-C\rvert$ and $\lvert z\rvert$, find the extrema of $\lvert z\rvert$ |
| D53 | Given two complex numbers with fixed moduli, minimize a modulus expression and derive the requested quantity |
| D54 | Given three complex numbers satisfying a relation, compute the area of their representing triangle |
