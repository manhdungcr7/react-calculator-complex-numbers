# -*- coding: utf-8 -*-
"""Problem type D68: positive a, b with
log_{pa+qb+1}((ra)^2+(sb)^2+1) + log_{tab+1}(pa+qb+1) = 2, where t = 2rs; find a + 2b.

Method of the source solution (p161 q37): AM-GM on the arguments, then AM-GM on the two logarithms;
equality forces ra = sb and pa + qb + 1 = tab + 1.
"""
import re

import framework as fw

MA_DANG = "D68"
TITLE_VI = "tìm $a+2b$ biết $\\log_{pa+qb+1}((ra)^2+(sb)^2+1)+\\log_{tab+1}(pa+qb+1)=2$"
OPTION_VARIABLES = True
MERGE_READING = True
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: positive reals $a,b$ satisfy $\log_{U}\big((ra)^2+(sb)^2+1\big)+\log_{V}(U)=2$, where $U=pa+qb+1$, $V=tab+1$ and $t=2rs$. We are asked for $a+2b$. (In the original problem the first argument is written $25a^2+b^2+1=(5a)^2+(b)^2+1$.)

**All bases and arguments exceed 1.** Since $a,b>0$, we have $U>1$, $V>1$ and $(ra)^2+(sb)^2+1>1$, so every logarithm is positive and defined.

**First inequality (AM-GM).** For non negative numbers, $(ra)^2+(sb)^2\ge2\cdot ra\cdot sb=2rs\,ab=t\,ab$, so $(ra)^2+(sb)^2+1\ge tab+1=V$. The logarithm to the base $U>1$ is increasing, so
$$\log_U\big((ra)^2+(sb)^2+1\big)\ge\log_U V.$$

**Second inequality (AM-GM again).** Hence the left side of the equation is at least $\log_U V+\log_V U$. Both terms are positive and their product is $\log_U V\cdot\log_V U=1$, so by AM-GM their sum is at least $2\sqrt{1}=2$. The equation says the sum equals exactly 2, so both inequalities must be equalities.

**The equality conditions.** The first one holds iff $ra=sb$, that is $b=\dfrac rs\,a$. The second holds iff $\log_U V=\log_V U$, and since their product is 1 this means $\log_U V=1$, that is $V=U$:
$$tab+1=pa+qb+1\iff t\,ab=pa+qb.$$

**Solving.** Put $\rho=\dfrac rs$, so $b=\rho a$. Then $t\rho a^2=(p+q\rho)\,a$, and because $a>0$,
$$a=\frac{p+q\rho}{t\rho},\qquad b=\rho a.$$
The requested number is $a+2b$. (Check on the original problem: $r=5$, $s=1$, $p=10$, $q=3$, $t=10$ give $\rho=5$, $a=\frac12$, $b=\frac52$, $a+2b=\frac{11}{2}$.)

**Why the product of the two logarithms is 1.** By the change of base formula $\log_V U=\dfrac{1}{\log_U V}$, so $\log_U V\cdot\log_V U=1$. For two positive numbers whose product is 1, the sum is at least 2 (AM-GM: $u+\frac1u\ge2$), with equality only when $u=\frac1u$, that is $u=1$.

**From the method to the Calculator.** `ratio` is $\rho=\dfrac rs$; `a_value` is $\dfrac{p+q\rho}{t\rho}$; `b_value` is $\rho\cdot a$; `answer` is $a+2b$ computed from the two stored values. All numbers stay exact fractions. The value is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Cho $a>0,b>0$ thỏa mãn\n"
    "$$\\log_{12a+5b+1}((3a)^2+(b)^2+1)+\\log_{6ab+1}(12a+5b+1)=2.$$\n"
    "Giá trị của $a+2b$ bằng\n"
    "\n"
    "A. $\\dfrac{19}{2}$.\n"
    "B. $\\dfrac{21}{2}$.\n"
    "C. $\\dfrac{23}{2}$.\n"
    "D. $21$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_READING = (
    "Reading the problem before any computation. The equation is "
    "$\\log_{12a+5b+1}\\big((3a)^2+(b)^2+1\\big)+\\log_{6ab+1}(12a+5b+1)=2$ and I want $a+2b$. "
    "In the first argument $(3a)^2+(b)^2+1$ the number next to $a$ is three, so $r=3$, and the bare $b$ means $s=1$. "
    "The base $12a+5b+1$ gives $p=12$ and $q=5$. The base of the second logarithm is $6ab+1$, so $t=6$, which equals $2rs=2\\cdot3\\cdot1$ as expected. "
    "I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "The equality condition of the first AM-GM is $ra=sb$, that is $b=\\rho a$ with $\\rho=\\dfrac rs$, where $r=3$ and $s=1$. I let the Calculator keep $\\rho$ as an exact fraction. I send `ratio = 3/1`.",
    "The second equality condition is $tab=pa+qb$. With $b=\\rho a$ it becomes $t\\rho a^2=(p+q\\rho)a$, and because $a>0$ I can divide by $a$: $a=\\dfrac{p+q\\rho}{t\\rho}$, with $p=12$, $q=5$, $t=6$ and the stored `ratio` for $\\rho$. I send `a_value = (12 + 5*ratio)/(6*ratio)`.",
    "Now $b=\\rho a$, with the stored `ratio` and `a_value`. I send `b_value = ratio*a_value`.",
    "The requested number is $a+2b$, from the two stored values. I send `answer = a_value + 2*b_value`.",
]


def _coef(text):
    return int(text) if text else 1


def _parse(question_text):
    q = question_text
    m = re.search(r"\\log_\{(\d*)a\+(\d*)b\+1\}\(\((\d*)a\)\^2\+\((\d*)b\)\^2\+1\)\+\\log_\{(\d*)ab\+1\}", q)
    if m:
        p, qq, r, s, t = [_coef(m.group(i)) for i in range(1, 6)]
        return p, qq, r, s, t
    # the source form: 25a^2 + b^2 + 1
    m = re.search(r"\\log_\{(\d*)a\+(\d*)b\+1\}\((\d*)a\^2\+(\d*)b\^2\+1\)\+\\log_\{(\d*)ab\+1\}", q)
    p, qq, r2, s2, t = [_coef(m.group(i)) for i in range(1, 6)]
    import math
    r, s = math.isqrt(r2), math.isqrt(s2)
    assert r * r == r2 and s * s == s2
    return p, qq, r, s, t


def program(question_text):
    p, q, r, s, t = _parse(question_text)
    return [
        f"ratio = {r}/{s}",
        f"a_value = ({p} + {q}*ratio)/({t}*ratio)",
        "b_value = ratio*a_value",
        "answer = a_value + 2*b_value",
    ]


def brute_force(question_text):
    """Independent of the method: minimise the left side minus 2 numerically over (a, b); it is >= 0 with
    equality only at the solution."""
    import numpy as np
    from scipy.optimize import minimize
    p, q, r, s, t = _parse(question_text)

    def g(v):
        a, b = np.exp(v)                     # keep a, b > 0
        u = p * a + q * b + 1
        w = t * a * b + 1
        arg = (r * a) ** 2 + (s * b) ** 2 + 1
        return np.log(arg) / np.log(u) + np.log(u) / np.log(w) - 2

    best = None
    for a0 in (0.05, 0.3, 1.0, 3.0):
        for b0 in (0.05, 0.3, 1.0, 3.0):
            res = minimize(g, np.log([a0, b0]), method="Nelder-Mead",
                           options={"xatol": 1e-12, "fatol": 1e-18, "maxiter": 20000, "maxfev": 20000})
            if best is None or res.fun < best.fun:
                best = res
    a, b = np.exp(best.x)
    return a + 2 * b


BRUTE_TOLERANCE = 1e-3

PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: from the base $pa+qb+1$ of the first logarithm, the numbers $p$ and $q$; from the first argument $(ra)^2+(sb)^2+1$, the numbers $r$ and $s$ (a bare $a$ or $b$ means 1); and from the base $tab+1$ of the second logarithm, the number $t$.",
    "Store `ratio = <r>/<s>`.",
    "Store `a_value = (<p> + <q>*ratio)/(<t>*ratio)`.",
    "Store `b_value = ratio*a_value`.",
    "Store `answer = a_value + 2*b_value`.",
], option_variables=True, merge_reading=True)
