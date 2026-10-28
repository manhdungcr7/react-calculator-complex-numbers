# -*- coding: utf-8 -*-
"""Round 5: D22, D24, D39, D75, D93."""
import json
import random
import re
import math
import sys
from importlib import import_module

sys.path.insert(0, "scripts/generate_questions")
utils = import_module("10_common_utils")
latex = utils.latex
render_mc = utils.render_mc
bump_until_distinct = utils.bump_until_distinct

import sympy as sp

x = sp.Symbol("x", positive=True)
ROWS = []


def add_row(ma_dang, ten_dang, id_goc, de_bai, dap_an, loi_giai, params):
    ROWS.append({
        "id_goc": id_goc, "ma_dang": ma_dang, "ten_dang": ten_dang,
        "nguon": "Nhân bản", "loai_bien_the": "chuan",
        "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai, "params": params,
    })


def try_add(ma_dang, ten_dang, id_goc, gen_fn, verify_fn, args_list):
    fails = []
    for args in args_list:
        try:
            de_bai, dap_an, loi_giai, params = gen_fn(*args)
        except AssertionError:
            continue
        if verify_fn(params):
            add_row(ma_dang, ten_dang, id_goc, de_bai, dap_an, loi_giai, params)
        else:
            fails.append((ma_dang, params))
    return fails


# ===================== D22: log_a b=C, P=log_{sqrt(b)/a} sqrt(b/a) =========
def gen_D22(C_num, C_is_sqrt):
    if C_is_sqrt:
        C = sp.sqrt(C_num)
        C_str = f"\\sqrt{{{C_num}}}"
    else:
        C = sp.Rational(C_num, 1)
        C_str = str(C_num)
    assert C != 2
    P = sp.simplify((C - 1) / (C - 2))
    correct = latex(P)
    wrong1 = latex(-P)
    wrong2 = latex(P + 1)
    wrong3 = latex(1 - P)
    vals_ok = len({correct, wrong1, wrong2, wrong3}) == 4
    assert vals_ok
    de_bai = (
        f"Cho $a, b$ là các số thực dương thỏa mãn $a\\neq 1, a\\neq\\sqrt{{b}}$ và $\\log_a b={C_str}$. "
        f"Tính $P=\\log_{{\\frac{{\\sqrt{{b}}}}{{a}}}}\\sqrt{{\\dfrac{{b}}{{a}}}}$.\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="P=")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$P=\\dfrac{{\\log_a\\sqrt{{b/a}}}}{{\\log_a(\\sqrt b/a)}}=\\dfrac{{\\frac12(\\log_a b-1)}}"
        f"{{\\frac12\\log_a b-1}}=\\dfrac{{{C_str}-1}}{{{C_str}-2}}={correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(C_num=str(C_num), C_is_sqrt=str(C_is_sqrt))


def verify_D22(params):
    C_num, C_is_sqrt = int(params["C_num"]), params["C_is_sqrt"] == "True"
    C = sp.sqrt(C_num) if C_is_sqrt else sp.Rational(C_num, 1)
    av = sp.Rational(7, 3)
    bv = av ** C
    P = sp.log(sp.sqrt(bv / av), sp.sqrt(bv) / av)
    target = sp.simplify((C - 1) / (C - 2))
    return abs(complex(P) - complex(target)) < 1e-6


# ===================== D24: y=ln(x)/x^n => x y'' + (n+1) y' = -n/x^(n+1) ===
def gen_D24(n):
    n = sp.Integer(n)
    np1 = n + 1
    xn = "x" if n == 1 else f"x^{{{n}}}"
    xn1 = f"x^{{{n-1}}}" if n != 2 else "x"
    xn1 = "" if n == 1 else (xn1 if n != 2 else "x")
    coef_n = "" if n == 1 else str(n)
    coef_np1 = "" if np1 == 1 else str(np1)
    de_bai = f"Cho hàm số $y=\\dfrac{{\\ln x}}{{{xn}}}$, mệnh đề nào dưới đây đúng?\n\n"
    correct = f"{coef_np1}y'+xy''=-\\dfrac{{{n}}}{{x^{{{np1}}}}}"
    wrong1 = f"{coef_np1}y'+xy''=\\dfrac{{{n}}}{{x^{{{np1}}}}}"
    wrong2 = f"y'+xy''=-\\dfrac{{{n}}}{{x^{{{np1}}}}}"
    wrong3 = f"{coef_n}y'+xy''=-\\dfrac{{{n}}}{{x^{{{np1}}}}}"
    vals_ok = len({correct, wrong1, wrong2, wrong3}) == 4
    assert vals_ok
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    step1_lhs = f"{n}{xn1}y+{xn}y'" if n != 1 else "y+xy'"
    loi_giai = (
        f"Ta có ${xn}y=\\ln x$. Lấy đạo hàm hai vế: ${step1_lhs}=\\dfrac1x$. "
        f"Lấy đạo hàm tiếp rồi rút gọn (thay lại $y$) ta được "
        f"${coef_np1}y'+xy''=-\\dfrac{{{n}}}{{x^{{{np1}}}}}$."
    )
    return de_bai, dap_an, loi_giai, dict(n=str(n))


def verify_D24(params):
    n = sp.sympify(params["n"])
    y = sp.log(x) / x ** n
    yp = sp.diff(y, x)
    ypp = sp.diff(y, x, 2)
    lhs = (n + 1) * yp + x * ypp
    rhs = -n / x ** (n + 1)
    return sp.simplify(lhs - rhs) == 0


# ===================== D39: log_{p^2}x=log_{pq}y=log_{q^2}(cx+y) =>x/y ======
def gen_D39(p, q, c, disc_ok):
    p, q, c = sp.Integer(p), sp.Integer(q), sp.Integer(c)
    assert p > 1 and q > 1 and p != q
    u = sp.Symbol("u", positive=True)
    sols = [s for s in sp.solve(sp.Eq(c * u ** 2 + u - 1, 0), u) if s.is_real and s > 0]
    assert len(sols) == 1
    ratio = sols[0]
    correct = latex(ratio)
    wrong1 = latex(1 / ratio)
    wrong2 = latex(-ratio)
    wrong3 = latex(ratio + 1)
    vals_ok = len({correct, wrong1, wrong2, wrong3}) == 4
    assert vals_ok
    cx_str = f"{c}x+y" if c != 1 else "x+y"
    de_bai = (
        f"Cho $x,y$ là các số thực dương thỏa mãn $\\log_{{{p**2}}}x=\\log_{{{p*q}}}y=\\log_{{{q**2}}}({cx_str})$. "
        f"Giá trị của $\\dfrac{{x}}{{y}}$ bằng\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Đặt $t$ là giá trị chung. $x=({p**2})^t$, $y=({p*q})^t$ và ${cx_str}=({q**2})^t$. "
        f"Chia hai vế cho $({q**2})^t$ và đặt $u=({p}/{q})^t=x/y$, ta được "
        f"${c}u^2+u-1=0\\Rightarrow u={correct}$. Vì $u=x/y$, đây là giá trị cần tìm."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), q=str(q), c=str(c))


def verify_D39(params):
    p, q, c = (sp.Integer(params[k]) for k in ("p", "q", "c"))
    if p <= 1 or q <= 1 or p == q or c <= 0:
        return False
    u = sp.Symbol("u", positive=True)
    roots = [r for r in sp.solve(sp.Eq(c*u**2+u-1, 0),u) if r.is_real and r > 0]
    return len(roots) == 1 and sp.simplify(c*roots[0]**2+roots[0]-1) == 0
def _d75_thresholds(a, c):
    import mpmath as mp
    a, c = int(a), sp.Rational(c)
    if a <= 1 or c <= 1:
        raise ValueError("a and c must be greater than 1")
    m1 = int(sp.floor(c ** (a*a)))
    square = sp.integer_nthroot(a, 2)
    equal_m = None
    if square[1]:
        r = int(square[0])
        for n in range(2, int(sp.floor(c**sp.Rational(1,r)))+2):
            if sp.Rational(n)**r == c:
                equal_m = n
                break
    with mp.workdps(100):
        cv = mp.mpf(int(c.p))/int(c.q)
        value = mp.exp(mp.log(cv)/mp.sqrt(a))
        nearest = mp.nint(value)
        if abs(value-nearest) < mp.mpf('1e-50'):
            if equal_m is None or int(nearest) != equal_m:
                raise ValueError("unresolved integer threshold")
            m2 = equal_m
        else:
            m2 = int(mp.floor(value))
    collision_x1 = sp.denom(c**(a*a)) == 1
    if m1 <= m2:
        raise ValueError("unexpected ordering of the two thresholds")
    return m1, m2, equal_m, collision_x1


def gen_D75(a, c):
    a, c = int(a), sp.Rational(c)
    m1, m2, equal_m, collision_x1 = _d75_thresholds(a, c)
    equal_x2 = equal_m is not None
    count = 1 + int(equal_x2) + (m1-m2) - int(collision_x1)
    assert count > 5
    vals = bump_until_distinct([sp.Integer(count), count+1, count-1, count+2])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    ctex = latex(c)
    de_bai = (
        f"Cho ph\u01b0\u01a1ng tr\u00ecnh $\\left(2\\log_{{{a}}}^2x-3\\log_{{{a}}}x-2\\right)"
        f"\\sqrt{{\\left({ctex}\\right)^x-m}}=0$ ($m$ l\u00e0 tham s\u1ed1 th\u1ef1c). "
        f"C\u00f3 t\u1ea5t c\u1ea3 bao nhi\u00eau gi\u00e1 tr\u1ecb nguy\u00ean d\u01b0\u01a1ng c\u1ee7a $m$ \u0111\u1ec3 ph\u01b0\u01a1ng tr\u00ecnh c\u00f3 \u0111\u00fang hai nghi\u1ec7m ph\u00e2n bi\u1ec7t?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    if equal_x2:
        equal_text = f"Gi\u00e1 tr\u1ecb $m={equal_m}$ l\u00e0 s\u1ed1 nguy\u00ean n\u00ean tr\u01b0\u1eddng h\u1ee3p $x_3=x_2$ \u0111\u01b0\u1ee3c t\u00ednh th\u00eam. "
    else:
        equal_text = f"Gi\u00e1 tr\u1ecb $({ctex})^{{1/\\sqrt{{{a}}}}}$ kh\u00f4ng l\u00e0 s\u1ed1 nguy\u00ean n\u00ean kh\u00f4ng c\u00f3 tr\u01b0\u1eddng h\u1ee3p $x_3=x_2$. "
    collision_text = ("T\u1ea1i $m=M_1$, $x_3=x_1$ n\u00ean lo\u1ea1i m\u1ed9t gi\u00e1 tr\u1ecb. "
                      if collision_x1 else "T\u1ea1i $m=M_1$, $x_1$ v\u00e0 $x_3$ ph\u00e2n bi\u1ec7t n\u00ean v\u1eabn t\u00ednh. ")
    loi_giai = (
        f"\u0110\u1eb7t $u=\\log_{{{a}}}x$. Ph\u01b0\u01a1ng tr\u00ecnh t\u01b0\u01a1ng \u0111\u01b0\u01a1ng "
        f"$(2u+1)(u-2)\\sqrt{{({ctex})^x-m}}=0$, n\u00ean hai nghi\u1ec7m t\u1eeb nh\u00e2n t\u1eed th\u1ee9 nh\u1ea5t l\u00e0 "
        f"$x_1={a}^2$ v\u00e0 $x_2=1/\\sqrt{{{a}}}$. \u0110\u1eb7t $x_3=\\log_{{{ctex}}}m$ khi $m>1$. "
        f"\u0110i\u1ec1u ki\u1ec7n \u0111\u1ec3 $x_i$ th\u1ecfa ph\u01b0\u01a1ng tr\u00ecnh l\u00e0 $m\\le({ctex})^{{x_i}}$. "
        f"\u0110\u1eb7t $M_1=\\lfloor({ctex})^{{{a}^2}}\\rfloor={m1}$, "
        f"$M_2=\\lfloor({ctex})^{{1/\\sqrt{{{a}}}}}\\rfloor={m2}$. "
        f"Khi $m=1$, $x_3=0$ kh\u00f4ng thu\u1ed9c mi\u1ec1n $x>0$, c\u00f2n $x_1,x_2$ \u0111\u1ec1u th\u1ecfa, n\u00ean t\u00ednh th\u00eam m\u1ed9t gi\u00e1 tr\u1ecb. "
        f"V\u1edbi $2\\le m\\le M_2$, ba nghi\u1ec7m \u0111\u1ec1u th\u1ecfa; ch\u1ec9 tr\u01b0\u1eddng h\u1ee3p $x_3=x_2$ c\u00f2n hai nghi\u1ec7m ph\u00e2n bi\u1ec7t. {equal_text}"
        f"V\u1edbi $M_2<m\\le M_1$, $x_2$ kh\u00f4ng th\u1ecfa, c\u00f2n $x_1,x_3$ th\u1ecfa; {collision_text}"
        f"Khi $m>M_1$, ch\u1ec9 c\u00f2n $x_3$. V\u1eady s\u1ed1 gi\u00e1 tr\u1ecb c\u1ea7n t\u00ecm l\u00e0 "
        f"$1+{m1-m2}+{int(equal_x2)}-{int(collision_x1)}={count}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), c=str(c), M1=str(m1), M2=str(m2),
                                           equal_x2=int(equal_x2), collision_x1=int(collision_x1))


def verify_D75_full(params, expected_count):
    import mpmath as mp
    a, c = int(params["a"]), sp.Rational(params["c"])
    if not (a > 1 and c > 1):
        return False
    m1 = int(sp.floor(c**(a*a)))
    square = sp.integer_nthroot(a, 2)
    equal_m = None
    if square[1]:
        r = int(square[0])
        for n in range(2, int(sp.floor(c**sp.Rational(1,r)))+2):
            if sp.Rational(n)**r == c:
                equal_m = n
                break
    collision_x1 = sp.denom(c**(a*a)) == 1
    with mp.workdps(100):
        cv = mp.mpf(int(c.p))/int(c.q)
        root = mp.sqrt(a)
        direct_count = 0
        direct_m2 = 0
        for m in range(1, m1+1):
            x1_ok = sp.Rational(m) <= c**(a*a)
            x2_ok = (m <= equal_m if equal_m is not None else mp.log(m)*root < mp.log(cv))
            if x2_ok:
                direct_m2 = m
            distinct = int(bool(x1_ok)) + int(bool(x2_ok))
            if m > 1:
                x3_duplicates = ((collision_x1 and m == m1) or
                                 (equal_m is not None and m == equal_m))
                distinct += int(not x3_duplicates)
            if distinct == 2:
                direct_count += 1
    return (int(params["M1"]) == m1 and int(params["M2"]) == direct_m2
            and int(params["equal_x2"]) == int(equal_m is not None)
            and int(params["collision_x1"]) == int(collision_x1)
            and direct_count == int(expected_count))


def _integer_interval(lo, lo_closed, hi, hi_closed):
    from fractions import Fraction
    lo, hi = Fraction(lo), Fraction(hi)
    first = -((-lo.numerator)//lo.denominator)
    if not lo_closed and Fraction(first) == lo:
        first += 1
    last = hi.numerator//hi.denominator
    if not hi_closed and Fraction(last) == hi:
        last -= 1
    return first, last, max(0,last-first+1)


def gen_D93(A, B, N):
    from fractions import Fraction
    A, B, N = int(A), int(B), int(N)
    assert A > 1 and B > 1 and N > 0
    low_first, low_last, low_count = _integer_interval(
        Fraction(N, B**5), True, Fraction(N, B**4), False
    )
    high_first, high_last, high_count = _integer_interval(
        N*B**2, False, N*B**3, True
    )
    count = low_count + high_count
    assert count > 5
    vals = bump_until_distinct([sp.Integer(count), count+1, count-1, count+2])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    de_bai = (
        f"C\u00f3 bao nhi\u00eau s\u1ed1 nguy\u00ean d\u01b0\u01a1ng $a$ sao cho \u1ee9ng v\u1edbi m\u1ed7i $a$ c\u00f3 \u0111\u00fang ba s\u1ed1 nguy\u00ean $b$ th\u1ecfa m\u00e3n "
        f"$({A}^b-{A})(a\\cdot{B}^b-{N})<0$?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    def interval_text(first, last, n):
        if n == 0:
            return r"\varnothing"
        return str(first) if first == last else f"{first},\\ldots,{last}"
    low_text = interval_text(low_first, low_last, low_count)
    high_text = interval_text(high_first, high_last, high_count)
    low_clause = (f"C\u00e1c s\u1ed1 nguy\u00ean d\u01b0\u01a1ng thu\u1ed9c kho\u1ea3ng th\u1ee9 nh\u1ea5t l\u00e0 $a\\in\\{{{low_text}\\}}$, c\u00f3 {low_count} gi\u00e1 tr\u1ecb. "
                  if low_count else "Kho\u1ea3ng th\u1ee9 nh\u1ea5t kh\u00f4ng ch\u1ee9a s\u1ed1 nguy\u00ean d\u01b0\u01a1ng n\u00e0o. ")
    loi_giai = (
        f"V\u00ec ${A}>1$, $({A}^b-{A})$ \u00e2m khi $b<1$, b\u1eb1ng $0$ khi $b=1$ v\u00e0 d\u01b0\u01a1ng khi $b>1$. "
        f"\u0110\u1eb7t $L=\\log_{{{B}}}\\dfrac{{{N}}}{{a}}$. Khi $b<1$, t\u00edch \u00e2m khi $L<b<1$; "
        f"khi $b>1$, t\u00edch \u00e2m khi $1<b<L$. V\u00ec v\u1eady c\u00f3 \u0111\u00fang ba s\u1ed1 nguy\u00ean $b$ khi v\u00e0 ch\u1ec9 khi "
        f"$4<L\\le5$ ho\u1eb7c $-3\\le L<-2$. V\u00ec ${B}>1$, hai \u0111i\u1ec1u ki\u1ec7n n\u00e0y t\u01b0\u01a1ng \u0111\u01b0\u01a1ng v\u1edbi "
        f"$\\dfrac{{{N}}}{{{B**5}}}\\le a<\\dfrac{{{N}}}{{{B**4}}}$ ho\u1eb7c "
        f"{chr(36)}{N*B**2}<a\\le{N*B**3}{chr(36)}. {low_clause}"
        f"C\u00e1c s\u1ed1 nguy\u00ean d\u01b0\u01a1ng thu\u1ed9c kho\u1ea3ng th\u1ee9 hai l\u00e0 $a\\in\\{{{high_text}\\}}$, c\u00f3 {high_count} gi\u00e1 tr\u1ecb. "
        f"V\u1eady c\u00f3 {chr(36)}{count}{chr(36)} gi\u00e1 tr\u1ecb $a$."
    )
    params = dict(A=A, B=B, N=N, low_first=low_first, low_last=low_last,
                  high_first=high_first, high_last=high_last)
    return de_bai, dap_an, loi_giai, params


def verify_D93_full(params, expected_count):
    from fractions import Fraction
    A, B, N = (int(params[k]) for k in ("A", "B", "N"))
    if not (A > 1 and B > 1 and N > 0):
        return False
    low = _integer_interval(Fraction(N, B**5), True, Fraction(N, B**4), False)
    high = _integer_interval(N*B**2, False, N*B**3, True)
    low_first, low_last, low_count = low
    high_first, high_last, high_count = high
    return (int(params["low_first"]) == low_first and int(params["low_last"]) == low_last
            and int(params["high_first"]) == high_first and int(params["high_last"]) == high_last
            and low_count+high_count == int(expected_count))

def expand_type(code, name, source_id, gen, verify, sampler, seed=0, target=90, max_tries=3000):
    rng = random.Random(seed)
    current = [row for row in ROWS if row["ma_dang"] == code]
    seen = {tuple(sorted(row["params"].items())) for row in current}
    questions = {row["de_bai"] for row in current}
    made = len(current)
    for _ in range(max_tries):
        if made >= target:
            break
        try:
            q, ans, sol, params = gen(*sampler(rng))
        except (AssertionError, ValueError, TypeError, ZeroDivisionError, OverflowError):
            continue
        key = tuple(sorted(params.items()))
        if key in seen or q in questions:
            continue
        opts = re.findall(r"(?m)^([A-D])\.\s*(.+)$", q)
        norm = [re.sub(r"[\s$.,]", "", v) for _, v in opts]
        if len(opts) != 4 or {k for k,_ in opts} != set("ABCD") or len(set(norm)) != 4:
            continue
        try:
            m = re.search(r"\$\s*(-?\d+)\s*\$", ans)
            if m:
                valid = verify(params, int(m.group(1)))
            else:
                valid = verify(params)
            if not valid:
                continue
        except Exception:
            continue
        add_row(code, name, source_id, q, ans, sol, params)
        seen.add(key); questions.add(q); made += 1
    print(f"{code}: {made}/{target}")
    return made


def main():
    fails = []
    for C_num, is_sqrt in [(3, True), (5, True), (2, True), (7, True), (3, False), (5, False), (10, False)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D22(C_num, is_sqrt)
        except AssertionError:
            continue
        if verify_D22(params):
            add_row("D22", "Tính giá trị biểu thức lôgarit phức hợp qua một lôgarit cho trước", "p038_q33",
                     de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D22", params))

    fails += try_add("D24", "Nhận biết tính chất (đạo hàm/đơn điệu) của hàm số chứa lôgarit", "p041_q40",
                      gen_D24, verify_D24, [(v,) for v in (1, 2, 3, 4, 5, 6)])

    for p, q, c in [(3, 2, 2), (2, 3, 2), (5, 2, 2), (4, 3, 2), (3, 5, 2), (5, 3, 2)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D39(p, q, c, True)
        except AssertionError:
            continue
        if verify_D39(params):
            add_row("D39", "Từ dãy đẳng thức lôgarit ba cơ số khác nhau suy ra tỉ lệ giữa các biến", "p087_q41",
                     de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D39", params))

    for a, c in [(2, 3), (2, 2), (3, 2), (2, 5), (3, 5)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D75(a, c)
        except AssertionError:
            continue
        expected = int(dap_an.split("$")[1])
        if verify_D75_full(params, expected):
            add_row("D75", "Đếm giá trị nguyên dương tham số để phương trình tích (lôgarit bậc hai và căn "
                            "chứa tham số) có nghiệm", "p186_q47", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D75", params))

    for A, B, N in [(3, 2, 18), (2, 3, 24), (3, 2, 20), (2, 2, 16), (3, 4, 30)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D93(A, B, N)
        except AssertionError:
            continue
        expected = int(dap_an.split("$")[1])
        if verify_D93_full(params, expected):
            add_row("D93", "Đếm số nguyên dương tham số sao cho có đúng k giá trị nguyên biến kia thỏa "
                            "bất phương trình tích", "p242_q39", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D93", params))

    expand_type("D22", "Evaluate a logarithmic expression from a given logarithm", "p038_q33",
                gen_D22, verify_D22, lambda r: (r.randint(3, 250), r.choice((True, False))), seed=2201)
    expand_type("D24", "Differentiate a logarithmic function identity", "p041_q40",
                gen_D24, verify_D24, lambda r: (r.randint(1, 500),), seed=2401)
    expand_type("D39", "Find a ratio from three equal logarithms", "p087_q41",
                lambda p, q, c: gen_D39(p, q, c, True), verify_D39,
                lambda r: (lambda p, q: (p, (p % 30 + 1) if q == p else q, r.randint(1, 30)))(r.randint(1, 30), r.randint(1, 30)), seed=3901)
    expand_type("D75", "Count integer parameters giving exactly two roots", "p186_q47",
                gen_D75, verify_D75_full, lambda r: (2, sp.Rational(200+r.randint(1, 90), 100)), seed=7501)
    expand_type("D93", "Count integer parameters meeting an exponential product inequality", "p242_q39",
                gen_D93, verify_D93_full,
                lambda r: (r.randint(2, 8), r.randint(2, 8), r.randint(2, 80)), seed=9301)

    with open("data/questions/mu_logarit_extraction/bien_the/batch_round5.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)

    with open("scripts/generate_questions/.tmp_round5_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Tong so hang sinh: {len(ROWS)}\n")
        f.write(f"That bai verify: {len(fails)}\n")
        for ma_dang, params in fails:
            f.write(f"  {ma_dang}: {params}\n")
        counts = {}
        for r in ROWS:
            counts[r['ma_dang']] = counts.get(r['ma_dang'], 0) + 1
        f.write("\nSo bien the theo dang:\n")
        for k, v in sorted(counts.items()):
            f.write(f"  {k}: {v}\n")


if __name__ == "__main__":
    main()
