# -*- coding: utf-8 -*-
"""Problem type D22: given log_a b = t, compute P = log_{sqrt(b)/a} sqrt(b/a).

Method of the source solution (p038 q33): P = log_a sqrt(b/a) / log_a(sqrt(b)/a) = (1/2)(t - 1)/((1/2) t - 1) = (t-1)/(t-2).
"""
import re

import framework as fw

MA_DANG = "D22"
TITLE_VI = "tính $P=\\log_{\\sqrt b/a}\\sqrt{b/a}$ biết $\\log_ab=t$"
FREE_UNKNOWNS = set()
OPTION_STYLE = "numeric"

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: positive reals $a,b$ with $a\ne1$, $a\ne\sqrt b$ satisfy $\log_a b=t$ (a given number, possibly a square root), and we compute $P=\log_{\frac{\sqrt b}{a}}\sqrt{\dfrac ba}$.

**Moving everything to the base $a$.** By the change of base formula, with the base $a$,
$$P=\frac{\log_a\sqrt{\dfrac ba}}{\log_a\dfrac{\sqrt b}{a}}.$$

**The numerator.** $\log_a\sqrt{\dfrac ba}=\dfrac12\big(\log_a b-\log_a a\big)=\dfrac12(t-1)$.

**The denominator.** $\log_a\dfrac{\sqrt b}{a}=\log_a\sqrt b-\log_a a=\dfrac12\log_a b-1=\dfrac t2-1=\dfrac{t-2}{2}$. (It is not zero, because $a\ne\sqrt b$ means $t\ne2$.)

**The quotient.**
$$P=\frac{\frac12(t-1)}{\frac12(t-2)}=\frac{t-1}{t-2}.$$
For the original problem $t=\sqrt3$: $P=\dfrac{\sqrt3-1}{\sqrt3-2}=-1-\sqrt3$. The answer may be written in a different but equal form in the options (for example with a rationalised denominator), so each option is tested by its numerical value.
'''

EXAMPLE_QUESTION = (
    "Cho $a, b$ là các số thực dương thỏa mãn $a\\neq 1, a\\neq\\sqrt{b}$ và $\\log_a b=\\sqrt{5}$. Tính $P=\\log_{\\frac{\\sqrt{b}}{a}}\\sqrt{\\dfrac{b}{a}}$.\n"
    "\n"
    "A. $P=3 - \\sqrt{5}$.\n"
    "B. $P=- \\sqrt{5} - 3$.\n"
    "C. $P=\\sqrt{5} + 3$.\n"
    "D. $P=\\sqrt{5} + 1$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_THOUGHTS = [
    "I read the problem. The given value is $\\log_a b=\\sqrt5$, so $t=\\sqrt5$. I store it as `log_value`.",
    "The method gives $P=\\dfrac{t-1}{t-2}$ with $t=$ `log_value`. The Calculator keeps the exact value, so the result is exact.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"\\log_a\s*b\s*=\s*(\\sqrt\{(\d+)\}|\d+)", stem)
    return f"sqrt({m.group(2)})" if m.group(2) else m.group(1)


def program(question_text):
    return [
        f"log_value = {_parse(question_text)}",
        "answer = (log_value - 1)/(log_value - 2)",
    ]


def brute_force(question_text):
    """Independent of the method: pick a = 2 and b = 2^t and evaluate the original logarithm directly."""
    import mpmath as mp
    import sympy as sp
    mp.mp.dps = 40
    t = mp.mpf(str(sp.N(sp.sympify(_parse(question_text)), 40)))
    a = mp.mpf(2)
    b = a ** t
    return mp.log(mp.sqrt(b / a)) / mp.log(mp.sqrt(b) / a)


BRUTE_TOLERANCE = 1e-9

PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the value of $\\log_a b$ given in the problem (a whole number such as 95, or a square root such as $\\sqrt{156}$).",
    "Store `log_value = <that value>`, writing a square root as `sqrt(156)`.",
    "Store `answer = (log_value - 1)/(log_value - 2)`.",
], style="numeric", extra_option_note="The options are expressions with fractions and square roots; write each one as a single expression, for example `sqrt(39)/76 + 77/76`. ")
