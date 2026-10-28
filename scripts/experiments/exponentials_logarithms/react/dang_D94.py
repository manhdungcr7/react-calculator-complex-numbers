# -*- coding: utf-8 -*-
"""Problem type D94: maximum of P = x^2 + y^2 + alpha x + beta y for the reals x, y with
a^(4x - log_5 a^2) <= 25^(K - y^2) for every positive a.

Method of the source solution (p243 q44): t = log_5 a turns the condition into t^2 - 2tx + K - y^2 >= 0 for all t,
so the discriminant gives x^2 + y^2 <= K; then the Bunyakovsky (Cauchy) inequality bounds alpha x + beta y.
"""
import re

import framework as fw

MA_DANG = "D94"
TITLE_VI = "giá trị lớn nhất của $P=x^2+y^2+\\alpha x+\\beta y$ khi $a^{4x-\\log_5a^2}\\le25^{K-y^2}$ với mọi $a>0$"
FREE_UNKNOWNS = set()
OPTION_STYLE = "numeric"

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the real numbers $x,y$ satisfy $a^{4x-\log_5 a^2}\le25^{K-y^2}$ for every positive real $a$, and we want the maximum of $P=x^2+y^2+\alpha x+\beta y$.

**Using the logarithm of $a$.** Since $a>0$, put $t=\log_5 a$, so $a=5^t$ and $\log_5a^2=2t$. Also $25^{K-y^2}=5^{2(K-y^2)}$. The condition becomes
$$5^{t(4x-2t)}\le5^{2(K-y^2)}\iff 4tx-2t^2\le2K-2y^2\iff t^2-2tx+K-y^2\ge0.$$
As $a$ ranges over all positive numbers, $t$ ranges over all real numbers, so this must hold for every real $t$.

**The discriminant.** A quadratic in $t$ with positive leading coefficient is non negative for every $t$ exactly when its discriminant is non positive: $\Delta'=x^2-(K-y^2)\le0$, that is
$$x^2+y^2\le K.$$

**The maximum of $P$.** Write $P=(x^2+y^2)+(\alpha x+\beta y)$. The first part is at most $K$. By the Bunyakovsky (Cauchy) inequality, $(\alpha x+\beta y)^2\le(\alpha^2+\beta^2)(x^2+y^2)\le(\alpha^2+\beta^2)K$, so $\alpha x+\beta y\le\sqrt{K(\alpha^2+\beta^2)}$. Therefore
$$P\le K+\sqrt{K(\alpha^2+\beta^2)}.$$
Equality is reached when $x^2+y^2=K$ and $(x,y)$ is a positive multiple of $(\alpha,\beta)$, which is a real point of the allowed disc. So $P_{\max}=K+\sqrt{K(\alpha^2+\beta^2)}$.

**Check on the original problem.** $K=40$, $\alpha=1$, $\beta=-3$: $\sqrt{40\cdot10}=20$, so $P_{\max}=60$. The value is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Xét tất cả các số thực $x, y$ sao cho $a^{4x-\\log_5(a^2)}\\le 25^{100-y^2}$ với mọi số thực dương $a$. Giá trị lớn nhất của biểu thức $P=x^2+y^2+8x-6y$ bằng\n"
    "\n"
    "A. $0$.\n"
    "B. $100$.\n"
    "C. $200$.\n"
    "D. $201$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_THOUGHTS = [
    "I read the problem. The constant in the exponent on the right is $K=100$ (from $25^{100-y^2}$), so $x^2+y^2\\le100$. I store it as `radius_squared`.",
    "In $P=x^2+y^2+8x-6y$ the coefficient of $x$ is $\\alpha=8$. I store it as `coef_x`.",
    "The coefficient of $y$ is $\\beta=-6$ (the sign is part of the number). I store it as `coef_y`.",
    "The maximum is $P_{\\max}=K+\\sqrt{K(\\alpha^2+\\beta^2)}$, with the stored values.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    k = int(re.search(r"25\^\{(\d+)-y\^2\}", stem).group(1))
    m = re.search(r"P\s*=\s*x\^2\+y\^2\s*([+-])\s*(\d*)x\s*([+-])\s*(\d*)y", stem)
    alpha = int(m.group(2) or 1) * (1 if m.group(1) == "+" else -1)
    beta = int(m.group(4) or 1) * (1 if m.group(3) == "+" else -1)
    return k, alpha, beta


def program(question_text):
    k, alpha, beta = _parse(question_text)
    return [
        f"radius_squared = {k}",
        f"coef_x = {alpha}",
        f"coef_y = {beta}",
        "answer = radius_squared + sqrt(radius_squared*(coef_x**2 + coef_y**2))",
    ]


def brute_force(question_text):
    """Independent of the method: maximise P over the boundary circle x^2 + y^2 = K numerically."""
    import math

    import numpy as np
    k, alpha, beta = _parse(question_text)
    th = np.linspace(0, 2 * math.pi, 4000001)
    r = math.sqrt(k)
    p = r * r + alpha * r * np.cos(th) + beta * r * np.sin(th)
    return float(p.max())


BRUTE_TOLERANCE = 1e-6

PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the number $K$ in $25^{K-y^2}$, and the coefficients of $x$ and of $y$ in $P=x^2+y^2+\\alpha x+\\beta y$ with their signs (a coefficient that is not written is 1, and after a minus sign it is $-1$).",
    "Store `radius_squared = <K>`.",
    "Store `coef_x = <alpha>`, then `coef_y = <beta>`, keeping the signs.",
    "Store `answer = radius_squared + sqrt(radius_squared*(coef_x**2 + coef_y**2))`.",
])
