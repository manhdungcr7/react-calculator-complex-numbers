# -*- coding: utf-8 -*-
"""Problem type D29: count the positive integers m for which A^x - p B^x + (m - k) C^x = 0 has a positive root
(A * C = B^2, B > C, p = 1 or 2).

Method of the source solution (p056 q34): divide by C^x and put t = (B/C)^x > 1, so the equation is
t^2 - p t + m - k = 0 and one needs a root t > 1; the table of m = f(t) = -t^2 + p t + k gives m < k + p - 1.
"""
import re

import framework as fw

MA_DANG = "D29"
TITLE_VI = "đếm số nguyên dương $m$ để $A^x-pB^x+(m-k)C^x=0$ có nghiệm dương"
OPTION_VARIABLES = True
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $A^x-p\cdot B^x+(m-k)\cdot C^x=0$ with $A\cdot C=B^2$ and $B>C$, where the number $p$ in front of $B^x$ is 2 (as in $16^x-2\cdot12^x+(m-2)\cdot9^x$, where $16\cdot9=12^2$) or is not written (then $p=1$, as in $48^x-12^x+(m-11)\cdot3^x$). It asks how many positive integers $m$ give the equation a positive root $x$.

**Step 1: dividing by $C^x$.** Since $C^x>0$, divide every term by it: $\left(\dfrac AC\right)^x-p\left(\dfrac BC\right)^x+(m-k)=0$. Because $A\cdot C=B^2$ we have $\dfrac AC=\left(\dfrac BC\right)^2$, hence $\left(\dfrac AC\right)^x=\left(\left(\dfrac BC\right)^x\right)^2$. Put
$$t=\left(\frac BC\right)^x .$$
The equation becomes the quadratic $t^2-p\,t+m-k=0$.

**Step 2: what "$x>0$" means for $t$.** The base $\dfrac BC$ is larger than 1 (because $B>C$), so $t=\left(\dfrac BC\right)^x$ is increasing, with $t=1$ at $x=0$. Therefore $x>0\iff t>1$, and each $t>1$ comes from exactly one $x>0$. The problem becomes: find the positive integers $m$ for which $t^2-pt+m-k=0$ has a root $t>1$.

**Step 3: separating $m$.** Move $m$ to one side: $m=f(t)=-t^2+p\,t+k$. The derivative $f'(t)=-2t+p$ is negative for every $t>1$ (because $p\le2$ gives $-2t+p<0$), so $f$ is strictly decreasing on $(1;+\infty)$. It starts at $f(1)=-1+p+k=k+p-1$ (this value is **not** reached, because $t>1$ is strict) and goes down to $-\infty$. By the intermediate value property, $f$ takes every value below $f(1)$ exactly once on $(1;+\infty)$ and no other value. Hence the equation has a root $t>1$ exactly when
$$m<f(1)=k+p-1 .$$

**Step 4: counting.** The positive integers $m$ with $m<f(1)$ are $1,2,\dots,\lceil f(1)\rceil-1$ (the ceiling takes care of the strict inequality), so their number is $\lceil f(1)\rceil-1$. (Original problem: $p=2$, $k=2$, $f(1)=3$, so $m=1,2$: two values.)

**From the method to the Calculator.** `supremum` is $f(1)=-1^2+p\cdot1+k$ and `answer` is $\lceil\text{supremum}\rceil-1$. It is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu giá trị nguyên dương của tham số $m$ để phương trình sau có nghiệm dương $245^x-35^x+(m-6)\\cdot5^x=0$?\n"
    "\n"
    "A. $4$.\n"
    "B. $5$.\n"
    "C. $6$.\n"
    "D. $11$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_READING = (
    "Reading the problem before any computation. The equation is $245^x-35^x+(m-6)\\cdot5^x=0$ and I count the positive integers $m$ for which it has a positive root $x$. "
    "The number in the bracket $(m-6)$ is six, so $k=6$. The middle term $35^x$ has no number in front of it, so $p=1$. "
    "As a check, $245\\cdot5=1225=35^2$, so $A\\cdot C=B^2$ holds. I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "After dividing by $5^x$ and putting $t=(35/5)^x$, the equation is $t^2-pt+m-k=0$, so $m=-t^2+pt+k$, and for $t>1$ this is a decreasing function whose supremum is its value at $t=1$, namely $-1^2+p\\cdot1+k$. With $p=1$ and $k=6$ I send `supremum = 6 + 1*1 - 1**2`.",
    "The supremum is stored. The values $m<$ `supremum` are admissible, and the positive integers among them are $1,2,\\dots,\\lceil\\text{supremum}\\rceil-1$, because the ceiling takes care of the strict inequality. I send `answer = ceiling(supremum) - 1`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"(\d+)\^x\s*-\s*(?:(\d+)\\cdot\s*)?(\d+)\^x\s*\+\s*\(m\s*-\s*(\d+)\)\\cdot\s*(\d+)\^x\s*=\s*0", stem)
    a, p, b, k, c = int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4)), int(m.group(5))
    assert a * c == b * b and b > c, stem
    return a, p, b, c, k


def program(question_text):
    _, p, _, _, k = _parse(question_text)
    return [
        f"supremum = {k} + {p}*1 - 1**2",
        "answer = ceiling(supremum) - 1",
    ]


def brute_force(question_text):
    """Independent of the method: for each positive m, does the equation (divided by C^x) dip below zero for x > 0?"""
    import math

    import numpy as np
    a, p, b, c, k = _parse(question_text)
    xs = np.linspace(1e-9, 40.0, 2000001)
    ra, rb = math.log(a / c), math.log(b / c)
    count = 0
    for m in range(1, k + 20):
        g = np.exp(xs * ra) - p * np.exp(xs * rb) + (m - k)
        if g.min() < -1e-9:              # dips below zero for some x > 0, and tends to +infinity: a root exists
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the number $k$ in the bracket $(m-k)$, and the number $p$ written in front of the middle power $B^x$ (it is 1 when no number is written).",
    "Store `supremum = <k> + <p>*1 - 1**2`. This is $f(1)=-1^2+p\\cdot1+k$.",
    "Store `answer = ceiling(supremum) - 1`.",
], option_variables=True)
