# -*- coding: utf-8 -*-
"""Problem type D56: count the integers x with log_p((x^2-A)/q^m) < log_q((x^2-A)/p^m)  (q > p).

Method of the source solution (p128 q39): split the logarithms of the quotients, collect the terms with
log(x^2-A) on one side, change to one base, obtain  0 < x^2 - A < (pq)^m  and count the integers.
"""
import re

import framework as fw

MA_DANG = "D56"
TITLE_VI = "đếm số nguyên $x$ thỏa $\\log_p\\frac{x^2-A}{q^m}<\\log_q\\frac{x^2-A}{p^m}$"
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $\log_p\dfrac{x^2-A}{B}<\log_q\dfrac{x^2-A}{C}$ with $B=q^m$, $C=p^m$ and $q>p>1$, and asks how many integers $x$ satisfy it.

**Domain.** Both arguments are positive exactly when $u=x^2-A>0$.

**Splitting the quotients.** Put $u=x^2-A>0$. Then
$$\log_p u-\log_p B<\log_q u-\log_q C,\qquad \log_p B=m\log_p q,\quad \log_q C=m\log_q p.$$
Let $s=\log_p q$; since $q>p>1$ we have $s>1$, and $\log_q p=\dfrac1s$, $\log_q u=\dfrac{\log_p u}{s}$. The inequality becomes
$$\log_p u-ms<\frac{\log_p u}{s}-\frac ms\iff\log_p u\left(1-\frac1s\right)<m\left(s-\frac1s\right).$$

**Collecting the terms in $\log_p u$.** Since $1-\frac1s=\frac{s-1}{s}>0$ and $s-\frac1s=\frac{(s-1)(s+1)}{s}$, dividing by the positive number $\frac{s-1}{s}$ gives
$$\log_p u<m(s+1)=m\log_p q+m=\log_p\big(q^mp^m\big)=\log_p\big((pq)^m\big).$$
The logarithm to the base $p>1$ is increasing, so $u<(pq)^m=q^m\cdot p^m=B\cdot C$.

**The integers.** Together with the domain, $0<x^2-A<B\cdot C$, that is $A<x^2<A+B\cdot C$, that is $\sqrt A<|x|<\sqrt{A+BC}$. The values $x$ and $-x$ both work, so we count the positive integers $n$ with $\sqrt A<n<\sqrt{A+BC}$ and double the count. The largest such $n$ is $\lceil\sqrt{A+BC}\rceil-1$ (the ceiling takes care of the strict inequality even if $\sqrt{A+BC}$ is an integer), and the smallest is $\lfloor\sqrt A\rfloor+1$ (again strict). So the number of positive integers is $\big(\lceil\sqrt{A+BC}\rceil-1\big)-\lfloor\sqrt A\rfloor$, and the answer is twice that. It is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu số nguyên $x$ thỏa mãn $\\log_{3}\\dfrac{x^2-25}{1024} < \\log_{4}\\dfrac{x^2-25}{243}$?\n"
    "\n"
    "A. $985$.\n"
    "B. $986$.\n"
    "C. $984$.\n"
    "D. $493$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_THOUGHTS = [
    "I read the problem. The constant under $x^2$ is $A=25$. The two denominators are $B=1024$ (under the first logarithm) and $C=243$ (under the second). The method says $x^2-A<B\\cdot C$, so I multiply the two denominators and store the product as `limit_value`.",
    "The positive integers $n$ with $n^2<A+BC$ are $1,\\dots,\\lceil\\sqrt{A+BC}\\rceil-1$ (the ceiling handles the strict inequality). I store the largest one as `n_high`.",
    "The positive integers $n$ with $n^2\\le A$ are those up to $\\lfloor\\sqrt A\\rfloor$, and they must be excluded because $n^2>A$ is required. I store this number as `n_low`.",
    "The positive integers $n$ with $\\sqrt A<n<\\sqrt{A+BC}$ number `n_high - n_low`, and each gives the two values $\\pm n$, so the answer is twice that.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"\\log_\{?(\d+)\}?\\dfrac\{x\^2-(\d+)\}\{(\d+)\}\s*<\s*\\log_\{?(\d+)\}?\\dfrac\{x\^2-\d+\}\{(\d+)\}", stem)
    p, a, b, q, c = map(int, m.groups())
    return p, a, b, q, c


def program(question_text):
    _, a, b, _, c = _parse(question_text)
    return [
        f"limit_value = {b}*{c}",
        f"n_high = ceiling(sqrt({a} + limit_value)) - 1",
        f"n_low = floor(sqrt({a}))",
        "answer = 2*(n_high - n_low)",
    ]


def brute_force(question_text):
    """Independent of the method: test the ORIGINAL inequality for every integer x in a safe range."""
    import math

    import mpmath as mp
    mp.mp.dps = 60
    p, a, b, q, c = _parse(question_text)
    top = math.isqrt(a + b * c) + 3
    count = 0
    for x in range(-top, top + 1):
        u = x * x - a
        if u <= 0:
            continue
        if mp.log(mp.mpf(u) / b, p) < mp.log(mp.mpf(u) / c, q):
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the number $A$ in $x^2-A$ (the same in both logarithms), the denominator $B$ under the first logarithm and the denominator $C$ under the second logarithm.",
    "Store `limit_value = <B>*<C>`, writing the two denominators from the problem.",
    "Store `n_high = ceiling(sqrt(<A> + limit_value)) - 1`.",
    "Store `n_low = floor(sqrt(<A>))`.",
    "Store `answer = 2*(n_high - n_low)`.",
])
