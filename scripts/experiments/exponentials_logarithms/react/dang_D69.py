# -*- coding: utf-8 -*-
"""Problem type D69: count the integers m in (lo; hi) for which a^x + m = log_a(x - m) has a solution.

Method of the source solution (p166 q45): a^x + x = log_a(x-m) + (x-m), f(t) = a^t + t is increasing,
so x = log_a(x-m), that is a^x - x = -m; g(x) = a^x - x has its minimum at x0 = log_a(1/ln a), so the
equation has a solution iff -m >= g(x0), i.e. m <= -g_min.
"""
import re

import framework as fw

MA_DANG = "D69"
TITLE_VI = "đếm số nguyên $m\\in(\\ell;h)$ để $a^x+m=\\log_a(x-m)$ có nghiệm"
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives the equation $a^x+m=\log_a(x-m)$ with an integer base $a\ge2$ and a parameter $m$, and asks how many integers $m$ of a given open interval $(\ell;h)$ make it have a solution.

**Making both sides the same function.** Add $x-m$ to both sides of the equation: $a^x+m=\log_a(x-m)\iff a^x+x=\log_a(x-m)+(x-m)$. The two sides now have the shape $f(t)=a^t+t$: the left side is $f(x)$ and, since $a^{\log_a(x-m)}=x-m$, the right side is $f\big(\log_a(x-m)\big)$.

**The function $f$ is increasing.** Since $f'(t)=a^t\ln a+1>0$ for every real $t$, the function $f$ is strictly increasing on $\mathbb R$, so $f(u)=f(v)$ happens only when $u=v$. Therefore
$$x=\log_a(x-m)\iff a^x=x-m\iff a^x-x=-m.$$

**A parameter alone on one side.** The equation has a solution exactly when the value $-m$ is taken by the function $g(x)=a^x-x$. Its derivative is $g'(x)=a^x\ln a-1$, which is zero when $a^x=\dfrac{1}{\ln a}$, that is at the single point $x_0=\log_a\dfrac{1}{\ln a}$. The derivative is negative before $x_0$ and positive after it, so $g$ has its minimum at $x_0$, and $g(x)\to+\infty$ on both sides. The values of $g$ are therefore exactly $[g_{\min};+\infty)$ with $g_{\min}=g(x_0)=a^{x_0}-x_0$.

**Condition on $m$.** The equation has a solution iff $-m\ge g_{\min}$, that is $m\le-g_{\min}$. For an integer base $a\ge2$ the number $g_{\min}$ lies strictly between 0 and 1, so $-g_{\min}$ is a non integer between $-1$ and $0$, and the integers $m$ with $m\le-g_{\min}$ are $m\le-1$.

**Counting.** The integers of the open interval $(\ell;h)$ are $\ell+1,\dots,h-1$. The admissible ones are those not above $\min\big(h-1,\lfloor-g_{\min}\rfloor\big)$, and their number is this top value minus $\ell$. This count is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Cho phương trình $6^x+m=\\log_{6}(x-m)$ với $m$ là tham số. Có bao nhiêu giá trị nguyên của $m\\in(-23;31)$ để phương trình đã cho có nghiệm?\n"
    "\n"
    "A. $23$.\n"
    "B. $53$.\n"
    "C. $22$.\n"
    "D. $21$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_THOUGHTS = [
    "I read the problem. The base is 6, and the interval for $m$ is $(-23;31)$, so $\\ell=-23$ and $h=31$. The minimum of $g(x)=6^x-x$ is at $x_0=\\log_6\\frac{1}{\\ln 6}$, which is $\\log(1/\\log(6))/\\log(6)$ in Calculator syntax. I take 20 digits and store it as `x_min`.",
    "Now the minimum value $g_{\\min}=6^{x_0}-x_0$, using the stored `x_min`, with 20 digits. I store it as `g_min`.",
    "The admissible integers are $m\\le-g_{\\min}$ and also $m\\le h-1=30$. The largest admissible integer is the smaller of $30$ and the floor of `-g_min`; I store it as `m_top`.",
    "The integers from $\\ell+1=-22$ up to `m_top` number `m_top` minus $\\ell$, that is `m_top - (-23)`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    a = int(re.search(r"(\d+)\^x\+m", stem).group(1))
    lo, hi = map(int, re.search(r"m\\in\((-?\d+);(-?\d+)\)", stem).groups())
    return a, lo, hi


def program(question_text):
    a, lo, hi = _parse(question_text)
    return [
        f"x_min = N(log(1/log({a}))/log({a}), 20)",
        f"g_min = N({a}**x_min - x_min, 20)",
        f"m_top = Min({hi} - 1, floor(-g_min))",
        f"answer = m_top - ({lo})",
    ]


def brute_force(question_text):
    """Independent of the method: for each m, does a^x + m - log_a(x - m) change sign for x > m?"""
    import math

    import numpy as np
    a, lo, hi = _parse(question_text)
    count = 0
    for m in range(lo + 1, hi):
        xs = m + np.concatenate([np.logspace(-12, 3, 600001)])
        f = a ** np.minimum(xs, 700 / math.log(a)) + m - np.log(xs - m) / math.log(a)
        if f.min() <= 0:
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the base $a$ (the same in $a^x$ and $\\log_a$), and the two ends $\\ell$ and $h$ of the interval $(\\ell;h)$ for $m$ (the lower end $\\ell$ is usually negative).",
    "Store `x_min = N(log(1/log(<a>))/log(<a>), 20)`, writing the base from the problem. This is $x_0=\\log_a\\frac{1}{\\ln a}$.",
    "Store `g_min = N(<a>**x_min - x_min, 20)`.",
    "Store `m_top = Min(<h> - 1, floor(-g_min))`.",
    "Store `answer = m_top - (<l>)`, writing the lower end $\\ell$ in parentheses (for example `m_top - (-23)`).",
])
