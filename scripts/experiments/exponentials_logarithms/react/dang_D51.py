# -*- coding: utf-8 -*-
"""Problem type D51: count the integers x with (4^x - B*2^(x+2) + C) * sqrt(a - log(c x)) >= 0.

Method of the source solution (p115 q39): domain 0 < x <= 10^a / c; the square root is >= 0 so the sign comes
from the first factor; with t = 2^x > 0 solve t^2 - 4B t + C >= 0 and intersect with the domain.
"""
import re

import framework as fw

MA_DANG = "D51"
TITLE_VI = "đếm số nguyên $x$ thỏa $(4^x-B\\cdot2^{x+2}+C)\\sqrt{a-\\log(cx)}\\ge0$"
FREE_UNKNOWNS = {"t"}

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $\left(4^x-B\cdot2^{x+2}+C\right)\sqrt{a-\log(cx)}\ge0$ ($\log$ is the common logarithm) and asks how many integers $x$ satisfy it.

**Domain.** The logarithm needs $cx>0$, that is $x>0$, and the square root needs $a-\log(cx)\ge0\iff\log(cx)\le a\iff cx\le10^a\iff x\le\dfrac{10^a}{c}$. So $0<x\le\dfrac{10^a}{c}$. The largest integer in the domain is $X=\left\lfloor\dfrac{10^a}{c}\right\rfloor$.

**Signs.** The square root is $\ge0$ (and it is $0$ only at the right end of the domain). In the whole domain, the product is $\ge0$ exactly where the first factor is $\ge0$ (at the right end the product is $0$, so it is accepted anyway; for the problems of this type that end is in the set where the first factor is $\ge0$ as well).

**The first factor.** Put $t=2^x>0$. Because $4^x=t^2$ and $2^{x+2}=4t$, the condition is
$$t^2-4B\,t+C\ge0.$$
This quadratic has two roots $t_1<t_2$ (both positive for this type, powers of 2), and it is $\ge0$ for $t\le t_1$ or $t\ge t_2$. Taking $\log_2$ (increasing), this means $x\le\log_2t_1$ or $x\ge\log_2t_2$. In the original problem $t^2-20t+64$ has the roots $4$ and $16$, so $x\le2$ or $x\ge4$.

**Counting the integers.** Let $k_1=\lfloor\log_2t_1\rfloor$ and $k_2=\lceil\log_2t_2\rceil$.
- The integers $x$ with $1\le x\le k_1$ (the domain starts above 0): $k_1$ of them.
- The integers $x$ with $k_2\le x\le X$: $X-k_2+1$ of them.
The total is $k_1+X-k_2+1$ (for the original problem $2+25-4+1=24$). It is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu số nguyên $x$ thỏa mãn $(4^x-18\\cdot2^{x+2}+512)\\sqrt{3-\\log(5x)}\\ge0$?\n"
    "\n"
    "A. $197$.\n"
    "B. $198$.\n"
    "C. $199$.\n"
    "D. $196$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_THOUGHTS = [
    "I read the problem. In $4^x-18\\cdot2^{x+2}+512$ we have $B=18$ and $C=512$; the second part is $\\sqrt{3-\\log(5x)}$, so $a=3$ and $c=5$. With $t=2^x$ the first factor is $t^2-4Bt+C=t^2-72t+512$. I ask the Calculator for its roots in $t$.",
    "The solver may list the roots in either order, so I take the smaller with Min. This is $t_1$.",
    "The larger root, with Max, is $t_2$.",
    "The domain gives $x\\le10^a/c=10^3/5$. The largest integer of the domain is the floor of this number; I store it as `x_max`.",
    "The integers $x$ with $x\\le\\log_2 t_1$ and $x\\ge1$ number the floor of $\\log_2 t_1$, written `log(t_small)/log(2)`. I store it as `count_low`.",
    "The integers from the ceiling of $\\log_2 t_2$ up to `x_max` number `x_max - ceiling(log(t_large)/log(2)) + 1`. I store it as `count_high`.",
    "The total is the sum of the two counts.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"4\^x\s*-\s*(\d+)\s*(?:\\cdot|\.|\\times)\s*2\^\{x\+2\}\s*([+-])\s*(\d+)", stem)
    b = int(m.group(1))
    const = int(m.group(3)) * (1 if m.group(2) == "+" else -1)
    a, c = map(int, re.search(r"\\sqrt\{(\d+)\s*-\s*\\log\((\d+)x\)\}", stem).groups())
    return b, const, a, c


def program(question_text):
    b, const, a, c = _parse(question_text)
    return [
        f"t_roots = solve(t**2 - {b}*4*t + ({const}), t)",
        "t_small = Min(t_roots[0], t_roots[1])",
        "t_large = Max(t_roots[0], t_roots[1])",
        f"x_max = floor(10**{a}/{c})",
        "count_low = floor(log(t_small)/log(2))",
        "count_high = x_max - ceiling(log(t_large)/log(2)) + 1",
        "answer = count_low + count_high",
    ]


def brute_force(question_text):
    """Independent of the method: test the ORIGINAL inequality on every integer of the domain."""
    import mpmath as mp
    mp.mp.dps = 50
    b, const, a, c = _parse(question_text)
    count = 0
    for x in range(1, 10 ** a // c + 5):
        inside = a - mp.log10(c * x)
        if inside < -mp.mpf(10) ** -40:
            continue
        first = mp.mpf(4) ** x - b * mp.mpf(2) ** (x + 2) + const
        root = mp.sqrt(max(inside, 0))
        if first * root >= -mp.mpf(10) ** -40:
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: from the first factor $4^x-B\\cdot2^{x+2}+C$, the number $B$ and the constant $C$ with its sign; from the square root $\\sqrt{a-\\log(cx)}$, the numbers $a$ and $c$.",
    "Store `t_roots = solve(t**2 - <B>*4*t + (<C>), t)`, writing the numbers from the problem. The letter `t` stands for $2^x$ here and needs no earlier assignment.",
    "Store `t_small = Min(t_roots[0], t_roots[1])`, then `t_large = Max(t_roots[0], t_roots[1])`.",
    "Store `x_max = floor(10**<a>/<c>)`.",
    "Store `count_low = floor(log(t_small)/log(2))`.",
    "Store `count_high = x_max - ceiling(log(t_large)/log(2)) + 1`.",
    "Store `answer = count_low + count_high`.",
])
