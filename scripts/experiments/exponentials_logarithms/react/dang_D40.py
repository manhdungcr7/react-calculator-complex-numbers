# -*- coding: utf-8 -*-
"""Problem type D40: values of m for which log_b^2(bx) - (m + s) log_b x + m + c0 = 0 has two distinct roots in [1; b].

Method of the source solution (p088 q43): put u = log_b x; the equation factors as (u - 1)(u - (m - 1)) = 0;
x in [1; b] means u in [0; 1]; two distinct roots need 0 <= m - 1 < 1.

Written again for the generated variants: for every variant c0 = s - 4, so the second root is u2 = 1 + m + c0 and the
set of m is [-1 - c0 ; -c0).  Only c0 is needed, so the Calculator part is four commands.  The four options are
stored first as Calculator intervals (option_a ... option_d) and compared with the result by Eq (ends and brackets).
In the 90 questions the four options are always (c; +oo), [a; b), [a; b] and (a; b), in some order.
"""
import re

import framework as fw

MA_DANG = "D40"
TITLE_VI = "tìm $m$ để $\\log_b^2(bx)-(m+s)\\log_bx+m+c=0$ có hai nghiệm phân biệt thuộc $[1;b]$"
FREE_UNKNOWNS = set()
OPTION_VARIABLES = True
MERGE_READING = True

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

**What the problem gives and asks.** The equation is
$$\log_b^2(bx)-(m+s)\log_b x+m+c_0=0,$$
where $b>1$ is the base, $m$ is a real parameter, and $s$ and $c_0$ are numbers that carry their signs (for example $-(m-23)$ means $s=-23$, and $+m-27$ means $c_0=-27$; $+m+10$ means $c_0=+10$; a bare $+m$ means $c_0=0$). We must find the set of all values of $m$ for which the equation has **two distinct solutions $x$ in the interval $[1;b]$**. The answer is an interval of numbers, such as $[26;27)$.

**Step 1: a new variable.** The logarithm needs $x>0$. Put $u=\log_b x$, so $x=b^u$. Since $\log_b(bx)=\log_b b+\log_b x=1+u$, the square is $\log_b^2(bx)=(1+u)^2$.

**Step 2: expanding.** $(1+u)^2=u^2+2u+1$, so the equation becomes
$$u^2+2u+1-(m+s)\,u+m+c_0=0\iff u^2+(2-m-s)\,u+(1+m+c_0)=0 .$$

**Step 3: one root is always $u=1$.** Put $u=1$ in the left side: $1+(2-m-s)+(1+m+c_0)=4-s+c_0$. For every problem of this type $c_0=s-4$, so this value is $0$: **$u=1$ is a root for every $m$**. The product of the two roots of a quadratic equals its constant term (Viète), here $1+m+c_0$. One root is 1, so the other root is
$$u_2=1+m+c_0,\qquad\text{and the equation is }(u-1)(u-u_2)=0 .$$
(Original problem: $s=2$ and $c_0=-2$, so $u^2-mu+m-1=(u-1)(u-(m-1))$ and $u_2=m-1$.) Notice that, because $c_0=s-4$, the number $s$ is not needed any more: only $c_0$ matters.

**Step 4: back to $x$.** The base $b>1$, so $x=b^u$ is increasing and one to one: $x\in[1;b]\iff u\in[0;1]$, and two different $u$ give two different $x$. The root $u=1$ (that is $x=b$) is always inside the interval. The equation has two distinct solutions in $[1;b]$ exactly when the other root $u_2$ is also in $[0;1]$ and is different from 1:
$$0\le u_2<1 .$$

**Step 5: solving for $m$.** Replace $u_2=1+m+c_0$: $0\le1+m+c_0<1$. Subtract $1+c_0$ from the three parts:
$$-1-c_0\le m<-c_0 .$$
The left end is allowed (at $m=-1-c_0$ we get $u_2=0$, that is $x=1$, a second solution different from $x=b$). The right end is not allowed (at $m=-c_0$ we get $u_2=1$, a double root, so only one distinct solution). So the set of $m$ is the interval
$$\big[\,-1-c_0\ ;\ -c_0\,\big),$$
**closed on the left and open on the right**. (Original problem: $c_0=-2$, so $[1;2)$.)

**The four options.** In these problems the four options are always the same four kinds of interval: $[a;b)$ (closed left, open right), $[a;b]$ (closed both), $(a;b)$ (open both), and $(c;+\infty)$. Only the one that has exactly the ends $-1-c_0$ and $-c_0$ **and** the brackets $[\ )$ is correct. Do not judge the brackets by eye: each option is written as a Calculator interval according to its own brackets, and the Calculator compares it with the result.

**From the method to the Calculator.** `last_constant` is $c_0$, with its sign. `lower_end` is $-1-c_0$ and `upper_end` is $-c_0$. `answer` is the interval `Interval.Ropen(lower_end, upper_end)` (closed on the left, open on the right). Each stored option is compared with `answer` by `Eq`, which is `True` only if the two ends and the two brackets are all the same.
'''

EXAMPLE_QUESTION = (
    "Cho phương trình $\\log_{5}^2(5x)-(m-11)\\log_{5}x+m-15=0$ ($m$ là tham số thực). Tập hợp tất cả các giá trị của $m$ để phương trình đã cho có hai nghiệm phân biệt thuộc đoạn $[1;5]$ là\n"
    "\n"
    "A. $(14;15)$.\n"
    "B. $[14;15)$.\n"
    "C. $[14;15]$.\n"
    "D. $(15;+\\infty)$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_READING = (
    "Reading the problem, digit by digit. The equation is $\\log_5^2(5x)-(m-11)\\log_5 x+m-15=0$ and the interval is $[1;5]$. "
    "The only number the method needs is the constant at the very end of the equation, the number after $m$ in $+m-15$. "
    "It is fifteen, written 1, 5, and it has a minus sign, so $c_0=-15$. "
    "(If the end had been $+m+10$ the constant would be $+10$, and if it had been just $+m$ it would be 0.)")

EXAMPLE_THOUGHTS = [
    "The constant $c_0$ is the only data of the method: the lower end of the set of $m$ is $-1-c_0$ and the upper end is $-c_0$. I keep $c_0$ with its sign under the name `last_constant`. I send `last_constant = -15`.",
    "The constant is stored. The second root is $u_2=1+m+c_0$, and the condition $0\\le u_2$ means $m\\ge-1-c_0$, so the lower end of the set of $m$ is $-1-c_0$, computed from the stored `last_constant`. I send `lower_end = -1 - last_constant`.",
    "The condition $u_2<1$ means $m<-c_0$, so the upper end of the set of $m$ is $-c_0$. I send `upper_end = -last_constant`.",
    "Both ends are stored. The lower end is allowed ($u_2=0$ is fine) and the upper end is not ($u_2=1$ would give only one distinct solution), so the set is closed on the left and open on the right. In Calculator syntax that is `Interval.Ropen` of the two stored ends. I send `answer = Interval.Ropen(lower_end, upper_end)`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    s_match = re.search(r"-(?:\(m([+-]\d+)\)|m)\s*\\log", stem)
    s = s_match.group(1) or "0"
    c0 = re.search(r"\\log_\{?\d+\}?\s*x\s*\+\s*m\s*(?:([+-])\s*(\d+))?\s*=\s*0", stem)
    c0 = (c0.group(1) + c0.group(2)) if c0.group(1) else "0"
    return int(s), int(c0)


def program(question_text):
    _, c0 = _parse(question_text)
    return [
        f"last_constant = {c0}",
        "lower_end = -1 - last_constant",
        "upper_end = -last_constant",
        "answer = Interval.Ropen(lower_end, upper_end)",
    ]


def option_expressions(question_text):
    return {letter: fw.interval_constructor(body) for letter, body in fw.parse_options(question_text).items()}


BRACKET_WORDS = {"[": "square, the end is included", "]": "square, the end is included",
                 "(": "round, the end is excluded", ")": "round, the end is excluded"}


def option_store_thought(letter, raw, calc):
    """The Thought before each option is stored: copy the option as written, name its two brackets, then translate."""
    left, lo, hi, right = fw.parse_interval(raw)
    ends = f"the ends are {lo} and {hi}" if hi != "oo" else f"the left end is {lo} and the right end is infinity, written oo"
    return (f"Option {letter} is written ${raw}$. Its left bracket is `{left}` ({BRACKET_WORDS[left]}) and its right bracket "
            f"is `{right}` ({BRACKET_WORDS[right]}); {ends}. So in Calculator syntax it is `{calc}`.")


def example_check(calc, question_text):
    """Independent of the method: count the distinct roots in [1, b] of the ORIGINAL equation for sample m."""
    import numpy as np
    s, c0 = _parse(question_text)
    lo, hi = float(calc.ns["lower_end"]), float(calc.ns["upper_end"])

    def n_roots(m):
        # u^2 + (2 - m - s) u + 1 + m + c0 = 0 with u = log_b x in [0, 1]
        coeffs = [1.0, 2.0 - m - s, 1.0 + m + c0]
        r = np.roots(coeffs)
        r = [z.real for z in r if abs(z.imag) < 1e-9 and -1e-9 <= z.real <= 1 + 1e-9]
        return len({round(v, 9) for v in r})

    assert n_roots(lo) == 2 and n_roots(lo + 0.5) == 2 and n_roots(hi - 1e-3) == 2
    assert n_roots(hi) == 1 and n_roots(hi + 0.5) <= 1 and n_roots(lo - 0.5) <= 1


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing, the signed constant $c_0$: the number after $m$ in the term $+m+c_0$ at the very end of the equation, with its sign (for example $+m-27$ gives $c_0=-27$, $+m+10$ gives $c_0=10$, and $+m$ alone gives $c_0=0$). Nothing else is needed from the equation.",
    "Store `last_constant = <c0>`, keeping the sign.",
    "Store `lower_end = -1 - last_constant`, then `upper_end = -last_constant`.",
    "Store `answer = Interval.Ropen(lower_end, upper_end)`: the set of $m$ is closed on the left and open on the right.",
], option_variables=True, merge_reading=True,
    extra_option_note=fw.INTERVAL_NOTE + (
        "In the Thought before each option, first copy the option exactly as it is written in the problem, character by character, "
        "then name its left bracket and its right bracket (square or round), and only then write the Calculator interval. "
        "Look at each option separately: two options often differ only in one bracket, for example `[3;4]` and `[3;4)`. "))
