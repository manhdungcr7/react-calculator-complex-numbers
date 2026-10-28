# -*- coding: utf-8 -*-
"""Problem type D16: values of m for which c^x + (d - m) e^x - m = 0 has a root in (0; 1).

Method of the source solution (p021 q20): isolate m = f(x) = (c^x + d e^x)/(e^x + 1); f is increasing, so
for x in (0; 1) the values of m fill the open interval (f(0); f(1)).
"""
import re

import framework as fw

MA_DANG = "D16"
TITLE_VI = "tìm $m$ để $c^x+(d-m)e^x-m=0$ có nghiệm trong $(0;1)$"
FREE_UNKNOWNS = set()
OPTION_STYLE = "boolean"

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $c^x+(d-m)\,e^x-m=0$ (with integers $c>e\ge2$ and $d$) and asks for the set of values of $m$ for which the equation has a root $x$ in the open interval $(0;1)$. (Here $e$ is a base, not Euler's number.)

**Separating the parameter.** Expand: $c^x+d\,e^x-m\,e^x-m=0$, so $m\,(e^x+1)=c^x+d\,e^x$, that is
$$m=f(x)=\frac{c^x+d\,e^x}{e^x+1}.$$
The equation has a root in $(0;1)$ exactly when $m$ is a value of $f$ on $(0;1)$.

**The function $f$ is increasing.** The numerator and the denominator are positive, and the derivative is
$$f'(x)=\frac{c^x e^x(\ln c-\ln e)+c^x\ln c+d\,e^x\ln e}{(e^x+1)^2}>0$$
because $c>e$. So $f$ is strictly increasing and continuous on $\mathbb R$.

**The values on the open interval.** For $0<x<1$ we have $f(0)<f(x)<f(1)$, and every value strictly between $f(0)$ and $f(1)$ is reached. So the set of $m$ is the **open** interval $\big(f(0);f(1)\big)$, with
$$f(0)=\frac{1+d}{2},\qquad f(1)=\frac{c+d\,e}{e+1}.$$

**Conclusion.** We compute the two ends exactly (as fractions). An option is correct only if its two ends equal $f(0)$ and $f(1)$ **and** both brackets are round: since $x$ is strictly between 0 and 1, the end values themselves are not reached, so an option with a square bracket can never be correct. The options are written like $\left(\frac{21}{2};\frac{74}{3}\right)$.
'''

EXAMPLE_QUESTION = (
    "Tìm tập hợp tất cả các giá trị của tham số thực $m$ để phương trình $89^x+(24-m)7^x-m=0$ có nghiệm thuộc khoảng $(0;1)$.\n"
    "\n"
    "A. $(12;\\dfrac{257}{8})$.\n"
    "B. $(\\dfrac{25}{2};\\dfrac{257}{8})$.\n"
    "C. $[\\dfrac{25}{2};\\dfrac{257}{8}]$.\n"
    "D. $(\\dfrac{25}{2};\\dfrac{265}{8})$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_THOUGHTS = [
    "I read the problem. The first base is $c=89$, the second base is $e=7$, and the number in $(24-m)$ is $d=24$. The lower end of the set is $f(0)=\\dfrac{1+d}{2}$. I store it as `lower_end`.",
    "The upper end is $f(1)=\\dfrac{c+d\\,e}{e+1}$ with $c=89$, $d=24$, $e=7$. I store it as `upper_end`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    c, d, e = map(int, re.search(r"(\d+)\^x\s*\+\s*\((\d+)\s*-\s*m\)\s*(\d+)\^x\s*-\s*m\s*=\s*0", stem).groups())
    return c, d, e


def program(question_text):
    c, d, e = _parse(question_text)
    return [
        f"lower_end = (1 + {d})/2",
        f"upper_end = ({c} + {d}*{e})/({e} + 1)",
    ]


def option_expressions(question_text):
    out = {}
    for letter, body in fw.parse_options(question_text).items():
        left, lo, hi, right = fw.parse_interval(body)
        if left == "[" or right == "]":
            out[letter] = "False"
        else:
            out[letter] = f"And(Eq(lower_end, {lo}), Eq(upper_end, {hi}))"
    return out


def example_check(calc, question_text):
    """Independent of the method: m is admissible when F(x) = c^x + (d-m)e^x - m changes sign in (0, 1)."""
    import numpy as np
    c, d, e = _parse(question_text)
    lo, hi = float(calc.ns["lower_end"]), float(calc.ns["upper_end"])
    xs = np.linspace(0, 1, 400001)[1:-1]

    def has_root(m):
        f = c ** xs + (d - m) * e ** xs - m
        return bool(np.any(np.sign(f[:-1]) != np.sign(f[1:])))

    delta = 1e-3
    assert has_root(lo + delta) and has_root(hi - delta) and has_root((lo + hi) / 2)
    assert not has_root(lo - delta) and not has_root(hi + delta)


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the base $c$ of the first term $c^x$; the number $d$ in $(d-m)$; and the base $e$ of the second term $(d-m)e^x$ (it is a number such as 17, not Euler's number).",
    "Store `lower_end = (1 + <d>)/2`.",
    "Store `upper_end = (<c> + <d>*<e>)/(<e> + 1)`.",
], style="boolean", extra_option_note="Each option is an interval of values of $m$ with two ends and two brackets. An option can be correct only if BOTH of its brackets are round (a square bracket `[` or `]` means the option is wrong, because the end values are not reached: for such an option write `test_X = False`). For an option with two round brackets write `test_X = And(Eq(lower_end, <its left end>), Eq(upper_end, <its right end>))`, where the ends are written in Calculator syntax (for example `21/2`). ")


def option_reason(question_text, letter):
    if option_expressions(question_text)[letter] == "False":
        return "It has a square bracket, so it can never be correct, because the end values are not reached. I write False."
    return None
