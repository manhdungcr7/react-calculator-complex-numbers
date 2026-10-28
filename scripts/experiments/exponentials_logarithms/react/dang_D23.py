# -*- coding: utf-8 -*-
"""Problem type D23: number of distinct real roots of p x^2 - q x + r ln(x+1) + c = 0.

Method of the source solution (p039 q35): domain x > -1; y' = 0 gives two critical points; the table of
variation: y goes from -infinity up to f(x1), down to f(x2), then up to +infinity; the sign of f(x1) and
f(x2) decides the number of roots.
"""
import re

import framework as fw

MA_DANG = "D23"
TITLE_VI = "số nghiệm phân biệt của $px^2-qx+\\ln\\left((x+1)^r\\right)+c=0$"
OPTION_VARIABLES = True
FREE_UNKNOWNS = {"x"}

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $px^2-qx+\ln\big((x+1)^r\big)+c=0$ ($c$ may be zero) and asks for the number of distinct real roots.

**Domain and the function.** The logarithm needs $x+1>0$, so $x>-1$, and then $\ln\big((x+1)^r\big)=r\ln(x+1)$. Let
$$f(x)=px^2-qx+r\ln(x+1)+c\quad(x>-1).$$
The roots of the equation are the zeros of $f$.

**Step 1: the derivative.** $f'(x)=2px-q+\dfrac{r}{x+1}$. Put everything over the common denominator $x+1$:
$$f'(x)=\frac{(2px-q)(x+1)+r}{x+1}=\frac{2px^2+(2p-q)x+(r-q)}{x+1}.$$
Since $x+1>0$ on the domain, the sign of $f'$ is the sign of the quadratic numerator $2px^2+(2p-q)x+(r-q)$. For this type of problem the numerator has two real roots, both larger than $-1$; call them $x_1<x_2$ (the critical points). (Original problem: $p=3$, $q=6$, $r=3$ gives $\dfrac{6x^2-3}{x+1}$, roots $\pm\dfrac{\sqrt2}{2}$.)

**Step 2: the sign of $f'$.** The leading coefficient $2p$ is positive, so the numerator is positive outside its roots and negative between them: $f'>0$ for $-1<x<x_1$, $f'<0$ for $x_1<x<x_2$, $f'>0$ for $x>x_2$.

**Step 3: table of variation.** At the left end of the domain, $x\to-1^+$, $\ln(x+1)\to-\infty$, so $f\to-\infty$. At the right end, $x\to+\infty$, the term $px^2$ wins and $f\to+\infty$. Hence $f$ rises from $-\infty$ up to the local maximum $f(x_1)$, falls down to the local minimum $f(x_2)$, then rises to $+\infty$.

**Step 4: counting the zeros.** On each of the three pieces $f$ is continuous and strictly monotone, so it has at most one zero on each piece.
- First piece (rising from $-\infty$ to $f(x_1)$): a zero exists exactly when $f(x_1)>0$.
- Second piece (falling from $f(x_1)$ to $f(x_2)$): a zero exists exactly when $f(x_1)>0>f(x_2)$.
- Third piece (rising from $f(x_2)$ to $+\infty$): a zero exists exactly when $f(x_2)<0$.
So if $f(x_1)>0$ and $f(x_2)<0$ there are **3 roots**. If $f(x_1)<0$ the function stays negative until after $x_2$, and if $f(x_2)>0$ it is positive after the first zero: in both cases there is **1 root**. (Original problem: $f(x_1)>0$ and $f(x_2)<0$, so 3 roots.)

**From the method to the Calculator.** `critical_points` lists the roots of the numerator; `x_first` and `x_second` are the smaller and the larger; `value_first` and `value_second` are $f(x_1)$ and $f(x_2)$ as decimals (a decimal is needed to see the sign of a value with a logarithm); `answer` is 3 when `value_first` is positive and `value_second` is negative, and 1 otherwise. The number of roots is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Phương trình $6x^2-25x+\\ln((x+1)^{4})-7=0$ có bao nhiêu nghiệm phân biệt?\n"
    "\n"
    "A. $2$.\n"
    "B. $4$.\n"
    "C. $3$.\n"
    "D. $5$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_READING = (
    "Reading the problem before any computation. The equation is $6x^2-25x+\\ln\\big((x+1)^{4}\\big)-7=0$. "
    "The coefficient of $x^2$ is six, so $p=6$. The number in $-25x$ is twenty five (2, 5), so $q=25$. "
    "The exponent inside the logarithm is four, so $r=4$. The constant at the end is seven with a minus sign, so $c=-7$. "
    "I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "The critical points are the roots of the numerator $2px^2+(2p-q)x+(r-q)$. With $p=6$, $q=25$, $r=4$ this is $2\\cdot6\\,x^2+(2\\cdot6-25)\\,x+(4-25)$. I send `critical_points = solve(2*6*x**2 + (2*6 - 25)*x + (4 - 25), x)`.",
    "The solver returns the two roots in a list whose order I cannot rely on. I need the smaller one, $x_1$, so I take the minimum of the two entries. I send `x_first = Min(critical_points[0], critical_points[1])`.",
    "Now the larger one, $x_2$, the maximum of the two entries. I send `x_second = Max(critical_points[0], critical_points[1])`.",
    "I need the sign of $f(x_1)$ where $f(x)=6x^2-25x+4\\ln(x+1)-7$. The logarithm makes an exact value hard to read, so I ask for a decimal with 20 digits, using the stored `x_first` in each place of $x$ and writing the constant $-7$ in parentheses with its sign. I send `value_first = N(6*x_first**2 - 25*x_first + 4*log(x_first + 1) + (-7), 20)`.",
    "Now the same for $f(x_2)$ with the stored `x_second`. I send `value_second = N(6*x_second**2 - 25*x_second + 4*log(x_second + 1) + (-7), 20)`.",
    "There are 3 roots when $f(x_1)>0$ and $f(x_2)<0$, and 1 root otherwise. A Piecewise decides this exactly from the two stored values, so I do not judge the signs myself. I send `answer = Piecewise((3, And(value_first > 0, value_second < 0)), (1, True))`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"\$(\d*)x\^2-(\d+)x\+\\ln\(\(x\+1\)\^\{(\d+)\}\)([+-]\d+)?=0\$", stem)
    if m:
        return int(m.group(1) or 1), int(m.group(2)), int(m.group(3)), int(m.group(4) or 0)
    m = re.search(r"\$(\d*)x\^2-(\d+)x\+\\ln\(x\+1\)\^(\d+)([+-]\d+)?=0\$", stem)
    return int(m.group(1) or 1), int(m.group(2)), int(m.group(3)), int(m.group(4) or 0)


def program(question_text):
    p, q, r, c = _parse(question_text)

    def f_at(name):
        return f"N({p}*{name}**2 - {q}*{name} + {r}*log({name} + 1) + ({c}), 20)"

    return [
        f"critical_points = solve(2*{p}*x**2 + (2*{p} - {q})*x + ({r} - {q}), x)",
        "x_first = Min(critical_points[0], critical_points[1])",
        "x_second = Max(critical_points[0], critical_points[1])",
        f"value_first = {f_at('x_first')}",
        f"value_second = {f_at('x_second')}",
        "answer = Piecewise((3, And(value_first > 0, value_second < 0)), (1, True))",
    ]


def brute_force(question_text):
    """Independent of the method: count the sign changes of f on (-1, +infinity) on a very fine grid."""
    import numpy as np
    p, q, r, c = _parse(question_text)
    xs = -1 + np.concatenate([np.logspace(-14, 0, 1500000), 1 + np.linspace(0, 60, 1500000)[1:]])
    f = p * xs ** 2 - q * xs + r * np.log(xs + 1) + c
    return int(np.sum(np.sign(f[:-1]) != np.sign(f[1:])))


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: $p$ (the coefficient of $x^2$, 1 if none is written), $q$ (the number in $-qx$), $r$ (the exponent in $\\ln\\big((x+1)^r\\big)$), and the constant $c$ with its sign (0 if none).",
    "Store `critical_points = solve(2*<p>*x**2 + (2*<p> - <q>)*x + (<r> - <q>), x)`, writing the numbers from the problem.",
    "Store `x_first = Min(critical_points[0], critical_points[1])`, then `x_second = Max(critical_points[0], critical_points[1])`.",
    "Store `value_first = N(<p>*x_first**2 - <q>*x_first + <r>*log(x_first + 1) + (<c>), 20)`, writing the constant $c$ in parentheses with its sign.",
    "Store `value_second = N(<p>*x_second**2 - <q>*x_second + <r>*log(x_second + 1) + (<c>), 20)` in the same way.",
    "Store `answer = Piecewise((3, And(value_first > 0, value_second < 0)), (1, True))`.",
], option_variables=True)
