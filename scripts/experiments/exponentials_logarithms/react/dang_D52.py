# -*- coding: utf-8 -*-
"""Problem type D52: count the integers a for which at least k integers b of the open window (-L; L)
satisfy c^(a^2+b) <= d^(b-a) + e.

Method of the source solution (p119 q48): the inequality is rewritten with b alone, the solution set in
b is studied, and the integers a are found with a table (a from -5 to 5).  When c > d the solution set is
a prefix b <= alpha of the window, but when c < d it need not be (the right side grows with b), so every
integer b of the window is tested for every a (Count inside Count).
"""
import re

import framework as fw

MA_DANG = "D52"
TITLE_VI = "đếm số nguyên $a$ để có ít nhất $k$ số nguyên $b\\in(-L;L)$ thỏa $c^{a^2+b}\\le d^{b-a}+e$"
OPTION_VARIABLES = True
FREE_UNKNOWNS = set()

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives the inequality $c^{a^2+b}\le d^{\,b-a}+e$ (with integers $c,d\ge2$ and $e>0$), an open window $(-L;L)$ for $b$ and a number $k$, and asks how many integers $a$ have at least $k$ integers $b$ in the window satisfying the inequality.

**Looking at the inequality as a condition on $b$.** Divide by $c^{b}>0$:
$$c^{a^2}\le d^{-a}\left(\frac dc\right)^{b}+e\,c^{-b}.$$
When $c>d$, both terms on the right decrease as $b$ grows (the base $\frac dc<1$ and the base $\frac1c<1$), so the right side is a decreasing function of $b$ and the integers $b$ that satisfy the inequality form a prefix of the window, $b\le\alpha$. Then "at least $k$ integers" simply means that the first $k$ integers of the window, $-L+1,\dots,-L+k$, all satisfy it, which is decided by testing the single value $b=-L+k$. When $c<d$ the term $\left(\frac dc\right)^b$ grows with $b$, and the satisfying integers do not have to be a prefix of the window. A safe way that works in every case is to test **every integer $b$ of the window** for each $a$.

**Which $a$ matter.** The left side $c^{a^2+b}$ grows extremely fast with $|a|$, much faster than the right side $d^{b-a}+e$. For $|a|>10$ no integer $b$ of the window can satisfy the inequality, so it is enough to examine the integers $a$ from $-10$ to $10$ (this is the table of values used in the original solution).

**Counting.** The window contains the integers $b=-L+1,\dots,L-1$. For a fixed $a$, the number of window integers $b$ that satisfy $c^{a^2+b}\le d^{b-a}+e$ is counted; the value $a$ is accepted when this number is at least $k$. The answer is the number of accepted integers $a$ in $[-10,10]$.

**The Calculator can do this table for you.** The function `Count(condition, (n, low, high))` returns how many integers $n$ from `low` to `high` make the condition true, deciding the condition exactly for each integer. It can be nested: the inner `Count` runs over $b$ and, for each value of $a$, counts the window integers that satisfy the inequality; the outer `Count` runs over $a$ from $-10$ to $10$ and counts the values of $a$ for which the inner count is at least $k$. The condition of the outer `Count` is the inequality "inner count $\ge k$".

**From the method to the Calculator.** `first_b` and `last_b` are the first and the last integer of the open window, $-L+1$ and $L-1$. `answer` is the nested `Count` described above, with $c$, $d$, $e$ and $k$ written as numbers. The letters `a` and `b` inside it are the counting letters of the `Count` and need no earlier assignment. The number is compared with the four options.
'''

EXAMPLE_QUESTION = (
    "Có bao nhiêu số nguyên $a$ sao cho có ít nhất 3 số nguyên $b\\in(-7;7)$ thỏa mãn $2^{a^2+b}\\le 3^{b-a}+8$?\n"
    "\n"
    "A. $4$.\n"
    "B. $6$.\n"
    "C. $5$.\n"
    "D. $3$."
)
EXAMPLE_ANSWER = "C"

EXAMPLE_READING = (
    "Reading the problem before any computation. The inequality is $2^{a^2+b}\\le3^{b-a}+8$. "
    "The base on the left is two, so $c=2$; the base on the right is three, so $d=3$; the added constant is eight, so $e=8$. "
    "The required number of integers $b$ is three (\"at least 3\"), so $k=3$. The window is $b\\in(-7;7)$, so $L=7$. I have computed nothing yet.")

EXAMPLE_THOUGHTS = [
    "The window $(-7;7)$ is open, so $b=-7$ is not allowed and its first integer is $-7+1$. I send `first_b = -7 + 1`.",
    "In the same way the open window stops before $7$, so its last integer is $7-1$. I send `last_b = 7 - 1`.",
    "Now the table. For each integer $a$ from $-10$ to $10$ the inner Count runs over $b$ from `first_b` to `last_b` and counts how many $b$ satisfy $2^{a^2+b}\\le3^{b-a}+8$; the outer Count runs over $a$ and counts the values of $a$ for which that inner count is at least 3. The number of such $a$ is the answer. I send `answer = Count(Count(2**(a**2 + b) <= 3**(b - a) + 8, (b, first_b, last_b)) >= 3, (a, -10, 10))`.",
]


def _parse(question_text):
    stem = question_text.split("\n")[0]
    words = {"một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5, "sáu": 6, "bảy": 7, "tám": 8, "chín": 9}
    k_text = re.search(r"ít nhất (\d+|\w+) số nguyên", stem).group(1)
    k = int(k_text) if k_text.isdigit() else words[k_text]
    big_l = int(re.search(r"b\s*\\in\s*\(-(\d+);(\d+)\)", stem).group(1))
    c, d, e = map(int, re.search(r"(\d+)\^\{a\^2\+b\}\s*\\le\s*(\d+)\^\{b-a\}\s*\+\s*(\d+)", stem).groups())
    return k, big_l, c, d, e


def program(question_text):
    k, big_l, c, d, e = _parse(question_text)
    return [
        f"first_b = -{big_l} + 1",
        f"last_b = {big_l} - 1",
        f"answer = Count(Count({c}**(a**2 + b) <= {d}**(b - a) + {e}, (b, first_b, last_b)) >= {k}, (a, -10, 10))",
    ]


def brute_force(question_text):
    """Independent of the method: exact enumeration over a wide range of a and every b of the window."""
    from fractions import Fraction
    k, big_l, c, d, e = _parse(question_text)
    count = 0
    for a in range(-40, 41):
        n = sum(1 for b in range(-big_l + 1, big_l) if Fraction(c) ** (a * a + b) <= Fraction(d) ** (b - a) + e)
        if n >= k:
            count += 1
    return count


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the base $c$ on the left $c^{a^2+b}$; the base $d$ and the added constant $e$ on the right $d^{b-a}+e$; the number $k$ in \"at least $k$ integers $b$\"; and the number $L$ of the window $(-L;L)$.",
    "Store `first_b = -<L> + 1`, then `last_b = <L> - 1`, writing the number $L$ from the problem.",
    "Store `answer = Count(Count(<c>**(a**2 + b) <= <d>**(b - a) + <e>, (b, first_b, last_b)) >= <k>, (a, -10, 10))`, writing the numbers from the problem. The letters `a` and `b` here are the summation variables of the Count and need no earlier assignment.",
], option_variables=True)
