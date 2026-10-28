# -*- coding: utf-8 -*-
"""Problem type D46: minimum of P = x + k*y for a, b > 1, a^x = b^y = (ab)^e, and which interval contains it.

Method of the source solution (p105 q47): t = log_a b > 0, x = e(1+t), y = e(1+1/t), then AM-GM on
P = e(1+k) + e*t + e*k/t.
"""
import re

import framework as fw

MA_DANG = "D46"
TITLE_VI = "giá trị nhỏ nhất của $P=x+ky$ với $a^x=b^y=(ab)^e$ thuộc tập nào"
FREE_UNKNOWNS = set()
OPTION_STYLE = "boolean"

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: $a,b>1$ and $a^x=b^y=(ab)^{e}$ (the exponent $e$ is a positive fraction; the original problem writes $\sqrt{ab}$, which is $e=\frac12$). We want the minimum of $P=x+ky$ and then the interval, among four, that contains it.

**Expressing $x$ and $y$ with one variable.** Let $t=\log_a b$. Since $a,b>1$, $t>0$. From $a^x=(ab)^e$ we get $x=e\log_a(ab)=e(1+\log_a b)=e(1+t)$. From $b^y=(ab)^e$ we get $y=e\log_b(ab)=e(1+\log_b a)=e\left(1+\dfrac1t\right)$.

**The function to minimise.**
$$P=x+ky=e(1+t)+ke\left(1+\frac1t\right)=e(1+k)+e\,t+\frac{ek}{t}.$$

**AM-GM.** For $t>0$, $e\,t+\dfrac{ek}{t}\ge2\sqrt{e\,t\cdot\dfrac{ek}{t}}=2e\sqrt k$, with equality when $t=\sqrt k$ (that is $b=a^{\sqrt k}$, which is allowed). Hence
$$P_{\min}=e(1+k)+2e\sqrt k=e\left(1+\sqrt k\right)^2.$$
Check on the original problem: $e=\tfrac12$, $k=2$ gives $\tfrac12(1+\sqrt2)^2=\tfrac32+\sqrt2\approx2{,}91$, which lies in $\left[\tfrac52;3\right)$.

**Conclusion.** We compute $P_{\min}$ and then, for each option, test whether it lies in the interval: the left end must be below or equal to $P_{\min}$ (strictly below when the bracket is round) and the right end above it (a square bracket allows equality). Exactly one interval contains it.
'''

EXAMPLE_QUESTION = (
    "Xét các số thực dương $a,b,x,y$ thỏa mãn $a,b>1$ và $a^x=b^y=(ab)^{1/4}$. Giá trị nhỏ nhất của biểu thức $P=x+5y$ thuộc tập nào dưới đây?\n"
    "\n"
    "A. $\\left[2;\\dfrac{5}{2}\\right)$.\n"
    "B. $\\left[\\dfrac{3}{2};2\\right)$.\n"
    "C. $\\left[3;\\dfrac{7}{2}\\right)$.\n"
    "D. $\\left[\\dfrac{5}{2};3\\right)$."
)
EXAMPLE_ANSWER = "D"

EXAMPLE_THOUGHTS = [
    "I read the problem. The common value is $(ab)^{1/4}$, so the exponent is $e=\\dfrac14$. I store it as `exponent`.",
    "The expression is $P=x+5y$, so the coefficient of $y$ is $k=5$. I store it as `weight`.",
    "The minimum is $P_{\\min}=e\\left(1+\\sqrt k\\right)^2$, using the stored `exponent` and `weight`. This is an exact number, and it is stored as `answer`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"\(ab\)\^\{1/(\d+)\}", stem)
    e_text = f"1/{m.group(1)}" if m else "1/2"
    if not m:
        assert "\\sqrt{ab}" in stem, stem
    k = int(re.search(r"P\s*=\s*x\+(\d*)y", stem).group(1) or 1)
    return e_text, k


def program(question_text):
    e_text, k = _parse(question_text)
    return [
        f"exponent = {e_text}",
        f"weight = {k}",
        "answer = exponent*(1 + sqrt(weight))**2",
    ]


def option_expressions(question_text):
    return {letter: fw.interval_condition(body) for letter, body in fw.parse_options(question_text).items()}


def brute_force(question_text):
    """Independent of the method: minimise P over t = log_a b numerically, with x and y from the definitions."""
    import math

    from scipy.optimize import minimize_scalar
    e_text, k = _parse(question_text)
    e = eval(e_text)

    def p_of(s):                               # t = exp(s) > 0, take a = 2 and b = 2^t
        t = math.exp(s)
        log_a_ab = 1 + t                       # log_2(ab) / log_2(a)  with a = 2, b = 2^t
        x = e * log_a_ab
        y = e * (1 + t) / t                    # log_b(ab) = (1 + t)/t
        return x + k * y

    res = minimize_scalar(p_of, bounds=(-8, 8), method="bounded", options={"xatol": 1e-12})
    return res.fun


BRUTE_TOLERANCE = 1e-7

PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the exponent $e$ in $a^x=b^y=(ab)^{e}$ (for example $\\frac{1}{4}$; if it is written $\\sqrt{ab}$ then $e=\\frac12$), and the coefficient $k$ of $y$ in $P=x+ky$.",
    "Store `exponent = <e>`, then `weight = <k>`.",
    "Store `answer = exponent*(1 + sqrt(weight))**2`.",
], style="boolean", extra_option_note="The options are intervals, so for each one write the condition that `answer` lies in it: a square bracket `[` at the left end means `left <= answer`, a round bracket `(` means `left < answer`, and at the right end `)` means `answer < right` and `]` means `answer <= right`; join the two conditions with `And(...)`, for example the interval [5/2; 3) becomes `And(5/2 <= answer, answer < 3)`. ")
