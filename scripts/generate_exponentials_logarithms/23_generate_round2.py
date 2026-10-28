# -*- coding: utf-8 -*-
"""
Round 2: cac dang truoc day bi xep vao nhom "kho/rui ro" nhung sau khi xem
lai ky hon thi TONG QUAT HOA duoc an toan:
- D35, D28(da lam): dap so la TONG/TICH nghiem qua Viete -> luon dep du
  tung nghiem rieng le co the vo ti.
- D69, D51, D56, D16: dap so la MOT SO DEM/MOT KHOANG tinh qua ham dac
  trung don dieu hoac lap luan dai so -> van dung du nguong trung gian xau.
- D40, D45, D67: phuong trinh bac hai theo an phu duoc THIET KE co nghiem
  dep (giu cau truc Viete/nhan tu nhu ban goc).
- D15, D08, D22, D29, D05: chi la dao ham/dong nhat thuc/bien doi dai so
  tong quat, truoc do bi bo qua nham (khong thuc su kho).

Verify doc lap: dung sp.solve/sp.diff/dem truc tiep (brute-force) nhu cac
batch truoc, KHONG dung lai cong thuc dong dang da sinh de bai.
"""
import json
import random
import re
import sys
from importlib import import_module

sys.path.insert(0, "scripts/generate_questions")
utils = import_module("10_common_utils")
latex = utils.latex
render_mc = utils.render_mc
bump_until_distinct = utils.bump_until_distinct

import sympy as sp

x = sp.Symbol("x")
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
        if ma_dang == "D40":
            verified = verify_fn(params, de_bai, dap_an)
        else:
            verified = verify_fn(params)
        if verified:
            add_row(ma_dang, ten_dang, id_goc, de_bai, dap_an, loi_giai, params)
        else:
            fails.append((ma_dang, params))
    return fails


# ===================== D15: dao ham ln(1+sqrt(x+k)) ==========================
def gen_D15(k):
    k = sp.Integer(k)
    de_bai = f"Tính đạo hàm của hàm số $y = \\ln(1+\\sqrt{{x+{k}}})$.\n\n"
    correct = f"\\dfrac{{1}}{{2\\sqrt{{x+{k}}}(1+\\sqrt{{x+{k}}})}}"
    wrong1 = f"\\dfrac{{1}}{{1+\\sqrt{{x+{k}}}}}"
    wrong2 = f"\\dfrac{{1}}{{\\sqrt{{x+{k}}}(1+\\sqrt{{x+{k}}})}}"
    wrong3 = f"\\dfrac{{2}}{{\\sqrt{{x+{k}}}(1+\\sqrt{{x+{k}}})}}"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="y'=")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$y'=\\dfrac{{(1+\\sqrt{{x+{k}}})'}}{{1+\\sqrt{{x+{k}}}}}"
        f"=\\dfrac{{\\frac{{1}}{{2\\sqrt{{x+{k}}}}}}}{{1+\\sqrt{{x+{k}}}}}=\\dfrac{{1}}{{2\\sqrt{{x+{k}}}(1+\\sqrt{{x+{k}}})}}$."
    )
    return de_bai, dap_an, loi_giai, dict(k=str(k))


def verify_D15(params):
    k = sp.sympify(params["k"])
    deriv = sp.diff(sp.log(1 + sp.sqrt(x + k)), x)
    target = 1 / (2 * sp.sqrt(x + k) * (1 + sp.sqrt(x + k)))
    return sp.simplify(deriv - target) == 0


# ===================== D05: menh de sai ve bien doi log cua a^x*b^(x^2) ====
def gen_D05(a, b):
    a, b = sp.Integer(a), sp.Integer(b)
    # dung: log_a(...)< log_a 1 => x + x^2 log_a b <0
    correct = f"x+x^2\\log_{{{a}}}{b}<0"
    wrong_sai = f"1+x\\log_{{{a}}}{b}<0"  # SAI (thieu nhan x)
    opt_c = f"x\\log_{{{b}}}{a}+x^2<0"  # dung (chia cho log_b)
    opt_d = f"x\\ln{a}+x^2\\ln{b}<0"  # dung (dung ln)
    de_bai = (
        f"Cho hàm số $y=f(x)={a}^x\\cdot{b}^{{x^2}}$. Khẳng định nào sau đây là khẳng định "
        f"**sai**?\n\n"
    )
    opts = [wrong_sai, correct, opt_c, opt_d]
    lines, dap_an = render_mc(opts, 0, prefix="f(x)<1\\Leftrightarrow ")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$f(x)<1\\Leftrightarrow\\log_{{{a}}}f(x)<0\\Leftrightarrow x+x^2\\log_{{{a}}}{b}<0"
        f"\\Leftrightarrow x(1+x\\log_{{{a}}}{b})<0$, KHÔNG tương đương với "
        f"$1+x\\log_{{{a}}}{b}<0$ (thiếu nhân tử $x$). Vậy khẳng định sai là "
        f"$1+x\\log_{{{a}}}{b}<0$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), b=str(b))


def verify_D05(params):
    a, b = sp.sympify(params["a"]), sp.sympify(params["b"])
    xv = sp.Rational(-1, 10)  # diem thu: x nho am, x(1+x logb)<0 co the dung hoac sai tuy dau
    # kiem tra doc lap: dang "dung" (correct) phai tuong duong f(x)<1 tai nhieu diem mau,
    # dang "sai" (thieu he so x) KHONG tuong duong
    f = a ** x * b ** (x ** 2)
    match_correct, mismatch_wrong = True, False
    for xv in [sp.Rational(1, 2), sp.Rational(-1, 2), sp.Integer(2), sp.Integer(-2), sp.Rational(3, 10)]:
        lhs = f.subs(x, xv) < 1
        rhs_correct = (xv + xv ** 2 * sp.log(b, a) < 0)
        rhs_wrong = (1 + xv * sp.log(b, a) < 0)
        if bool(lhs) != bool(rhs_correct):
            match_correct = False
        if bool(lhs) != bool(rhs_wrong):
            mismatch_wrong = True
    return match_correct and mismatch_wrong


# ===================== D45: A^(2x)+p*A^x-q>0 factor (A^x-r1)(A^x-r2)>0 =====
def gen_D45(A, r1, r2):
    A, r1, r2 = sp.Integer(A), sp.Integer(r1), sp.Integer(r2)
    assert r1 > 0 > r2
    p = -(r1 + r2)
    const = r1 * r2
    lhs = f"{A**2}^x" + (f"+{p}\\cdot{A}^x" if p > 0 else (f"{p}\\cdot{A}^x" if p < 0 else ""))
    lhs += (f"+{const}" if const > 0 else (f"{const}" if const < 0 else ""))
    de_bai = f"Tập nghiệm của bất phương trình ${lhs}>0$ là\n\n"
    boundary = sp.log(r1, A)
    correct = f"({latex(boundary)};+\\infty)"
    wrong1 = f"(-\\infty;{latex(boundary)})"
    wrong2 = f"[{latex(boundary)};+\\infty)"
    wrong3 = f"({latex(boundary+1)};+\\infty)"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$({A}^x-{r1})({A}^x+{abs(int(r2))})>0$. Vì ${A}^x>0>{r2}$ nên ${A}^x+{abs(int(r2))}>0$ luôn đúng, "
        f"do đó bất phương trình $\\Leftrightarrow {A}^x>{r1}\\Leftrightarrow x>\\log_{{{A}}}{r1}$."
    )
    return de_bai, dap_an, loi_giai, dict(A=str(A), r1=str(r1), r2=str(r2))


def verify_D45(params):
    A, r1, r2 = (sp.sympify(params[k]) for k in ("A", "r1", "r2"))
    p, const = -(r1 + r2), r1 * r2
    sol = sp.solve_univariate_inequality(A ** (2 * x) + p * A ** x + const > 0, x, relational=False)
    return sol == sp.Interval.open(sp.log(r1, A), sp.oo)


# ===================== D67: t^2-k*m*t+c*m^2-c=0 (dat t=B^x), 2 nghiem duong
def gen_D67(B, k, c):
    B, k, c = sp.Integer(B), sp.Integer(k), sp.Integer(c)
    assert k == B, "The source question ties the coefficient to the base: k = B."
    m = sp.Symbol("m", real=True)
    disc = sp.expand((k * m) ** 2 - 4 * (c * m ** 2 - c))
    sol_disc = sp.solve_univariate_inequality(disc > 0, m, relational=False)
    sol_sum = sp.solve_univariate_inequality(k * m > 0, m, relational=False)
    sol_prod = sp.solve_univariate_inequality(c * m ** 2 - c > 0, m, relational=False)
    sol = sol_disc.intersect(sol_sum).intersect(sol_prod)
    assert isinstance(sol, sp.Interval)
    lo, hi = sol.start, sol.end
    assert lo.is_finite and hi.is_finite
    int_vals = [v for v in range(int(sp.floor(lo)) - 1, int(sp.ceiling(hi)) + 2) if lo < v < hi]
    assert 1 <= len(int_vals) <= 6
    count = len(int_vals)
    de_bai = (
        f"Gọi $S$ là tập hợp tất cả các giá trị nguyên của tham số $m$ sao cho phương trình "
        f"${B**2}^x-m\\cdot{B}^{{x+1}}+{c}m^2-{c}=0$ có hai nghiệm phân biệt. Hỏi $S$ có bao nhiêu phần tử?\n\n"
    )
    correct = str(count)
    wrong1, wrong2, wrong3 = str(count + 1), str(max(count - 1, 0)), str(count + 2)
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Đặt $t={B}^x>0$: $t^2-{k}mt+{c}m^2-{c}=0$. YCBT $\\Leftrightarrow$ PT có 2 nghiệm dương phân biệt "
        f"$\\Leftrightarrow \\Delta>0,\\ {k}m>0,\\ {c}m^2-{c}>0 \\Leftrightarrow m\\in\\left({latex(lo)};{latex(hi)}\\right)$. "
        f"Vậy $S=\\{{{','.join(str(v) for v in int_vals)}\\}}$, có ${count}$ phần tử."
    )
    return de_bai, dap_an, loi_giai, dict(B=str(B), k=str(k), c=str(c))


def verify_D67_full(params, expected_count):
    B, k, c = (int(params[key]) for key in ("B", "k", "c"))
    if not (B > 1 and k == B and c > 0 and 4*c > k*k):
        return False
    # Two distinct positive roots require m>=2 and
    # m^2 < 4c/(4c-k^2). Count this exact integer interval, with no fixed search cap.
    bound_sq = sp.Rational(4*c, 4*c-k*k)
    count = max(0, int(sp.ceiling(sp.sqrt(bound_sq)))-2)
    return count == int(expected_count)
def gen_D40(a, b_coef, p, q=None):
    a, b_coef, p = sp.Integer(a), sp.Integer(b_coef), sp.Integer(p)
    q = 4 - p  # rang buoc bat buoc de PT luon co nghiem t=1 co dinh (xem suy luan trong doc string)
    p_int = int(p)
    t = sp.Symbol("t")
    # ho tro b_coef=a (tuc log_a(a x)=1+t voi t=log_a x)
    assert b_coef == a
    m = sp.Symbol("m")
    full = sp.expand((1 + t) ** 2 - (m + p) * t + m - q)
    full_poly = sp.Poly(full, t)
    coeffs = full_poly.all_coeffs()  # [1, coef_t, const] dang t^2+B t+C voi B,C phu thuoc m
    B_of_m = full_poly.coeff_monomial(t)
    C_of_m = full_poly.coeff_monomial(1)
    # roots theo m: gia su factor thanh (t-1)(t-(m-r)) dang thiet ke
    roots_m = sp.solve(sp.Eq(full, 0), t)
    assert len(roots_m) == 2
    r_fixed = [r for r in roots_m if not r.has(m)]
    r_var = [r for r in roots_m if r.has(m)]
    assert len(r_fixed) == 1 and len(r_var) == 1
    r_fixed = r_fixed[0]
    r_var = r_var[0]
    assert 0 <= r_fixed <= 1
    lo = sp.solve(sp.Eq(r_var, 0), m)
    hi = sp.solve(sp.Eq(r_var, 1), m)
    assert len(lo) == 1 and len(hi) == 1
    lo, hi = lo[0], hi[0]
    if lo > hi:
        lo, hi = hi, lo
    correct = f"[{latex(lo)};{latex(hi)})" if r_fixed != 0 else f"({latex(lo)};{latex(hi)}]"
    p_term = f"(m{p_int:+d})" if p_int else "m"
    q_term = f"m{-int(q):+d}" if int(q) else "m"
    wrong1 = f"({latex(lo)};{latex(hi)})"
    wrong2 = f"[{latex(lo)};{latex(hi)}]"
    wrong3 = f"({latex(hi)};+\\infty)"
    de_bai = (
        f"Cho phương trình $\\log_{{{a}}}^2({a}x)-{p_term}\\log_{{{a}}}x+{q_term}=0$ ($m$ là tham số thực). "
        f"Tập hợp tất cả các giá trị của $m$ để phương trình đã cho có hai nghiệm phân biệt thuộc đoạn "
        f"$[1;{a}]$ là\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    coeff = 2 - int(p)
    shift = int(p) - 3
    loi_giai = (
        f"Đặt $t=\\log_{{{a}}}x$. Khai triển, phương trình tương đương "
        f"$(t+1)^2-{p_term}t+{q_term}=0$"
        f" $\\Leftrightarrow t^2+({coeff}-m)t+(m{shift:+d})=0$"
        f" $\\Leftrightarrow (t-1)(t-(m{shift:+d}))=0$. "
        f"Điều kiện $x\\in[1;{a}]$ tương đương $t\\in[0;1]$. "
        f"Hai nghiệm phân biệt thuộc $[0;1]$ khi và chỉ khi $m{shift:+d}\\in[0;1)$, "
        f"suy ra $m\\in{correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), p=str(p), q=str(q), lo=str(lo), hi=str(hi), r_fixed=str(r_fixed))


def verify_D40_full(params, question=None, answer=None):
    a, p, q, lo, hi, r_fixed = (sp.sympify(params[k]) for k in ("a", "p", "q", "lo", "hi", "r_fixed"))
    t, m = sp.symbols("t m", real=True)
    if a <= 1 or q != 4 - p:
        return False
    # Under t=log_a(x), the polynomial must factor identically as
    # (t-1)(t-(m+p-3)); the fixed root t=1 is included in [0,1].
    original = sp.expand((1 + t) ** 2 - (m + p) * t + m - q)
    expected_factor = sp.expand((t - 1) * (t - (m + p - 3)))
    if sp.expand(original - expected_factor) != 0 or r_fixed != 1:
        return False
    # The roots are distinct and both lie in [0,1] exactly when
    # 0 <= m+p-3 < 1, i.e. 3-p <= m < 4-p.
    expected_lo, expected_hi = 3 - p, 4 - p
    if lo != expected_lo or hi != expected_hi:
        return False
    if question is None and answer is None:
        return True
    if question is None or answer is None:
        return False
    generated_question, generated_answer, _, _ = gen_D40(int(a), int(a), int(p))
    def question_stem(text):
        lines = text.splitlines()
        stop = next((i for i, line in enumerate(lines) if re.match(r"^[A-D]\.\s", line)), len(lines))
        return "\n".join(lines[:stop]).strip()
    def answer_body(text):
        return re.sub(r"^[A-D]\.\s*", "", text.strip()).replace(" ", "").replace("$", "").rstrip(".")
    return (question_stem(question) == question_stem(generated_question)
            and answer_body(answer) == answer_body(generated_answer))


# ===================== D16: A^x+(c-m)B^x-m=0 co nghiem thuoc (0,1) ========
def gen_D16(A, B, c):
    A, B, c = sp.Integer(A), sp.Integer(B), sp.Integer(c)
    assert A > B
    f = lambda t: (A ** t + c * B ** t) / (B ** t + 1)
    fp = sp.diff((A ** x + c * B ** x) / (B ** x + 1), x)
    samples = [fp.subs(x, sp.Rational(i, 10)) for i in range(0, 11)]
    assert all(sp.sign(v) == 1 for v in samples)
    f0, f1 = f(0), f(1)
    assert f0 != f1
    lo, hi = (f0, f1) if f0 < f1 else (f1, f0)
    correct = f"({latex(lo)};{latex(hi)})"
    wrong1 = f"[{latex(lo)};{latex(hi)}]"
    wrong2 = f"({latex(lo-1)};{latex(hi)})"
    wrong3 = f"({latex(lo)};{latex(hi+1)})"
    de_bai = (
        f"Tìm tập hợp tất cả các giá trị của tham số thực $m$ để phương trình "
        f"${A}^x+({c}-m){B}^x-m=0$ có nghiệm thuộc khoảng $(0;1)$.\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"PT $\\Leftrightarrow m=\\dfrac{{{A}^x+{c}\\cdot{B}^x}}{{{B}^x+1}}=f(x)$. Hàm $f$ đồng biến trên "
        f"$\\mathbb{{R}}$ (do ${A}>{B}$), nên $0<x<1\\Leftrightarrow f(0)<f(x)<f(1)\\Leftrightarrow {correct}$ "
        f"vì $f(0)={latex(f0)}, f(1)={latex(f1)}$."
    )
    return de_bai, dap_an, loi_giai, dict(A=str(A), B=str(B), c=str(c))


def verify_D16(params):
    A, B, c = (sp.sympify(params[k]) for k in ("A", "B", "c"))
    fp = sp.diff((A ** x + c * B ** x) / (B ** x + 1), x)
    samples = [fp.subs(x, sp.Rational(i, 20)) for i in range(0, 21)]
    return all(sp.sign(v) == 1 for v in samples)


# ===================== D35: log_a(N-a^x)=k-x, tong nghiem qua Viete ========
def gen_D35(a, N, k):
    a, N, k = sp.Integer(a), sp.Integer(N), sp.Integer(k)
    t = sp.Symbol("t", positive=True)
    poly = sp.Poly(t ** 2 - N * t + a ** k, t)
    disc = N ** 2 - 4 * a ** k
    assert disc > 0
    roots = sp.solve(sp.Eq(poly.as_expr(), 0), t)
    assert len(roots) == 2 and all(r.is_real and r > 0 for r in roots)
    total = k  # tong nghiem x1+x2 = log_a(t1*t2) = log_a(a^k) = k, luon dung theo Viete
    correct = str(total)
    wrong1 = str(N)
    wrong2 = str(k + 1)
    wrong3 = str(2 * k)
    vals = bump_until_distinct([sp.Integer(total), N, k + 1, 2 * k])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    de_bai = f"Tổng tất cả các nghiệm của phương trình $\\log_{{{a}}}({N}-{a}^x)={k}-x$ bằng\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"ĐK: ${N}-{a}^x>0$. $\\log_{{{a}}}({N}-{a}^x)={k}-x \\Leftrightarrow {N}-{a}^x={a}^{{{k}-x}}=\\dfrac{{{a}^{{{k}}}}}{{{a}^x}}"
        f"\\Leftrightarrow ({a}^x)^2-{N}\\cdot{a}^x+{a}^{{{k}}}=0$. Đặt $t={a}^x$, PT có 2 nghiệm $t_1,t_2$ với "
        f"$t_1t_2={a}^{{{k}}}$ (Viète), suy ra ${a}^{{x_1+x_2}}={a}^{{{k}}}\\Leftrightarrow x_1+x_2={k}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), N=str(N), k=str(k))


def verify_D35(params):
    a, N, k = (sp.Integer(params[key]) for key in ("a", "N", "k"))
    if a <= 1 or N <= 0:
        return False
    t = sp.Symbol("t", positive=True)
    roots = sp.solve(sp.Eq(t**2-N*t+a**k, 0), t)
    valid = [r for r in roots if r.is_real and r > 0]
    if len(valid) != 2:
        return False
    return sp.simplify(valid[0]*valid[1]-a**k) == 0
def gen_D69(a, lo, hi):
    a, lo, hi = sp.Integer(a), sp.Integer(lo), sp.Integer(hi)
    g = lambda t: a ** t - t
    xv = sp.Symbol("xv", real=True)
    crit = sp.solve(sp.Eq(sp.diff(a ** xv - xv, xv), 0), xv)
    assert len(crit) == 1
    crit = crit[0]
    threshold = -g(crit)
    threshold_f = float(threshold)
    count = 0
    m_list = []
    for mv in range(int(lo) + 1, int(hi)):
        if mv < threshold_f:
            count += 1
            m_list.append(mv)
    assert count > 0
    correct = str(count)
    wrong1, wrong2, wrong3 = str(count + 1), str(count - 1 if count > 1 else count + 2), str(hi - lo - 1)
    de_bai = (
        f"Cho phương trình ${a}^x+m=\\log_{{{a}}}(x-m)$ với $m$ là tham số. Có bao nhiêu giá trị nguyên "
        f"của $m\\in({lo};{hi})$ để phương trình đã cho có nghiệm?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$\\Leftrightarrow {a}^x+x=\\log_{{{a}}}(x-m)+(x-m)$. Xét $f(t)={a}^t+t$ đồng biến trên $\\mathbb{{R}}$ nên "
        f"$x=\\log_{{{a}}}(x-m)\\Leftrightarrow {a}^x=x-m\\Leftrightarrow {a}^x-x=-m$. Xét $g(x)={a}^x-x$ có "
        f"$g'(x)=0$ tại $x\\approx{float(crit):.4f}$, giá trị nhỏ nhất $g_{{\\min}}\\approx{float(g(crit)):.4f}$. "
        f"PT có nghiệm khi $m<{float(threshold):.4f}$. Với $m$ nguyên trong $({lo};{hi})$, có ${count}$ giá trị."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), lo=str(lo), hi=str(hi))


def verify_D69_full(params, expected_count):
    import mpmath as mp
    a, lo, hi = (int(params[k]) for k in ("a", "lo", "hi"))
    if not (a > 1 and lo < hi):
        return False
    with mp.workdps(100):
        la = mp.log(a)
        xcrit = mp.log(1/la)/la
        threshold = xcrit - 1/la
        count = sum(1 for m in range(lo+1, hi) if mp.mpf(m) < threshold)
    return count == int(expected_count)
def gen_D51(A, e_val, F, D):
    A, e_val, F, D = (sp.Integer(v) for v in (A, e_val, F, D))
    dk_hi = sp.Rational(10 ** D, F)
    assert dk_hi == sp.floor(dk_hi) and dk_hi > 0
    dk_hi = sp.Integer(dk_hi)
    # A^x - 5*A^(x+2)/... giu dung cau truc ban goc: 4^x - 5*2^(x+2) + 64 >=0 voi A=2 (4=A^2)
    t = sp.Symbol("t", positive=True)
    poly = t ** 2 - 20 * t + 64  # giu nguyen dang cau truc goc (A=2 co dinh de dam bao dep)
    roots = sp.solve(sp.Eq(poly, 0), t)
    roots = sorted(roots)
    r1, r2 = roots
    assert r1 == sp.floor(r1) and r2 == sp.floor(r2)
    x1, x2 = sp.log(r1, 2), sp.log(r2, 2)
    assert x1 == sp.floor(x1) and x2 == sp.floor(x2)
    lo_x, hi_x = int(x1), int(x2)
    count = (lo_x - 0) + (dk_hi - hi_x) if lo_x >= 0 else None
    # so nguyen trong (0;lo_x] hop [hi_x;dk_hi]
    count = lo_x + (dk_hi - hi_x + 1)
    vals = bump_until_distinct([sp.Integer(count), count + 1, count - 1, dk_hi])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    de_bai = (
        f"Có bao nhiêu số nguyên $x$ thỏa mãn $(4^x-5\\cdot2^{{x+2}}+64)\\sqrt{{{D}-\\log({F}x)}}\\ge 0$?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"ĐKXĐ: $0<x\\le{dk_hi}$. Vì căn $\\ge0$ nên BPT $\\Leftrightarrow 4^x-20\\cdot2^x+64\\ge0"
        f"\\Leftrightarrow 2^x\\le{r1}$ hoặc $2^x\\ge{r2}\\Leftrightarrow x\\le{lo_x}$ hoặc $x\\ge{hi_x}$. "
        f"Kết hợp ĐKXĐ: $S=(0;{lo_x}]\\cup[{hi_x};{dk_hi}]$, có ${count}$ số nguyên."
    )
    return de_bai, dap_an, loi_giai, dict(F=str(F), D=str(D), lo_x=str(lo_x), hi_x=str(hi_x), dk_hi=str(dk_hi))


def verify_D51_full(params, expected_count):
    F, D, lo_x, hi_x, dk_hi = (sp.sympify(params[k]) for k in ("F", "D", "lo_x", "hi_x", "dk_hi"))
    count = 0
    for xv in range(0, int(dk_hi) + 2):
        if xv <= 0 or F * xv <= 0:
            continue
        if sp.log(F * xv, 10) > D:
            continue
        if 4 ** xv - 20 * 2 ** xv + 64 >= 0:
            count += 1
    return count == expected_count


def main():
    fails = []
    fails += try_add("D15", "Đạo hàm hàm hợp chứa lôgarit tự nhiên", "p021_q18", gen_D15, verify_D15,
                      [(v,) for v in (2, 3, 0, 4, 5, 6)])
    fails += try_add("D05", "Nhận biết mệnh đề đúng/sai về biến đổi lôgarit của tích lũy thừa", "p006_q16",
                      gen_D05, verify_D05, [(2, 7), (3, 5), (2, 9), (5, 3), (2, 11), (3, 7)])
    fails += try_add("D45", "Giải bất phương trình mũ bằng đặt ẩn phụ t=a^x", "p099_q31", gen_D45, verify_D45,
                      [(3, 1, -3), (2, 4, -1), (5, 1, -5), (3, 2, -9), (2, 1, -8), (5, 5, -1)])

    for a, p, q in [(2, 2, 7), (3, 1, 6), (2, 3, 8), (5, 2, 9), (3, 2, 5), (2, 1, 6)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D40(a, a, p, q)
        except AssertionError:
            continue
        if verify_D40_full(params):
            add_row("D40", "Tìm tham số để phương trình lôgarit bậc hai (đặt ẩn phụ) có hai nghiệm phân biệt thỏa điều kiện",
                     "p088_q43", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D40", params))

    for A, B, c in [(6, 2, 3), (8, 2, 4), (9, 3, 2), (12, 2, 6), (15, 3, 5), (4, 2, 2)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D16(A, B, c)
        except AssertionError:
            continue
        if verify_D16(params):
            add_row("D16", "Tìm tham số để phương trình mũ có nghiệm thuộc một khoảng (đặt ẩn phụ, xét hàm)",
                     "p021_q20", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D16", params))

    for a, N, k in [(3, 7, 2), (2, 5, 1), (5, 30, 2), (3, 15, 3), (2, 10, 3), (3, 20, 2)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D35(a, N, k)
        except AssertionError:
            continue
        if verify_D35(params):
            add_row("D35", "Giải phương trình lôgarit bằng đặt ẩn phụ t=a^x, tính tổng nghiệm", "p070_q31",
                     de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D35", params))

    for B, k, c in [(4, 4, 5), (5, 5, 7), (6, 6, 10), (7, 7, 13), (8, 8, 17), (9, 9, 21)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D67(B, k, c)
        except AssertionError:
            continue
        expected = int(dap_an.split("$")[1])
        if verify_D67_full(params, expected):
            add_row("D67", "Tìm tham số nguyên để phương trình mũ đặt ẩn phụ có hai nghiệm ẩn phụ phân biệt",
                     "p161_q35", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D67", params))

    for a, lo, hi in [(3, -15, 15), (2, -10, 10), (3, -20, 20), (5, -12, 12)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D69(a, lo, hi)
        except AssertionError:
            continue
        expected = int(dap_an.split("$")[1])
        if verify_D69_full(params, expected):
            add_row("D69", "Đếm giá trị nguyên tham số để phương trình mũ-lôgarit lồng nhau có nghiệm",
                     "p166_q45", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D69", params))

    for F, D in [(4, 2), (2, 3), (5, 3), (2, 2)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D51(2, 2, F, D)
        except AssertionError:
            continue
        expected = int(dap_an.split("$")[1])
        if verify_D51_full(params, expected):
            add_row("D51", "Đếm số nguyên thỏa bất phương trình mũ-lôgarit-căn phức hợp", "p115_q39",
                     de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D51", params))

    with open("data/questions/mu_logarit_extraction/bien_the/batch_round2.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)

    with open("scripts/generate_questions/.tmp_round2_output.txt", "w", encoding="utf-8") as f:
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
