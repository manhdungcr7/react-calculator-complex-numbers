# -*- coding: utf-8 -*-
"""
Nhom "tu dang thuc logarit suy ra quan he giua cac bien" (D32, D37, D44,
D50a, D50b, D64, D72, D77, D87). Moi ham gen_* tra ve de bai/dap an/loi giai theo
DUNG phuong phap cua loi giai goc; verify_* kiem tra doc lap bang thay so
cu the va tinh true dinh nghia (khong dung lai cong thuc rut gon da sinh).

Bo qua D39 (dang co 3 co so khac nhau voi rang buoc dac biet 9=3^2,6=2*3,
4=2^2 giua cac he so, kho tong quat hoa an toan ma khong sinh sai) - ghi
chu ro trong bao cao thay vi ep sinh co the sai.
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

import sympy as sp

ROWS = []


def add_row(ma_dang, ten_dang, id_goc, de_bai, dap_an, loi_giai, params):
    ROWS.append({
        "id_goc": id_goc, "ma_dang": ma_dang, "ten_dang": ten_dang,
        "nguon": "Nhân bản", "loai_bien_the": "chuan",
        "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai, "params": params,
    })


# ===================== D32: doi co so qua an phu ============================
TEN_D32 = "Đổi cơ số lôgarit qua ẩn phụ cho trước"


def gen_D32(p, q, m, n):
    p, q, m, n = (sp.Integer(v) for v in (p, q, m, n))
    assert m != n, "m=n lam cac phuong an trung nhau"
    assert p != q, "p=q lam a=log_q p=1, cau hoi thoai hoa"
    correct = f"\\dfrac{{{n}}}{{{m}a}}"
    wrong1 = f"\\dfrac{{{m}}}{{{n}a}}"
    wrong2 = f"\\dfrac{{{n}a}}{{{m}}}"
    wrong3 = f"\\dfrac{{{m}a}}{{{n}}}"
    de_bai = f"Đặt $\\log_{{{q}}} {p}=a$ khi đó $\\log_{{{p**m}}}{q**n}$ bằng\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$\\log_{{{p**m}}}{q**n}=\\log_{{{p}^{{{m}}}}}{q}^{{{n}}}=\\dfrac{{{n}}}{{{m}}}\\log_{{{p}}} {q}"
        f"=\\dfrac{{{n}}}{{{m}\\log_{{{q}}} {p}}}=\\dfrac{{{n}}}{{{m}a}}$."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), q=str(q), m=str(m), n=str(n))


def verify_D32(params):
    p, q, m, n = (sp.sympify(params[k]) for k in ("p", "q", "m", "n"))
    av = sp.log(p, q)  # a = log_q(p) numerically
    lhs = sp.log(q ** n, p ** m)
    rhs = n / (m * av)
    return abs(float(lhs - rhs)) < 1e-9


# ===================== D37: log_p a = log_{p^k}(ab) => a^(k-1)=b ============
TEN_D37 = "Từ đẳng thức lôgarit hai cơ số khác nhau suy ra quan hệ giữa hai biến"


def gen_D37(p, k):
    p, k = sp.Integer(p), sp.Integer(k)
    km1 = k - 1
    correct = f"a^{{{km1}}}=b" if km1 != 1 else "a=b"
    wrong1 = f"a^{{{k}}}=b"
    wrong2 = "a=b" if km1 != 1 else "a=2b"
    wrong3 = f"a=b^{{{km1}}}" if km1 != 1 else "a=b^{2}"
    de_bai = (
        f"Xét tất cả các số thực dương $a$ và $b$ thỏa mãn $\\log_{{{p}}} a=\\log_{{{p**k}}}(ab)$.\n"
        f"Mệnh đề nào dưới đây đúng?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$\\log_{{{p}}} a=\\log_{{{p}^{{{k}}}}}(ab) \\Leftrightarrow \\log_{{{p}}} a=\\dfrac{{1}}{{{k}}}\\log_{{{p}}}(ab)"
        f"\\Leftrightarrow {k}\\log_{{{p}}} a=\\log_{{{p}}}(ab) \\Leftrightarrow a^{{{k}}}=ab \\Leftrightarrow {correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), k=str(k))


def verify_D37(params):
    p, k = sp.sympify(params["p"]), sp.sympify(params["k"])
    av = sp.Rational(5, 2)
    bv = av ** (k - 1)
    lhs = sp.log(av, p)
    rhs = sp.log(av * bv, p ** k)
    return abs(float(lhs - rhs)) < 1e-9


# ===================== D44: log_p(p^a p^(cb)) = log_{p^k} p ================
TEN_D44 = "Từ đẳng thức lôgarit chứa lũy thừa của cơ số suy ra quan hệ giữa các biến"


def gen_D44(c, k):
    c, k = sp.Integer(c), sp.Integer(k)
    ka, kc = k, k * c
    correct = f"{ka}a+{kc}b=1" if ka != 1 else f"a+{kc}b=1"
    wrong1 = f"{ka}a+{c}b=1"
    wrong2 = f"a+{kc}b=1"
    wrong3 = f"{ka}a-{kc}b=1"
    de_bai = (
        f"Xét số thực $a$ và $b$ thỏa mãn $\\log_2(2^a\\cdot{2**c}^b)=\\log_{{{2**k}}}2$. "
        f"Mệnh đề nào dưới đây đúng\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$\\log_2(2^a\\cdot 2^{{{c}b}})=\\log_{{{2**k}}}2 \\Leftrightarrow a+{c}b=\\dfrac{{1}}{{{k}}} "
        f"\\Leftrightarrow {ka}a+{kc}b=1$."
    )
    return de_bai, dap_an, loi_giai, dict(c=str(c), k=str(k))


def verify_D44(params):
    c, k = sp.sympify(params["c"]), sp.sympify(params["k"])
    av = sp.Rational(3, 2)
    bv = (sp.Rational(1, k) - av) / c
    lhs = sp.log(2 ** av * (2 ** c) ** bv, 2)
    rhs = sp.log(2, 2 ** k)
    return abs(float(lhs - rhs)) < 1e-9


# ===================== D50a: log_c a - m log_c b = n => a=c^n b^m =========
TEN_D50A = "Dùng hiệu hai lôgarit để suy ra quan hệ giữa hai biến"
TEN_D50B = "Dùng tổng hai lôgarit để suy ra quan hệ giữa hai biến"


def gen_D50a(c, m, n):
    c, m, n = sp.Integer(c), sp.Integer(m), sp.Integer(n)
    cn = c ** n
    cn_disp = "" if cn == 1 else str(cn)
    correct = f"a={cn_disp}b^{{{m}}}"
    wrong1 = f"a={m}b+{n}"
    wrong2 = f"a={m}b+{cn}"
    wrong3 = f"a=\\dfrac{{{cn}}}{{b^{{{m}}}}}"
    de_bai = (
        f"Với mọi $a,b$ thỏa mãn $\\log_{{{c}}} a-{m}\\log_{{{c}}} b={n}$, khẳng định nào dưới đây đúng?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$\\log_{{{c}}} a-{m}\\log_{{{c}}} b={n} \\Leftrightarrow \\log_{{{c}}}\\dfrac{{a}}{{b^{{{m}}}}}={n}"
        f"\\Leftrightarrow \\dfrac{{a}}{{b^{{{m}}}}}={c}^{{{n}}} \\Leftrightarrow {correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(c=str(c), m=str(m), n=str(n))


def verify_D50a(params):
    c, m, n = (sp.sympify(params[k]) for k in ("c", "m", "n"))
    bv = sp.Rational(3, 2)
    av = c ** n * bv ** m
    lhs = sp.log(av, c) - m * sp.log(bv, c)
    return abs(float(lhs - n)) < 1e-9


def gen_D50b(c, p, n):
    c, p, n = sp.Integer(c), sp.Integer(p), sp.Integer(n)
    correct = f"a^{{{p}}} b={c**n}"
    wrong1 = f"a^{{{p}}}+b={c*n}"
    wrong2 = f"a^{{{p}}} b={c*n}"
    wrong3 = f"a^{{{p}}}+b={c**n}"
    de_bai = (
        f"Với mọi $a, b$ thỏa mãn $\\log_{{{c}}} a^{{{p}}}+\\log_{{{c}}} b={n}$, "
        f"khẳng định nào sau đây là đúng?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$\\log_{{{c}}} a^{{{p}}}+\\log_{{{c}}} b={n} \\Leftrightarrow \\log_{{{c}}}(a^{{{p}}} b)={n} "
        f"\\Leftrightarrow {correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(c=str(c), p=str(p), n=str(n))


def verify_D50b(params):
    c, p, n = (sp.sympify(params[k]) for k in ("c", "p", "n"))
    av = sp.Rational(4, 3)
    bv = c ** n / av ** p
    lhs = sp.log(av ** p, c) + sp.log(bv, c)
    return abs(float(lhs - n)) < 1e-9


# ===================== D64: log_a x=p, log_b x=q => log_{ab} x = pq/(p+q) ===
TEN_D64 = "Tính giá trị lôgarit theo tích hai cơ số qua công thức đổi cơ số"


def gen_D64(p, q):
    p, q = sp.Integer(p), sp.Integer(q)
    val = sp.Rational(p * q, p + q)
    d1 = sp.Rational(p + q, p * q)
    d2 = sp.Rational(p * q, p - q) if p != q else sp.Rational(p * q, 1)
    d3 = p + q
    vals = utils.bump_until_distinct([val, d1, d2, d3])
    val, d1, d2, d3 = vals
    de_bai = (
        f"Cho $\\log_a x={p}$, $\\log_b x={q}$ với $a,b$ là các số thực lớn hơn 1. Tính $P=\\log_{{ab}}x$.\n\n"
    )
    lines, dap_an = render_mc([latex(val), latex(d1), latex(d2), latex(d3)], 0, prefix="P=")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$\\log_a x={p}\\Rightarrow\\log_x a=\\dfrac1{{{p}}}$; $\\log_b x={q}\\Rightarrow\\log_x b=\\dfrac1{{{q}}}$. "
        f"$P=\\log_{{ab}}x=\\dfrac{{1}}{{\\log_x(ab)}}=\\dfrac{{1}}{{\\log_x a+\\log_x b}}={latex(val)}$."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), q=str(q))


def verify_D64(params):
    p, q = sp.sympify(params["p"]), sp.sympify(params["q"])
    xv = sp.Rational(5, 2)
    av = xv ** (sp.Rational(1, p))
    bv = xv ** (sp.Rational(1, q))
    lhs = sp.log(xv, av * bv)
    rhs = sp.Rational(p * q, p + q)
    return abs(float(lhs - rhs)) < 1e-9


# ===================== D72: a^p b^q = c^r => p log_c a + q log_c b = r =====
TEN_D72 = "Từ đẳng thức lũy thừa của hai biến suy ra tổng lôgarit có hệ số"


def _pow_str(base, exp):
    return base if exp == 1 else f"{base}^{{{exp}}}"


def _coef_log_str(coef, var, c):
    mag = "" if abs(coef) == 1 else str(abs(coef))
    sign = "-" if coef < 0 else ""
    return f"{sign}{mag}\\log_{{{c}}}{var}"


def gen_D72(c, p, q, r):
    c, p, q, r = (sp.Integer(v) for v in (c, p, q, r))
    assert p != 0 and q != 0, "p=0 hoac q=0 lam bien a hoac b bien mat khoi de"
    N = c ** r
    vals = utils.bump_until_distinct([r, N, p + q, r * 2])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    term_p = _coef_log_str(p, "a", c)
    term_q = _coef_log_str(q, "b", c)
    expr = term_p + ("+" + term_q if q > 0 else term_q)
    de_bai = (
        f"Cho $a$ và $b$ là hai số thực dương thỏa mãn ${_pow_str('a', p)}{_pow_str('b', q)}={N}$. "
        f"Giá trị của ${expr}$ bằng\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Ta có $\\log_{{{c}}}({_pow_str('a', p)}{_pow_str('b', q)})=\\log_{{{c}}}{N}\\Leftrightarrow "
        f"{expr}={r}$."
    )
    return de_bai, dap_an, loi_giai, dict(c=str(c), p=str(p), q=str(q), r=str(r))


def verify_D72(params):
    c, p, q, r = (sp.sympify(params[k]) for k in ("c", "p", "q", "r"))
    av = sp.Rational(7, 3)
    bv = (c ** r / av ** p) ** (sp.Rational(1, q))
    lhs = p * sp.log(av, c) + q * sp.log(bv, c)
    return abs(float(lhs - r)) < 1e-9


# ===================== D77: (2^s)^log2(ab) = m*a => a^(s-1) b^s = m =======
TEN_D77 = "Biến đổi biểu thức chứa a^log_a(...) để suy ra quan hệ giữa các biến"


def gen_D77(s, m):
    s, m = sp.Integer(s), sp.Integer(m)
    sm1 = s - 1
    correct = f"a^{{{sm1}}} b^{{{s}}}={m}" if sm1 != 1 else f"ab^{{{s}}}={m}"
    wrong1 = f"a^{{{s}}} b^{{{sm1}}}={m}"
    wrong2 = f"a^{{{sm1}}} b^{{{s}}}={m*2}"
    wrong3 = f"a^{{{s}}} b^{{{s}}}={m}"
    de_bai = (
        f"Cho $a, b$ là hai số thực dương thỏa mãn ${2**s}^{{\\log_2(ab)}}={m}a$. "
        f"Giá trị của $a^{{{sm1}}}b^{{{s}}}$ bằng\n\n"
    ) if sm1 != 1 else (
        f"Cho $a, b$ là hai số thực dương thỏa mãn ${2**s}^{{\\log_2(ab)}}={m}a$. "
        f"Giá trị của $ab^{{{s}}}$ bằng\n\n"
    )
    lines, dap_an = render_mc([str(m), str(m*2), str(m+1), str(m-1) if m > 1 else str(m+2)], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$({2**s})^{{\\log_2(ab)}}=({2}^{{\\log_2(ab)}})^{{{s}}}=(ab)^{{{s}}}={m}a "
        f"\\Leftrightarrow a^{{{sm1}}}b^{{{s}}}={m}$."
    )
    return de_bai, dap_an, loi_giai, dict(s=str(s), m=str(m))


def verify_D77(params):
    s, m = sp.sympify(params["s"]), sp.sympify(params["m"])
    av = sp.Rational(5, 4)
    bv = (m * av / av ** s) ** (sp.Rational(1, s))
    lhs = (2 ** s) ** sp.log(av * bv, 2)
    rhs = m * av
    return abs(float(lhs - rhs)) < 1e-6


# ===================== D87: log_c(c^s a) = B => log_c(c^u a^p) = pB+(u-ps) =
TEN_D87 = "Biểu diễn một lôgarit qua ẩn phụ lôgarit cho trước"


def _coef_const_str(coef, const):
    s = f"{coef}b"
    if const > 0:
        s += f"+{const}"
    elif const < 0:
        s += f"-{-const}"
    return s


def gen_D87(c, s, u, p):
    c, s, u, p = (sp.Integer(v) for v in (c, s, u, p))
    coef = p
    const = u - p * s
    alt_const = 0 if const != 0 else -2
    correct = _coef_const_str(coef, const)
    wrong1 = _coef_const_str(coef, const + 2)
    wrong2 = _coef_const_str(coef * 2, const)
    wrong3 = _coef_const_str(coef, alt_const)
    ka = "" if c**s == 1 else f"{c**s}"
    km = "" if c**u == 1 else f"{c**u}"
    premise_sum = f"{s}+\\log_{{{c}}}a" if s != 0 else f"\\log_{{{c}}}a"
    target_sum = f"{u}+{p}\\log_{{{c}}}a" if u != 0 else f"{p}\\log_{{{c}}}a"
    b_minus_s_paren = "b" if s == 0 else f"(b-{s})"
    target_substitution = f"{u}+{p}{b_minus_s_paren}" if u != 0 else f"{p}{b_minus_s_paren}"
    de_bai = (
        f"Với $a>0$, đặt $\\log_{{{c}}}({ka}a)=b$, khi đó $\\log_{{{c}}}({km}a^{{{p}}})$ bằng\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    b_minus_s = "b" if s == 0 else f"b-{s}"
    if s == 0:
        first_step = f"$\\log_{{{c}}}a=b$.\n"
    else:
        first_step = (
            f"$\\log_{{{c}}}({ka}a)=b\\Leftrightarrow {premise_sum}=b"
            f"\\Leftrightarrow\\log_{{{c}}}a={b_minus_s}$.\n"
        )
    loi_giai = first_step + (
        f"$\\log_{{{c}}}({km}a^{{{p}}})={target_sum}={target_substitution}={correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(c=str(c), s=str(s), u=str(u), p=str(p))


def verify_D87(params):
    c, s, u, p = (sp.sympify(params[k]) for k in ("c", "s", "u", "p"))
    av = sp.Rational(9, 5)
    b_val = sp.log((c ** s) * av, c)
    lhs = sp.log((c ** u) * av ** p, c)
    rhs = p * b_val + (u - p * s)
    return abs(float(lhs - rhs)) < 1e-9


# =============================================================================
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
            margin = 8 if ma_dang in {"D07", "D21", "D28", "D37", "D44", "D64", "D77", "D86"} else 3
            lo, hi = min(values) - margin, max(values) + margin
            if min(values) > 1:
                lo = max(2, lo)
            elif min(values) >= 0:
                lo = max(0, lo)
            domains.append((lo, hi))
        else:
            domains.append(tuple(sorted(set(values), key=str)))
    if ma_dang in {"D02", "D42", "D80"}:
        domains[0] = (2, 91)
    elif ma_dang == "D43":
        domains[0] = (-10, 10)
    rng = random.Random(sum(ord(ch) for ch in ma_dang) + len(ROWS))
    cardinalities = [hi - lo + 1 if len(d) == 2 and all(isinstance(v, int) for v in d) else len(d)
                     for d in domains for lo, hi in ([d] if len(d) == 2 and all(isinstance(v, int) for v in d) else [(0, 0)])]
    combination_count = math.prod(cardinalities)
    max_tries = min(1000, max(50, combination_count * 5))
    tries = 0
    seen_args = set()
    while len(existing) < target and tries < max_tries:
        tries += 1
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


def main():
    fails = []
    fails += try_add("D32", TEN_D32, "p068_q20", gen_D32, verify_D32,
                      [(2, 3, 4, 3), (2, 5, 3, 2), (3, 2, 4, 5), (5, 2, 3, 4), (2, 7, 2, 3), (3, 5, 4, 3)])
    fails += try_add("D37", TEN_D37, "p081_q20", gen_D37, verify_D37,
                      [(2, 3), (3, 2), (5, 3), (2, 4), (3, 4), (2, 2)])
    fails += try_add("D44", TEN_D44, "p098_q29", gen_D44, verify_D44,
                      [(2, 2), (3, 2), (2, 3), (4, 2), (3, 3), (2, 4)])
    fails += try_add("D50a", TEN_D50A, "p113_q31", gen_D50a, verify_D50a,
                      [(2, 3, 2), (3, 2, 1), (2, 2, 3), (5, 3, 1), (2, 4, 2), (3, 3, 2)])
    fails += try_add("D50b", TEN_D50B, "p213_q38", gen_D50b, verify_D50b,
                      [(2, 3, 8), (3, 2, 4), (2, 2, 6), (5, 2, 3), (2, 4, 9), (3, 3, 5)])
    fails += try_add("D64", TEN_D64, "p146_q42", gen_D64, verify_D64,
                      [(3, 4), (2, 5), (4, 3), (5, 2), (2, 7), (3, 5)])
    fails += try_add("D72", TEN_D72, "p176_q25", gen_D72, verify_D72,
                      [(2, 3, 2, 5), (3, 2, 1, 4), (2, 2, 3, 6), (5, 1, 2, 3), (2, 4, 1, 5), (3, 1, 3, 4)])
    fails += try_add("D77", TEN_D77, "p195_q30", gen_D77, verify_D77,
                      [(2, 3), (3, 2), (2, 5), (4, 3), (2, 7), (3, 4)])
    fails += try_add("D87", TEN_D87, "p225_q31", gen_D87, verify_D87,
                      [(2, 1, 2, 3), (2, 2, 1, 2), (3, 1, 3, 2), (2, 1, 4, 3), (3, 2, 2, 3), (2, 3, 1, 2)])

    with open("data/questions/mu_logarit_extraction/bien_the/batch_identities_B.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)

    with open("scripts/generate_questions/.tmp_batchB_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Tong so hang sinh: {len(ROWS)}\n")
        f.write(f"That bai verify: {len(fails)}\n")
        for ma_dang, params in fails:
            f.write(f"  {ma_dang}: {params}\n")


if __name__ == "__main__":
    main()
