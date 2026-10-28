# -*- coding: utf-8 -*-
"""Problem type D57: count the integer pairs (x; y), x > 0, with
log_2(x^2+y^2+x) + log_4(x^2+y^2) <= log_2 x + log_4(x^2+y^2+Kx).

Method of the source solution (p133 q47, which has the bases 3 and 2): put t = (x^2+y^2)/x, reduce the
inequality to t <= t0, so that (x - t0/2)^2 + y^2 <= (t0/2)^2, then count the lattice points of that disc
x by x.  For the bases 2 and 4 of the generated variants the reduction is t^3 + 2t^2 <= K; the source
question itself uses other bases, so it is not replayed.
"""
import re

import framework as fw

MA_DANG = "D57"
TITLE_VI = "đếm số cặp nguyên $(x;y)$, $x>0$, thỏa $\\log_2(x^2+y^2+x)+\\log_4(x^2+y^2)\\le\\log_2x+\\log_4(x^2+y^2+Kx)$"
OPTION_VARIABLES = True
FREE_UNKNOWNS = {"t"}
SOURCE_REPLAY = False

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem asks for the number of integer pairs $(x;y)$ with $x>0$ satisfying
$$\log_2(x^2+y^2+x)+\log_4(x^2+y^2)\le\log_2x+\log_4(x^2+y^2+Kx),$$
where $K$ is a given positive integer.

**Domain.** With $x>0$ every argument is positive, since $x^2+y^2>0$.

**One variable for the whole inequality.** Write $S=x^2+y^2$ and use $\log_4u=\tfrac12\log_2u$. Collecting the logarithms of the same side,
$$\log_2\frac{S+x}{x}\le\tfrac12\log_2\frac{S+Kx}{S}.$$
Put $t=\dfrac{S}{x}=\dfrac{x^2+y^2}{x}>0$. Then $\dfrac{S+x}{x}=t+1$ and $\dfrac{S+Kx}{S}=1+\dfrac Kt$, so the inequality is $2\log_2(t+1)\le\log_2\left(1+\dfrac Kt\right)$.

**Removing the logarithms.** The logarithm to the base 2 is increasing and both arguments are positive, so the inequality is equivalent to $(t+1)^2\le1+\dfrac Kt$. Multiplying by $t>0$: $t(t+1)^2\le t+K$, that is
$$t^3+2t^2\le K.$$
For $t>0$ the function $t^3+2t^2$ is strictly increasing, so the inequality holds exactly when $t\le t_0$, where $t_0$ is the unique positive root of $t^3+2t^2=K$. For every problem of this type $t_0$ is a positive integer.

**A disc.** Going back, $t\le t_0$ means $x^2+y^2\le t_0x$, that is $\left(x-\tfrac{t_0}{2}\right)^2+y^2\le\left(\tfrac{t_0}{2}\right)^2$: the lattice points in a disc whose horizontal extent is $0<x\le t_0$ (the boundary is included).

**Counting the points $x$ by $x$.** For a fixed integer $x$ with $1\le x\le t_0$ the condition is $y^2\le t_0x-x^2$, that is $|y|\le\sqrt{t_0x-x^2}$. The integers $y$ with $|y|\le\sqrt{t_0x-x^2}$ number $2\left\lfloor\sqrt{t_0x-x^2}\right\rfloor+1$ (the $y$ from $-\lfloor\cdot\rfloor$ to $\lfloor\cdot\rfloor$). The total number of pairs is the sum of these counts over $x=1,2,\dots,t_0$.

**Two Calculator tools for this.** `real_roots(polynomial)` lists the real roots of a polynomial exactly (here a list with the single integer $t_0$). A sum of a formula over consecutive integers is written `Sum(term, (k, first, last)).doit()`: the Calculator adds the terms exactly, with $k$ running from `first` to `last`.

**A built-in check on the number $K$.** For every problem of this type $K=t_0^3+2t_0^2$ for an integer $t_0$, so the Calculator must return a list holding one plain integer. If it returns anything else (for example a `CRootOf(...)` expression or a decimal), the number $K$ was copied wrongly: read $K$ again from the problem, digit by digit, and send the call again with the correct $K$. Do not try to repair a non integer root by rounding.

**From the method to the Calculator.** `t_roots` lists the real roots of $t^3+2t^2-K$; `t_top` is $t_0$ (its only entry); `answer` is $\sum_{x=1}^{t_0}\left(2\lfloor\sqrt{t_0x-x^2}\rfloor+1\right)$, with the summation letter `k` in place of $x$. The total is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu cặp số nguyên $(x;y)$ thỏa mãn $x>0$ và\n"
    "$\\log_2(x^2+y^2+x)+\\log_4(x^2+y^2)\\le\\log_2 x+\\log_4(x^2+y^2+23520x)$?\n"
    "\n"
    "A. $610$.\n"
    "B. $613$.\n"
    "C. $612$.\n"
    "D. $611$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_READING = (
    "Reading the problem before any computation. The inequality is "
    "$\\log_2(x^2+y^2+x)+\\log_4(x^2+y^2)\\le\\log_2x+\\log_4(x^2+y^2+23520x)$ with $x>0$. "
    "The number multiplying $x$ in the last logarithm is twenty three thousand five hundred twenty, written 2, 3, 5, 2, 0, so $K=23520$. "
    "I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "The inequality reduces to $t^3+2t^2\\le K$ with $t=\\dfrac{x^2+y^2}{x}$, and $t_0$ is the positive root of $t^3+2t^2=K$. I ask the Calculator for the real roots of $t^3+2t^2-K$ exactly, with $K=23520$ copied digit by digit: 2, 3, 5, 2, 0. I send `t_roots = real_roots(t**3 + 2*t**2 - 23520)`.",
    "The list holds one plain integer, 28, which is what the method predicts for a correct $K$. If it had shown a `CRootOf` expression or a decimal, $K$ would have been copied wrongly, and I would read it again digit by digit. The single entry is $t_0$. I send `t_top = t_roots[0]`.",
    "For each integer $x$ from 1 to $t_0$ the number of integers $y$ is $2\\lfloor\\sqrt{t_0x-x^2}\\rfloor+1$. I add these counts over $x$ from 1 to `t_top` with a Sum, using the letter `k` for $x$ and ending with doit() so that the Calculator adds the terms. I send `answer = Sum(2*floor(sqrt(t_top*k - k**2)) + 1, (k, 1, t_top)).doit()`.",
]


def _parse(question_text):
    return int(re.search(r"\+(\d+)x\)", question_text).group(1))


def program(question_text):
    k = _parse(question_text)
    return [
        f"t_roots = real_roots(t**3 + 2*t**2 - {k})",
        "t_top = t_roots[0]",
        "answer = Sum(2*floor(sqrt(t_top*k - k**2)) + 1, (k, 1, t_top)).doit()",
    ]


def brute_force(question_text):
    """Independent of the method: test the original logarithmic inequality on every lattice point of a box."""
    import mpmath as mp
    mp.mp.dps = 60
    K = _parse(question_text)
    t0 = 1
    while t0 ** 3 + 2 * t0 ** 2 < K:
        t0 += 1
    count = 0
    for x in range(1, 2 * t0 + 3):
        for y in range(-2 * t0 - 3, 2 * t0 + 4):
            s = x * x + y * y
            lhs = mp.log(s + x, 2) + mp.log(s, 4)
            rhs = mp.log(x, 2) + mp.log(s + K * x, 4)
            if lhs <= rhs + mp.mpf(10) ** -40:
                count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the number $K$ that multiplies $x$ in the last logarithm $\\log_4(x^2+y^2+Kx)$.",
    "Store `t_roots = real_roots(t**3 + 2*t**2 - <K>)`, writing the number $K$ from the problem. This lists the real roots of $t^3+2t^2-K$.",
    "Look at the Observation of the previous call: it must be a list with one plain integer. If it is anything else (for example `CRootOf(...)` or a decimal), $K$ was copied wrongly: read $K$ again digit by digit from the problem and repeat the previous call with the correct $K$. Then store `t_top = t_roots[0]`.",
    "Store `answer = Sum(2*floor(sqrt(t_top*k - k**2)) + 1, (k, 1, t_top)).doit()`.",
], option_variables=True)
