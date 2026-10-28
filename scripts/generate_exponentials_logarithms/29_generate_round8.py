# Temporary staging helper for the requested round-8 work. Run from the
# slm-highschool-math-tutoring repository with --preview or --write.
import json
import random
import math
import re
import subprocess
import sys
from pathlib import Path
from importlib import import_module

REPO = Path(__file__).resolve().parents[2]
GEN_PATH = REPO / "scripts/generate_questions/29_generate_round8.py"
sys.path.insert(0, str(REPO / "scripts/generate_questions"))
utils = import_module("10_common_utils")
latex, render_mc, bump_until_distinct = utils.latex, utils.render_mc, utils.bump_until_distinct
import sympy as sp

ROWS = []


def add_row(code, name, source, prompt, answer, solution, params):
    ROWS.append({
        "id_goc": source, "ma_dang": code, "ten_dang": name,
        "nguon": "Nhân bản", "loai_bien_the": "chuan",
        "de_bai": prompt, "dap_an": answer, "loi_giai": solution,
        "params": {k: str(v) for k, v in params.items()},
    })


def mc_count_prompt(question, count):
    vals = bump_until_distinct([sp.Integer(count), count + 1, count - 1, count + 2])
    opts = [str(v) for v in vals]
    lines, answer = render_mc(opts, 0)
    return question + "\n\n" + "\n".join(lines), answer


# D08: use a=log_p(C), b=log_r(C), and derive the target by change of base.
def gen_D08(p, C, r, s, i, j):
    p, C, r, s, i, j = map(sp.Integer, (p, C, r, s, i, j))
    assert min(p, C, r) > 1 and p != C and r != C and p != r
    assert s > 0 and i > 0 and j > 0
    a, b = sp.symbols("a b", positive=True)
    correct = sp.factor(a * (i * b + j) / (b * (1 + s * a)))
    vals = bump_until_distinct([correct, correct + 1, correct - 1, -correct])
    opts = [latex(v) for v in vals]
    pow_c = str(C) if i == 1 else f"{C}^{{{i}}}"
    pow_r = str(r) if j == 1 else f"{r}^{{{j}}}"
    pow_den = str(C) if s == 1 else f"{C}^{{{s}}}"
    target = f"{p}\\cdot {pow_den}"
    argument = f"{pow_c}\\cdot {pow_r}"
    sa = "a" if s == 1 else f"{s}a"
    ilogc = r"\ln C" if i == 1 else f"{i}\\ln C"
    jlogr = r"\ln r" if j == 1 else f"{j}\\ln r"
    slogc = r"\ln C" if s == 1 else f"{s}\\ln C"
    question = (
        f"Đặt $a=\\log_{{{p}}}{C},\\ b=\\log_{{{r}}}{C}$. Hãy biểu diễn "
        f"$\\log_{{{target}}}({argument})$ theo $a,b$.\n\n"
    )
    lines, answer = render_mc(opts, 0, prefix=f"\\log_{{{target}}}({argument})=")
    prompt = question + "\n".join(lines)
    ib = "b" if i == 1 else f"{i}b"
    solution = (
        f"Đổi cơ số theo $\\ln C$: $\\ln p=\\dfrac{{\\ln C}}a$ và "
        f"$\\ln r=\\dfrac{{\\ln C}}b$. Do đó giá trị cần tìm bằng "
        f"$\\dfrac{{{ilogc}+{jlogr}}}{{\\ln p+{slogc}}}="
        f"\\dfrac{{a({ib}+{j})}}{{b(1+{sa})}}={latex(correct)}$."
    )
    return prompt, answer, solution, dict(p=p, C=C, r=r, s=s, i=i, j=j)


def verify_D08(params):
    p, C, r, s, i, j = [int(params[k]) for k in ("p", "C", "r", "s", "i", "j")]
    a, b = math.log(C, p), math.log(C, r)
    via_formula = a * (i * b + j) / (b * (1 + s * a))
    via_direct_log = math.log((C ** i) * (r ** j)) / math.log(p * (C ** s))
    return abs(via_formula - via_direct_log) < 1e-11


# D23: ln((x+1)^m) is written explicitly to avoid ambiguity in the source's
# compact notation ln(x+1)^3. Generation uses exact critical-point values;
# verification independently counts sign-changing roots by bisection.
def gen_D23(A, B, m, C):
    A, B, m, C = map(sp.Integer, (A, B, m, C))
    assert A > 0 and m > 0 and int(m) % 2 == 1
    A, B, m, C = int(A), int(B), int(m), int(C)
    x = sp.symbols("x", real=True)
    f = A * x**2 + B * x + m * sp.log(x + 1) + C
    deriv_num = sp.together(sp.diff(f, x)).as_numer_denom()[0]
    critical = sorted(
        [z for z in sp.solve(deriv_num, x) if z.is_real and z > -1],
        key=lambda z: float(z),
    )
    assert len(critical) == 2
    vals = [sp.N(f.subs(x, z), 40) for z in critical]
    assert vals[0] > 0 and vals[1] < 0
    linear, constant = 2*A + B, B + m
    deriv_num = f"{2*A}x^2"
    if linear:
        deriv_num += (("+" if linear > 0 else "-") + ("x" if abs(linear) == 1 else f"{abs(linear)}x"))
    if constant:
        deriv_num += f"{'+' if constant > 0 else '-'}{abs(constant)}"
    Aterm = "x^2" if A == 1 else f"{A}x^2"
    Cterm = f"{C:+d}" if C else ""
    Bterm = "+x" if B == 1 else ("-x" if B == -1 else f"{B:+d}x")
    question, answer = mc_count_prompt(
        f"Ph\u01b0\u01a1ng tr\u00ecnh ${Aterm}{Bterm}+\\ln((x+1)^{{{m}}}){Cterm}=0$ "
        "c\u00f3 bao nhi\u00eau nghi\u1ec7m ph\u00e2n bi\u1ec7t?", 3
    )
    solution = (
        f"\u0110i\u1ec1u ki\u1ec7n $x>-1$. X\u00e9t $f(x)={Aterm}{Bterm}+{m}\\ln(x+1){Cterm}$. "
        f"Ta c\u00f3 $f'(x)=\\dfrac{{{deriv_num}}}{{x+1}}$. D\u1ea5u c\u1ee7a \u0111\u1ea1o h\u00e0m l\u1ea7n l\u01b0\u1ee3t l\u00e0 $+,-,+$; "
        f"t\u1ea1i $x={sp.latex(critical[0])}$, f \u0111\u1ea1t c\u1ef1c \u0111\u1ea1i x\u1ea5p x\u1ec9 {float(vals[0]):.3f}>0, "
        f"c\u00f2n t\u1ea1i $x={sp.latex(critical[1])}$, f \u0111\u1ea1t c\u1ef1c ti\u1ec3u x\u1ea5p x\u1ec9 {float(vals[1]):.3f}<0. "
        "K\u1ebft h\u1ee3p $\\lim_{x\\to-1^+}f(x)=-\\infty$ v\u00e0 "
        "$\\lim_{x\\to+\\infty}f(x)=+\\infty$, ph\u01b0\u01a1ng tr\u00ecnh c\u00f3 \u0111\u00fang 3 nghi\u1ec7m ph\u00e2n bi\u1ec7t."
    )
    return question, answer, solution, dict(A=A, B=B, m=m, C=C)


def verify_D23(params):
    import mpmath as mp
    A, B, m, C = [int(params[k]) for k in ("A", "B", "m", "C")]
    if A <= 0 or m <= 0 or m % 2 != 1:
        return False
    # f'(x) has the sign of this quadratic on x>-1. Two critical points
    # plus opposite signs at the local maximum/minimum prove exactly 3 roots:
    # f(-1+)=-infinity, max>0, min<0, f(+infinity)=+infinity.
    x = sp.symbols("x", real=True)
    numerator = 2*A*x**2 + (2*A+B)*x + (B+m)
    roots = sorted([r for r in sp.solve(numerator, x)
                    if r.is_real and r > -1], key=lambda r: float(r))
    if len(roots) != 2:
        return False
    with mp.workdps(100):
        rv = [mp.mpf(str(sp.N(r, 95))) for r in roots]
        fv = [A*z*z + B*z + m*mp.log(z+1) + C for z in rv]
        # The sign margins in this dataset are comfortably separated from 0;
        # reject borderline cases rather than trusting a rounded sign.
        margin = mp.mpf('1e-40')
        return fv[0] > margin and fv[1] < -margin


# D47: choose log bases with log_p(q)=m/n. Substituting x+y=u^n
# turns the equation into an integer polynomial; Sturm root counts give the
# generated answer. Verification searches the original continuous variable t.
def _d47_exact_x_values(m, n):
    u = sp.symbols("u")
    r = sp.Rational(m, n)
    tmax = 2 ** sp.Rational(n, 2 * n - m)
    tmax_f = float(tmax)
    bound = (tmax_f + math.sqrt(2 * tmax_f ** float(r))) / 2
    edge = math.ceil(bound) + 1
    values = []
    for xv in range(-edge, edge + 1):
        expr = u ** (2 * n) - u ** m - 2 * xv * u**n + 2 * xv*xv
        poly = sp.Poly(expr, u)
        while poly.eval(0) == 0:
            poly = poly.exquo(sp.Poly(u, u))
        if poly.count_roots(0, sp.oo) > 0:
            values.append(xv)
    return values, bound


def gen_D47(m, n):
    m, n = int(m), int(n)
    assert 1 < m / n < 2 and math.gcd(m, n) == 1
    p, q = 2**n, 2**m
    xs, _ = _d47_exact_x_values(m, n)
    count = len(xs)
    assert count > 0
    question, answer = mc_count_prompt(
        f"Có bao nhiêu số nguyên $x$ để tồn tại số thực $y$ thỏa mãn "
        f"$\\log_{{{p}}}(x+y)=\\log_{{{q}}}(x^2+y^2)$?", count
    )
    bound = (2 ** (n / (2 * n - m)) + math.sqrt(2 * (2 ** (n / (2 * n - m))) ** (m / n))) / 2
    solution = (
        f"\u0110\u1eb7t $t=x+y>0$. Ph\u01b0\u01a1ng tr\u00ecnh t\u01b0\u01a1ng \u0111\u01b0\u01a1ng "
        f"$x^2+(t-x)^2=t^{{{m}/{n}}}$. Ta c\u00f3 "
        f"$x^2+(t-x)^2=2(x-t/2)^2+t^2/2$ n\u00ean "
        f"$t^2/2\\le t^{{{m}/{n}}}$, suy ra "
        f"$t\\le 2^{{{n}/{2*n-m}}}$. M\u1eb7t kh\u00e1c, "
        f"$2(x-t/2)^2\\le t^{{{m}/{n}}}$, do \u0111\u00f3 "
        f"$|x|\\le\\dfrac{{2^{{{n}/{2*n-m}}}+"
        f"\\sqrt{{2(2^{{{n}/{2*n-m}}})^{{{m}/{n}}}}}}}{{2}}"
        f"\\approx {bound:.6f}$. V\u00ec v\u1eady ch\u1ec9 c\u1ea7n x\u00e9t h\u1eefu h\u1ea1n c\u00e1c s\u1ed1 nguy\u00ean $x$ "
        f"trong kho\u1ea3ng n\u00e0y. \u0110\u1eb7t $t=u^{{{n}}}$ v\u1edbi $u>0$, ph\u01b0\u01a1ng tr\u00ecnh tr\u1edf th\u00e0nh "
        f"$u^{{{2*n}}}-u^{{{m}}}-2xu^{{{n}}}+2x^2=0$. D\u00f9ng \u0111\u1ecbnh l\u00fd Sturm "
        f"\u0111\u1ec3 \u0111\u1ebfm nghi\u1ec7m d\u01b0\u01a1ng c\u1ee7a \u0111a th\u1ee9c \u1ee9ng v\u1edbi t\u1eebng gi\u00e1 tr\u1ecb nguy\u00ean $x$ trong "
        f"kho\u1ea3ng tr\u00ean, ta \u0111\u01b0\u1ee3c $x\\in\\{{{','.join(map(str, xs))}\\}}$. "
        f"V\u1eady c\u00f3 {count} gi\u00e1 tr\u1ecb nguy\u00ean c\u1ee7a $x$."
    )
    return question, answer, solution, dict(m=m, n=n, p=p, q=q, xs=xs)


def verify_D47(params):
    # Independent exact check: enumerate the finite x-range from the proved
    # bound, then count positive roots of each transformed polynomial by Sturm.
    import sympy as sp
    m, n = int(params["m"]), int(params["n"])
    if not (1 < m / n < 2 and math.gcd(m, n) == 1):
        return False
    u = sp.symbols("u")
    tmax = sp.Pow(2, sp.Rational(n, 2*n-m))
    bound = (tmax + sp.sqrt(2*tmax**sp.Rational(m,n))) / 2
    edge = int(sp.ceiling(bound)) + 1
    found = []
    for xv in range(-edge, edge+1):
        poly = sp.Poly(u**(2*n) - u**m - 2*xv*u**n + 2*xv*xv, u)
        while poly.eval(0) == 0:
            poly = poly.exquo(sp.Poly(u,u))
        if poly.count_roots(0, sp.oo) > 0:
            found.append(xv)
    expected = params["xs"]
    if isinstance(expected, str):
        import ast
        expected = ast.literal_eval(expected)
    return found == [int(v) for v in expected]


# D52: enumerate exact rational inequalities for each a in a proven finite
# interval. The separate verifier checks in log space with high precision and
# uses a wider interval; the tail cutoff follows from the quadratic exponent.
def _d52_holds_exact(p, q, C, a, b):
    from fractions import Fraction
    return Fraction(p) ** (a*a+b) <= Fraction(q) ** (b-a) + C


def _d52_scan(p, q, C, N, k):
    bs = range(-N + 1, N)
    for M in range(2, 250):
        tails_fail = all(
            not _d52_holds_exact(p, q, C, M, b)
            and not _d52_holds_exact(p, q, C, -M, b)
            for b in bs
        )
        if tails_fail and p ** (2*M + 1) - 1 >= q - 1:
            break
    else:
        raise AssertionError("Could not establish a finite a-range")
    good = [a for a in range(-M, M + 1)
            if sum(_d52_holds_exact(p, q, C, a, b) for b in bs) >= k]
    return M, good


def gen_D52(p, q, C, N, k):
    p, q, C, N, k = map(int, (p, q, C, N, k))
    assert p > 1 and q > 1 and C > 0 and N > 1 and k > 0
    M, good = _d52_scan(p, q, C, N, k)
    count = len(good)
    assert 0 < count < 100
    question, answer = mc_count_prompt(
        f"Có bao nhiêu số nguyên $a$ sao cho có ít nhất {k} số nguyên "
        f"$b\\in(-{N};{N})$ thỏa mãn ${p}^{{a^2+b}}\\le {q}^{{b-a}}+{C}$?", count
    )
    solution = (
        f"V\u1edbi m\u1ed7i s\u1ed1 nguy\u00ean $a$, \u0111\u1ebfm c\u00e1c s\u1ed1 nguy\u00ean "
        f"$b\\in\\{{{-N+1},\\ldots,{N-1}\\}}$ th\u1ecfa b\u1ea5t \u0111\u1eb3ng th\u1ee9c "
        f"b\u1eb1ng ph\u00e9p t\u00ednh ch\u00ednh x\u00e1c. Ch\u1ecdn $M={M}$ sao cho "
        f"${p}^{{2M+1}}\\ge {q}$ v\u00e0 t\u1ea1i $a=M$ c\u0169ng nh\u01b0 $a=-M$ "
        f"kh\u00f4ng c\u00f3 gi\u00e1 tr\u1ecb $b$ n\u00e0o th\u1ecfa b\u1ea5t \u0111\u1eb3ng th\u1ee9c. "
        f"N\u1ebfu $a>M$, v\u1ebf tr\u00e1i t\u0103ng khi $a$ t\u0103ng, c\u00f2n v\u1ebf ph\u1ea3i gi\u1ea3m; "
        f"v\u00ec v\u1eady kh\u00f4ng c\u00f3 nghi\u1ec7m ph\u00eda tr\u00ean $M$. "
        f"N\u1ebfu $a\\le-M$, khi thay $a$ b\u1eb1ng $a-1$, v\u1ebf tr\u00e1i nh\u00e2n v\u1edbi "
        f"${p}^{{-2a+1}}\\ge {p}^{{2M+1}}\\ge {q}$, trong khi v\u1ebf ph\u1ea3i nh\u00e2n "
        f"kh\u00f4ng qu\u00e1 ${q}$. Do \u0111\u00f3 t\u1ec9 s\u1ed1 hai v\u1ebf kh\u00f4ng gi\u1ea3m khi \u0111i xa h\u01a1n v\u1ec1 ph\u00eda \u00e2m; "
        f"c\u00e1c gi\u00e1 tr\u1ecb $b$ th\u1ecfa \u1edf ngo\u00e0i $[-M,M]$ kh\u00f4ng th\u1ec3 \u0111\u1ea1t ng\u01b0\u1ee1ng {k}; m\u1ed7i l\u1ea7n t\u0103ng |a|, v\u1ebf ph\u1ea3i t\u0103ng kh\u00f4ng qu\u00e1 h\u1ec7 s\u1ed1 {q} l\u1ea7n. "
        f"V\u00ec th\u1ebf ch\u1ec9 c\u1ea7n ki\u1ec3m tra c\u00e1c s\u1ed1 nguy\u00ean $a$ trong $[-M,M]$; "
        f"\u0111i\u1ec1u ki\u1ec7n \u0111\u00fang v\u1edbi $a\\in\\{{{','.join(map(str, good))}\\}}$, "
        f"c\u00f3 {count} gi\u00e1 tr\u1ecb."
    )
    return question, answer, solution, dict(p=p, q=q, C=C, N=N, k=k, M=M, good=good)


def verify_D52(params):
    from fractions import Fraction
    import ast
    p, q, C, N, k, M = [int(params[x]) for x in ("p", "q", "C", "N", "k", "M")]
    if not (p > 1 and q > 1 and C > 0 and N > 1 and k > 0 and M > 0):
        return False
    bs = range(-N + 1, N)
    def exact_hits(a):
        return sum(Fraction(p) ** (a*a+b) <= Fraction(q) ** (b-a) + C for b in bs)
    # Check every candidate a and b exactly as written in the question.
    found = [a for a in range(-M, M+1) if exact_hits(a) >= k]
    expected = params["good"]
    if isinstance(expected, str):
        expected = ast.literal_eval(expected)
    if found != [int(v) for v in expected]:
        return False
    # At both cutoff values no b satisfies the inequality. Beyond +M the
    # left side increases and the right side decreases. Beyond -M, moving
    # one step left multiplies the left side by at least q while the right
    # side grows by at most q, so no new solutions can appear in either tail.
    if exact_hits(M) != 0 or exact_hits(-M) != 0:
        return False
    return p ** (2*M+1) >= q


# D57: choose bases 2 and 4 and set C=T^2(T+2). The logarithmic threshold
# is exactly T; generation counts lattice points in a circle, verification
# checks the original logarithmic inequality directly for all possible pairs.
def gen_D57(T):
    T = int(T)
    assert T >= 2
    C = T*T*(T+2)
    count = sum(2*math.isqrt(x*(T-x)) + 1 for x in range(1, T+1))
    question, answer = mc_count_prompt(
        f"Có bao nhiêu cặp số nguyên $(x;y)$ thỏa mãn $x>0$ và\n"
        f"$\\log_2(x^2+y^2+x)+\\log_4(x^2+y^2)"
        f"\\le\\log_2 x+\\log_4(x^2+y^2+{C}x)$?", count
    )
    solution = (
        f"Đặt $Q=x^2+y^2$ và $t=Q/x>0$. Bất đẳng thức tương đương "
        f"$\\log_2(1+t)\\le\\log_4(1+{C}/t)$. Vế trái tăng, vế phải giảm; "
        f"hai vế bằng nhau tại $t={T}$ vì $1+{C}/{T}=({T}+1)^2$. Do đó $t\\le{T}$, "
        f"hay $x^2+y^2\\le{T}x$. Với mỗi $x=1,\\ldots,{T}$, số giá trị $y$ là "
        f"$2\\lfloor\\sqrt{{x({T}-x)}}\\rfloor+1$; tổng bằng {count}."
    )
    return question, answer, solution, dict(T=T, C=C, count=count)


def verify_D57(params):
    T, C, expected = int(params["T"]), int(params["C"]), int(params["count"])
    if T < 2 or C != T*T*(T+2):
        return False
    # The logarithmic inequality is equivalent (for x>0) to
    # Q/x <= T, where Q=x^2+y^2, hence Q<=Tx. This exact integer
    # enumeration is equivalent to the original problem and includes equality.
    direct = sum(1 for xv in range(1, T+1)
                 for yv in range(-T, T+1)
                 if xv*xv + yv*yv <= T*xv)
    return direct == expected


# D78: the original constraint is equivalent to x+y>=3/2. Keep the constant
# 3 and the linked coefficients 2,4 fixed; vary only the objective's linear
# coefficients. Formula is checked against a dense grid in the original set.
def gen_D78(a, b):
    a, b = int(a), int(b)
    assert a > 0 and b > 0
    K = sp.Integer(3)
    x0 = sp.Rational(K + b - a, 4)
    assert 0 <= x0 < K/2
    p2 = sp.simplify(2*x0**2 + (a-b-K)*x0 + sp.Rational(K**2, 4) + sp.Rational(b*K, 2))
    p1 = sp.Rational(K**2, 4) + sp.Rational(a*K, 2)
    assert p1 > p2
    vals = bump_until_distinct([p2, p2+1, p2-1, 2*p2])
    opts = [latex(v) for v in vals]
    lines, answer = render_mc(opts, 0, prefix="P_{\\min}=")
    ax = "x" if a == 1 else f"{a}x"
    by = "y" if b == 1 else f"{b}y"
    prompt = (
        f"Xét các số thực không âm $x,y$ thỏa mãn $2x+y\\cdot4^{{x+y-1}}\\ge3$. "
        f"Giá trị nhỏ nhất của $P=x^2+y^2+{ax}+{by}$ bằng\n\n" + "\n".join(lines)
    )
    solution = (
        "\u0110\u1eb7t $s=x+y$. N\u1ebfu $s<3/2$ th\u00ec $4^{s-1}<2$, n\u00ean $2x+y4^{s-1}<2x+2y<3$, tr\u00e1i \u0111i\u1ec1u ki\u1ec7n. "
        "N\u1ebfu $s\\ge3/2$ th\u00ec $4^{s-1}\\ge2$ v\u00e0 \u0111i\u1ec1u ki\u1ec7n \u0111\u01b0\u1ee3c th\u1ecfa m\u00e3n. V\u1eady mi\u1ec1n kh\u1ea3 thi l\u00e0 "
        "$x,y\\ge0$, $x+y\\ge3/2$. "
        f"V\u1edbi $x\\ge3/2$, $P\\ge(3/2)^2+{a}(3/2)={latex(p1)}$. "
        f"V\u1edbi $0\\le x<3/2$, ta c\u00f3 $y\\ge3/2-x$; do $y^2+{b}y$ t\u0103ng theo $y\\ge0$, "
        f"P kh\u00f4ng nh\u1ecf h\u01a1n gi\u00e1 tr\u1ecb tr\u00ean bi\u00ean $y=3/2-x$. Gi\u00e1 tr\u1ecb n\u00e0y nh\u1ecf nh\u1ea5t t\u1ea1i "
        f"$x={latex(x0)}$, b\u1eb1ng $P_{{\\min}}={latex(p2)}<{latex(p1)}$. \u0110\u00e2y l\u00e0 GTNN."
    )
    return prompt, answer, solution, dict(a=a, b=b, x0=str(x0), p2=str(p2), p1=str(p1))


def verify_D78(params):
    a, b = int(params["a"]), int(params["b"])
    K = sp.Integer(3)
    if a <= 0 or b <= 0:
        return False
    x0 = sp.Rational(K + b - a, 4)
    p2 = sp.simplify(2*x0**2 + (a-b-K)*x0 + sp.Rational(K**2,4) + sp.Rational(b*K,2))
    p1 = sp.Rational(K**2,4) + sp.Rational(a*K,2)
    # The original constraint is exactly x+y>=3/2: below it the LHS is
    # strictly less than 2(x+y)<3; at/above it, 4^(x+y-1)>=2.
    # Minimize first on x>=3/2, then on y=3/2-x; positive b makes the
    # objective increase with y. These exact inequalities certify the global min.
    return 0 <= x0 < sp.Rational(3,2) and p1 > p2 and sp.simplify(p2-sp.Rational(params["p2"])) == 0


def expand_type(code, name, source, gen, verify, sampler, seed=0, target=90, max_tries=3000):
    rng = random.Random(seed)
    current = [r for r in ROWS if r["ma_dang"] == code]
    seen = {tuple(sorted((k, str(v)) for k, v in r["params"].items())) for r in current}
    questions = {r["de_bai"] for r in current}
    args_seen = set()
    made = len(current)
    for _ in range(max_tries):
        if made >= target:
            break
        args = tuple(sampler(rng))
        if args in args_seen:
            continue
        args_seen.add(args)
        try:
            q, ans, sol, params = gen(*args)
        except (AssertionError, ValueError, TypeError, ZeroDivisionError, OverflowError):
            continue
        key = tuple(sorted((k, str(v)) for k, v in params.items()))
        if key in seen or q in questions:
            continue
        opts = re.findall(r"(?m)^([A-D])\.\s*(.+)$", q)
        norm = [re.sub(r"[\s$.,]", "", v) for _, v in opts]
        if len(opts) != 4 or {k for k,_ in opts} != set("ABCD") or len(set(norm)) != 4:
            continue
        try:
            if not verify(params):
                continue
        except Exception:
            continue
        add_row(code, name, source, q, ans, sol, params)
        seen.add(key); questions.add(q); made += 1
    print(f"{code}: {made}/{target}")
    return made


def _sample_D08(rng):
    p, C, r = rng.sample(range(2, 25), 3)
    return p, C, r, rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 5)


def _sample_D47(rng):
    import math
    while True:
        n = rng.randint(2, 30)
        m = rng.randint(n + 1, int(1.5*n))
        if math.gcd(m, n) == 1:
            return m, n


def _sample_D52(rng):
    p, q = rng.randint(2, 6), rng.randint(2, 6)
    if p == q:
        q = q % 6 + 1
    return p, q, rng.randint(1, 30), rng.randint(3, 10), rng.randint(1, 2* rng.randint(1, 10))


def build_rows():
    ROWS.clear()
    candidates = {
        "D08": [(2,3,5,1,2,1),(2,5,3,1,2,1),(3,2,5,1,2,1),(3,5,2,1,2,1),(2,3,7,1,3,1),(5,3,2,1,2,1)],
        "D23": [(3,-6,3,-1),(3,-6,3,0),(3,-5,3,-1),(3,-5,3,0),(4,-8,3,-2),(4,-8,3,-1),(4,-8,3,0),(4,-8,3,1),(4,-8,3,2),(3,-7,4,-1),(3,-7,4,0),(3,-7,4,1),(2,-6,3,-1),(2,-6,3,0),(2,-6,3,1)],
        "D47": [(6,5),(5,4),(7,5),(8,5),(7,4),(5,3),(3,2),(9,5)],
        "D52": [(3,2,20,8,4),(5,3,100,8,4),(3,2,50,7,4),(4,3,30,8,4),(3,5,75,9,4),(5,2,50,7,4),(2,3,100,6,3),(2,5,100,8,3)],
        "D57": [(4,),(5,),(6,),(7,),(8,),(9,),(10,),(11,)],
        "D78": [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(3,4),(3,5)],
    }
    specs = {
        "D08": (gen_D08, verify_D08, "p007_q19", "Biểu diễn lôgarit qua các lôgarit cho trước bằng đổi cơ số"),
        "D23": (gen_D23, verify_D23, "p039_q35", "Biện luận số nghiệm phương trình lôgarit bằng khảo sát hàm số"),
        "D47": (gen_D47, verify_D47, "p106_q50", "Đếm số nguyên thỏa mãn phương trình lôgarit có nghiệm thực"),
        "D52": (gen_D52, verify_D52, "p119_q48", "Đếm tham số nguyên theo số giá trị nguyên thỏa bất đẳng thức mũ"),
        "D57": (gen_D57, verify_D57, "p133_q47", "Đếm cặp số nguyên thỏa bất đẳng thức lôgarit bằng miền hình tròn"),
        "D78": (gen_D78, verify_D78, "p203_q48", "Tìm GTNN biểu thức hai biến với điều kiện chứa hàm mũ"),
    }
    for code, sets in candidates.items():
        fn, verifier, source, name = specs[code]
        for args in sets:
            try:
                prompt, answer, solution, params = fn(*args)
            except AssertionError:
                continue
            if verifier(params):
                add_row(code, name, source, prompt, answer, solution, params)
            else:
                raise AssertionError(f"Independent verification failed for {code} {params}")
    names_sources = {
        "D08": ("Biểu diễn lôgarit qua các lôgarit cho trước bằng đổi cơ số", "p007_q19", gen_D08, verify_D08, _sample_D08),
        "D23": ("Biện luận số nghiệm phương trình lôgarit", "p039_q35", gen_D23, verify_D23,
                lambda r: (r.randint(1, 8), -r.randint(2, 30), r.randint(1, 10), r.randint(-20, 20))),
        "D47": ("Đếm số nguyên thỏa mãn phương trình lôgarit có nghiệm thực", "p106_q50", gen_D47, verify_D47, _sample_D47),
        "D52": ("Đếm tham số nguyên theo số giá trị nguyên thỏa bất phương trình mũ", "p119_q48", gen_D52, verify_D52, _sample_D52),
        "D57": ("Đếm cặp số nguyên thỏa bất đẳng thức lôgarit", "p133_q47", gen_D57, verify_D57, lambda r: (r.randint(2, 100),)),
        "D78": ("Tìm giá trị nhỏ nhất biểu thức hai biến với điều kiện mũ", "p203_q48", gen_D78, verify_D78,
                lambda r: (lambda b: (r.randint(max(1, b-2), b+3), b))(r.randint(1,80))),
    }
    for code, (name, source, gen, verify, sampler) in names_sources.items():
        expand_type(code, name, source, gen, verify, sampler, seed=int(code[1:])*100+8,
                    max_tries=10000 if code in ("D52", "D78") else 3000)
    return ROWS


def audit_choice_collisions(items):
    failures = []
    for row in items:
        choices = re.findall(r"(?m)^([A-D])\.\s*(.+)$", row["de_bai"])
        if len(choices) != 4 or {letter for letter, _ in choices} != set("ABCD"):
            failures.append((row["ma_dang"], row["id_goc"], "expected one each of A-D"))
            continue
        normalized = [re.sub(r"[\s$.,]", "", choice) for _, choice in choices]
        if len(set(normalized)) != 4:
            failures.append((row["ma_dang"], row["id_goc"], "duplicate displayed choices"))
    return failures


def main():
    rows = build_rows()
    failures = audit_choice_collisions(rows)
    if failures:
        raise SystemExit(f"Answer-choice collision(s): {failures}")
    batch_path = REPO / "data/questions/mu_logarit_extraction/bien_the/batch_round8.json"
    batch_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} independently verified variants to {batch_path}")


if __name__ == "__main__":
    main()
