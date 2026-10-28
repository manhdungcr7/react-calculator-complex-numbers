# -*- coding: utf-8 -*-
"""Problem type D83: count the integers x with (c^(x^2) - c^(2x)) * [log_b(x + D) - e] <= 0.

Method of the source solution (p213 q39): domain x > -D; zeros of the two factors; a sign table gives the
solution set (-D; 0] together with the isolated point x = 2 (the zero of the logarithm factor is a double
root there); the integers of that set are counted.
"""
import re

import framework as fw

MA_DANG = "D83"
TITLE_VI = "đếm số nguyên $x$ thỏa $(c^{x^2}-c^{2x})[\\log_b(x+D)-e]\\le0$"
OPTION_VARIABLES = True
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives $\left(c^{x^2}-c^{2x}\right)\left[\log_b(x+D)-e\right]\le0$ (with $b,c>1$; in the original problem the first factor is written $3^{x^2}-9^x$, the same thing with $9^x=3^{2x}$) and asks how many integers $x$ satisfy it.

**Domain.** $x+D>0$, that is $x>-D$.

**Zeros of the two factors.**
- First factor: $c^{x^2}-c^{2x}=0\iff x^2=2x\iff x=0$ or $x=2$.
- Second factor: $\log_b(x+D)=e\iff x+D=b^e\iff x=b^e-D$. For the problems of this type this value is exactly $2$, the same as the second zero of the first factor. The Calculator computes $b^e-D$ and we check that it is 2.

**Sign table.** Since $c>1$, the first factor has the sign of $x^2-2x$: it is positive for $x<0$, zero at $0$, negative on $(0;2)$, zero at $2$, positive for $x>2$. Since $b>1$, the second factor is negative for $-D<x<2$, zero at $x=2$, positive for $x>2$. The product $f(x)$:
- on $(-D;0)$: positive times negative, so $f<0$;
- at $x=0$: $f=0$;
- on $(0;2)$: negative times negative, so $f>0$;
- at $x=2$: $f=0$ (a double zero, both factors vanish);
- on $(2;+\infty)$: positive times positive, so $f>0$.
So $f(x)\le0$ exactly on $(-D;0]\cup\{2\}$.

**Counting the integers.** The integers of $(-D;0]$ are $-D+1,-D+2,\dots,0$. From $-D+1$ up to $0$ there are $0-(-D+1)+1=D$ numbers, and the single point $x=2$ adds one more. The total is $D+1$. (Original problem: $D=30$, so $31$ integers.)

**From the method to the Calculator.** `log_zero` is $b^e-D$, the zero of the logarithm factor; `zero_check` confirms that it equals 2, which is the structure the sign table above relies on; `answer` is $D+1$. It is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu số nguyên $x$ thỏa mãn $\\left(6^{x^2}-6^{2x}\\right)\\left[\\log_{5}(x+123)-3\\right]\\le 0$?\n"
    "\n"
    "A. $123$.\n"
    "B. $124$.\n"
    "C. $125$.\n"
    "D. $122$."
)
EXAMPLE_ANSWER = "B"

EXAMPLE_READING = (
    "Reading the problem before any computation. The inequality is $\\left(6^{x^2}-6^{2x}\\right)\\left[\\log_5(x+123)-3\\right]\\le0$. "
    "The factor with the logarithm is $\\log_5(x+123)-3$: the base is five, so $b=5$; the number added to $x$ is one hundred twenty three, written 1, 2, 3, so $D=123$; "
    "the number subtracted is three, so $e=3$. The first factor has the base six, which only matters through its sign. I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "The logarithm factor is zero when $\\log_5(x+123)=3$, that is $x+123=5^3$, so $x=5^3-123$, with $b=5$, $e=3$ and $D=123$. I send `log_zero = 5**3 - 123`.",
    "The sign table needs the zero of the logarithm factor to be exactly 2, the same as the second zero of the first factor. I ask whether the stored `log_zero` equals 2. I send `zero_check = Eq(log_zero, 2)`.",
    "The check is True, so the product is non positive exactly on $(-D;0]$ together with the single point $x=2$. The integers from $-D+1$ to $0$ number $D$, and $x=2$ adds one, so the answer is $D+1$ with $D=123$. I send `answer = 123 + 1`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    b, d, e = map(int, re.search(r"\\log_\{?(\d+)\}?\(x\+(\d+)\)\s*-\s*(\d+)\\right\]", stem).groups())
    return b, d, e


def program(question_text):
    b, d, e = _parse(question_text)
    return [
        f"log_zero = {b}**{e} - {d}",
        "zero_check = Eq(log_zero, 2)",
        f"answer = {d} + 1",
    ]


def brute_force(question_text):
    """Independent of the method: test the original inequality on every integer with high precision logs."""
    import mpmath as mp
    mp.mp.dps = 60
    stem = question_text.split("\n")[0]
    c = int(re.search(r"\\left\((\d+)\^\{x\^2\}", stem).group(1))
    b, d, e = _parse(question_text)
    count = 0
    for x in range(-d + 1, 80):
        f1 = mp.mpf(c) ** (x * x) - mp.mpf(c) ** (2 * x)
        f2 = mp.log(x + d, b) - e
        if abs(f1) < mp.mpf(10) ** -40 or abs(f2) < mp.mpf(10) ** -40 or f1 * f2 <= 0:
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: from the logarithm factor $\\log_b(x+D)-e$, the base $b$, the number $D$ and the number $e$.",
    "Store `log_zero = <b>**<e> - <D>`, writing the numbers from the problem.",
    "Store `zero_check = Eq(log_zero, 2)`. It must be `True`.",
    "Store `answer = <D> + 1`.",
], option_variables=True)
