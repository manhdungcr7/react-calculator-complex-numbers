# -*- coding: utf-8 -*-
"""Problem type D08: with a = log_p q and b = log_r q, express log_M(N) in terms of a and b.

Method of the source solution (p007 q19): change to the common base q; log_q p = 1/a and log_q r = 1/b;
split M and N into products of powers of p, q, r and add the logarithms.
"""
import re

import sympy as sp

import framework as fw

MA_DANG = "D08"
TITLE_VI = "biểu diễn $\\log_M N$ theo $a=\\log_pq$ và $b=\\log_rq$"
FREE_UNKNOWNS = {"a", "b"}

PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem defines $a=\log_p q$ and $b=\log_r q$ (the same number $q$ is the argument of both), and asks for $\log_M N$ expressed with $a$ and $b$, where $M$ and $N$ are products of powers of $p$, $q$, $r$ (in the original problem $\log_6 45$, with $6=2\cdot3$ and $45=3^2\cdot5$).

**Change to the base $q$.** By the change of base formula,
$$\log_M N=\frac{\log_q N}{\log_q M}.$$

**The three basic logarithms in the base $q$.**
- $\log_q q=1$.
- $\log_q p=\dfrac{1}{\log_p q}=\dfrac1a$.
- $\log_q r=\dfrac{1}{\log_r q}=\dfrac1b$.

**Splitting products and powers.** Write $M$ and $N$ as products of powers of $p$, $q$, $r$ (factor numbers if necessary). The logarithm of a product is the sum of the logarithms, and $\log_q u^k=k\log_q u$. So a product such as $p^{i}q^{j}r^{k}$ has
$$\log_q\big(p^{i}q^{j}r^{k}\big)=\frac{i}{a}+j+\frac{k}{b}.$$
For the original problem: $\log_3 45=\log_3(3^2\cdot5)=2+\dfrac1b$ and $\log_3 6=\log_3(2\cdot3)=\dfrac1a+1$, so $\log_6 45=\dfrac{2+\frac1b}{\frac1a+1}=\dfrac{a+2ab}{ab+b}$.

**Conclusion.** We compute the numerator $\log_q N$ and the denominator $\log_q M$ as expressions in $a$ and $b$ (the Calculator treats `a` and `b` as symbols), divide them, and test each option as an exact identity in $a$ and $b$: `Eq(answer, option)` is `True` only if the two expressions are equal for all $a$ and $b$.
'''

EXAMPLE_QUESTION = (
    "Đặt $a=\\log_{3}5,\\ b=\\log_{7}5$. Hãy biểu diễn $\\log_{3\\cdot 5^{2}}(5^{3}\\cdot 7)$ theo $a,b$.\n"
    "\n"
    "A. $\\log_{3\\cdot 5^{2}}(5^{3}\\cdot 7)=\\dfrac{a \\left(3 b + 1\\right)}{b \\left(2 a + 1\\right)}$.\n"
    "B. $\\log_{3\\cdot 5^{2}}(5^{3}\\cdot 7)=\\dfrac{a \\left(3 b + 1\\right)}{b \\left(2 a + 1\\right)} + 1$.\n"
    "C. $\\log_{3\\cdot 5^{2}}(5^{3}\\cdot 7)=\\dfrac{a \\left(3 b + 1\\right)}{b \\left(2 a + 1\\right)} - 1$.\n"
    "D. $\\log_{3\\cdot 5^{2}}(5^{3}\\cdot 7)=- \\dfrac{a \\left(3 b + 1\\right)}{b \\left(2 a + 1\\right)}$."
)
EXAMPLE_ANSWER = "A"

EXAMPLE_THOUGHTS = [
    "I read the problem. The definitions are $a=\\log_3 5$ and $b=\\log_7 5$, so the common argument is $q=5$, with $p=3$ and $r=7$. The base is $M=3\\cdot5^2$: in the base 5, $\\log_5 3=\\dfrac1a$ and $\\log_5 5^2=2$, so $\\log_5 M=\\dfrac1a+2$. I store it as `base_part`.",
    "The argument is $N=5^3\\cdot7$: $\\log_5 5^3=3$ and $\\log_5 7=\\dfrac1b$, so $\\log_5 N=3+\\dfrac1b$. I store it as `argument_part`.",
    "By the change of base formula $\\log_M N=\\dfrac{\\log_5 N}{\\log_5 M}$, which is `argument_part / base_part`.",
]


def _factors(text, primes_hint=None):
    """'3\\cdot 5^{2}' -> {3: 1, 5: 2}; a plain number such as '45' is factored into primes."""
    t = text.strip().strip("()")
    if "\\cdot" not in t and "^" not in t and t.isdigit():
        return {int(p): int(e) for p, e in sp.factorint(int(t)).items()}
    out = {}
    for piece in t.split("\\cdot"):
        m = re.fullmatch(r"\s*(\d+)\s*(?:\^\{?(\d+)\}?)?\s*", piece)
        base, exp = int(m.group(1)), int(m.group(2) or 1)
        out[base] = out.get(base, 0) + exp
    return out


def _parse(question_text):
    stem = question_text.split("\n")[0]
    m = re.search(r"a\s*=\s*\\log_\{?(\d+)\}?\s*(\d+)\s*,\s*(?:\\\s*)?b\s*=\s*\\log_\{?(\d+)\}?\s*(\d+)", stem)
    p, q, r, q2 = map(int, m.groups())
    assert q == q2
    start = stem.index("biểu diễn $\\log_") + len("biểu diễn $\\log_")
    if stem[start] == "{":
        end = fw._match_brace(stem, start)
        base_text = stem[start + 1:end]
        rest = stem[end + 1:]
    else:
        m2 = re.match(r"(\d+)", stem[start:])
        base_text = m2.group(1)
        rest = stem[start + len(base_text):]
    arg_text = re.match(r"\s*(\(.*?\)|\d+)\$", rest).group(1)
    return p, q, r, _factors(base_text), _factors(arg_text)


def _log_q(factors, p, q, r):
    terms = []
    for base in (p, q, r):
        e = factors.get(base, 0)
        if not e:
            continue
        if base == q:
            terms.append(str(e))
        elif base == p:
            terms.append("1/a" if e == 1 else f"{e}/a")
        else:
            terms.append("1/b" if e == 1 else f"{e}/b")
    assert set(factors) <= {p, q, r}, factors
    return " + ".join(terms)


def program(question_text):
    p, q, r, mf, nf = _parse(question_text)
    return [
        f"base_part = {_log_q(mf, p, q, r)}",
        f"argument_part = {_log_q(nf, p, q, r)}",
        "answer = argument_part/base_part",
    ]


def _expr(text):
    s = text.replace("\\left", "").replace("\\right", "")
    s = re.sub(r"([A-Za-z0-9])\s+\(", r"\1*(", s)
    c = fw.latex_to_calc(s)
    return c.replace("ab", "a*b").replace("ba", "b*a")


def option_expressions(question_text):
    out = {}
    for letter, body in fw.parse_options(question_text).items():
        if "=" in body:
            rhs = body.split("=", 1)[1]
        else:
            rhs = body[body.index("\\dfrac"):]
        out[letter] = _expr(rhs)
    return out


def brute_force(question_text):
    """Independent of the method: numeric values of a, b and of the original logarithm."""
    import mpmath as mp
    mp.mp.dps = 40
    p, q, r, mf, nf = _parse(question_text)
    a = mp.log(q) / mp.log(p)
    b = mp.log(q) / mp.log(r)
    big_m = mp.mpf(1)
    for base, e in mf.items():
        big_m *= mp.mpf(base) ** e
    big_n = mp.mpf(1)
    for base, e in nf.items():
        big_n *= mp.mpf(base) ** e
    return mp.log(big_n) / mp.log(big_m), a, b


def example_check(calc, question_text):
    import mpmath as mp
    value, a, b = brute_force(question_text)
    expr = calc.ns["answer"]
    sa, sb = calc.ns["a"], calc.ns["b"]
    got = expr.subs({sa: sp.Float(str(a), 40), sb: sp.Float(str(b), 40)}).evalf(30)
    assert abs(mp.mpf(str(got)) - value) < mp.mpf(10) ** -20


PART_NHIEMVU = fw.make_nhiemvu([
    "Read the problem and write down, without computing: the common argument $q$ of $a=\\log_p q$ and $b=\\log_r q$, and the numbers $p$ and $r$; then write the base $M$ and the argument $N$ of the logarithm to express as products of powers of $p$, $q$, $r$ (factor a plain number such as 45 into primes).",
    "Store `base_part = <expression>` for $\\log_q M$: each power $q^j$ contributes `j`, each power $p^i$ contributes `i/a`, each power $r^k$ contributes `k/b`; add the contributions (for example $3\\cdot5^2$ with $p=3$, $q=5$ gives `1/a + 2`).",
    "Store `argument_part = <expression>` for $\\log_q N$ in the same way.",
    "Store `answer = argument_part/base_part`. The letters `a` and `b` are symbols of the Calculator and need no earlier assignment.",
], extra_option_note="Each option is a formula in $a$ and $b$ after the equals sign (ignore the part before the equals sign). Write it in Calculator syntax with explicit multiplication, for example `a*(3*b + 1)/(b*(2*a + 1))`, and test it with `Eq(answer, <formula>)`; the Calculator decides whether the two expressions are identical. ")
