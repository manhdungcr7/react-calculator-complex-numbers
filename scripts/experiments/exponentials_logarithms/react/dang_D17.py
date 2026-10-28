# -*- coding: utf-8 -*-
"""Problem type D17: minimum of P = A*log^2_{a/b}(a) + B*log_b(a/b) for a > b > 1.

Method of the source solution (p021 q21): t = log_{a/b} b > 0; log_{a/b} a = 1 + t and log_b(a/b) = 1/t, so
P = A(1+t)^2 + B/t; the derivative vanishes at the root of 2A t^2 (1+t) = B; evaluate P there.
"""
import re

import framework as fw

MA_DANG = "D17"
TITLE_VI = "giá trị nhỏ nhất của $P=A\\log^2_{a/b}a+B\\log_b\\frac ab$ với $a>b>1$"
OPTION_VARIABLES = True
FREE_UNKNOWNS = {"t"}

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: real numbers $a>b>1$, and $P=c_1\log^2_{\frac ab}(a^{k})+c_2\log_b\dfrac ab$ with $k=1$ or $k=2$ (the original problem has $\log^2_{\frac ab}(a^2)$) and numbers $c_1,c_2$ (a coefficient not written is 1). We want the minimum of $P$.

**Reducing to one variable.** Let $t=\log_{\frac ab}b$. Since $a>b>1$, we have $\frac ab>1$ and $b>1$, so $t>0$.
- $\log_{\frac ab}a=\log_{\frac ab}\left(\dfrac ab\cdot b\right)=1+\log_{\frac ab}b=1+t$. Hence $\log_{\frac ab}(a^k)=k(1+t)$ and $\log^2_{\frac ab}(a^k)=k^2(1+t)^2$.
- $\log_b\dfrac ab=\dfrac{1}{\log_{\frac ab}b}=\dfrac1t$.
So with $A=c_1k^2$ and $B=c_2$:
$$P=f(t)=A(1+t)^2+\frac{B}{t},\qquad t>0.$$
(In the original problem $A=4$, $B=3$, and $P=4(1+t)^2+\dfrac3t$.)

**The minimum.** The derivative is $f'(t)=2A(1+t)-\dfrac{B}{t^2}=\dfrac{2A\,t^3+2A\,t^2-B}{t^2}$. It vanishes where $2At^3+2At^2-B=0$. The cubic $2At^3+2At^2-B$ is increasing for $t>0$, so it has exactly one positive root $t^*$; $f'$ is negative before it and positive after it, so $f$ has its minimum at $t^*$. For the problems of this type $t^*$ is a rational number. (Original problem: $8t^3+8t^2-3=(2t-1)(4t^2+6t+3)$, so $t^*=\frac12$ and $f\left(\frac12\right)=15$.)

**Conclusion.** The Calculator lists the real roots of the cubic exactly (`real_roots(polynomial)`; for this type the list has a single entry), and we evaluate $f$ at that root.

**From the method to the Calculator.** `coef_first` is $A=c_1k^2$ (the Calculator does the multiplication $c_1\cdot k^2$) and `coef_second` is $B=c_2$; these two names are then used inside the later commands. `t_roots` lists the real roots of $2At^3+2At^2-B$; `t_star` is its only entry; `answer` is $f(t^*)=A(1+t^*)^2+\dfrac B{t^*}$. The value is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Xét các số thực $a, b$ thỏa mãn $a>b>1$. Tìm giá trị nhỏ nhất $P_{\\min}$ của biểu thức $P = 2\\log^2_{\\frac{a}{b}}a + 144\\log_b\\left(\\dfrac{a}{b}\\right)$.\n"
    "\n"
    "A. $P_{\\min}=78$.\n"
    "B. $P_{\\min}=80$.\n"
    "C. $P_{\\min}=82$.\n"
    "D. $P_{\\min}=160$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_READING = (
    "Reading the problem before any computation. The expression is $P=2\\log^2_{\\frac ab}a+144\\log_b\\left(\\frac ab\\right)$. "
    "The coefficient of the first term is two, so $c_1=2$, and its argument is $a$ (not $a^2$), so $k=1$. "
    "The coefficient of the second term is one hundred forty four, written 1, 4, 4, so $c_2=144$. I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "The coefficient $A$ of $(1+t)^2$ is $c_1k^2$, with $c_1=2$ and $k=1$. I let the Calculator do the product $c_1\\cdot k^2$ and keep the result under the name `coef_first`, which I will use in the later commands. I send `coef_first = 2*1**2`.",
    "The coefficient $B$ of $\\frac1t$ is $c_2=144$. I keep it under the name `coef_second`. I send `coef_second = 144`.",
    "The minimum is where the derivative vanishes, that is where $2At^3+2At^2-B=0$. I write it with the two stored names, `coef_first` for $A$ and `coef_second` for $B$, and ask for the real roots exactly, with `t` as the unknown. I send `t_roots = real_roots(2*coef_first*t**3 + 2*coef_first*t**2 - coef_second)`.",
    "The Calculator returned a list with one entry, the positive root $t^*$, which is what the method predicts. I take its first element. I send `t_star = t_roots[0]`.",
    "The minimum value is $f(t^*)=A(1+t^*)^2+\\dfrac{B}{t^*}$, with `coef_first` for $A$, `coef_second` for $B$ and `t_star` for $t^*$. I send `answer = coef_first*(1 + t_star)**2 + coef_second/t_star`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"P\s*=\s*(\d*)\\log\^2_\{\\frac\{a\}\{b\}\}\s*\(?a(\^2)?\)?\s*\+\s*(\d*)\\log_b", stem)
    c1 = int(m.group(1) or 1)
    k = 2 if m.group(2) else 1
    c2 = int(m.group(3) or 1)
    return c1, k, c2


def program(question_text):
    c1, k, c2 = _parse(question_text)
    return [
        f"coef_first = {c1}*{k}**2",
        f"coef_second = {c2}",
        "t_roots = real_roots(2*coef_first*t**3 + 2*coef_first*t**2 - coef_second)",
        "t_star = t_roots[0]",
        "answer = coef_first*(1 + t_star)**2 + coef_second/t_star",
    ]


def brute_force(question_text):
    """Independent of the method: pick b = 2, a = 2^(1+1/t)... and minimise the ORIGINAL expression numerically."""
    import math

    from scipy.optimize import minimize_scalar
    c1, k, c2 = _parse(question_text)
    a_coef, b_coef = c1 * k * k, c2

    def p_of(s):
        t = math.exp(s)                    # t = log_{a/b} b
        # take b = e (natural), then a/b = e^(1/t), so a = e^(1 + 1/t)
        ln_b = 1.0
        ln_a = 1.0 + 1.0 / t
        ln_ab = ln_a - ln_b
        log_ab_a = ln_a / ln_ab            # log_{a/b} a
        log_b_ab = ln_ab / ln_b            # log_b (a/b)
        return a_coef * log_ab_a ** 2 + b_coef * log_b_ab

    res = minimize_scalar(p_of, bounds=(-6, 6), method="bounded", options={"xatol": 1e-12})
    return res.fun


BRUTE_TOLERANCE = 1e-6

PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the coefficient $c_1$ of the first term $c_1\\log^2_{\\frac ab}(\\cdot)$ and whether its argument is $a$ (then $k=1$) or $a^2$ (then $k=2$); the coefficient $c_2$ of the second term $c_2\\log_b\\left(\\frac ab\\right)$. A coefficient that is not written is 1.",
    "Store `coef_first = <c1>*<k>**2` and `coef_second = <c2>`, writing the numbers from the previous step. These are the two names used in the commands below: `coef_first` is $A=c_1k^2$ and `coef_second` is $B=c_2$.",
    "Store `t_roots = real_roots(2*coef_first*t**3 + 2*coef_first*t**2 - coef_second)`. The letter `t` needs no earlier assignment; `coef_first` and `coef_second` are the stored names, not letters to be filled in.",
    "Store `t_star = t_roots[0]`.",
    "Store `answer = coef_first*(1 + t_star)**2 + coef_second/t_star`.",
], option_variables=True)
