# -*- coding: utf-8 -*-
"""Problem type D65: minimum of P = x + y for positive reals x, y with
log_b((c - xy)/(px + qy)) = b*xy + px + qy - (b*c + 1).

Method of the source solution (p148 q47): f(t) = log_b t + t is increasing, so the equation says
b(c - xy) = px + qy; express y through x and minimise P(x) = x + y(x) with the derivative.
"""
import re

import framework as fw

MA_DANG = "D65"
TITLE_VI = "tìm $P_{\\min}$ của $P=x+y$ biết $\\log_b\\frac{c-xy}{px+qy}=b\\,xy+px+qy-m$"
FREE_UNKNOWNS = set()
OPTION_STYLE = "numeric"
BRUTE_TOLERANCE = 1e-6

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: positive reals $x,y$ satisfy $\log_b\dfrac{c-xy}{px+qy}=b\,xy+px+qy-m$ (with $m=bc+1$), and we want the minimum of $P=x+y$.

**Turning the equation into one relation.** Split the logarithm: $\log_b(c-xy)-\log_b(px+qy)=b\,xy+px+qy-m$. Since $m=bc+1$, we have $b\,xy-m=-b(c-xy)-1$, and $-1=-\log_b b$, so the equation can be written
$$\log_b\big[b(c-xy)\big]+b(c-xy)=\log_b(px+qy)+(px+qy).$$
Let $f(t)=\log_b t+t$ for $t>0$. Its derivative $f'(t)=\dfrac{1}{t\ln b}+1>0$, so $f$ is strictly increasing. The equation says $f\big(b(c-xy)\big)=f(px+qy)$, hence
$$b(c-xy)=px+qy\iff y=\frac{bc-px}{bx+q}.$$
Because $y>0$, we need $0<x<\dfrac{bc}{p}$.

**Minimising.** Now $P(x)=x+\dfrac{bc-px}{bx+q}$ on $\left(0;\dfrac{bc}{p}\right)$. Its derivative is
$$P'(x)=1-\frac{pq+b^2c}{(bx+q)^2}.$$
Set $w=\sqrt{pq+b^2c}$. Then $P'(x)=0$ when $bx+q=w$ (the other sign is negative and rejected), that is $x^*=\dfrac{w-q}{b}$. The derivative is negative before $x^*$ and positive after it, so $P$ has its minimum there, provided $x^*$ lies in $\left(0;\dfrac{bc}{p}\right)$.

**The minimum value.** At $x^*$ we have $bx^*+q=w$ and $y=\dfrac{bc-px^*}{w}$. Putting these together and using $w^2=pq+b^2c$, the value simplifies to
$$P_{\min}=\frac{2w-(p+q)}{b}.$$
Check on the original problem ($b=3$, $c=1$, $p=1$, $q=2$): $w=\sqrt{11}$ and $P_{\min}=\dfrac{2\sqrt{11}-3}{3}$.

**Conclusion.** We compute $w$, confirm that $x^*$ lies in the allowed interval, and compute $P_{\min}$ exactly. It is then compared with the four options; an option may be written in a different but equal form (for example $-\frac{15}{4}+\frac{\sqrt{2145}}{4}$ instead of $\frac{2\sqrt{2145}-30}{8}$), so each option is tested by its numerical value.
'''

EXAMPLE_QUESTION = (
    "Xét các số thực dương $x,y$ thỏa mãn $\\log_{5}\\dfrac{7-xy}{3x+4y}=5xy+3x+4y-36$. Tìm giá trị nhỏ nhất $P_{\\min}$ của $P=x+y$.\n"
    "\n"
    "A. $P_{\\min}=\\dfrac{7}{5} + \\dfrac{2 \\sqrt{187}}{5}$.\n"
    "B. $P_{\\min}=- \\dfrac{7}{5} + \\dfrac{2 \\sqrt{187}}{5}$.\n"
    "C. $P_{\\min}=- \\dfrac{7}{5} + \\dfrac{\\sqrt{187}}{5}$.\n"
    "D. $P_{\\min}=- \\dfrac{7}{10} + \\dfrac{\\sqrt{187}}{5}$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_THOUGHTS = [
    "I read the problem. The base is $b=5$, the constant in the numerator is $c=7$, the coefficients in the denominator are $p=3$ (of $x$) and $q=4$ (of $y$). The method uses $w=\\sqrt{pq+b^2c}$; I store it as `critical_root`, exact, with no decimals.",
    "The critical point is $x^*=\\dfrac{w-q}{b}$. I store it as `x_star`.",
    "The allowed interval for $x$ is $(0;\\,bc/p)$. I store its right end $bc/p$ as `x_limit`.",
    "The critical point must lie inside the interval: its distance to 0 and its distance to `x_limit` must both be positive, so I ask the Calculator whether the smaller of `x_star` and `x_limit - x_star` is above 0.",
    "The minimum value is $P_{\\min}=\\dfrac{2w-(p+q)}{b}$. I store it as `answer`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"\\log_\{?(\d+)\}?\\dfrac\{(\d+)-xy\}\{(\d*)x\+(\d*)y\}", stem)
    b, c = int(m.group(1)), int(m.group(2))
    p = int(m.group(3) or 1)
    q = int(m.group(4) or 1)
    s_ = re.search(r"=(\d+)xy\+", stem)
    mm = re.search(r"y-(\d+)\$\.", stem)
    return b, c, p, q, int(s_.group(1)), int(mm.group(1))


def program(question_text):
    b, c, p, q, _, _ = _parse(question_text)
    return [
        f"critical_root = sqrt({p}*{q} + {b}**2*{c})",
        f"x_star = (critical_root - {q})/{b}",
        f"x_limit = {b}*{c}/{p}",
        "domain_check = Min(x_star, x_limit - x_star) > 0",
        f"answer = (2*critical_root - ({p} + {q}))/{b}",
    ]


def brute_force(question_text):
    """Independent of the method: solve the ORIGINAL equation for y at each x and minimise x + y numerically."""
    import mpmath as mp
    mp.mp.dps = 30
    b, c, p, q, s, m = _parse(question_text)
    assert s == b and m == b * c + 1

    def y_of(x):
        lo, hi = mp.mpf(0), mp.mpf(c) / x - mp.mpf(10) ** -25
        f = lambda y: mp.log((c - x * y) / (p * x + q * y), b) - (s * x * y + p * x + q * y - m)
        if f(lo + mp.mpf(10) ** -25) < 0:
            return None
        for _ in range(200):
            mid = (lo + hi) / 2
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    def big_p(x):
        y = y_of(x)
        return None if y is None else x + y

    best = None
    xs = [mp.mpf(i) / 400 * (mp.mpf(b * c) / p) for i in range(1, 400)]
    values = [(big_p(x), x) for x in xs]
    values = [(v, x) for v, x in values if v is not None]
    v0, x0 = min(values)
    a_, b_ = x0 - mp.mpf(b * c) / p / 400, x0 + mp.mpf(b * c) / p / 400
    for _ in range(80):                      # golden section
        m1, m2 = a_ + (b_ - a_) * 0.382, a_ + (b_ - a_) * 0.618
        v1, v2 = big_p(m1), big_p(m2)
        if v1 is None or v2 is None:
            break
        if v1 < v2:
            b_ = m2
        else:
            a_ = m1
    return big_p((a_ + b_) / 2)


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the base $b$ of the logarithm; the constant $c$ in the numerator $c-xy$; the coefficient $p$ of $x$ and the coefficient $q$ of $y$ in the denominator $px+qy$ (a coefficient that is not written is 1).",
    "Store `critical_root = sqrt(<p>*<q> + <b>**2*<c>)`, writing the numbers from the problem. This is $w=\\sqrt{pq+b^2c}$, kept exact.",
    "Store `x_star = (critical_root - <q>)/<b>`, then `x_limit = <b>*<c>/<p>`.",
    "Store `domain_check = Min(x_star, x_limit - x_star) > 0`. It must be `True`.",
    "Store `answer = (2*critical_root - (<p> + <q>))/<b>`.",
], style="numeric", extra_option_note="The options are written as sums of fractions and square roots; write each one as a single expression, for example `-7/5 + 2*sqrt(187)/5`. ")
