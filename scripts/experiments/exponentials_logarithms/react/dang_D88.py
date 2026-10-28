# -*- coding: utf-8 -*-
"""Problem type D88: count the integers x with [log_b(x^2+1) - log_b(x+D)] * (N - c^(x-1)) >= 0.

Method of the source solution (p227 q40): domain x > -D; the product is >= 0 when both factors are >= 0
or both are <= 0; the first factor has the sign of x^2 - x + 1 - D and the second is >= 0 iff x <= x0.
"""
import re

import framework as fw

MA_DANG = "D88"
TITLE_VI = "đếm số nguyên $x$ thỏa $[\\log_b(x^2+1)-\\log_b(x+D)](N-c^{x-1})\\ge0$"
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $\big[\log_b(x^2+1)-\log_b(x+D)\big]\,(N-c^{x-1})\ge0$ with $N=c^k$ for a positive integer $k$, and asks how many integers $x$ satisfy it.

**Domain.** The logarithm of $x+D$ needs $x+D>0$, so $x>-D$ ($x^2+1$ is always positive).

**A product is $\ge0$ when both factors are $\ge0$ or both are $\le0$.**

**The first factor.** The base $b$ is larger than 1, so $\log_b(x^2+1)-\log_b(x+D)$ has the sign of $(x^2+1)-(x+D)$, that is of $x^2-x+1-D$. This quadratic has two roots $r_1<r_2$ with $r_1+r_2=1$. The first factor is $\ge0$ when $x\le r_1$ or $x\ge r_2$, and $\le0$ when $r_1\le x\le r_2$.

**The second factor.** $N-c^{x-1}\ge0\iff c^{x-1}\le c^k\iff x-1\le k$ (the base $c>1$), so it is $\ge0$ exactly when $x\le x_0$ with $x_0=k+1$, and $\le0$ when $x\ge x_0$.

**How the two fit.** For the problems of this type the zero of the second factor is also the larger root of the first quadratic: $x_0^2-x_0+1-D=0$, that is $r_2=x_0$, so $r_1=1-x_0$. (In the original problem $D=21$, $x_0=5$, the roots are $5$ and $-4$.)

**Combining.**
- Both factors $\ge0$: ($x\le r_1$ or $x\ge x_0$) and $x\le x_0$, which gives $x\le r_1$ or $x=x_0$.
- Both factors $\le0$: $r_1\le x\le x_0$ and $x\ge x_0$, which gives $x=x_0$.
With the domain $x>-D$ the solution set is $-D<x\le 1-x_0$ or $x=x_0$.

**Counting the integers.** The integers $-D+1,\dots,1-x_0$ number $(1-x_0)-(-D+1)+1=D-x_0+1$, and $x=x_0$ adds one more, so the total is $D-x_0+2$. This is compared with the four options.

**Finding $k$.** The number $k$ with $N=c^k$ is $\log_c N$; the Calculator gives it as a decimal, so we round it to the nearest integer with `floor(value + 1/2)`.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu số nguyên $x$ thỏa mãn $\\left[\\log_{5}(x^2+1)-\\log_{5}(x+43)\\right]\\left(15625-5^{x-1}\\right)\\ge 0$?\n"
    "\n"
    "A. $37$.\n"
    "B. $38$.\n"
    "C. $39$.\n"
    "D. $40$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_THOUGHTS = [
    "I read the problem. The domain bound is $D=43$ (from $x+43$), the number in the second factor is $N=15625$ and its base is $c=5$. The exponent $k$ with $5^k=15625$ is $\\log(15625)/\\log(5)$; I take 20 digits and round to the nearest integer with floor(value + 1/2). I store it as `power_k`.",
    "The second factor is non negative for $x\\le k+1$. I store $x_0=k+1$ as `x_zero`.",
    "For this type $x_0$ must also be the larger root of $x^2-x+1-D=0$. I ask the Calculator whether $x_0^2-x_0+1-D$ equals 0.",
    "The integers are $-D+1,\\dots,1-x_0$ plus the single value $x_0$, in total $D-x_0+2$.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    d = int(re.search(r"\\log_\{?\d+\}?\(x\+(\d+)\)", stem).group(1))
    n, c = map(int, re.search(r"\((\d+)-(\d+)\^\{x-1\}(?:\\right)?\)", stem).groups())
    return d, n, c


def program(question_text):
    d, n, c = _parse(question_text)
    return [
        f"power_k = floor(N(log({n})/log({c}), 20) + 1/2)",
        "x_zero = power_k + 1",
        f"coincidence_check = Eq(x_zero**2 - x_zero + 1 - {d}, 0)",
        f"answer = {d} - x_zero + 2",
    ]


def brute_force(question_text):
    """Independent of the method: test the ORIGINAL inequality (exactly, through the signs) for every integer."""
    d, n, c = _parse(question_text)
    count = 0
    for x in range(-d + 1, 200):
        s1 = (x * x + 1) - (x + d)                      # sign of the logarithm difference (base > 1)
        s2 = n - c ** (x - 1) if x - 1 >= 0 else n - 1 / c ** (1 - x)
        if ((s1 > 0) - (s1 < 0)) * ((s2 > 0) - (s2 < 0)) >= 0:
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the number $D$ in $\\log_b(x+D)$; the number $N$ in the second factor $N-c^{x-1}$; and its base $c$.",
    "Store `power_k = floor(N(log(<N>)/log(<c>), 20) + 1/2)`, writing $N$ and $c$ from the problem.",
    "Store `x_zero = power_k + 1`.",
    "Store `coincidence_check = Eq(x_zero**2 - x_zero + 1 - <D>, 0)`. It must be `True`.",
    "Store `answer = <D> - x_zero + 2`.",
])
