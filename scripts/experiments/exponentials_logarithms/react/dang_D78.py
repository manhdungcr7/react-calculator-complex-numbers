# -*- coding: utf-8 -*-
"""Problem type D78: minimum of P = x^2 + y^2 + alpha*x + beta*y for x, y >= 0 with 2x + y*4^(x+y-1) >= 3.

Method of the source solution (p203 q48): Case 1, x >= 3/2: P >= x^2 + alpha*x, minimal at x = 3/2.
Case 2, x < 3/2: the condition becomes f(2y) >= f(3 - 2x) with f(t) = t + log_2 t increasing, so
2y >= 3 - 2x and P is bounded below by a quadratic in x, minimised at its vertex.
"""
import re

import framework as fw

MA_DANG = "D78"
TITLE_VI = "tìm giá trị nhỏ nhất của $P=x^2+y^2+\\alpha x+\\beta y$ với $x,y\\ge0$, $2x+y\\cdot4^{x+y-1}\\ge3$"
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: non negative reals $x,y$ satisfy $2x+y\cdot4^{x+y-1}\ge3$, and we want the minimum of $P=x^2+y^2+\alpha x+\beta y$ (with $\alpha,\beta>0$). Write the condition as $y\cdot4^{x+y-1}\ge3-2x$.

**Case 1: $x\ge\frac32$.** Then $3-2x\le0$, so the condition holds for every $y\ge0$. Since $y^2+\beta y\ge0$, we get $P\ge x^2+\alpha x$, and $x^2+\alpha x$ is increasing for $x\ge\frac32$ (its derivative $2x+\alpha$ is positive). So in this case $P\ge\frac94+\frac32\alpha$, reached at $x=\frac32,\ y=0$.

**Case 2: $x<\frac32$.** Now $3-2x>0$, so the condition forces $y>0$, and we can divide by $y$ and take logarithms to the base 4, then convert to the base 2:
$$4^{x+y-1}\ge\frac{3-2x}{y}\iff x+y-1\ge\tfrac12\log_2\frac{3-2x}{y}\iff 2x+2y-2\ge\log_2(3-2x)-\log_2y.$$
Rearranging gives $2y+\log_2(2y)\ge(3-2x)+\log_2(3-2x)$. The function $f(t)=t+\log_2t$ is strictly increasing for $t>0$, because $f'(t)=1+\dfrac{1}{t\ln2}>0$. Hence the condition is equivalent to
$$2y\ge3-2x,\qquad\text{that is }y\ge\tfrac32-x.$$
Since $P$ increases with $y\ge0$, its smallest value for a given $x$ is reached at $y=\frac32-x$ (this point satisfies the original condition with equality, because then $x+y=\frac32$ and $4^{1/2}=2$). Substituting $y=\frac32-x$:
$$P\ge Q(x)=x^2+\left(\tfrac32-x\right)^2+\alpha x+\beta\left(\tfrac32-x\right)=2x^2+(\alpha-\beta-3)x+\tfrac94+\tfrac32\beta.$$

**Minimising $Q$.** $Q$ is a quadratic with positive leading coefficient. Its vertex is at $x_v=\dfrac{3+\beta-\alpha}{4}$. The allowed $x$ in this case is $0\le x\le\frac32$ (at $x=\frac32$ Case 2 meets Case 1), so the minimum is attained at the vertex when $x_v$ lies in $[0;\tfrac32]$, and otherwise at the nearer end. In Case 1 the minimum $\frac94+\frac32\alpha$ equals $Q\left(\frac32\right)$, so it is already covered. Therefore
$$P_{\min}=Q\big(\operatorname{clamp}(x_v,\,0,\,\tfrac32)\big).$$
The value is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Xét các số thực không âm $x,y$ thỏa mãn $2x+y\\cdot4^{x+y-1}\\ge3$. Giá trị nhỏ nhất của $P=x^2+y^2+23x+25y$ bằng\n"
    "\n"
    "A. $P_{\\min}=\\dfrac{301}{8}$.\n"
    "B. $P_{\\min}=\\dfrac{293}{8}$.\n"
    "C. $P_{\\min}=\\dfrac{285}{8}$.\n"
    "D. $P_{\\min}=\\dfrac{293}{4}$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_THOUGHTS = [
    "I read the problem. The expression is $P=x^2+y^2+23x+25y$, so the coefficient of $x$ is 23. I store it as `coef_x`.",
    "The coefficient of $y$ is 25. I store it as `coef_y`.",
    "The vertex of $Q(x)$ is $x_v=\\dfrac{3+\\beta-\\alpha}{4}$, with $\\alpha=$ `coef_x` and $\\beta=$ `coef_y`. I store it as `x_vertex`.",
    "The allowed $x$ in Case 2 is from 0 to $\\frac32$, so I clamp the vertex into this range: the larger of 0 and the smaller of $\\frac32$ and `x_vertex`. I store it as `x_best`.",
    "Now $Q(x)=2x^2+(\\alpha-\\beta-3)x+\\frac94+\\frac32\\beta$ at `x_best`. This is the minimum of $P$.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"P\s*=\s*x\^2\+y\^2\+(\d*)x\+(\d*)y", stem)
    return int(m.group(1) or 1), int(m.group(2) or 1)


def program(question_text):
    alpha, beta = _parse(question_text)
    return [
        f"coef_x = {alpha}",
        f"coef_y = {beta}",
        "x_vertex = (3 + coef_y - coef_x)/4",
        "x_best = Max(0, Min(3/2, x_vertex))",
        "answer = 2*x_best**2 + (coef_x - coef_y - 3)*x_best + 9/4 + 3*coef_y/2",
    ]


def brute_force(question_text):
    """Independent of the method: for each x find the smallest feasible y of the ORIGINAL constraint (bisection)
    and minimise P over x numerically."""
    import mpmath as mp
    from scipy.optimize import minimize_scalar
    alpha, beta = _parse(question_text)

    def cons(x, y):
        return 2 * x + y * 4 ** (x + y - 1) - 3

    def p_of_x(x):
        if cons(x, 0.0) >= 0:
            y = 0.0
        else:
            lo, hi = 0.0, 3.0
            for _ in range(200):
                mid = (lo + hi) / 2
                if cons(x, mid) >= 0:
                    hi = mid
                else:
                    lo = mid
            y = hi
        return x * x + y * y + alpha * x + beta * y

    best = min((p_of_x(i / 20000 * 3.0), i) for i in range(0, 20001))
    x0 = best[1] / 20000 * 3.0
    res = minimize_scalar(p_of_x, bounds=(max(0, x0 - 0.001), min(3, x0 + 0.001)), method="bounded", options={"xatol": 1e-12})
    return min(res.fun, best[0])


BRUTE_TOLERANCE = 1e-6

PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the coefficient $\\alpha$ of $x$ and the coefficient $\\beta$ of $y$ in $P=x^2+y^2+\\alpha x+\\beta y$ (a coefficient that is not written is 1).",
    "Store `coef_x = <alpha>`, then `coef_y = <beta>`.",
    "Store `x_vertex = (3 + coef_y - coef_x)/4`.",
    "Store `x_best = Max(0, Min(3/2, x_vertex))`.",
    "Store `answer = 2*x_best**2 + (coef_x - coef_y - 3)*x_best + 9/4 + 3*coef_y/2`.",
])
