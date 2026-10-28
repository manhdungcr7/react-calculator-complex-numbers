# -*- coding: utf-8 -*-
"""Problem type D28: sum of the real roots of log_b x * log_{b^2} x * log_{b^3} x * log_{b^4} x = K.

Method of the source solution (p053 q27): x > 0; log_{b^k} x = (1/k) log_b x, so the product is
(1/24)(log_b x)^4 = K; (log_b x)^4 = 24K gives log_b x = +-c and the roots b^c and b^(-c).
"""
import re

import framework as fw

MA_DANG = "D28"
TITLE_VI = "tổng các nghiệm của $\\log_bx\\cdot\\log_{b^2}x\\cdot\\log_{b^3}x\\cdot\\log_{b^4}x=K$"
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $\log_b x\cdot\log_{b^2}x\cdot\log_{b^3}x\cdot\log_{b^4}x=K$ (the four bases are $b,b^2,b^3,b^4$) and asks for the sum of its real roots.

**Domain.** The logarithms need $x>0$.

**One logarithm for all four factors.** For the base $b^k$ we have $\log_{b^k}x=\dfrac1k\log_b x$. So the four factors are $\log_b x$, $\tfrac12\log_b x$, $\tfrac13\log_b x$, $\tfrac14\log_b x$, and the product is
$$\left(1\cdot\tfrac12\cdot\tfrac13\cdot\tfrac14\right)(\log_b x)^4=\tfrac1{24}(\log_b x)^4=K\iff(\log_b x)^4=24K.$$

**Solving the equation in $\log_b x$.** Let $c=(24K)^{1/4}>0$. A fourth power equal to $c^4$ means $\log_b x=c$ or $\log_b x=-c$, that is $x=b^{c}$ or $x=b^{-c}$. Both are positive, so both are roots.

**Conclusion.** The sum of the real roots is $b^{c}+b^{-c}$. For example, in the original problem $b=3$, $K=\frac23$: $24K=16$, $c=2$, and the roots are $9$ and $\frac19$ with sum $\frac{82}{9}$. The sum is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Tính tổng các nghiệm thực của phương trình $\\log_{6}x.\\log_{36}x.\\log_{216}x.\\log_{1296}x=\\dfrac{27}{8}$ bằng\n"
    "\n"
    "A. $0$.\n"
    "B. $\\dfrac{46655}{216}$.\n"
    "C. $216$.\n"
    "D. $\\dfrac{46657}{216}$."
)
EXAMPLE_ANSWER = "D"

EXAMPLE_THOUGHTS = [
    "I read the problem. The smallest base is $b=6$ (the other bases 36, 216, 1296 are its powers $6^2,6^3,6^4$), and the right side is $K=\\dfrac{27}{8}$. The product of the four logarithms is $\\frac{1}{24}(\\log_6 x)^4$, so $(\\log_6 x)^4=24K$. I compute $24K$ and store it as `fourth_power`.",
    "Now $c=(24K)^{1/4}$, the positive fourth root of `fourth_power`. I store it as `log_value`.",
    "The roots are $x=b^{c}$ and $x=b^{-c}$, with $b=6$, and their sum is $6^{c}+6^{-c}$, using the stored `log_value`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    bases = [int(b) for b in re.findall(r"\\log_\{?(\d+)\}?\s*x", stem)]
    assert len(bases) == 4 and bases == [bases[0] ** k for k in (1, 2, 3, 4)], bases
    m = re.search(r"=\s*\\dfrac\{(\d+)\}\{(\d+)\}", stem)
    if m:
        k_text = f"{m.group(1)}/{m.group(2)}"
    else:
        k_text = re.search(r"=\s*(\d+)\s*\$", stem).group(1)
    return bases[0], k_text


def program(question_text):
    b, k_text = _parse(question_text)
    k_part = f"({k_text})" if "/" in k_text else k_text
    return [
        f"fourth_power = 24*{k_part}",
        "log_value = fourth_power**(1/4)",
        f"answer = {b}**log_value + {b}**(-log_value)",
    ]


def brute_force(question_text):
    """Independent of the method: find the real roots of the original equation numerically and add them."""
    from fractions import Fraction

    import mpmath as mp
    mp.mp.dps = 40
    b, k_text = _parse(question_text)
    k = Fraction(k_text)
    kk = mp.mpf(k.numerator) / k.denominator
    # t = log_b x; the product of the four logarithms is t * (t/2) * (t/3) * (t/4) = t^4/24
    coeffs = [mp.mpf(1) / 24, 0, 0, 0, -kk]
    roots = [z.real for z in mp.polyroots(coeffs, maxsteps=500, extraprec=200) if abs(z.imag) < mp.mpf(10) ** -20]
    return sum(mp.mpf(b) ** r for r in roots)


BRUTE_TOLERANCE = 1e-9

PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the first base $b$ (the bases are $b,b^2,b^3,b^4$) and the right side $K$ (a fraction such as $\\frac{256}{24}$, or an integer).",
    "Store `fourth_power = 24*<K>`, writing the fraction $K$ in parentheses.",
    "Store `log_value = fourth_power**(1/4)`.",
    "Store `answer = <b>**log_value + <b>**(-log_value)`.",
])
