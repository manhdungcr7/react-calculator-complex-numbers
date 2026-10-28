# -*- coding: utf-8 -*-
"""Problem type D93: count the positive integers a such that exactly three integers b satisfy
(p^b - p)(a * q^b - r) < 0.

Method of the source solution (p242 q39): split on the sign of p^b - p (b > 1 or b < 1); in each case the
second factor gives a bound on q^b, and "exactly three integers b" pins down the position of log_q(r/a).
"""
import re

import framework as fw

MA_DANG = "D93"
TITLE_VI = "đếm số nguyên dương $a$ để có đúng ba số nguyên $b$ thỏa $(p^b-p)(a\\cdot q^b-r)<0$"
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $(p^b-p)(a\cdot q^b-r)<0$ with integers $p,q\ge2$ and $r\ge1$, and asks how many positive integers $a$ have exactly three integers $b$ satisfying it.

**The product is negative when its two factors have opposite signs.** The first factor $p^b-p$ is positive exactly when $b>1$, negative when $b<1$, and zero at $b=1$ (where the product is $0$, not negative). So we split into two cases.

**Case 1: $b>1$** (so $b\ge2$). The first factor is positive, so we need $a\cdot q^b-r<0$, that is $q^b<\dfrac ra$, that is $b<L$ with $L=\log_q\dfrac ra$. The integers $b$ are $2,3,\dots$ up to just below $L$. Exactly three of them means $b\in\{2,3,4\}$, which happens when $4<L\le5$, that is
$$q^4<\frac ra\le q^5\iff\frac{r}{q^5}\le a<\frac{r}{q^4}.$$
The positive integers $a$ in this range are $\left\lceil\frac r{q^5}\right\rceil,\dots,\left\lceil\frac r{q^4}\right\rceil-1$, and their number is $\left\lceil\frac r{q^4}\right\rceil-\left\lceil\frac r{q^5}\right\rceil$.

**Case 2: $b<1$** (so $b\le0$). The first factor is negative, so we need $a\cdot q^b-r>0$, that is $q^b>\dfrac ra$, that is $b>L$ with the same $L=\log_q\dfrac ra$. The integers $b$ are the integers above $L$ up to $0$. Exactly three of them means $b\in\{-2,-1,0\}$, which happens when $-3\le L<-2$, that is
$$q^{-3}\le\frac ra<q^{-2}\iff r\,q^2<a\le r\,q^3.$$
The integers $a$ in this range number $r\,q^3-r\,q^2$.

**The two cases cannot overlap.** Case 1 needs $L>4$ and Case 2 needs $L<-2$, so no $a$ belongs to both, and for an $a$ of one case the other case contributes no $b$. The total number of values of $a$ is the sum of the two counts. It is then compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu số nguyên dương $a$ sao cho ứng với mỗi $a$ có đúng ba số nguyên $b$ thỏa mãn $(4^b-4)(a\\cdot3^b-20)<0$?\n"
    "\n"
    "A. $361$.\n"
    "B. $359$.\n"
    "C. $362$.\n"
    "D. $360$."
)
EXAMPLE_ANSWER = "D"

EXAMPLE_THOUGHTS = [
    "I read the problem. The first factor is $4^b-4$; its base does not matter beyond the sign split. In the second factor $a\\cdot3^b-20$ the base is $q=3$ and the number is $r=20$. In Case 1 the number of values of $a$ is $\\lceil r/q^4\\rceil-\\lceil r/q^5\\rceil$, with exact fractions. I store it as `case_one`.",
    "In Case 2 the number of values of $a$ is $r\\,q^3-r\\,q^2$; with $q=3$ and $r=20$ it is an exact integer. I store it as `case_two`.",
    "The two cases never overlap, so the total is the sum.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    p, q, r = map(int, re.search(r"\((\d+)\^b-\d+\)\(a\\cdot(\d+)\^b-(\d+)\)<0", stem).groups())
    return p, q, r


def program(question_text):
    _, q, r = _parse(question_text)
    return [
        f"case_one = ceiling({r}/{q}**4) - ceiling({r}/{q}**5)",
        f"case_two = {r}*{q}**3 - {r}*{q}**2",
        "answer = case_one + case_two",
    ]


def brute_force(question_text):
    """Independent of the method: for each positive a, count the integers b with the exact product negative."""
    from fractions import Fraction
    p, q, r = _parse(question_text)
    total = 0
    for a in range(1, r * q ** 3 + 50):
        n = sum(1 for b in range(-60, 61) if (Fraction(p) ** b - p) * (a * Fraction(q) ** b - r) < 0)
        if n == 3:
            total += 1
    return total


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the base $q$ and the number $r$ of the second factor $a\\cdot q^b-r$ (the first factor $p^b-p$ is not needed for the numbers).",
    "Store `case_one = ceiling(<r>/<q>**4) - ceiling(<r>/<q>**5)`, writing the numbers from the problem.",
    "Store `case_two = <r>*<q>**3 - <r>*<q>**2`.",
    "Store `answer = case_one + case_two`.",
])
