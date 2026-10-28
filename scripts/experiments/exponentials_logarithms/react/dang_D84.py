# -*- coding: utf-8 -*-
"""Problem type D84: count the integers y for which 27^(3x^2+xy) = (1+xy) 27^(Cx) has a solution
x in the open interval (1/3; A), C = 3A.

Method of the source solution (p216 q45): y <= 0 is checked directly (y = -1, -2 work, y = 0 does not);
for y >= 1 the equation becomes g(x) = 0 with g increasing, so a solution exists exactly when
g(1/3) < 0, i.e. y - log_3(1 + y/3) < C - 1.  The left side is increasing in y, so the admissible
y are the integers below the single root y0 of y - log_3(1 + y/3) = C - 1.
"""
import re

import framework as fw

MA_DANG = "D84"
TITLE_VI = "đếm số nguyên $y$ để $27^{3x^2+xy}=(1+xy)27^{Cx}$ có nghiệm $x\\in(\\frac13;A)$"
FREE_UNKNOWNS = {"y"}

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives the equation $27^{3x^2+xy}=(1+xy)\,27^{Cx}$ (with $C=3A$) and asks how many integers $y$ make it have a solution $x$ in the open interval $\left(\frac13;A\right)$.

**Case 1: $y\le0$.** The factor $1+xy$ equals a power of 27, which is positive, so $1+xy>0$. Since $x>\frac13$ this forces $y>-3$, so only $y=0,-1,-2$ can work, and we check them directly.
- For $y=0$ the equation is $27^{3x^2}=27^{Cx}$, so $3x^2=Cx$, that is $3x(x-A)=0$; the solutions $x=0$ and $x=A$ are not in the open interval, so $y=0$ is rejected.
- For $y=-1$ and $y=-2$ the equation has a solution in $\left(\frac13;-\frac1y\right)$ (the function $27^{3x^2+(y-C)x}-(1+xy)$ is negative at $x=\frac13$ and tends to a positive number at the right end of that interval), so both values are accepted.
This case gives exactly 2 values of $y$.

**Case 2: $y\ge1$.** Take the logarithm to the base 27 of both sides: $3x^2+xy=\log_{27}(1+xy)+Cx$. Divide by $x>0$ and move everything to one side:
$$g(x)=3x-C-\frac{\log_{27}(1+xy)}{x}+y=0.$$
The derivative is $g'(x)=3+\dfrac{\ln(1+xy)}{x^2\ln27}-\dfrac{y}{x(1+xy)\ln27}>3-\dfrac{1}{3x^2\ln3}\ge3-\dfrac{3}{\ln3}>0$ on $\left[\frac13;A\right]$, so $g$ is strictly increasing there. An increasing continuous function has a zero in the open interval exactly when $g\left(\frac13\right)\cdot g(A)<0$. Using $\ln(1+u)<u$ for $u>0$ one shows $g(A)>0$, so the condition is $g\left(\frac13\right)<0$. Substituting $x=\frac13$:
$$g\left(\tfrac13\right)=y+1-C-\log_3\left(1+\tfrac y3\right)<0\iff y-\log_3\left(1+\tfrac y3\right)<C-1.$$

**Counting the integers $y\ge1$.** The left side $h(y)=y-\log_3\left(1+\frac y3\right)$ is strictly increasing in $y$ (because $h'(y)=1-\dfrac{1}{(y+3)\ln3}>0$). Hence the equation $h(y)=C-1$ has exactly one root $y_0$, and the inequality $h(y)<C-1$ holds exactly for $y<y_0$. The positive integers below $y_0$ are $1,2,\dots,\lceil y_0\rceil-1$. If $y_0$ happened to be an integer itself, that integer is excluded because the inequality is strict; subtracting a tiny number such as $10^{-9}$ before taking the ceiling handles this case correctly. The number of positive integers is therefore $\lceil y_0-10^{-9}\rceil-1$.

**Finding $y_0$ with the Calculator.** The equation $y-\log_3\left(1+\frac y3\right)=C-1$ has no simple closed form, so the Calculator solves it numerically: `nsolve(expression, y, start)` returns the root of `expression = 0` found by starting the search at the number `start` (use $C$ as the starting value). A logarithm to the base 3 is written `log(u)/log(3)`.

**Conclusion.** The total number of integers $y$ is that count plus the 2 values $y=-1,-2$ of Case 1. This total is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu số nguyên $y$ tồn tại sao cho $x\\in\\left(\\dfrac{1}{3};2\\right)$ thỏa mãn $27^{3x^2+xy}=(1+xy)27^{6x}$?\n"
    "\n"
    "A. $5$.\n"
    "B. $8$.\n"
    "C. $6$.\n"
    "D. $7$."
)
EXAMPLE_ANSWER = "D"

EXAMPLE_THOUGHTS = [
    "I read the problem. The right side is $27^{6x}$, so $C=6$ (the interval is $\\left(\\frac13;2\\right)$, consistent with $C=3A$). For $y\\ge1$ the condition is $y-\\log_3\\left(1+\\frac y3\\right)<C-1$, and its left side is increasing, so I need the single root $y_0$ of $y-\\log_3\\left(1+\\frac y3\\right)=6-1$. The Calculator finds it numerically with nsolve, starting the search at $y=6$ (the value of $C$); the logarithm to the base 3 is written $\\log(\\cdot)/\\log(3)$.",
    "The positive integers $y$ with $y<y_0$ are $1,\\dots,\\lceil y_0\\rceil-1$. To be safe if $y_0$ were itself an integer, I subtract $10^{-9}$ before taking the ceiling; the number of positive integers is stored as `positive_count`.",
    "Case 1 of the method gave exactly 2 more values, $y=-1$ and $y=-2$, so the total is `positive_count + 2`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"\(1\+xy\)27\^\{(\d+)x\}", stem)
    return int(m.group(1))


def program(question_text):
    c = _parse(question_text)
    return [
        f"y_limit = nsolve(y - log(1 + y/3)/log(3) - ({c} - 1), y, {c})",
        "positive_count = ceiling(y_limit - 10**(-9)) - 1",
        "answer = positive_count + 2",
    ]


def brute_force(question_text):
    """Independent of the method: sign changes of the logarithmic form of the equation for y >= 1, plus the
    two values y = -1, -2 checked through the intermediate value theorem."""
    import math

    import numpy as np
    stem = question_text.split("\n")[0]
    c = _parse(question_text)
    a = int(re.search(r"\\dfrac\{1\}\{3\};\s*(\d+)\\right", stem).group(1))
    count = 0
    for y in range(1, 4 * c + 20):
        xs = np.linspace(1 / 3, a, 200001)[1:-1]
        g = 3 * xs ** 2 + xs * y - np.log(1 + xs * y) / math.log(27) - c * xs
        if np.any(np.sign(g[:-1]) != np.sign(g[1:])):
            count += 1
    for y in (-1, -2):
        x0 = 1 / 3
        left = 3 * x0 ** 2 + x0 * y - math.log(1 + x0 * y) / math.log(27) - c * x0
        assert left < 0          # tends to +infinity at x -> -1/y, so a root exists
        count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the number $C$ in the exponent $27^{Cx}$ on the right side of the equation (the bound $A$ of the interval is not needed).",
    "Store `y_limit = nsolve(y - log(1 + y/3)/log(3) - (<C> - 1), y, <C>)`, writing the number $C$ twice. This is the root $y_0$.",
    "Store `positive_count = ceiling(y_limit - 10**(-9)) - 1`. This is the number of positive integers $y$.",
    "Store `answer = positive_count + 2`, where 2 stands for the values $y=-1$ and $y=-2$ of Case 1.",
])
