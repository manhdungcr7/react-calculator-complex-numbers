# -*- coding: utf-8 -*-
"""Problem type D41: count the integer pairs (x; y), 0 <= x <= N, with log_b(bx+b) + x = 2y + (b^2)^y.

Method of the source solution (p090 q47): log_b(bx+b) = 1 + log_b(x+1); t = log_b(x+1); f(h) = h + b^h is
increasing, so t = 2y, x + 1 = b^(2y); every integer y >= 0 with b^(2y) <= N + 1 gives exactly one x.
"""
import re

import framework as fw

MA_DANG = "D41"
TITLE_VI = "đếm số cặp nguyên $(x;y)$ thỏa $0\\le x\\le N$ và $\\log_b(bx+b)+x=2y+(b^2)^y$"
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem asks for the number of integer pairs $(x;y)$ with $0\le x\le N$ satisfying $\log_b(bx+b)+x=2y+q^{\,y}$, where $q=b^2$.

**Rewriting.** $\log_b(bx+b)=\log_b\big(b(x+1)\big)=1+\log_b(x+1)$, so the equation is
$$1+\log_b(x+1)+x=2y+b^{2y}\qquad(\text{because }q^{\,y}=b^{2y}).$$

**A new variable.** Let $t=\log_b(x+1)$, so $x+1=b^t$ and $x=b^t-1$. Substituting, $1+t+b^t-1=2y+b^{2y}$, that is
$$t+b^{t}=2y+b^{2y}.$$

**The function $f(h)=h+b^h$ is increasing.** Its derivative is $f'(h)=1+b^h\ln b>0$, so $f$ is strictly increasing on $\mathbb R$. The equation says $f(t)=f(2y)$, hence $t=2y$, that is
$$\log_b(x+1)=2y\iff x+1=b^{2y}=q^{\,y}.$$

**Counting the pairs.** Each integer $y$ with $x=q^{\,y}-1$ an integer in $[0;N]$ gives exactly one pair, and different $y$ give different $x$. The condition $0\le x\le N$ means $1\le q^{\,y}\le N+1$. Since $q>1$, $q^{\,y}\ge1$ means $y\ge0$, and $q^{\,y}\le N+1$ is checked exactly (an equality $q^{\,y}=N+1$ is allowed). So the number of pairs is the number of integers $y\ge0$ with $q^{\,y}\le N+1$.

**The Calculator can count them.** `Count(condition, (y, low, high))` returns how many integers $y$ from `low` to `high` make the condition true, deciding each condition exactly (here $y$ from 0 to 40 is more than enough, since $q^{\,y}$ grows very fast). The count is then compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu cặp số nguyên $(x;y)$ thỏa mãn $0\\le x\\le 624$ và $\\log_{5}(5x+5)+x=2y+25^y$?\n"
    "\n"
    "A. $2$.\n"
    "B. $3$.\n"
    "C. $4$.\n"
    "D. $624$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_THOUGHTS = [
    "I read the problem. The upper bound is $N=624$, so $x+1$ can be at most $N+1$. I compute $N+1$ and store it as `limit_value`.",
    "The number multiplying the exponent on the right is $q=25$ (it is $b^2$ with $b=5$). I count the integers $y$ from 0 to 40 with $25^y\\le$ `limit_value`; an equality is allowed, and the Count decides each case exactly.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    low, n = map(int, re.search(r"(\d+)\\le x\\le (\d+)", stem).groups())
    q = int(re.search(r"=\s*2y\+(\d+)\^y", stem).group(1))
    assert low == 0, stem
    return n, q


def program(question_text):
    n, q = _parse(question_text)
    return [
        f"limit_value = {n} + 1",
        f"answer = Count({q}**y <= limit_value, (y, 0, 40))",
    ]


def brute_force(question_text):
    """Independent of the method: test the ORIGINAL equation exactly for every x and a range of y."""
    import mpmath as mp
    mp.mp.dps = 60
    n, q = _parse(question_text)
    b = int(round(q ** 0.5))
    assert b * b == q
    count = 0
    for x in range(0, n + 1):
        lhs = mp.log(b * x + b, b) + x
        for y in range(-3, 25):
            if abs(lhs - (2 * y + mp.mpf(q) ** y)) < mp.mpf(10) ** -30:
                count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the upper bound $N$ in $0\\le x\\le N$, and the number $q$ in $2y+q^y$ on the right side.",
    "Store `limit_value = <N> + 1`.",
    "Store `answer = Count(<q>**y <= limit_value, (y, 0, 40))`. The letter `y` here is the counting variable of the Count and needs no earlier assignment.",
])
