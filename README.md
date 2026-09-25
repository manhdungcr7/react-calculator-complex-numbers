# ReAct-Calculator for Multiple-Choice Complex Number Problems

This repository accompanies the paper **"Improving Small Language Model
Performance on High-School Mathematics Using ReAct: A Case Study on Complex
Numbers,"** submitted to SoICT 2026.

The study investigates whether a small language model (SLM) can answer every
multiple-choice problem correctly within a defined set of high-school Complex
Numbers problem types. The proposed method combines problem-type-specific
solution guidance with ReAct and an external Calculator. The model decides how
to solve the problem and which computation is needed, while the Calculator
evaluates the mathematical expression and returns the result to the model.

## Main results

- The evaluation set contains **4,860 questions across 54 problem types**, generated
  from 65 questions in a real high-school review document.
- On the full evaluation set, Qwen3-4B achieved **85.7%** accuracy and
  Gemini-2.5-Flash achieved **98.5%** accuracy.
- Adding a solution guide increased Qwen3-4B accuracy from **28.9% to 82.1%**
  on 810 questions from the nine most difficult types, but did not reach 100%.
- ReAct-Calculator enabled Qwen3-4B to answer all **2,160 questions across the
  24 remaining difficult types correctly**.
- Reusing the same prompt and procedure increased Llama-3.2-3B-Instruct
  accuracy from **20.7% to 53.5%**, while DeepSeek-R1-Distill-Qwen-1.5B
  changed from **40.3% to 38.9%**.

## Repository structure

| Directory | Contents |
|---|---|
| [`appendix/`](appendix/) | The 54 Complex Numbers problem-type codes and names used in the paper |
| [`data/`](data/) | Questions and per-question model outputs used to verify the reported results |
| [`scripts/`](scripts/) | PDF-to-Markdown conversion and question-generation scripts |
| [`experiments/`](experiments/) | Kaggle notebooks for the baseline and ReAct-Calculator experiments |

Each directory contains a README with additional details.

## Research workflow

1. **Build the evaluation dataset.** Extract Complex Numbers questions from a
   real review document, group them into problem types, and generate variants
   by changing numerical values while preserving the question structure and
   solution method.
2. **Evaluate the baseline.** Ask the models to solve the questions directly,
   without problem-type-specific guidance or tool use.
3. **Add a solution guide.** Provide Qwen3-4B with the solution method for each
   selected problem type while leaving all computations to the model.
4. **Apply ReAct-Calculator.** Let Qwen3-4B alternate between reasoning,
   Calculator calls, and Calculator results until it produces a final answer.
5. **Test prompt and procedure reuse.** Apply the same ReAct-Calculator prompt
   and procedure to Llama-3.2-3B-Instruct and
   DeepSeek-R1-Distill-Qwen-1.5B.

## Data and reproducibility

The generated questions and detailed model outputs are available under
[`data/`](data/). The original review PDF is not distributed in this
repository. Scripts that process the source document and generate question
variants are under [`scripts/`](scripts/), while the experiment notebooks are
under [`experiments/`](experiments/).

Some scripts require source files, API credentials, or Kaggle datasets that
must be supplied by the user. See the README in each directory for the expected
inputs and paths.

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
