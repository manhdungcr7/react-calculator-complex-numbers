# -*- coding: utf-8 -*-
"""Problem type D24: for y = (ln x)/x^n, which of four identities of the form
c*y' + x*y'' = +-k/x^m holds?

Method of the source solution (p041 q40): x*y = ln x; differentiate twice to get 2y' + x y'' = -1/x^2.
For a general power n the true identity is (n+1) y' + x y'' = -n/x^(n+1); the Calculator differentiates
exactly and tests each option as an identity in x.
"""
import re

import framework as fw

MA_DANG = "D24"
TITLE_VI = "mệnh đề đúng về $y=\\frac{\\ln x}{x^n}$ liên hệ $y',xy''$"
FREE_UNKNOWNS = {"x"}
OPTION_STYLE = "boolean"

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $y=\dfrac{\ln x}{x^{n}}$ ($x>0$; the power is 1 when only $x$ is written) and four statements of the form $c\,y'+x\,y''=\pm\dfrac{k}{x^{m}}$, and asks which one is true for every $x>0$.

**The idea of the original solution.** Multiply by the power of $x$: $x^n y=\ln x$. Differentiate both sides, then differentiate again, and use the product rule each time so that only $y$, $y'$, $y''$ and powers of $x$ appear. For $n=1$ this gives $y+xy'=\dfrac1x$ and then $2y'+xy''=-\dfrac1{x^2}$. For a general $n$ the same computation leads to
$$(n+1)\,y'+x\,y''=-\frac{n}{x^{\,n+1}}.$$

**How we check it with the Calculator.** To avoid any algebra slip, we let the Calculator do the differentiation exactly. First $y=\ln x\cdot x^{-n}$, then the first derivative $y'$, then the second derivative $y''$ (the command `diff(expression, x)` gives the exact derivative with respect to $x$). Each statement is then tested as an exact identity: `Eq(c*first_derivative + x*second_derivative, right side)` is `True` only if the left side minus the right side simplifies to zero for all $x$. Exactly one of the four statements is an identity.

**Writing the statements in Calculator syntax.** In every option, the symbol $y'$ becomes `first_derivative`, the symbol $y''$ becomes `second_derivative`, a coefficient is multiplied explicitly (for example $429y'$ becomes `429*first_derivative` and $xy''$ becomes `x*second_derivative`), a missing coefficient means 1, and a fraction such as $-\dfrac{428}{x^{429}}$ becomes `-428/x**429`.
'''

EXAMPLE_QUESTION = (
    "Cho hàm số $y=\\dfrac{\\ln x}{x^{4}}$, mệnh đề nào dưới đây đúng?\n"
    "\n"
    "A. $4y'+xy''=-\\dfrac{4}{x^{5}}$.\n"
    "B. $5y'+xy''=\\dfrac{4}{x^{5}}$.\n"
    "C. $5y'+xy''=-\\dfrac{4}{x^{5}}$.\n"
    "D. $y'+xy''=-\\dfrac{4}{x^{5}}$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_THOUGHTS = [
    "I read the problem. The function is $\\dfrac{\\ln x}{x^4}$, so the power is $n=4$. I write it as `log(x)/x**4` and store it as `function_y`.",
    "The first derivative of `function_y` with respect to $x$ is $y'$. I store it as `first_derivative`.",
    "The second derivative, the derivative of `first_derivative`, is $y''$. I store it as `second_derivative`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"\\dfrac\{\\ln x\}\{x(?:\^\{(\d+)\})?\}", stem)
    return int(m.group(1) or 1)


def program(question_text):
    n = _parse(question_text)
    return [
        f"function_y = log(x)/x**{n}",
        "first_derivative = diff(function_y, x)",
        "second_derivative = diff(first_derivative, x)",
    ]


def _side(text):
    s = text.replace("y''", "\x02").replace("y'", "\x01")
    s = re.sub(r"(?<=[0-9A-Za-z\)\}])([\x01\x02])", r"*\1", s)
    s = s.replace("\x02", "second_derivative").replace("\x01", "first_derivative")
    return fw.latex_to_calc(s)


def option_expressions(question_text):
    out = {}
    for letter, body in fw.parse_options(question_text).items():
        left, right = body.split("=")
        out[letter] = f"Eq({_side(left)}, {_side(right)})"
    return out


def example_check(calc, question_text):
    """Independent of the method: the stored derivatives agree with numerical differentiation at a point."""
    import mpmath as mp
    n = _parse(question_text)
    f = lambda t: mp.log(t) / t ** n
    x0 = mp.mpf("1.7")
    d1 = mp.diff(f, x0, 1)
    d2 = mp.diff(f, x0, 2)
    x = calc.ns["x"]
    assert abs(calc.ns["first_derivative"].subs(x, x0).evalf(25) - d1) < 1e-12
    assert abs(calc.ns["second_derivative"].subs(x, x0).evalf(25) - d2) < 1e-12


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the power $n$ of $x$ in the denominator of $y=\\dfrac{\\ln x}{x^{n}}$ (it is 1 when only $x$ is written).",
    "Store `function_y = log(x)/x**<n>`.",
    "Store `first_derivative = diff(function_y, x)`, then `second_derivative = diff(first_derivative, x)`.",
], style="boolean", extra_option_note="Each option is a statement about $y'$ and $y''$. In it, $y'$ is `first_derivative` and $y''$ is `second_derivative`, coefficients are multiplied explicitly (for example `5*first_derivative + x*second_derivative`), and the whole statement is written as `Eq(left side, right side)`, with a power such as $x^{5}$ written `x**5`. ")
