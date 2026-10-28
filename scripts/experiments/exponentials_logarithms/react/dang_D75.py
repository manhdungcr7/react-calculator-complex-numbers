# -*- coding: utf-8 -*-
"""Problem type D75: count the positive integers m for which
(2 log_2^2 x - 3 log_2 x - 2) * sqrt(a^x - m) = 0 has exactly two distinct solutions.

Method of the source solution (p186 q47): domain x > 0 and a^x >= m; the first factor gives x = 4 and
x = 1/sqrt(2); the second factor gives x = log_a m. The case m = 1 is treated apart (x = 0 is outside
the domain); for m > 1 there are exactly two solutions iff 1/sqrt(2) <= log_a m < 4.
"""
import re

import framework as fw

MA_DANG = "D75"
TITLE_VI = "đếm số nguyên dương $m$ để $(2\\log_2^2x-3\\log_2x-2)\\sqrt{a^x-m}=0$ có đúng hai nghiệm"
OPTION_VARIABLES = True
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $\left(2\log_2^2x-3\log_2x-2\right)\sqrt{a^x-m}=0$ with a base $a>1$ and a parameter $m$, and asks how many positive integers $m$ give exactly two distinct real solutions.

**Domain.** The logarithm needs $x>0$ and the square root needs $a^x-m\ge0$, that is $a^x\ge m$, equivalently $x\ge\log_a m$ (for $m\ge1$). A candidate solution is accepted only if it satisfies both conditions.

**The solutions.** A product is zero when one of its factors is zero.
- The first factor: put $u=\log_2x$; then $2u^2-3u-2=0$ has the roots $u=2$ and $u=-\tfrac12$, so $x_1=2^2=4$ and $x_2=2^{-1/2}=\tfrac{1}{\sqrt2}$. Each of them is a solution only if it also satisfies the domain, that is only if $a^{x_i}\ge m$.
- The second factor: $\sqrt{a^x-m}=0$ gives $a^x=m$, so $x_3=\log_a m$. It satisfies the domain with equality, but it needs $x_3>0$, that is $m>1$.

**Case $m=1$.** Then $x_3=\log_a 1=0$ is not allowed ($x>0$). The candidates $x_1=4$ and $x_2=\tfrac1{\sqrt2}$ both satisfy $a^{x_i}\ge1$, so there are exactly two solutions: $m=1$ is accepted.

**Case $m>1$.** All three candidates compete, and $x_3$ is always a solution. The solution $x_1$ is valid iff $m\le a^4$, and $x_2$ is valid iff $m\le a^{1/\sqrt2}$ (note $a^{1/\sqrt2}<a^4$).
- If $m\le a^{1/\sqrt2}$, then all of $x_1,x_2,x_3$ are valid. They are three distinct numbers, because $a^{1/\sqrt2}$ is not an integer, so $x_3\ne x_2$ (and $x_3\ne x_1$ since $m<a^4$). Three solutions are too many.
- If $a^{1/\sqrt2}<m<a^4$, then $x_2$ is not valid, while $x_1$ and $x_3$ are valid and distinct: exactly two solutions. This is the condition $\tfrac1{\sqrt2}<\log_a m<4$.
- If $m=a^4$ (possible only when $a^4$ is an integer), then $x_3=x_1$ and only one solution remains. If $m>a^4$, only $x_3$ remains.

**Counting.** The integers $m$ with $a^{1/\sqrt2}<m<a^4$ are $\lceil a^{1/\sqrt2}\rceil,\dots,\lceil a^4\rceil-1$. The ceiling of $a^4$ takes care of the strict inequality $m<a^4$: if $a^4$ is not an integer, the largest admissible $m$ is the integer part of $a^4$, which is $\lceil a^4\rceil-1$; if $a^4$ is an integer (for example $a=2$, $a^4=16$) then $m=a^4$ is excluded and the largest admissible $m$ is $a^4-1=\lceil a^4\rceil-1$ again. The smallest admissible $m$ is $\lceil a^{1/\sqrt2}\rceil$ (the number $a^{1/\sqrt2}$ is not an integer, and it is larger than 1, so this smallest value is at least 2). Their number is
$$\lceil a^4\rceil-\lceil a^{1/\sqrt2}\rceil .$$
Adding the value $m=1$ of the first case, the answer is $\lceil a^4\rceil-\lceil a^{1/\sqrt2}\rceil+1$.

**From the method to the Calculator.** `low_bound` is the decimal value of $a^{1/\sqrt2}$ (a decimal is needed because the ceiling of an irrational number must be located). `high_bound` is $a^4$, kept exact. `count_range` is $\lceil a^4\rceil-\lceil a^{1/\sqrt2}\rceil$. `answer` adds the value $m=1$. This count is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Cho phương trình $\\left(2\\log_{2}^2x-3\\log_{2}x-2\\right)\\sqrt{\\left(4\\right)^x-m}=0$ ($m$ là tham số thực). Có tất cả bao nhiêu giá trị nguyên dương của $m$ để phương trình có đúng hai nghiệm phân biệt?\n"
    "\n"
    "A. $253$.\n"
    "B. $255$.\n"
    "C. $252$.\n"
    "D. $254$."
)
EXAMPLE_ANSWER = "D"

EXAMPLE_READING = (
    "Reading the problem before any computation. The equation is $\\left(2\\log_2^2x-3\\log_2x-2\\right)\\sqrt{4^x-m}=0$ "
    "and I count the positive integers $m$ that give exactly two distinct solutions. "
    "The base of the exponential under the square root is four, written 4, so $a=4$. I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "The solution $x_2=\\frac1{\\sqrt2}$ of the first factor is valid only when $m\\le a^{1/\\sqrt2}$, so the lower limit for $m$ is $a^{1/\\sqrt2}$ with $a=4$. This number is irrational, and I need to know between which integers it lies, so I ask the Calculator for its decimal value with 20 digits. I send `low_bound = N(4**(1/sqrt(2)), 20)`.",
    "The lower limit is stored as a decimal. The solution $x_1=4$ is valid only when $m\\le a^4$, so the upper limit for $m$ is $a^4$ with $a=4$. This number is rational, and I keep it exact. I send `high_bound = 4**4`.",
    "Both limits are stored. The integers $m$ strictly between them are $\\lceil\\text{low\\_bound}\\rceil,\\dots,\\lceil\\text{high\\_bound}\\rceil-1$, and there are $\\lceil\\text{high\\_bound}\\rceil-\\lceil\\text{low\\_bound}\\rceil$ of them. The ceiling of the upper limit handles the strict inequality, also when the upper limit is an integer, as it is here. I send `count_range = ceiling(high_bound) - ceiling(low_bound)`.",
    "The value $m=1$ was treated separately: it gives exactly the two solutions $x_1$ and $x_2$, so it is one more value. I add 1 to the count. I send `answer = count_range + 1`.",
]


def _base(question_text):
    stem = question_text.split("\n")[0]
    s = re.search(r"\\sqrt\{(.*?)\^x-m\}", stem).group(1)
    s = s.replace("\\left", "").replace("\\right", "").strip()
    if s.startswith("(") and s.endswith(")"):
        s = s[1:-1]
    return fw.latex_to_calc(s)


def program(question_text):
    base = _base(question_text)
    b = f"({base})" if "/" in base else base
    return [
        f"low_bound = N({b}**(1/sqrt(2)), 20)",
        f"high_bound = {b}**4",
        "count_range = ceiling(high_bound) - ceiling(low_bound)",
        "answer = count_range + 1",
    ]


def brute_force(question_text):
    """Independent of the method: for each integer m, count the distinct valid solutions of the equation."""
    import mpmath as mp
    import sympy as sp
    mp.mp.dps = 40
    value = sp.nsimplify(sp.sympify(_base(question_text)))
    a = mp.mpf(value.p) / value.q
    count = 0
    for m in range(1, int(mp.floor(a ** 4)) + 10):
        sols = [x for x in (mp.mpf(4), 1 / mp.sqrt(2)) if a ** x >= m]
        if m > 1:
            sols.append(mp.log(m) / mp.log(a))
        distinct = []
        for s in sols:
            if all(abs(s - u) > mp.mpf(10) ** -25 for u in distinct):
                distinct.append(s)
        if len(distinct) == 2:
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the base $a$ of the exponential in $\\sqrt{a^x-m}$ (it may be a fraction such as $\\frac{111}{50}$).",
    "Store `low_bound = N(<a>**(1/sqrt(2)), 20)`, writing the base from the problem (a fraction goes in parentheses, for example `(111/50)`).",
    "Store `high_bound = <a>**4` exactly, with no N.",
    "Store `count_range = ceiling(high_bound) - ceiling(low_bound)`.",
    "Store `answer = count_range + 1`.",
], option_variables=True)
