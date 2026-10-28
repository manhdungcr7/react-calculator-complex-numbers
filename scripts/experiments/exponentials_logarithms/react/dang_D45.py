# -*- coding: utf-8 -*-
"""Problem type D45: solution set of  a^(2x) + B a^x + D > 0  (written A^x + B*a^x + D > 0 with A = a^2).

Method of the source solution (p099 q31): factor / solve the quadratic in t = a^x > 0; since t > 0, only the
larger root matters: t > t_big, that is x > log_a t_big.  The solution set is stored as an interval and each
option, written as a Calculator interval, is compared with it (ends and brackets).
"""
import re

import framework as fw

MA_DANG = "D45"
TITLE_VI = "tập nghiệm của bất phương trình $a^{2x}+B\\cdot a^x+D>0$"
OPTION_VARIABLES = True
FREE_UNKNOWNS = {"t"}

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives an exponential inequality $A^x+B\cdot a^x+D>0$ where $A=a^2$ (for example $225^x+14\cdot15^x-2352>0$, where $225=15^2$), with a negative constant $D$, and asks for its solution set among four intervals.

**Step 1: a new variable.** Put $t=a^x$. An exponential is always positive, so $t>0$ for every real $x$. Because $A=a^2$, we have $A^x=(a^2)^x=(a^x)^2=t^2$. The inequality becomes the quadratic inequality
$$t^2+B\,t+D>0,\qquad t>0 .$$

**Step 2: the roots of the quadratic.** Let $t_1<t_2$ be the roots of $t^2+Bt+D=0$. A quadratic with positive leading coefficient is positive outside its roots: $t^2+Bt+D>0\iff t<t_1$ or $t>t_2$. The constant $D$ is negative, and the product of the roots is $D$, so the roots have opposite signs: $t_1<0<t_2$. (Original problem: $t^2+2t-3=(t-1)(t+3)$, roots $-3$ and $1$.)

**Step 3: only the positive part counts.** We need $t>0$. The branch $t<t_1$ would need a negative $t$, which is impossible, so the inequality is simply
$$t>t_2,\qquad t_2=\text{the larger root, which is positive.}$$

**Step 4: back to $x$.** $t=a^x>t_2$. The base $a>1$, so $a^x$ is increasing and $a^x>t_2\iff x>\log_a t_2=\dfrac{\ln t_2}{\ln a}$. The solution set is the open interval
$$\left(\frac{\ln t_2}{\ln a};+\infty\right),$$
with a **round** bracket on the left (the inequality is strict) and $+\infty$ on the right. (Original problem: $t_2=1$, $\log_3 1=0$, so the set is $(0;+\infty)$.)

**From the method to the Calculator.** `t_roots` lists the two roots of $t^2+Bt+D$; `t_big` is the larger one ($t_2$); `threshold` is $\dfrac{\log(t_2)}{\log(a)}$; `answer` is the interval `Interval.open(threshold, oo)`. Each option, written as a Calculator interval according to its own brackets, is compared with `answer` by `Eq`, which is `True` only if the ends and the brackets are all the same. The ends of the options are written with logarithms, for example $\dfrac{\log(42)}{\log(15)}$; an option such as $1+\dfrac{\log(42)}{\log(15)}$ has a different end and is therefore a different interval.
'''

EXAMPLE_QUESTION = (
    "Tập nghiệm của bất phương trình $169^x+12\\cdot13^x-85>0$ là\n"
    "\n"
    "A. $(-\\infty;\\dfrac{\\log{\\left(5 \\right)}}{\\log{\\left(13 \\right)}})$.\n"
    "B. $(1 + \\dfrac{\\log{\\left(5 \\right)}}{\\log{\\left(13 \\right)}};+\\infty)$.\n"
    "C. $(\\dfrac{\\log{\\left(5 \\right)}}{\\log{\\left(13 \\right)}};+\\infty)$.\n"
    "D. $[\\dfrac{\\log{\\left(5 \\right)}}{\\log{\\left(13 \\right)}};+\\infty)$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_READING = (
    "Reading the problem before any computation. The inequality is $169^x+12\\cdot13^x-85>0$. "
    "The base of the second power is thirteen (1, 3), so $a=13$, and the first base is 169, which is $13^2$, as expected. "
    "The coefficient in front of $13^x$ is twelve (1, 2) with a plus sign, so $B=+12$. "
    "The constant at the end is eighty five (8, 5) with a minus sign, so $D=-85$. I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "With $t=13^x$ the inequality is $t^2+12t-85>0$, so the boundary values of $t$ are the roots of $t^2+12t-85=0$. The signs are written as in the problem: plus 12, minus 85. I send `t_roots = solve(t**2 + 12*t - 85, t)`.",
    "The solver returns the two roots in a list, in an order I cannot rely on, so I do not use their positions. The inequality needs the larger root, the positive one, so I take the maximum of the two list entries. I send `t_big = Max(t_roots[0], t_roots[1])`.",
    "The solution is $t>t_2$, that is $13^x>t_2$, which means $x>\\log_{13}t_2$. By the change of base formula $\\log_{13}t_2=\\log(t_2)/\\log(13)$, with the stored `t_big` for $t_2$. I send `threshold = log(t_big)/log(13)`.",
    "The threshold is stored. The solution set is every $x$ above it; the inequality is strict, so the bracket on the left is round, and the right end is $+\\infty$. In Calculator syntax this is `Interval.open(threshold, oo)`. I send `answer = Interval.open(threshold, oo)`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"\$(\d+)\^x\s*([+-])\s*(\d+)\s*\\cdot\s*(\d+)\^x\s*([+-])\s*(\d+)\s*>\s*0\$", stem)
    big, sb, b, a, sd, d = m.groups()
    assert int(big) == int(a) ** 2, stem
    return int(a), int(b) * (1 if sb == "+" else -1), int(d) * (1 if sd == "+" else -1)


def _signed(n):
    return f"+ {n}" if n >= 0 else f"- {-n}"


def program(question_text):
    a, b, d = _parse(question_text)
    return [
        f"t_roots = solve(t**2 {_signed(b)}*t {_signed(d)}, t)",
        "t_big = Max(t_roots[0], t_roots[1])",
        f"threshold = log(t_big)/log({a})",
        "answer = Interval.open(threshold, oo)",
    ]


def _log_calc(text):
    """The options use \\log{\\left(42 \\right)}: turn it into log(42) before the general conversion."""
    return re.sub(r"\\log\{\\left\(\s*([^{}]*?)\s*\\right\)\}", r"log(\1)", text)


def option_expressions(question_text):
    out = {}
    for letter, body in fw.parse_options(question_text).items():
        out[letter] = fw.interval_constructor(_log_calc(body))
    return out


def example_check(calc, question_text):
    """Independent of the method: find the zero of the original inequality's left side numerically."""
    import mpmath as mp
    mp.mp.dps = 40
    a, b, d = _parse(question_text)
    f = lambda x: mp.mpf(a) ** (2 * x) + b * mp.mpf(a) ** x + d
    root = mp.findroot(f, 1)
    assert abs(mp.mpf(str(calc.ns["threshold"].evalf(30))) - root) < mp.mpf(10) ** -20
    assert f(root + 1) > 0 and f(root - 1) < 0


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the base $a$ of the second power $a^x$ (the first power is $a^2$ raised to $x$), the coefficient $B$ with its sign, and the constant $D$ with its sign.",
    "Store `t_roots = solve(t**2 + <B>*t + <D>, t)`, writing the signs as in the problem (for example `t**2 + 14*t - 2352`). The letter `t` stands for $a^x$ and needs no earlier assignment.",
    "Store `t_big = Max(t_roots[0], t_roots[1])`.",
    "Store `threshold = log(t_big)/log(<a>)`.",
    "Store `answer = Interval.open(threshold, oo)`: the solution set is every $x$ above the threshold, with a round bracket.",
], option_variables=True,
    extra_option_note=fw.INTERVAL_NOTE + "A logarithm written `\\log{\\left(42 \\right)}` is `log(42)` in Calculator syntax (for example `log(42)/log(15)`, or `1 + log(42)/log(15)`). ")
