# -*- coding: utf-8 -*-
"""Problem type D47: count the integers x for which some real y satisfies log_a(x+y) = log_b(x^2+y^2).

Method of the source solution (p106 q50): common value t, the system x+y = a^t, x^2+y^2 = b^t, the
Cauchy inequality (x+y)^2 <= 2(x^2+y^2) for the bound on t, and the exclusion of negative x by a
contradiction.  The source bounds x crudely and tests each candidate by hand; for the generated
variants (bases 2^m and 2^n with n/m up to 1.9) the exact largest x is found instead with y = lambda * x.
"""
import re

import framework as fw

MA_DANG = "D47"
TITLE_VI = "đếm số nguyên $x$ để tồn tại $y$ thực thỏa $\\log_a(x+y)=\\log_b(x^2+y^2)$"
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $\log_a(x+y)=\log_b(x^2+y^2)$ with two different bases $a$ and $b$ (with $a^2>b$), and asks how many integers $x$ admit a real number $y$ satisfying it.

**A common value and a system.** Let $t=\log_a(x+y)=\log_b(x^2+y^2)$. Then $x+y=a^t$ and $x^2+y^2=b^t$. Write $r=\log_a b$, that is $b=a^r$; then $b^t=(a^t)^r$, so the system gives the single relation
$$x^2+y^2=(x+y)^r,\qquad x+y>0.$$

**Cauchy gives the range of $t$ and shows $r<2$.** The inequality $(x+y)^2\le2(x^2+y^2)$ gives $a^{2t}\le2\,b^t$, that is $(a^2/b)^t\le2$, so $t\le\log_{a^2/b}2$. Since $a^2>b$ we have $r=\log_a b<2$, and this is what the later steps need.

**The candidates for $x$ (as in the original solution).** From $x^2\le x^2+y^2=b^t\le b^{t_{\max}}$ with $t_{\max}=\log_{a^2/b}2$ we get $|x|\le\sqrt{b^{t_{\max}}}$. In the original problem ($a=3$, $b=4$) this is $x^2\le4^{\log_{9/4}2}\approx1{,}89$, so the only candidates are $x\in\{-1,0,1\}$, and each candidate is then tested: $x=0$ works with $y=1$ ($t=0$), $x=1$ works with $y=0$ ($t=0$), and $x=-1$ is impossible. When $r=\log_a b$ is close to 2 this bound allows many candidates (for the bases $2^m$ and $2^n$ up to dozens), so instead of testing them one by one we find the exact largest admissible $x$ below.

**Negative $x$ is impossible.** Suppose $x\le-1$. Then $y=(x+y)-x\ge(x+y)+1$. If $x+y\ge1$, then $y^2>(x+y)^2\ge(x+y)^r$ (because $r<2$), so $x^2+y^2>(x+y)^r$, a contradiction. If $0<x+y<1$, then $y\ge1$, so $x^2+y^2\ge2>1>(x+y)^r$, again a contradiction. So $x\ge0$.

**$x=0$ and $x\ge1$.** For $x=0$ take $y=1$ (then $t=0$): it works. For $x>0$ put $y=\lambda x$; since $x+y>0$ we need $\lambda>-1$. The relation becomes $x^2(1+\lambda^2)=x^r(1+\lambda)^r$, that is
$$x=X(\lambda)=\left[\frac{(1+\lambda)^r}{1+\lambda^2}\right]^{\frac{1}{2-r}}.$$
The function $X$ is continuous on $(-1;+\infty)$, tends to 0 when $\lambda\to-1$ and when $\lambda\to+\infty$, and $X(0)=1$. Hence $x$ takes every value in $(0;X_{\max}]$, where $X_{\max}$ is the largest value of $X$.

**The largest value.** Set the derivative of $\ln X$ to zero: $\dfrac{r}{1+\lambda}=\dfrac{2\lambda}{1+\lambda^2}$, which simplifies to $(2-r)\lambda^2+2\lambda-r=0$. This quadratic has exactly one root greater than $-1$, namely
$$\lambda_0=\frac{-1+\sqrt{1+r(2-r)}}{2-r},$$
and $X_{\max}=X(\lambda_0)$.

**Counting.** The admissible integers are $x=0$ and $x=1,2,\dots,\lfloor X_{\max}\rfloor$ (note $X_{\max}\ge X(0)=1$). Their number is $\lfloor X_{\max}\rfloor+1$. This count is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu số nguyên $x$ để tồn tại số thực $y$ thỏa mãn $\\log_{128}(x+y)=\\log_{4096}(x^2+y^2)$?\n"
    "\n"
    "A. $6$.\n"
    "B. $8$.\n"
    "C. $7$.\n"
    "D. $5$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_THOUGHTS = [
    "I read the problem. The base of the first logarithm is 128 and the base of the second is 4096. With $b=a^r$ the exponent is $r=\\log_a b=\\log_{128}4096$, which by the change of base formula is $\\log(4096)/\\log(128)$. I need it as a decimal for the next formulas, so I wrap it in N with 20 digits and store it as `ratio`.",
    "The method gives $\\lambda_0=\\dfrac{-1+\\sqrt{1+r(2-r)}}{2-r}$. I use the stored `ratio` for $r$, with 20 digits, and store the result as `lam`.",
    "Now $X_{\\max}=\\left[\\dfrac{(1+\\lambda_0)^r}{1+\\lambda_0^2}\\right]^{1/(2-r)}$, with the stored `lam` and `ratio`, again with 20 digits. I store it as `x_max`.",
    "The admissible integers are $0,1,\\dots,\\lfloor X_{\\max}\\rfloor$, which is the floor of `x_max` plus 1 numbers.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    a, b = map(int, re.search(r"\\log_\{?(\d+)\}?\(x\+y\)\s*=\s*\\log_\{?(\d+)\}?\(x\^2\+y\^2\)", stem).groups())
    return a, b


def program(question_text):
    a, b = _parse(question_text)
    return [
        f"ratio = N(log({b})/log({a}), 20)",
        "lam = N((-1 + sqrt(1 + ratio*(2 - ratio)))/(2 - ratio), 20)",
        "x_max = N(((1 + lam)**ratio/(1 + lam**2))**(1/(2 - ratio)), 20)",
        "answer = floor(x_max) + 1",
    ]


def brute_force(question_text):
    """Independent of the method: for each integer x, does x^2+(t-x)^2 = t^r have a root t in (0, Tmax]?"""
    import math

    import numpy as np
    a, b = _parse(question_text)
    r = math.log(b) / math.log(a)
    tmax = 2 ** (1 / (2 - r))
    ts = np.linspace(1e-9, tmax, 3000001)
    count = 1                                   # x = 0 (t = 1, y = 1)
    for x in range(-5, 3 * int(tmax) + 5):
        if x == 0:
            continue
        phi = x * x + (ts - x) ** 2 - ts ** r
        if phi.min() <= 0:
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the base $a$ of the first logarithm $\\log_a(x+y)$ and the base $b$ of the second logarithm $\\log_b(x^2+y^2)$.",
    "Store `ratio = N(log(<b>)/log(<a>), 20)`, writing the two bases from the problem. This is $r=\\log_a b$.",
    "Store `lam = N((-1 + sqrt(1 + ratio*(2 - ratio)))/(2 - ratio), 20)`.",
    "Store `x_max = N(((1 + lam)**ratio/(1 + lam**2))**(1/(2 - ratio)), 20)`.",
    "Store `answer = floor(x_max) + 1`.",
])
