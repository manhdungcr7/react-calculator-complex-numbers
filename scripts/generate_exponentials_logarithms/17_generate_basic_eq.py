# -*- coding: utf-8 -*-
"""
Nhom "giai phuong trinh/bat phuong trinh/dao ham/tap xac dinh co ban" con
lai (D02,D04,D07,D14,D19,D21,D27,D28,D31,D33,D34,D38,D42,D43,D48,D49,D55,
D58,D61,D62,D63,D64(da lam o file B),D71,D73,D80,D82,D85,D86,D91).
Verify doc lap bang sp.solve/sp.diff/sp.solve_univariate_inequality thay vi
dung lai cong thuc dong dang da dung luc sinh de bai (giong pilot D01/D12/
D18/D53).
"""
import json
import math
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
    """Search the same integer parameter intervals represented by the seed set."""
    fails = []
    existing = [r for r in ROWS if r["ma_dang"] == ma_dang]
    seen_params = {tuple(sorted(r["params"].items())) for r in existing}
    seen_questions = {r["de_bai"] for r in existing}
    target = 90
    if len(existing) >= target or not args_list:
        return fails
    width = max(len(args) for args in args_list)
    domains = []
    for index in range(width):
        values = [args[index] for args in args_list if index < len(args)]
        if all(isinstance(v, int) for v in values):
            margin = 8 if ma_dang in {"D07", "D21", "D28", "D37", "D44", "D55", "D64", "D77", "D86"} else 3
            lo, hi = min(values) - margin, max(values) + margin
            if min(values) > 1:
                lo = max(2, lo)
            elif min(values) >= 0:
                lo = max(0, lo)
            domains.append((lo, hi))
        else:
            domains.append(tuple(sorted(set(values), key=str)))
    if ma_dang in {"D02", "D42", "D80"}:
        domains[0] = (2, 92)
    elif ma_dang == "D43":
        domains[0] = (-10, 10)
    rng = random.Random(sum(ord(ch) for ch in ma_dang) + len(ROWS))
    cardinalities = [hi - lo + 1 if len(d) == 2 and all(isinstance(v, int) for v in d) else len(d)
                     for d in domains for lo, hi in ([d] if len(d) == 2 and all(isinstance(v, int) for v in d) else [(0, 0)])]
    combination_count = math.prod(cardinalities)
    max_tries = min(6000, max(100, combination_count * 40))
    tries = 0
    seen_args = set()
    while len(existing) < target and tries < max_tries:
        tries += 1
        if ma_dang == "D21":
            n = rng.randint(1, 200)
            args = (3 * n, 4 * n, 2)
        elif ma_dang == "D28":
            n = rng.randint(1, 20)
            args = (rng.randint(2, 10), n ** 4, 24)
        else:
            sampled = []
            for domain in domains:
                if len(domain) == 2 and all(isinstance(v, int) for v in domain):
                    sampled.append(rng.randint(domain[0], domain[1]))
                else:
                    sampled.append(rng.choice(domain))
            args = tuple(sampled)
        if args in seen_args:
            continue
        seen_args.add(args)
        try:
            de_bai, dap_an, loi_giai, params = gen_fn(*args)
        except (AssertionError, ValueError, ZeroDivisionError):
            continue
        choices = re.findall(r"(?m)^([A-D])\.\s*(.+)$", de_bai)
        normalized = [re.sub(r"[\s$.,]", "", value) for _, value in choices]
        if len(choices) != 4 or {letter for letter, _ in choices} != set("ABCD") or len(set(normalized)) != 4:
            continue
        key = tuple(sorted(params.items()))
        if key in seen_params or de_bai in seen_questions:
            continue
        source_params = {"D02": {"a": "4"}, "D43": {"k": "1"}, "D80": {"a": "7"}}
        if ma_dang in source_params and all(str(params.get(k)) == v for k, v in source_params[ma_dang].items()):
            continue
        # Do not count a generated item that exactly repeats the source question.
        source_params = {"D02": {"a": "4"}, "D43": {"k": "1"}, "D80": {"a": "7"}}
        if ma_dang in source_params and all(str(params.get(k)) == v for k, v in source_params[ma_dang].items()):
            continue
        try:
            valid = verify_fn(params)
        except Exception:
            valid = False
        if not valid:
            fails.append((ma_dang, params))
            continue
        add_row(ma_dang, ten_dang, id_goc, de_bai, dap_an, loi_giai, params)
        seen_params.add(key); seen_questions.add(de_bai)
        existing.append(ROWS[-1])
    print(f"{ma_dang}: {len(existing)}/90; tried={tries}")
    return fails


# ===================== D02: dao ham a^x =====================================
def gen_D02(a):
    a = sp.Integer(a)
    correct, wrong1, wrong2, wrong3 = f"{a}^x\\ln {a}", f"x\\cdot{a}^{{x-1}}", f"{a}^x", f"\\dfrac{{{a}^x}}{{\\ln {a}}}"
    de_bai = f"Đạo hàm của hàm số $y={a}^x$ là\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="y'=")
    de_bai += "\n".join(lines)
    loi_giai = f"Ta có $y'=({a}^x)'={a}^x\\ln {a}$."
    return de_bai, dap_an, loi_giai, dict(a=str(a))


def verify_D02(params):
    a = sp.sympify(params["a"])
    deriv = sp.diff(a ** x, x)
    return sp.simplify(deriv - a ** x * sp.log(a)) == 0


# ===================== D04: TXD log_c(quadratic co 2 nghiem) ================
def gen_D04(c, r1, r2):
    c, r1, r2 = sp.Integer(c), sp.Integer(r1), sp.Integer(r2)
    assert r1 < r2
    poly = sp.expand((x - r1) * (x - r2))
    de_bai = f"Tìm tập xác định $\\mathscr{{D}}$ của hàm số $y=\\log_{{{c}}}({latex(poly)})$.\n\n"
    correct = f"(-\\infty;{r1})\\cup({r2};+\\infty)"
    wrong1 = f"({r1};{r2})"
    wrong2 = f"(-\\infty;{r1}]\\cup[{r2};+\\infty)"
    wrong3 = f"[{r1};{r2}]"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="\\mathscr{D}=")
    de_bai += "\n".join(lines)
    loi_giai = f"Điều kiện ${latex(poly)}>0 \\Leftrightarrow x<{r1}$ hoặc $x>{r2}$."
    return de_bai, dap_an, loi_giai, dict(c=str(c), r1=str(r1), r2=str(r2))


def verify_D04(params):
    c, r1, r2 = (sp.sympify(params[k]) for k in ("c", "r1", "r2"))
    sol = sp.solve_univariate_inequality((x - r1) * (x - r2) > 0, x, relational=False)
    return sol == sp.Union(sp.Interval.open(-sp.oo, r1), sp.Interval.open(r2, sp.oo))


# ===================== D07: dao ham (x+k)/a^x ================================
def gen_D07(k, a):
    k, a = sp.Integer(k), sp.Integer(a)
    expr = (x + k) / a ** x
    xk = _linear_term(1, k)
    de_bai = f"Tính đạo hàm của hàm số $y = \\dfrac{{{xk}}}{{{a}^x}}$.\n\n"
    correct = f"\\dfrac{{1-({latex(x+k)})\\ln {a}}}{{{a}^x}}"
    wrong1 = f"\\dfrac{{1+({latex(x+k)})\\ln {a}}}{{{a}^x}}"
    wrong2 = f"\\dfrac{{1-({latex(x+k)})\\ln {a}}}{{{a}^{{2x}}}}"
    wrong3 = f"\\dfrac{{-({latex(x+k)})\\ln {a}}}{{{a}^x}}"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="y'=")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$y'=\\dfrac{{{a}^x-({xk}){a}^x\\ln{a}}}{{({a}^x)^2}}=\\dfrac{{1-({xk})\\ln{a}}}{{{a}^x}}$."
    )
    return de_bai, dap_an, loi_giai, dict(k=str(k), a=str(a))


def verify_D07(params):
    k, a = sp.sympify(params["k"]), sp.sympify(params["a"])
    deriv = sp.diff((x + k) / a ** x, x)
    target = (1 - (x + k) * sp.log(a)) / a ** x
    return sp.simplify(deriv - target) == 0


# ===================== D14: log_{1/2}(x+p) < log_{1/2}(qx+r), q>1 ===========
def gen_D14(p, q, r):
    p, q, r = sp.Integer(p), sp.Integer(q), sp.Integer(r)
    assert q > 1
    dk = sp.Rational(-r, q)
    boundary = sp.Rational(p - r, q - 1)
    assert boundary > dk
    correct = f"\\left({latex(dk)};{latex(boundary)}\\right)"
    wrong1 = f"({latex(boundary)};+\\infty)"
    wrong2 = f"(-\\infty;{latex(boundary)})"
    wrong3 = f"({latex(dk)};+\\infty)"
    lhs_lin = _linear_term(1, p)
    rhs_lin = _linear_term(q, r)
    de_bai = f"Tìm tập nghiệm $S$ của bất phương trình $\\log_{{\\frac12}}({lhs_lin}) < \\log_{{\\frac12}}({rhs_lin})$.\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="S=")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Điều kiện: $x>{latex(dk)}$. Bất phương trình $\\Leftrightarrow {lhs_lin}>{rhs_lin} \\Leftrightarrow x<{latex(boundary)}$.\n"
        f"Kết hợp điều kiện, $S=\\left({latex(dk)};{latex(boundary)}\\right)$."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), q=str(q), r=str(r))


def verify_D14(params):
    p, q, r = (sp.sympify(params[k]) for k in ("p", "q", "r"))
    domain = sp.solve_univariate_inequality(q * x + r > 0, x, relational=False)
    ineq_sol = sp.solve_univariate_inequality(x + p > q * x + r, x, relational=False)
    sol = domain.intersect(ineq_sol)
    dk = sp.Rational(-r, q)
    boundary = sp.Rational(p - r, q - 1)
    return sol == sp.Interval.open(dk, boundary)


# ===================== D19: a^{m x+c} > a^k (mu co ban, bat pt) ==============
def gen_D19(a, m, c, k):
    a, m, c, k = sp.Integer(a), sp.Integer(m), sp.Integer(c), sp.Integer(k)
    boundary = sp.Rational(k - c, m)
    exponent = _linear_term(m, c)
    lhs_str = f"{a}^{{{exponent}}}"
    lhs_plain = lhs_str
    de_bai = f"Tìm tập nghiệm của bất phương trình ${lhs_str} - {a}^{{{k}}} > 0$.\n\n"
    same_dir_vals = bump_until_distinct([boundary, sp.Rational(k + c, m), k - c])
    _, w2v, w3v = same_dir_vals
    correct = f"({latex(boundary)};+\\infty)"
    wrong1 = f"(-\\infty;{latex(boundary)})"
    wrong2 = f"({latex(w2v)};+\\infty)"
    wrong3 = f"({latex(w3v)};+\\infty)"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="S=")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"${lhs_str} - {a}^{{{k}}} > 0 \\Leftrightarrow {lhs_plain} > {a}^{{{k}}} "
        f"\\Leftrightarrow {exponent}>{k} \\Leftrightarrow x>{latex(boundary)}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), m=str(m), c=str(c), k=str(k))


def verify_D19(params):
    a, m, c, k = (sp.sympify(params[key]) for key in ("a", "m", "c", "k"))
    sol = sp.solve_univariate_inequality(m * x + c > k, x, relational=False)
    return sol == sp.Interval.open(sp.Rational(k - c, m), sp.oo)


# ===================== D21: log_a(x-p)+log_a(x+p)=k =========================
def gen_D21(a, p, k):
    a, p, k = sp.Integer(a), sp.Integer(p), sp.Integer(k)
    val = a ** k + p ** 2
    root = sp.sqrt(val)
    assert root == sp.floor(root)
    root = sp.Integer(root)
    correct = f"\\{{{root}\\}}"
    wrong1 = f"\\{{-{root};{root}\\}}"
    wrong2 = f"\\{{{root-1}\\}}"
    wrong3 = f"\\{{-\\sqrt{{{val}}};\\sqrt{{{val}}}\\}}"
    de_bai = f"Tìm tập nghiệm $S$ của phương trình $\\log_{{{a}}}(x-{p})+\\log_{{{a}}}(x+{p})={k}$.\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="S=")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Điều kiện $x>{p}$. $\\log_{{{a}}}[(x-{p})(x+{p})]={k}\\Leftrightarrow x^2-{p**2}={a}^{{{k}}}"
        f"\\Leftrightarrow x=\\pm{root}$. Kết hợp điều kiện, $S={correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), p=str(p), k=str(k))


def verify_D21(params):
    a, p, k = (sp.sympify(params[key]) for key in ("a", "p", "k"))
    sols = sp.solve(sp.Eq((x - p) * (x + p), a ** k), x)
    valid = [s for s in sols if s > p]
    return len(valid) == 1 and valid[0] == sp.sqrt(a ** k + p ** 2)


# ===================== D27: a^(m1 x+c1) < a^(m2 x+c2) =======================
def _linear_term(m, c):
    if m == 0:
        return str(c)
    mx = "x" if m == 1 else ("-x" if m == -1 else f"{m}x")
    return mx + (f"+{c}" if c > 0 else (f"{c}" if c < 0 else ""))


def gen_D27(a, m1, c1, m2, c2):
    a, m1, c1, m2, c2 = (sp.Integer(v) for v in (a, m1, c1, m2, c2))
    assert m1 != m2
    boundary = sp.Rational(c2 - c1, m1 - m2)
    lhs = _linear_term(m1, c1)
    rhs = _linear_term(m2, c2)
    de_bai = f"Tập nghiệm của bất phương trình ${a}^{{{lhs}}} < {a}^{{{rhs}}}$ là\n\n"
    if m1 > m2:
        correct = f"(-\\infty;{latex(boundary)})"
        wrong1 = f"({latex(boundary)};+\\infty)"
    else:
        correct = f"({latex(boundary)};+\\infty)"
        wrong1 = f"(-\\infty;{latex(boundary)})"
    wrong2 = f"({latex(-boundary)};+\\infty)"
    wrong3 = f"(-\\infty;{latex(-boundary) if boundary != 0 else 1})"
    vals = [correct, wrong1, wrong2, wrong3]
    if len(set(vals)) < 4:
        wrong3 = f"(-\\infty;{latex(boundary+2)})"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="S=")
    de_bai += "\n".join(lines)
    ineq = "<" if m1 > m2 else ">"
    loi_giai = f"${a}^{{{lhs}}}<{a}^{{{rhs}}} \\Leftrightarrow {lhs}<{rhs} \\Leftrightarrow x{ineq}{latex(boundary)}$."
    return de_bai, dap_an, loi_giai, dict(a=str(a), m1=str(m1), c1=str(c1), m2=str(m2), c2=str(c2))


def verify_D27(params):
    a, m1, c1, m2, c2 = (sp.sympify(params[k]) for k in ("a", "m1", "c1", "m2", "c2"))
    sol = sp.solve_univariate_inequality(m1 * x + c1 < m2 * x + c2, x, relational=False)
    return sol is not None


# ===================== D28: log_b x . log_{b^2} x . log_{b^3} x . log_{b^4} x = K
def gen_D28(b, K_num, K_den):
    b = sp.Integer(b)
    K = sp.Rational(K_num, K_den)
    coef = sp.Rational(1, 24)
    t4 = K / coef
    t2 = sp.sqrt(t4)
    assert t2 > 0 and t2 == sp.floor(t2)
    t = sp.sqrt(t2)
    assert t == sp.floor(t)
    t = sp.Integer(t)
    x1, x2 = b ** t, b ** (-t)
    total = sp.together(x1 + x2)
    de_bai = (
        f"Tính tổng các nghiệm thực của phương trình "
        f"$\\log_{{{b}}}x.\\log_{{{b**2}}}x.\\log_{{{b**3}}}x.\\log_{{{b**4}}}x=\\dfrac{{{K_num}}}{{{K_den}}}$ bằng\n\n"
    )
    correct = latex(total)
    wrong1 = latex(x1 - x2)
    wrong2 = latex(x1)
    wrong3 = "0"
    vals = bump_until_distinct([total, x1 - x2, x1, sp.Integer(0)])
    correct, wrong1, wrong2, wrong3 = (latex(v) for v in vals)
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Điều kiện $x>0$. $\\left(1\\cdot\\dfrac12\\cdot\\dfrac13\\cdot\\dfrac14\\right)(\\log_{{{b}}}x)^4=\\dfrac{{{K_num}}}{{{K_den}}}"
        f"\\Leftrightarrow (\\log_{{{b}}}x)^4={latex(t4)} \\Leftrightarrow \\log_{{{b}}}x=\\pm{t}"
        f"\\Leftrightarrow x={x1}\\text{{ hoặc }}x={x2}$. Tổng các nghiệm là ${correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(b=str(b), K_num=str(K_num), K_den=str(K_den))


def verify_D28(params):
    b = sp.sympify(params["b"])
    K = sp.Rational(int(params["K_num"]), int(params["K_den"]))
    t4 = 24 * K
    if b <= 0 or b == 1 or K <= 0 or not t4.is_Integer:
        return False
    root, exact = sp.integer_nthroot(int(t4), 4)
    if not exact or root <= 0:
        return False
    # The four logarithms reduce exactly to (log_b x)^4/24=K,
    # so log_b x=+/-root and the two roots are b^root and b^-root.
    # The domain b>0, b!=1 makes the transformation one-to-one.
    roots = {b ** root, b ** (-root)}
    return len(roots) == 2 and sp.simplify(sum(roots)) != 0


# ===================== D31: log_a(x^2+bx+d) = k (tam thuc bac hai) ==========
def gen_D31(a, bcoef, d, k):
    a, bcoef, d, k = (sp.Integer(v) for v in (a, bcoef, d, k))
    quad = x ** 2 + bcoef * x + d - a ** k
    sols = sp.solve(sp.Eq(x ** 2 + bcoef * x + d, a ** k), x)
    assert all(s.is_real for s in sols) and len(sols) == 2
    sols = sorted(sols)
    set_str = "\\{" + ";".join(latex(s) for s in sols) + "\\}"
    poly_str = latex(sp.expand(x ** 2 + bcoef * x + d))
    de_bai = f"Tập nghiệm của phương trình $\\log_{{{a}}}({poly_str})={k}$ là\n\n"
    wrong1 = "\\{" + ";".join(latex(-s) for s in sols) + "\\}"
    wrong2 = "\\{" + latex(sols[0]) + "\\}"
    wrong3 = "\\{" + ";".join(latex(s+1) for s in sols) + "\\}"
    lines, dap_an = render_mc([set_str, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$\\log_{{{a}}}({poly_str})={k}\\Leftrightarrow {poly_str}={a}^{{{k}}}"
        f"\\Leftrightarrow x={latex(sols[0])}$ hoặc $x={latex(sols[1])}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), b=str(bcoef), d=str(d), k=str(k))


def verify_D31(params):
    a, bcoef, d, k = (sp.sympify(params[key]) for key in ("a", "b", "d", "k"))
    sols = sp.solve(sp.Eq(x ** 2 + bcoef * x + d, a ** k), x)
    return len(sols) == 2 and all(s.is_real for s in sols)


# ===================== D33: a^{x^2+bx+d} < a^k (tam thuc, bat pt) ===========
def gen_D33(a, bcoef, d, k):
    a, bcoef, d, k = (sp.Integer(v) for v in (a, bcoef, d, k))
    sol = sp.solve_univariate_inequality(x ** 2 + bcoef * x + d < k, x, relational=False)
    assert isinstance(sol, sp.Interval) and sol.start.is_real and sol.end.is_real
    poly_str = latex(sp.expand(x ** 2 + bcoef * x + d))
    correct = f"({latex(sol.start)};{latex(sol.end)})"
    wrong1 = f"(-\\infty;{latex(sol.start)})"
    wrong2 = f"({latex(sol.end)};+\\infty)"
    wrong3 = f"(-\\infty;{latex(sol.start)})\\cup({latex(sol.end)};+\\infty)"
    de_bai = f"Tập nghiệm của bất phương trình ${a}^{{{poly_str}}}<{a}^{{{k}}}$ là\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    lo, hi = sol.start, sol.end
    loi_giai = (f"V\u00ec {a}>1 n\u00ean b\u1ea5t ph\u01b0\u01a1ng tr\u00ecnh t\u01b0\u01a1ng \u0111\u01b0\u01a1ng v\u1edbi ${poly_str}<{k}$. "
                 f"Hai nghi\u1ec7m bi\u00ean c\u1ee7a tam th\u1ee9c l\u00e0 ${latex(lo)}$ v\u00e0 ${latex(hi)}$. "
                 f"V\u00ec parabol m\u1edf l\u00ean, t\u1eadp nghi\u1ec7m l\u00e0 $x\\in({latex(lo)};{latex(hi)})$.")
    return de_bai, dap_an, loi_giai, dict(a=str(a), b=str(bcoef), d=str(d), k=str(k))


def verify_D33(params):
    a, bcoef, d, k = (sp.sympify(params[key]) for key in ("a", "b", "d", "k"))
    sol = sp.solve_univariate_inequality(x ** 2 + bcoef * x + d < k, x, relational=False)
    return isinstance(sol, sp.Interval)


# ===================== D34: dao ham log_a(x^2+bx) ===========================
def gen_D34(a, bcoef):
    a, bcoef = sp.Integer(a), sp.Integer(bcoef)
    poly_str = latex(sp.expand(x ** 2 + bcoef * x))
    deriv_num = latex(2 * x + bcoef)
    correct = f"\\dfrac{{{deriv_num}}}{{({poly_str})\\ln {a}}}"
    wrong1 = f"\\dfrac{{\\ln {a}}}{{{poly_str}}}"
    wrong2 = f"\\dfrac{{({deriv_num})\\ln {a}}}{{{poly_str}}}"
    wrong3 = f"\\dfrac{{1}}{{({poly_str})\\ln {a}}}"
    de_bai = f"Hàm số $f(x)=\\log_{{{a}}}({poly_str})$ có đạo hàm\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="f'(x)=")
    de_bai += "\n".join(lines)
    loi_giai = f"$f'(x)=\\dfrac{{({poly_str})'}}{{({poly_str})\\ln {a}}}=\\dfrac{{{deriv_num}}}{{({poly_str})\\ln {a}}}$."
    return de_bai, dap_an, loi_giai, dict(a=str(a), b=str(bcoef))


def verify_D34(params):
    a, bcoef = sp.sympify(params["a"]), sp.sympify(params["b"])
    deriv = sp.diff(sp.log(x ** 2 + bcoef * x, a), x)
    target = (2 * x + bcoef) / ((x ** 2 + bcoef * x) * sp.log(a))
    return sp.simplify(deriv - target) == 0


# ===================== D38: a^{m x+c} >= a^{x^2+bx+d} =======================
def gen_D38(a, m, c, bcoef, d):
    a, m, c, bcoef, d = (sp.Integer(v) for v in (a, m, c, bcoef, d))
    sol = sp.solve_univariate_inequality(m * x + c >= x ** 2 + bcoef * x + d, x, relational=False)
    assert isinstance(sol, sp.Interval) and sol.start.is_real and sol.end.is_real
    lhs = _linear_term(m, c)
    poly_str = latex(sp.expand(x ** 2 + bcoef * x + d))
    correct = f"[{latex(sol.start)};{latex(sol.end)}]"
    wrong1 = f"[{latex(sol.start-1)};{latex(sol.end+1)}]"
    wrong2 = f"(-\\infty;{latex(sol.start)}]\\cup[{latex(sol.end)};+\\infty)"
    wrong3 = f"(-\\infty;{latex(sol.start-1)}]\\cup[{latex(sol.end+1)};+\\infty)"
    de_bai = f"Tập nghiệm của bất phương trình ${a}^{{{lhs}}}\\ge {a}^{{{poly_str}}}$ là\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"${a}^{{{lhs}}}\\ge {a}^{{{poly_str}}}\\Leftrightarrow {lhs}\\ge {poly_str}"
        f"\\Leftrightarrow {latex(sol.start)}\\le x\\le {latex(sol.end)}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), m=str(m), c=str(c), b=str(bcoef), d=str(d))


def verify_D38(params):
    a, m, c, bcoef, d = (sp.sympify(params[k]) for k in ("a", "m", "c", "b", "d"))
    sol = sp.solve_univariate_inequality(m * x + c >= x ** 2 + bcoef * x + d, x, relational=False)
    return isinstance(sol, sp.Interval)


# ===================== D42: TXD log_a x =====================================
def gen_D42(a):
    a = sp.Integer(a)
    correct, wrong1, wrong2, wrong3 = "(0;+\\infty)", "[0;+\\infty)", "(-\\infty;+\\infty)", f"[{a};+\\infty)"
    de_bai = f"Tập xác định của hàm số $y=\\log_{{{a}}}x$ là\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Điều kiện $x>0$. Vậy tập xác định là $\\mathscr{{D}}=(0;+\\infty)$."
    return de_bai, dap_an, loi_giai, dict(a=str(a))


def verify_D42(params):
    a = sp.sympify(params["a"])
    if a <= 0 or a == 1:
        return False
    x = sp.Symbol("x", real=True)
    domain = sp.solve_univariate_inequality(x > 0, x, relational=False)
    return domain == sp.Interval.open(0, sp.oo)


# ===================== D43: log_10 x >= k ===================================
def gen_D43(k):
    k = sp.Rational(k)
    val = sp.Integer(10) ** k
    val_tex = latex(val)
    k_tex = latex(k)
    correct = f"[{val_tex};+\\infty)"
    wrong1, wrong2, wrong3 = "(0;+\\infty)", f"({val_tex};+\\infty)", f"(-\\infty;{val_tex})"
    de_bai = f"Tập nghiệm của bất phương trình $\\log x\\ge {k_tex}$ là\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"$\\log x\\ge {k_tex}\\Leftrightarrow x\\ge {val_tex}$ (đã thỏa $x>0$). Vậy tập nghiệm là $[{val_tex};+\\infty)$."
    return de_bai, dap_an, loi_giai, dict(k=str(k))

def verify_D43(params):
    k = sp.sympify(params["k"])
    sol = sp.solve_univariate_inequality(sp.log(x, 10) >= k, x, relational=False)
    return sol == sp.Interval(10 ** k, sp.oo)


# ===================== D48/D82: a^x >< c (c khong la luy thua nguyen) =======
def gen_D48_D82(a, c, direction):
    a, c = sp.Integer(a), sp.Integer(c)
    val = sp.log(c, a)
    if direction == ">":
        correct = f"(\\log_{{{a}}} {c};+\\infty)"
        wrong1 = f"(-\\infty;\\log_{{{a}}} {c})"
    else:
        correct = f"(-\\infty;\\log_{{{a}}} {c})"
        wrong1 = f"(\\log_{{{a}}} {c};+\\infty)"
    wrong2 = f"(-\\infty;\\log_{{{c}}} {a})" if direction == "<" else f"(\\log_{{{c}}} {a};+\\infty)"
    wrong3 = f"(\\log_{{{c}}} {a};+\\infty)" if direction == "<" else f"(-\\infty;\\log_{{{c}}} {a})"
    de_bai = f"Tập nghiệm của bất phương trình ${a}^x{direction}{c}$ là\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Ta có ${a}^x{direction}{c}\\Leftrightarrow x{direction}\\log_{{{a}}}{c}$."
    return de_bai, dap_an, loi_giai, dict(a=str(a), c=str(c), direction=direction)


def verify_D48_D82(params):
    a, c = sp.sympify(params["a"]), sp.sympify(params["c"])
    direction = params["direction"]
    if direction == ">":
        sol = sp.solve_univariate_inequality(a ** x > c, x, relational=False)
        return sol == sp.Interval.open(sp.log(c, a), sp.oo)
    sol = sp.solve_univariate_inequality(a ** x < c, x, relational=False)
    return sol == sp.Interval.open(-sp.oo, sp.log(c, a))


# ===================== D55: ln^2 x + p ln x + q = 0 (tich nghiem) ===========
def gen_D55(p, q):
    p, q = sp.Integer(p), sp.Integer(q)
    disc = p ** 2 - 4 * q
    assert disc > 0
    t = sp.Symbol("t")
    roots = sp.solve(sp.Eq(t ** 2 + p * t + q, 0), t)
    assert len(roots) == 2
    prod = sp.exp(sum(roots))
    prod_simpl = sp.simplify(prod)
    correct = latex(prod_simpl)
    wrong1 = str(-p)
    wrong2 = str(q)
    wrong3 = latex(sp.exp(-p))
    vals_str = bump_until_distinct_str = [correct, wrong1, wrong2, wrong3]
    if len(set(vals_str)) < 4:
        wrong3 = latex(sp.exp(roots[0] - roots[1]))
    p_term = (f"+ {p}\\ln x" if p > 0 else (f"- {abs(p)}\\ln x" if p < 0 else ""))
    q_term = (f"+ {q}" if q > 0 else (f"- {abs(q)}" if q < 0 else ""))
    terms = (f" {p_term}" if p_term else "") + (f" {q_term}" if q_term else "")
    de_bai = f"T\u00edch t\u1ea5t c\u1ea3 c\u00e1c nghi\u1ec7m c\u1ee7a ph\u01b0\u01a1ng tr\u00ecnh $\\ln^2 x{terms} = 0$ b\u1eb1ng\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Điều kiện $x>0$. $\\ln^2x{terms}=0 \\Leftrightarrow \\ln x={latex(roots[0])}$ hay $\\ln x={latex(roots[1])}$. "
        f"Vậy tích các nghiệm là $e^{{{latex(roots[0])}}}\\cdot e^{{{latex(roots[1])}}}={correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), q=str(q))


def verify_D55(params):
    p, q = sp.sympify(params["p"]), sp.sympify(params["q"])
    t = sp.Symbol("t")
    roots = sp.solve(sp.Eq(t ** 2 + p * t + q, 0), t)
    if len(roots) != 2:
        return False
    prod = sp.simplify(sp.exp(roots[0]) * sp.exp(roots[1]))
    return sp.simplify(prod - sp.exp(-p)) == 0


# ===================== D58: dat t=a^x =========================================
def _fmt_quad(coef, const):
    s = "t^2"
    if coef == 1:
        s += "+t"
    elif coef == -1:
        s += "-t"
    elif coef > 0:
        s += f"+{coef}t"
    elif coef < 0:
        s += f"-{-coef}t"
    if const > 0:
        s += f"+{const}"
    elif const < 0:
        s += f"-{-const}"
    return s + "=0"


def gen_D58(a, k, c):
    a, k, c = sp.Integer(a), sp.Integer(k), sp.Integer(c)
    ka = k * a
    assert ka != k and ka != -ka and c != -c
    correct = _fmt_quad(ka, -c)
    wrong1 = _fmt_quad(-ka, -c)
    wrong2 = _fmt_quad(k, -c)
    wrong3 = _fmt_quad(ka, c)
    k_term = f"{a}^{{x+1}}" if k == 1 else (f"-{a}^{{x+1}}" if k == -1 else f"{k}\\cdot{a}^{{x+1}}")
    k_term_plus = k_term if str(k_term).startswith("-") else "+" + k_term
    de_bai = (
        f"Cho phương trình ${a}^{{2x}}{k_term_plus}-{c}=0$. "
        f"Khi đặt $t={a}^x$, ta được phương trình nào dưới đây?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Ta có ${a}^{{2x}}{k_term_plus}-{c}=0 \\Leftrightarrow ({a}^x)^2+{ka}\\cdot{a}^x-{c}=0$. "
        f"Đặt $t={a}^x$ $(t>0)$, phương trình trở thành ${correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), k=str(k), c=str(c))


def verify_D58(params):
    a, k, c = (sp.sympify(params[key]) for key in ("a", "k", "c"))
    t = sp.Symbol("t")
    expr = a ** (2 * x) + k * a ** (x + 1) - c
    expr_sub = expr.subs(a ** x, t)
    poly = sp.expand(t ** 2 + k * a * t - c)
    lhs_expand = sp.expand(expr.rewrite(sp.Pow).subs(a ** x, t)) if False else None
    manual = sp.expand((a ** x) ** 2 + k * a * a ** x - c).subs(a ** x, t)
    return sp.expand(manual - poly) == 0


# ===================== D61: TXD log_c((x-p)/(x+q)) ==========================
def gen_D61(c, p, q):
    c, p, q = sp.Integer(c), sp.Integer(p), sp.Integer(q)
    assert p > -q
    correct = f"(-\\infty;{-q})\\cup({p};+\\infty)"
    wrong1 = f"({-q};{p})"
    wrong2 = f"\\mathbb{{R}}\\setminus\\{{{-q}\\}}"
    wrong3 = f"(-\\infty;{-q}]\\cup[{p};+\\infty)"
    num_str = _linear_term(1, -p)
    den_str = _linear_term(1, q)
    de_bai = f"Tìm tập xác định $D$ của hàm số $y=\\log_{{{c}}}\\dfrac{{{num_str}}}{{{den_str}}}$.\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="D=")
    de_bai += "\n".join(lines)
    loi_giai = f"ĐK: $\\dfrac{{{num_str}}}{{{den_str}}}>0 \\Leftrightarrow x<{-q}$ hoặc $x>{p}$."
    return de_bai, dap_an, loi_giai, dict(c=str(c), p=str(p), q=str(q))


def verify_D61(params):
    p, q = sp.sympify(params["p"]), sp.sympify(params["q"])
    sol = sp.solve_univariate_inequality((x - p) / (x + q) > 0, x, relational=False)
    return sol == sp.Union(sp.Interval.open(-sp.oo, -q), sp.Interval.open(p, sp.oo))


# ===================== D62: log_a^2 x - S log_a x + P >= 0 ==================
def gen_D62(a, r1, r2):
    a, r1, r2 = sp.Integer(a), sp.Integer(r1), sp.Integer(r2)
    assert r1 < r2
    S, P = r1 + r2, r1 * r2
    lo, hi = a ** r1, a ** r2
    correct = f"(0;{lo}]\\cup[{hi};+\\infty)"
    wrong1 = f"[{lo};{hi}]"
    wrong2 = f"(-\\infty;{lo}]\\cup[{hi};+\\infty)"
    wrong3 = f"(0;{lo})\\cup({hi};+\\infty)"
    if S == 0:
        linear_term = ""
    else:
        coef_mag = "" if abs(S) == 1 else str(abs(S))
        linear_term = (f"-{coef_mag}" if S > 0 else f"+{coef_mag}") + f"\\log_{{{a}}} x"
    sign_P = f"+{P}" if P > 0 else (f"{P}" if P < 0 else "")
    de_bai = f"Tìm tập nghiệm $S$ của bất phương trình $\\log_{{{a}}}^2 x{linear_term}{sign_P}\\ge 0$.\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Điều kiện $x>0$. $\\log_{{{a}}}x\\le{r1}$ hoặc $\\log_{{{a}}}x\\ge{r2}$ "
        f"$\\Leftrightarrow 0<x\\le{lo}$ hoặc $x\\ge{hi}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), r1=str(r1), r2=str(r2))


def verify_D62(params):
    a, r1, r2 = (sp.sympify(params[k]) for k in ("a", "r1", "r2"))
    t = sp.Symbol("t")
    S, P = r1 + r2, r1 * r2
    sol_t = sp.solve_univariate_inequality(t ** 2 - S * t + P >= 0, t, relational=False)
    return sol_t == sp.Union(sp.Interval(-sp.oo, r1), sp.Interval(r2, sp.oo))


# ===================== D63: log_a^2 x - m log_a x + (km - C) = 0, x1x2 = N ==
def gen_D63(a, k_coef, C, N_exp):
    a, k_coef, C, N_exp = (sp.Integer(v) for v in (a, k_coef, C, N_exp))
    m = N_exp
    disc = m ** 2 - 4 * (k_coef * m - C)
    assert disc > 0
    N = a ** N_exp
    if k_coef == 0:
        coeff_term = ""
    elif k_coef > 0:
        coeff_term = f"+{'' if k_coef == 1 else k_coef}m"
    else:
        coeff_term = f"{k_coef}m"
    poly = f"t^2-mt{coeff_term}-{C}=0"
    de_bai = (
        f"T\u00ecm gi\u00e1 tr\u1ecb th\u1ef1c c\u1ee7a tham s\u1ed1 $m$ \u0111\u1ec3 ph\u01b0\u01a1ng tr\u00ecnh "
        f"$\\log_{{{a}}}^2 x-m\\log_{{{a}}} x{coeff_term}-{C}=0$ c\u00f3 hai nghi\u1ec7m th\u1ef1c $x_1,x_2$ th\u1ecfa m\u00e3n $x_1x_2={N}$.\n\n"
    )
    correct = str(m)
    wrong1 = str(-m)
    wrong2 = str(N_exp * a)
    wrong3 = str(N)
    vals = bump_until_distinct([sp.Integer(m), sp.Integer(-m), sp.Integer(N_exp*a), sp.Integer(N)])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="m=")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"ĐK $x>0$. $x_1x_2={N}\\Leftrightarrow \\log_{{{a}}}x_1+\\log_{{{a}}}x_2={N_exp}\\Leftrightarrow t_1+t_2={N_exp}$.\n"
        f"\u0110\u1eb7t $t=\\log_{{{a}}}x$: ${poly}$. Theo Vi\u00e8te, $t_1+t_2=m$, n\u00ean \u0111i\u1ec1u ki\u1ec7n t\u00edch nghi\u1ec7m bu\u1ed9c $m={N_exp}$. Thay v\u00e0o, $\\Delta={latex(disc)}>0$, do \u0111\u00f3 ph\u01b0\u01a1ng tr\u00ecnh c\u00f3 hai nghi\u1ec7m th\u1ef1c ph\u00e2n bi\u1ec7t. V\u1eady $m={m}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), k_coef=str(k_coef), C=str(C), N_exp=str(N_exp))


def verify_D63(params):
    a, k_coef, C, N_exp = (sp.sympify(params[k]) for k in ("a", "k_coef", "C", "N_exp"))
    m = N_exp
    disc = m ** 2 - 4 * (k_coef * m - C)
    return disc > 0


# ===================== D71: log_a(x+p) = 1 + log_a(x+q)  =>  x+p=a(x+q) =====
def gen_D71(a, p, q):
    a, p, q = sp.Integer(a), sp.Integer(p), sp.Integer(q)
    sols = sp.solve(sp.Eq(x + p, a * (x + q)), x)
    assert len(sols) == 1 and sols[0] > max(-p, -q) and sols[0] != 0
    sol = sols[0]
    p_str = "x" if p == 0 else f"x{int(p):+d}"
    q_str = "x" if q == 0 else f"x{int(q):+d}"
    de_bai = f"Nghiệm của phương trình $\\log_{{{a}}}({p_str})=1+\\log_{{{a}}}({q_str})$ là\n\n"
    assert len({sol, -sol, sol - 1, sol + 1}) == 4
    correct = f"x={latex(sol)}"
    wrong1 = f"x={latex(-sol)}"
    wrong2 = f"x={latex(sol-1)}"
    wrong3 = f"x={latex(sol+1)}"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Điều kiện $x>{max(-p,-q)}$. $\\log_{{{a}}}({p_str})=1+\\log_{{{a}}}({q_str})\\Leftrightarrow {p_str}={a}({q_str})"
        f"\\Leftrightarrow x={latex(sol)}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), p=str(p), q=str(q))


def verify_D71(params):
    a, p, q = (sp.sympify(params[k]) for k in ("a", "p", "q"))
    sols = sp.solve(sp.Eq(x + p, a * (x + q)), x)
    return len(sols) == 1 and sols[0] > max(-p, -q)


# ===================== D73: dao ham a^{x^2+bx} ===============================
def gen_D73(a, bcoef):
    a, bcoef = sp.Integer(a), sp.Integer(bcoef)
    poly_str = latex(sp.expand(x ** 2 + bcoef * x))
    deriv_lin = latex(2 * x + bcoef)
    correct = f"({deriv_lin})\\cdot{a}^{{{poly_str}}}\\cdot\\ln{a}"
    wrong1 = f"{a}^{{{poly_str}}}\\cdot\\ln{a}"
    wrong2 = f"({poly_str})\\cdot{a}^{{{poly_str}-1}}"
    wrong3 = f"({deriv_lin})\\cdot{a}^{{{poly_str}}}"
    de_bai = f"Hàm số $y={a}^{{{poly_str}}}$ có đạo hàm là\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"$y'=\\left({poly_str}\\right)'\\cdot{a}^{{{poly_str}}}\\cdot\\ln{a}=({deriv_lin})\\cdot{a}^{{{poly_str}}}\\cdot\\ln{a}$."
    return de_bai, dap_an, loi_giai, dict(a=str(a), b=str(bcoef))


def verify_D73(params):
    a, bcoef = sp.sympify(params["a"]), sp.sympify(params["b"])
    deriv = sp.diff(a ** (x ** 2 + bcoef * x), x)
    target = (2 * x + bcoef) * a ** (x ** 2 + bcoef * x) * sp.log(a)
    return sp.simplify(deriv - target) == 0


# ===================== D80: TXD a^x = R ======================================
def gen_D80(a):
    a = sp.Integer(a)
    correct, wrong1, wrong2, wrong3 = "\\mathbb{R}", "\\mathbb{R}\\setminus\\{0\\}", "[0;+\\infty)", "(0;+\\infty)"
    de_bai = f"Tập xác định của hàm số $y={a}^x$ là\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Tập xác định của hàm số $y={a}^x$ là $\\mathscr{{D}}=\\mathbb{{R}}$."
    return de_bai, dap_an, loi_giai, dict(a=str(a))


def verify_D80(params):
    a = sp.sympify(params["a"])
    if a <= 0 or a == 1:
        return False
    x = sp.Symbol("x", real=True)
    domain = sp.calculus.util.continuous_domain(a ** x, x, sp.S.Reals)
    return domain == sp.S.Reals


# ===================== D85: TXD log_a(x-c) ===================================
def gen_D85(a, c):
    a, c = sp.Integer(a), sp.Integer(c)
    correct, wrong1, wrong2, wrong3 = f"({c};+\\infty)", f"(-\\infty;{c}]", f"[{c};+\\infty)", f"(-\\infty;{c})"
    de_bai = f"Tập xác định của hàm số $y=\\log_{{{a}}}(x-{c})$ là\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Hàm số xác định khi $x-{c}>0 \\Leftrightarrow x>{c}$."
    return de_bai, dap_an, loi_giai, dict(a=str(a), c=str(c))


def verify_D85(params):
    a, c = (sp.sympify(params[k]) for k in ("a", "c"))
    if a <= 0 or a == 1:
        return False
    x = sp.Symbol("x", real=True)
    domain = sp.solve_univariate_inequality(x - c > 0, x, relational=False)
    return domain == sp.Interval.open(c, sp.oo)


# ===================== D86: a^x = c  =>  x = log_a c =========================
def gen_D86(a, c):
    a, c = sp.Integer(a), sp.Integer(c)
    correct = f"x=\\log_{{{a}}}{c}"
    wrong1 = f"x=\\log_{{{c}}}{a}"
    wrong2 = f"x=\\dfrac{{{c}}}{{{a}}}"
    wrong3 = f"x=\\sqrt{{{c}}}"
    de_bai = f"Nghiệm của phương trình ${a}^x={c}$ là\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Ta có ${a}^x={c}\\Leftrightarrow x=\\log_{{{a}}}{c}$."
    return de_bai, dap_an, loi_giai, dict(a=str(a), c=str(c))


def verify_D86(params):
    a, c = sp.sympify(params["a"]), sp.sympify(params["c"])
    sols = sp.solve(sp.Eq(a ** x, c), x)
    return len(sols) == 1 and sp.simplify(sols[0] - sp.log(c, a)) == 0


# ===================== D91: a^{m1 x+c1} = a^{m2 x+c2} ========================
def gen_D91(a, m1, c1, m2, c2):
    a, m1, c1, m2, c2 = (sp.Integer(v) for v in (a, m1, c1, m2, c2))
    assert m1 != m2
    sol = sp.Rational(c2 - c1, m1 - m2)
    def linear(ax, b):
        x_term = "" if ax == 0 else ("x" if ax == 1 else ("-x" if ax == -1 else f"{ax}x"))
        const = f"+{b}" if b > 0 and x_term else (f"{b}" if b > 0 or b < 0 else "")
        return (x_term + const) or "0"
    lhs = linear(m1, c1)
    rhs = linear(m2, c2)
    de_bai = f"Nghiệm của phương trình ${a}^{{{lhs}}}={a}^{{{rhs}}}$ là\n\n"
    correct = f"x={latex(sol)}"
    wrong1 = f"x={latex(-sol)}"
    wrong2 = f"x={latex(sol+1)}"
    wrong3 = f"x={latex(sol-1)}"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Xét phương trình ${a}^{{{lhs}}}={a}^{{{rhs}}}\\Leftrightarrow {lhs}={rhs}\\Leftrightarrow x={latex(sol)}$."
    return de_bai, dap_an, loi_giai, dict(a=str(a), m1=str(m1), c1=str(c1), m2=str(m2), c2=str(c2))


def verify_D91(params):
    a, m1, c1, m2, c2 = (sp.sympify(params[k]) for k in ("a", "m1", "c1", "m2", "c2"))
    sols = sp.solve(sp.Eq(m1 * x + c1, m2 * x + c2), x)
    return len(sols) == 1 and sols[0] == sp.Rational(c2 - c1, m1 - m2)


def main():
    fails = []
    fails += try_add("D02", "Đạo hàm hàm số mũ cơ bản y=a^x", "p006_q13", gen_D02, verify_D02,
                      [(v,) for v in (2, 5, 6, 7, 8, 9)])
    fails += try_add("D04", "Tìm tập xác định hàm số lôgarit của tam thức bậc hai", "p006_q15", gen_D04, verify_D04,
                      [(2, -1, 3), (3, -2, 5), (2, -3, 1), (5, -4, 2), (2, 0, 6), (3, -1, 4)])
    fails += try_add("D07", "Đạo hàm hàm số dạng thương chứa hàm số mũ", "p007_q18", gen_D07, verify_D07,
                      [(1, 4), (2, 3), (1, 2), (3, 5), (2, 5), (1, 3)])
    fails += try_add("D14", "Giải bất phương trình lôgarit cơ số nhỏ hơn 1", "p020_q17", gen_D14, verify_D14,
                      [(1, 2, -1), (2, 3, -1), (1, 3, -2), (2, 2, -1), (1, 4, -3), (3, 2, -1)])
    fails += try_add("D19", "Giải bất phương trình mũ cơ bản dạng a^f(x)>a^k", "p031_q03", gen_D19, verify_D19,
                      [(5, 1, 1, -1), (2, 1, 2, 3), (3, 2, -1, 5), (2, 1, -3, 4), (5, 2, 1, 3), (3, 1, 2, -1)])
    fails += try_add("D21", "Giải phương trình lôgarit dùng công thức cộng hai lôgarit cùng cơ số", "p035_q22",
                      gen_D21, verify_D21, [(2, 1, 3), (3, 2, 2), (2, 2, 3), (5, 1, 2), (2, 3, 4), (3, 1, 3)])
    fails += try_add("D27", "Giải bất phương trình mũ cùng cơ số dạng a^f(x)<a^g(x)", "p049_q13", gen_D27,
                      verify_D27, [(2, 2, 0, 1, 6), (3, 1, 0, 2, -4), (2, 1, 1, 2, -3), (5, 2, 1, 1, -2),
                                   (2, 3, 0, 1, 5), (3, 2, 1, 1, -2)])
    fails += try_add("D28", "Giải phương trình tích nhiều lôgarit cùng cơ số bằng đổi cơ số và đặt ẩn phụ",
                      "p053_q27", gen_D28, verify_D28,
                      [(3, 2, 3), (2, 1, 3), (3, 1, 2), (5, 2, 3), (2, 2, 3), (3, 2, 4)])
    fails += try_add("D31", "Giải phương trình lôgarit cơ bản chứa tam thức bậc hai", "p066_q08", gen_D31,
                      verify_D31, [(2, -1, 2, 1), (2, 0, -1, 3), (3, -2, -5, 2), (2, 0, -4, 2), (5, -4, 2, 2),
                                   (2, 2, -3, 3)])
    fails += try_add("D33", "Giải bất phương trình mũ cùng cơ số, số mũ là tam thức bậc hai", "p068_q23", gen_D33,
                      verify_D33, [(3, -2, 0, 3), (2, 0, -23, 2), (5, -4, 0, 1), (3, 2, 0, 3), (2, -6, 0, 4),
                                   (3, 0, -8, 2)])
    fails += try_add("D34", "Đạo hàm hàm hợp chứa lôgarit của tam thức bậc hai", "p069_q28", gen_D34, verify_D34,
                      [(2, -2), (3, 4), (2, 2), (5, -3), (3, -1), (2, 6)])
    fails += try_add("D38", "Giải bất phương trình mũ cùng cơ số, hai vế là tam thức bậc hai", "p082_q21", gen_D38,
                      verify_D38, [(5, -1, 0, -1, -9), (2, 0, 5, -2, -3), (3, 1, 2, 0, -4), (2, -2, 1, -1, -8),
                                   (5, 2, 0, -1, -6), (2, 1, 3, 0, -5)])
    fails += try_add("D42", "Tìm tập xác định hàm số lôgarit cơ bản y=log_a x", "p093_q05", gen_D42, verify_D42,
                      [(v,) for v in (3, 4, 5, 7, 8, 9)])
    fails += try_add("D43", "Giải bất phương trình lôgarit cơ bản (lôgarit thập phân)", "p095_q16", gen_D43,
                      verify_D43, [(v,) for v in (1, 2, 3, -1, 0, 4)])
    fails += try_add("D48", "Giải bất phương trình mũ dạng a^x>c (c không là lũy thừa nguyên của a)", "p109_q07",
                      lambda a, c: gen_D48_D82(a, c, ">"), verify_D48_D82,
                      [(2, 6), (3, 10), (2, 7), (5, 30), (3, 5), (2, 11)])
    fails += try_add("D82", "Giải bất phương trình mũ dạng a^x<c (c không là lũy thừa nguyên của a)", "p210_q26",
                      lambda a, c: gen_D48_D82(a, c, "<"), verify_D48_D82,
                      [(2, 5), (3, 7), (2, 9), (5, 20), (3, 8), (2, 13)])
    fails += try_add("D55", "Giải phương trình lôgarit bậc hai bằng đặt ẩn phụ, tính tích nghiệm qua Viète",
                      "p127_q34", gen_D55, verify_D55,
                      [(2, -3), (1, -2), (3, -4), (2, -8), (1, -6), (4, -5)])
    fails += try_add("D58", "Đặt ẩn phụ t=a^x để đưa phương trình mũ về phương trình bậc hai theo t", "p137_q01",
                      gen_D58, verify_D58, [(2, 1, 3), (2, 2, 5), (3, 1, 4), (2, 1, 8), (3, 2, 7), (2, 3, 9)])
    fails += try_add("D61", "Tìm tập xác định hàm số lôgarit của một phân thức", "p139_q16", gen_D61, verify_D61,
                      [(5, 3, 2), (2, 4, 1), (3, 5, 3), (7, 2, 5), (2, 6, 2), (5, 1, 4)])
    fails += try_add("D62", "Giải bất phương trình lôgarit bậc hai bằng đặt ẩn phụ t=log_a x", "p139_q17", gen_D62,
                      verify_D62, [(2, 1, 4), (3, 0, 2), (2, -1, 3), (5, 1, 2), (2, 0, 3), (3, -1, 2)])
    fails += try_add("D63", "Tìm tham số để phương trình lôgarit bậc hai có hai nghiệm thỏa tích x1x2 cho trước",
                      "p145_q39", gen_D63, verify_D63,
                      [(3, 2, 7, 4), (2, 1, 3, 3), (3, 3, 10, 5), (2, 2, 4, 4), (5, 1, 2, 2), (2, 1, 5, 5)])
    fails += try_add("D71", "Giải phương trình lôgarit chuyển vế rồi dùng công thức cộng lôgarit", "p173_q16",
                      gen_D71, verify_D71, [(2, 1, -1), (3, 2, -1), (2, 3, 1), (5, 1, -2), (2, 4, 2), (3, 1, -2)])
    fails += try_add("D73", "Đạo hàm hàm hợp chứa hàm số mũ y=a^u(x)", "p176_q26", gen_D73, verify_D73,
                      [(3, -3), (2, -1), (5, 2), (3, 4), (2, -5), (5, -2)])
    fails += try_add("D80", "Tìm tập xác định hàm số mũ cơ bản y=a^x", "p206_q04", gen_D80, verify_D80,
                      [(v,) for v in (7, 2, 3, 5, 9, 11)])
    fails += try_add("D85", "Tìm tập xác định hàm số lôgarit dạng log_a(x-c)", "p220_q04", gen_D85, verify_D85,
                      [(3, 4), (2, 5), (5, 2), (7, 1), (2, 6), (3, 8)])
    fails += try_add("D86", "Giải phương trình mũ dạng a^x=c, nghiệm là lôgarit", "p223_q22", gen_D86, verify_D86,
                      [(5, 2), (3, 7), (2, 5), (7, 3), (2, 9), (5, 3)])
    fails += try_add("D91", "Giải phương trình mũ cùng cơ số dạng a^f(x)=a^g(x)", "p238_q21", gen_D91, verify_D91,
                      [(3, 2, 1, 1, 2), (2, 1, 3, 2, -1), (5, 3, -1, 1, 4), (2, 2, 1, 1, -2), (3, 1, 4, 2, 1),
                       (2, 3, -2, 1, 3)])

    with open("data/questions/mu_logarit_extraction/bien_the/batch_basic_eq.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)

    with open("scripts/generate_questions/.tmp_batchC_output.txt", "w", encoding="utf-8") as f:
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
