# -*- coding: utf-8 -*-
"""Problem type D10: values of m for which y = ln(x^2 + c) - m x + 1 is increasing on the whole real line.

Method of the source solution (p018 q09): y' = 2x/(x^2+c) - m >= 0 for all x, so m <= min g with
g(x) = 2x/(x^2+c); g' = 0 at x = +-sqrt(c); the minimum is at x = -sqrt(c).  The set of m is stored as an
interval and each option, written as a Calculator interval, is compared with it (ends and brackets).
"""
import re

import framework as fw

MA_DANG = "D10"
TITLE_VI = "tìm $m$ để $y=\\ln(x^2+c)-mx+1$ đồng biến trên $\\mathbb R$"
OPTION_VARIABLES = True
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $y=\ln(x^2+c)-mx+1$ with a positive constant $c$ and asks for the set of all $m$ for which $y$ is increasing on $(-\infty;+\infty)$.

**Step 1: the derivative.** $y'=\dfrac{2x}{x^2+c}-m$ (the derivative of $\ln(x^2+c)$ is $\dfrac{2x}{x^2+c}$, that of $-mx$ is $-m$, that of $1$ is $0$).

**Step 2: the condition "increasing on the whole line".** A differentiable function is increasing on $(-\infty;+\infty)$ exactly when $y'\ge0$ for every real $x$ (it may be zero at isolated points). So we need
$$g(x)=\frac{2x}{x^2+c}\ge m\ \text{ for all real }x\iff m\le\min_{\mathbb R}g(x).$$

**Step 3: the minimum of $g$.** By the quotient rule $g'(x)=\dfrac{2(x^2+c)-2x\cdot2x}{(x^2+c)^2}=\dfrac{2(c-x^2)}{(x^2+c)^2}$. It is zero at $x=\pm\sqrt c$, negative for $x<-\sqrt c$, positive for $-\sqrt c<x<\sqrt c$, negative for $x>\sqrt c$. So $g$ decreases, increases, then decreases again, and $g(x)\to0$ when $x\to\pm\infty$. The two critical values are $g(\sqrt c)=\dfrac{2\sqrt c}{2c}=\dfrac1{\sqrt c}>0$ and $g(-\sqrt c)=-\dfrac1{\sqrt c}<0$. The local minimum $-\dfrac1{\sqrt c}$ is below the limit $0$ at infinity, so it is the minimum of $g$ on the whole line:
$$\min_{\mathbb R}g=g(-\sqrt c)=-\frac{1}{\sqrt c}.$$
(Original problem: $c=1$, minimum $-1$.)

**Step 4: the set of $m$.** $m\le-\dfrac1{\sqrt c}$. The set is $\left(-\infty;-\dfrac1{\sqrt c}\right]$: the left end is $-\infty$ with a round bracket, and the right end is $-\dfrac1{\sqrt c}$ with a **square** bracket (when $m$ equals the minimum, $y'$ is zero at the single point $x=-\sqrt c$ and $y$ is still increasing).

**From the method to the Calculator.** `critical_point` is $x=-\sqrt c$. `min_value` is $g(-\sqrt c)=\dfrac{2x}{x^2+c}$ evaluated at that point. `answer` is the interval `Interval.Lopen(-oo, min_value)` (round on the left, square on the right). Each option, written as a Calculator interval according to its own brackets, is compared with `answer` by `Eq`, which is `True` only if the ends and the brackets are all the same.
'''

EXAMPLE_QUESTION = (
    "Tìm tập hợp tất cả các giá trị của tham số thực $m$ để hàm số $y = \\ln(x^2+4900) - mx + 1$ đồng biến trên khoảng $(-\\infty; +\\infty)$.\n"
    "\n"
    "A. $\\left[\\dfrac{1}{70};+\\infty\\right)$.\n"
    "B. $\\left(-\\infty;- \\dfrac{1}{70}\\right)$.\n"
    "C. $\\left[- \\dfrac{1}{70};\\dfrac{1}{70}\\right]$.\n"
    "D. $\\left(-\\infty;- \\dfrac{1}{70}\\right]$."
)
EXAMPLE_ANSWER = "D"

EXAMPLE_READING = (
    "Reading the problem before any computation. The function is $y=\\ln(x^2+4900)-mx+1$ and it must be increasing on the whole line. "
    "The constant added to $x^2$ inside the logarithm is four thousand nine hundred, written 4, 9, 0, 0, so $c=4900$. "
    "I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "The minimum of $g(x)=\\dfrac{2x}{x^2+c}$ is reached at $x=-\\sqrt c$, with $c=4900$. I want the exact value of the square root, so I send `critical_point = -sqrt(4900)`.",
    "The critical point is stored. Now the value of $g$ there: $g=\\dfrac{2x}{x^2+c}$ with $x$ replaced by the stored `critical_point` and $c=4900$. This number is the right end of the set of $m$. I send `min_value = 2*critical_point/(critical_point**2 + 4900)`.",
    "The right end is stored. The set of $m$ starts at $-\\infty$ with a round bracket and ends at `min_value` with a square bracket, which is `Interval.Lopen` in Calculator syntax. I send `answer = Interval.Lopen(-oo, min_value)`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    return int(re.search(r"\\ln\(x\^2\s*\+\s*(\d+)\)", stem).group(1))


def program(question_text):
    c = _parse(question_text)
    return [
        f"critical_point = -sqrt({c})",
        f"min_value = 2*critical_point/(critical_point**2 + {c})",
        "answer = Interval.Lopen(-oo, min_value)",
    ]


def option_expressions(question_text):
    return {letter: fw.interval_constructor(body) for letter, body in fw.parse_options(question_text).items()}


def example_check(calc, question_text):
    """Independent of the method: minimise g(x) = 2x/(x^2+c) numerically."""
    import numpy as np
    c = _parse(question_text)
    xs = np.linspace(-20 * c ** 0.5, 20 * c ** 0.5, 4000001)
    g = 2 * xs / (xs ** 2 + c)
    assert abs(float(calc.ns["min_value"]) - g.min()) < 1e-8


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the constant $c$ in $\\ln(x^2+c)$.",
    "Store `critical_point = -sqrt(<c>)`.",
    "Store `min_value = 2*critical_point/(critical_point**2 + <c>)`.",
    "Store `answer = Interval.Lopen(-oo, min_value)`: the set of $m$ starts at $-\\infty$ (round bracket) and ends at `min_value` (square bracket).",
], option_variables=True, extra_option_note=fw.INTERVAL_NOTE)
