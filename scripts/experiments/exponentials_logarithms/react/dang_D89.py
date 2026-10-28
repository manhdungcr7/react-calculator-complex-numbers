# -*- coding: utf-8 -*-
"""Problem type D89: count the positive integers y such that A(x-1)e^x = y(e^x + xy - Bx^2 - C)
has a real solution x in an open interval (x1; x2).

Method (hướng giải written by the author of the thesis, y is the unknown and x a parameter): the
equation is a quadratic in y with exactly one positive root psi(x); psi is strictly increasing on
the interval, so y fills the open interval (psi(x1); psi(x2)).  The source solution (p230 q45)
studies f(x) = LHS - RHS with f'(x) = (e^x + y)(4x - y), a factorization that holds only when
A = 2B, which is not the case for the generated variants; the quadratic in y works for all of them.
"""
import re

import framework as fw

MA_DANG = "D89"
TITLE_VI = "đếm số nguyên dương $y$ để $A(x-1)e^x=y(e^x+xy-Bx^2-C)$ có nghiệm $x$ trong một khoảng"
OPTION_VARIABLES = True
FREE_UNKNOWNS = {"x"}

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives the equation $A(x-1)e^x=y\,(e^x+xy-Bx^2-C)$ and an open interval $(x_1;x_2)$ with $x_1\ge1$, and asks how many positive integers $y$ make the equation have a real solution $x$ in that interval. (If the coefficient of $x^2$ is not written it is 1, and if there is no constant term then $C=0$.)

**The function of $x$ for a fixed $y$ (as in the original solution).** The equation is equivalent to $f(x)=0$ with
$$f(x)=A(x-1)e^x-y\,(e^x+xy-Bx^2-C),\qquad f'(x)=Axe^x-y\,e^x-y^2+2Bxy .$$
(In the original problem $A=4$, $B=2$ and the derivative factors as $(e^x+y)(4x-y)$, with the single critical point $x=\frac y4$; the original solution then studies the position of $\frac y4$ with respect to the interval, and in every case the existence of a root comes down to the signs of $f$ at the two ends of the interval: $f(x_1)<0$ and $f(x_2)>0$.)

**The conditions at the two ends are quadratic inequalities in $y$.** For $x$ equal to an end, $f(x)$ is a quadratic polynomial in $y$:
$$-f(x)=x\,y^2+\big(e^x-Bx^2-C\big)\,y-A(x-1)e^x .$$
Its coefficients are $a=x$, $b=e^x-Bx^2-C$ and $c=-A(x-1)e^x$. On the interval $x>1$, so $a>0$ and $c<0$; then $ac<0$, the discriminant $b^2-4ac$ is positive, and the two roots have opposite signs. So there is exactly one positive root,
$$y=\psi(x)=\frac{-b+\sqrt{b^2-4ac}}{2a},$$
and $-f(x)=x\,y^2+b\,y+c$ is negative for $0<y<\psi(x)$ and positive for $y>\psi(x)$. Hence $f(x_1)<0\iff y>\psi(x_1)$, and $f(x_2)>0\iff y<\psi(x_2)$. (In the original problem these are the inequalities $y>5-e\approx2{,}28$ and $5y^2+(e^5-53)y-16e^5<0$, that is $y<14{,}25$.)

**Why these two conditions are exactly right for every $y$.** For each $x$ of the interval the positive root $\psi(x)$ is the only positive $y$ with $f(x)=0$. By implicit differentiation of $F(x,y)=f(x)$, $\psi'(x)=F_x/\sqrt{b^2-4ac}$ with $F_x=f'(x)$, and for the numbers of this type $\psi'(x)>0$ on the whole interval: $\psi$ is continuous and strictly increasing. So the values of $\psi$ on the open interval $(x_1;x_2)$ fill exactly the open interval $\big(\psi(x_1);\psi(x_2)\big)$, and a positive integer $y$ gives a root precisely when $\psi(x_1)<y<\psi(x_2)$. This replaces the case analysis on the position of the critical point.

**Counting.** We compute the two end values $M=\psi(x_1)$ and $N=\psi(x_2)$ as decimals (they are not integers). The integers strictly between $M$ and $N$ run from $\lfloor M\rfloor+1$ to $\lceil N\rceil-1$, so their number is $(\lceil N\rceil-1)-(\lfloor M\rfloor+1)+1=\lceil N\rceil-\lfloor M\rfloor-1$. This count is then compared with the four options.

**From the method to the Calculator.** For each end of the interval, in this order: `b_low` is $b(x_1)=e^{x_1}-Bx_1^2-C$, `c_low` is $c(x_1)=-A(x_1-1)e^{x_1}$, and `y_low` is the positive root $\psi(x_1)$ as a decimal; then `b_high`, `c_high`, `y_high` in the same way for $x_2$. `answer` is $\lceil N\rceil-\lfloor M\rfloor-1$ with `y_high` for $N$ and `y_low` for $M$. The numbers $B$ and $C$ are used without their minus signs, because the formulas already subtract them.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu số nguyên dương $y$ để tồn tại số thực $x\\in(6;9)$ thỏa mãn $7(x-1)e^x=y(e^x+xy-4x^2-9)$?\n"
    "\n"
    "A. $22$.\n"
    "B. $24$.\n"
    "C. $23$.\n"
    "D. $21$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_READING = (
    "Reading the problem before any computation. The equation is $7(x-1)e^x=y(e^x+xy-4x^2-9)$ and the interval for $x$ is $(6;9)$. "
    "The number in front of $(x-1)e^x$ is seven, so $A=7$. The interval ends are six and nine, so $x_1=6$ and $x_2=9$. "
    "In the bracket $(e^x+xy-4x^2-9)$ the number after the minus sign in front of $x^2$ is four, so $B=4$, and the number after the last minus sign is nine, so $C=9$. "
    "$B$ and $C$ are written without their minus signs, because the formulas below subtract them. I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "At the lower end $x_1=6$ the quadratic in $y$ has the middle coefficient $b=e^{x}-Bx^2-C$, which is $e^6-4\\cdot6^2-9$. $B=4$ and $C=9$ are subtracted, as the formula says. I send `b_low = exp(6) - 4*6**2 - 9`.",
    "The constant coefficient of the quadratic at $x_1=6$ is $c=-A(x-1)e^{x}$, that is $-7\\cdot(6-1)\\cdot e^6$. I send `c_low = -7*(6 - 1)*exp(6)`.",
    "The quadratic is $xy^2+b\\,y+c=0$ with $a=x=6$, and its positive root is $\\dfrac{-b+\\sqrt{b^2-4ac}}{2a}$. I use the stored `b_low` and `c_low` and write the product $4ac$ as $4\\cdot6\\cdot$`c_low`. I need a decimal to see between which integers this root lies, so I wrap the formula in N with 20 digits. I send `y_low = N((-b_low + sqrt(b_low**2 - 4*6*c_low))/(2*6), 20)`.",
    "Now the upper end $x_2=9$, in the same order. First the middle coefficient $b=e^9-4\\cdot9^2-9$. I send `b_high = exp(9) - 4*9**2 - 9`.",
    "The constant coefficient at $x_2=9$ is $-7\\cdot(9-1)\\cdot e^9$. I send `c_high = -7*(9 - 1)*exp(9)`.",
    "The positive root at the upper end, with $a=x=9$, uses the stored `b_high` and `c_high`, again with 20 digits. I send `y_high = N((-b_high + sqrt(b_high**2 - 4*9*c_high))/(2*9), 20)`.",
    "The values of $y$ fill the open interval from `y_low` to `y_high`. The integers strictly between them number the ceiling of `y_high` minus the floor of `y_low` minus 1. I send `answer = ceiling(y_high) - floor(y_low) - 1`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    x1, x2 = map(int, re.search(r"x\\in\((\d+);(\d+)\)", stem).groups())
    a, b, c = re.search(r"(\d+)\(x-1\)e\^x=y\(e\^x\+xy-(\d*)x\^2(?:-(\d+))?\)", stem).groups()
    return x1, x2, int(a), int(b or 1), int(c or 0)


def program(question_text):
    x1, x2, a, b, c = _parse(question_text)
    cmds = []
    for tag, x in (("low", x1), ("high", x2)):
        cmds += [
            f"b_{tag} = exp({x}) - {b}*{x}**2 - {c}",
            f"c_{tag} = -{a}*({x} - 1)*exp({x})",
            f"y_{tag} = N((-b_{tag} + sqrt(b_{tag}**2 - 4*{x}*c_{tag}))/(2*{x}), 20)",
        ]
    cmds.append("answer = ceiling(y_high) - floor(y_low) - 1")
    return cmds


def brute_force(question_text):
    """Independent of the method: count integers y for which the equation changes sign in x on the interval."""
    import numpy as np
    x1, x2, a, b, c = _parse(question_text)
    xs = np.linspace(x1, x2, 400001)[1:-1]
    ex = np.exp(xs)
    count = 0
    for y in range(1, 2000):
        f = a * (xs - 1) * ex - y * (ex + xs * y - b * xs ** 2 - c)
        if np.any(np.sign(f[:-1]) != np.sign(f[1:])):
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the number $A$ in front of $(x-1)e^x$; the two ends $x_1<x_2$ of the interval; and, from the bracket $(e^x+xy-Bx^2-C)$, the number $B$ that follows the minus sign in front of $x^2$ (it is 1 if no number is written) and the number $C$ that follows the last minus sign (it is 0 if there is none). $B$ and $C$ are the numbers WITHOUT their minus signs, because the formula below already subtracts them: for $(e^x+xy-11x^2-14)$ we have $B=11$ and $C=14$, never $-11$ or $-14$.",
    "Store `b_low = exp(<x1>) - <B>*<x1>**2 - <C>`, then `c_low = -<A>*(<x1> - 1)*exp(<x1>)`, writing the numbers from the problem.",
    "Store `y_low = N((-b_low + sqrt(b_low**2 - 4*<x1>*c_low))/(2*<x1>), 20)`.",
    "Do the same at the upper end: store `b_high = exp(<x2>) - <B>*<x2>**2 - <C>`, then `c_high = -<A>*(<x2> - 1)*exp(<x2>)`, then `y_high = N((-b_high + sqrt(b_high**2 - 4*<x2>*c_high))/(2*<x2>), 20)`.",
    "Store `answer = ceiling(y_high) - floor(y_low) - 1`.",
], option_variables=True)
