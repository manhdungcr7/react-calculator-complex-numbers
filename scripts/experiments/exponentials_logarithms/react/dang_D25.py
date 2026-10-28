# -*- coding: utf-8 -*-
"""Problem type D25: number of integers m in [-L; L] for which log(mx) = 2 log(x + a) has exactly one solution.

Method of the source solution (p042 q45): domain x > -a, x != 0; mx = (x+a)^2, so m = f(x) = (x+a)^2/x; the
table of variation of f: unique solution iff m < 0 or m equals the minimum of f on x > 0.
"""
import re

import framework as fw

MA_DANG = "D25"
TITLE_VI = "đếm số nguyên $m\\in[-L;L]$ để $\\log(mx)=2\\log(x+a)$ có nghiệm duy nhất"
OPTION_VARIABLES = True
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $\log(mx)=2\log(x+a)$ (the common logarithm, $a$ a positive integer) and an interval $[-L;L]$, and asks how many integers $m$ of the interval make the equation have exactly one solution.

**Domain.** We need $x+a>0$ and $mx>0$. So $x>-a$, $x\ne0$, and $m$ and $x$ have the same sign.

**Separating the parameter.** For $x$ in the domain, $\log(mx)=2\log(x+a)=\log\big((x+a)^2\big)$ means $mx=(x+a)^2$, that is
$$m=f(x)=\frac{(x+a)^2}{x},\qquad x>-a,\ x\ne0.$$
(The condition $mx>0$ holds automatically, since $mx=(x+a)^2>0$.) The number of solutions equals the number of $x$ in the domain with $f(x)=m$.

**Table of variation.** $f'(x)=\dfrac{(x+a)(x-a)}{x^2}$, which vanishes on the domain only at $x=a$.
- On $(-a;0)$: $f'<0$, so $f$ decreases from $f(-a)=0$ to $-\infty$. Every $m<0$ is taken exactly once here.
- On $(0;a)$: $f$ decreases from $+\infty$ to $f(a)=4a$.
- On $(a;+\infty)$: $f$ increases from $4a$ to $+\infty$.
So for $m>4a$ there are two solutions (one on each side of $a$), for $m=4a$ exactly one ($x=a$), for $0\le m<4a$ none, and for $m<0$ exactly one.

**Step 4: the limits behind the table.** On $(-a;0)$, as $x\to-a^+$ we get $f(x)=\frac{(x+a)^2}{x}\to0$ from below, and as $x\to0^-$ the denominator tends to $0^-$ while the numerator tends to $a^2>0$, so $f\to-\infty$. On $(0;+\infty)$, $f\to+\infty$ both when $x\to0^+$ and when $x\to+\infty$, and the minimum is $f(a)=\frac{(2a)^2}{a}=4a$. The value $m=0$ is impossible, because $mx=0$ would make $\log(mx)$ undefined.

**Conclusion.** The equation has exactly one solution iff $m<0$ or $m=4a$. In the interval $[-L;L]$ the negative integers are $-1,\dots,-L$, which is $L$ values, and the value $m=4a$ is available only when $4a\le L$. So the count is $L$, plus 1 when $4a\le L$. (Original problem: $a=1$, $L=2017$, $4a=4\le2017$, count $2017+1=2018$.)

**From the method to the Calculator.** `special_m` is $4a$, the one positive value of $m$ with exactly one solution. `answer` is $L$ plus a Piecewise term that is 1 when `special_m` is not above $L$ and 0 otherwise. It is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Hỏi có bao nhiêu giá trị $m$ nguyên trong đoạn $[-90;90]$ để phương trình $\\log(mx)=2\\log(x+7)$ có nghiệm duy nhất?\n"
    "\n"
    "A. $90$.\n"
    "B. $181$.\n"
    "C. $91$.\n"
    "D. $92$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_READING = (
    "Reading the problem before any computation. The equation is $\\log(mx)=2\\log(x+7)$ and $m$ runs over the integers of $[-90;90]$. "
    "The number added to $x$ is seven, so $a=7$. The bound of the interval is ninety, written 9, 0, so $L=90$. I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "The only positive value of $m$ that gives exactly one solution is the minimum of $f(x)=\\frac{(x+a)^2}{x}$ on $x>0$, which is $4a$, with $a=7$. I send `special_m = 4*7`.",
    "Every negative integer of $[-90;90]$ gives exactly one solution, and there are $L=90$ of them. The value $m=4a$ gives one more solution-count only if it lies in the interval, that is if `special_m` is not above 90. The Piecewise returns 1 in that case and 0 otherwise, so I do not judge the comparison myself. I send `answer = 90 + Piecewise((1, special_m <= 90), (0, True))`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    big_l = int(re.search(r"\[-(\d+);(\d+)\]", stem).group(1))
    coef, a = map(int, re.search(r"\\log\(mx\)\s*=\s*(\d+)\\log\(x\+(\d+)\)", stem).groups())
    assert coef == 2, stem
    return big_l, a


def program(question_text):
    big_l, a = _parse(question_text)
    return [
        f"special_m = 4*{a}",
        f"answer = {big_l} + Piecewise((1, special_m <= {big_l}), (0, True))",
    ]


def brute_force(question_text):
    """Independent of the method: count the roots of m x = (x + a)^2 with x > -a, x != 0, for every integer m."""
    big_l, a = _parse(question_text)
    count = 0
    for m in range(-big_l, big_l + 1):
        # m x = (x+a)^2  ->  x^2 + (2a - m) x + a^2 = 0
        disc = (2 * a - m) ** 2 - 4 * a * a
        if disc < 0:
            continue
        import math
        roots = {(m - 2 * a + s * math.sqrt(disc)) / 2 for s in ((-1, 1) if disc > 0 else (0,))}
        valid = [x for x in roots if x > -a and abs(x) > 1e-12 and m * x > 0]
        if len(valid) == 1:
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the number $a$ in $\\log(x+a)$, and the number $L$ in the interval $[-L;L]$.",
    "Store `special_m = 4*<a>`.",
    "Store `answer = <L> + Piecewise((1, special_m <= <L>), (0, True))`.",
], option_variables=True)
