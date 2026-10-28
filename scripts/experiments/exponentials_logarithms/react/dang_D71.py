# -*- coding: utf-8 -*-
"""Problem type D71: solve log_b(x+p) = 1 + log_b(x+q) (the second argument may be just x).

Method of the source solution (p173 q16): state the domain, write 1 = log_b b, merge the
right side into one logarithm, equate the arguments, solve the linear equation.
"""
import re

import framework as fw

MA_DANG = "D71"
TITLE_VI = "giải phương trình $\\log_b(x+p)=1+\\log_b(x+q)$"
OPTION_VARIABLES = True
FREE_UNKNOWNS = {"x"}

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives an equation $\log_b(x+p)=1+\log_b(x+q)$ with the same base $b$ on both sides (the second argument may be just $x$), and asks for its solution among four options.

**Domain.** A logarithm exists only for a positive argument, so we need $x+p>0$ and $x+q>0$ at the same time. Any solution found later is accepted only if it satisfies both inequalities.

**Merging the right side into one logarithm.** The number 1 is the logarithm of the base itself: $1=\log_b b$. Adding two logarithms with the same base multiplies their arguments, so
$$1+\log_b(x+q)=\log_b b+\log_b(x+q)=\log_b\big[b\,(x+q)\big].$$
The equation now has one logarithm on each side, both with the base $b$.

**Equating the arguments.** The logarithm to the base $b>1$ is strictly increasing, so two logarithms with the same base are equal exactly when their arguments are equal (both arguments are positive by the domain). The equation therefore becomes the linear equation
$$x+p=b\,(x+q).$$

**Solving the linear equation.** Moving everything to one side gives $(x+p)-b\,(x+q)=0$, that is $(1-b)\,x+(p-bq)=0$, a linear equation with exactly one solution $x=\dfrac{p-bq}{b-1}$. (Original problem: $b=2$, $p=1$, $q=-1$ gives $x=\dfrac{1+2}{1}=3$.)

**Checking the domain.** Substitute the solution into both arguments, $x+p$ and $x+q$, and confirm that both are positive; a solution that makes one of them zero or negative would be rejected. (Original problem: $3+1=4>0$ and $3-1=2>0$.)

**From the method to the Calculator.** `equation_roots` is the list of solutions of $(x+p)-b(x+q)=0$; `answer` is its single entry (here the name `answer` holds the solution $x$); `first_argument` and `second_argument` are $x+p$ and $x+q$ at that solution; `domain_check` asks whether the smaller of them is above 0. The solution is compared with the four options, which are written as $x=\dots$ (compare the number after the equals sign).
'''

EXAMPLE_QUESTION = (
    "Nghiệm của phương trình $\\log_{3}(x+4)=1+\\log_{3}(x-1)$ là\n"
    "\n"
    "A. $x=\\dfrac{5}{2}$.\n"
    "B. $x=- \\dfrac{7}{2}$.\n"
    "C. $x=\\dfrac{7}{2}$.\n"
    "D. $x=\\dfrac{9}{2}$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_READING = (
    "Reading the problem before any computation. The equation is $\\log_3(x+4)=1+\\log_3(x-1)$. "
    "The base of both logarithms is three, so $b=3$. The argument of the left logarithm is $x+4$ (the number added is four, with a plus sign). "
    "The argument of the logarithm on the right is $x-1$ (the number is one, with a minus sign). I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "The method writes $1=\\log_3 3$ and merges the right side, so the arguments must be equal: $x+4=3\\,(x-1)$. I move everything to one side, $(x+4)-3\\,(x-1)=0$, and ask the Calculator to solve it for $x$. I send `equation_roots = solve((x + 4) - 3*(x - 1), x)`.",
    "The solver returned a list with one solution. I take its first element and keep it under the name `answer`, which here holds the value of $x$. I send `answer = equation_roots[0]`.",
    "Now the domain. The first argument is $x+4$, evaluated at the stored solution. I send `first_argument = answer + 4`.",
    "The second argument is $x-1$ at the stored solution. I send `second_argument = answer - 1`.",
    "Both arguments must be positive, so the smaller of the two must be above 0. I ask whether the minimum of the two stored values is greater than 0, and I expect True. I send `domain_check = Min(first_argument, second_argument) > 0`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"\\log_\{?(\d+)\}?\((x(?:[+-]\d+)?)\)\s*=\s*1\s*\+\s*\\log_\{?\d+\}?\((x(?:[+-]\d+)?)\)", stem)
    base, first, second = m.group(1), m.group(2), m.group(3)
    return int(base), first, second


def program(question_text):
    base, first, second = _parse(question_text)
    to_answer = lambda e: fw.spaced(e.replace("x", "answer"))
    return [
        f"equation_roots = solve(({fw.spaced(first)}) - {base}*({fw.spaced(second)}), x)",
        "answer = equation_roots[0]",
        f"first_argument = {to_answer(first)}",
        f"second_argument = {to_answer(second)}",
        "domain_check = Min(first_argument, second_argument) > 0",
    ]


def brute_force(question_text):
    """Independent of the method: bisection on the original equation inside its domain."""
    import mpmath as mp
    base, first, second = _parse(question_text)
    p = eval(first.replace("x", "0"))
    q = eval(second.replace("x", "0"))
    f = lambda x: mp.log(x + p, base) - 1 - mp.log(x + q, base)
    lo = mp.mpf(max(-p, -q))
    a, b = lo + mp.mpf("1e-12"), lo + mp.mpf(10 ** 6)
    fa = f(a)
    assert (f(b) > 0) != (fa > 0)
    for _ in range(400):
        mid = (a + b) / 2
        fm = f(mid)
        if (fm > 0) == (fa > 0):
            a, fa = mid, fm
        else:
            b = mid
    return (a + b) / 2


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the base $b$ (the same in both logarithms), the argument of the left logarithm (for example $x+4$), and the argument of the logarithm on the right side (for example $x-1$, or just $x$).",
    "Store `equation_roots = solve((<left argument>) - <b>*(<right argument>), x)`, writing the two arguments and the base from the problem.",
    "Store `answer = equation_roots[0]`.",
    "Store `first_argument = <left argument with x replaced by answer>`, then `second_argument = <right argument with x replaced by answer>`.",
    "Store `domain_check = Min(first_argument, second_argument) > 0`. It must be `True`.",
], option_variables=True)
