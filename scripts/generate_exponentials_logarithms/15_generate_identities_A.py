"""
Sinh bien the cho nhom "rut gon / nhan biet cong thuc logarit" - moi cau la
1 dang thuc DUNG VOI MOI a,b DUONG (khong phai giai phuong trinh). Sinh bien
the bang cach doi cac tham so nguyen trong cong thuc (co so, so mu, he so),
giu nguyen phuong phap bien doi cua loi giai goc.

Kiem tra doc lap: thay so ngau nhien cho a,b (>0) va tinh true LHS/RHS bang
sympy so hoc (khong dung lai bieu thuc da rut gon luc sinh), so sanh bang
sp.log(...) truc tiep.
"""
import json
import random
import sys
from importlib import import_module

sys.path.insert(0, "scripts/generate_questions")
utils = import_module("10_common_utils")
latex = utils.latex
bump_until_distinct = utils.bump_until_distinct
render_mc = utils.render_mc

import sympy as sp

a, b = sp.symbols("a b", positive=True)

ROWS = []


def add_row(ma_dang, ten_dang, id_goc, loai, de_bai, dap_an, loi_giai, params):
    ROWS.append({
        "id_goc": id_goc, "ma_dang": ma_dang, "ten_dang": ten_dang,
        "nguon": "Nhân bản", "loai_bien_the": loai,
        "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai, "params": params,
    })


# =====================================================================
# D06: log_{a^n}(ab) = 1/n + (1/n) log_a b
# =====================================================================
def gen_D06(n):
    n = sp.Integer(n)
    correct = f"\\dfrac{{1}}{{{n}}} + \\dfrac{{1}}{{{n}}}\\log_a b"
    wrong1 = f"{n} + {n}\\log_a b"
    wrong2 = f"\\dfrac{{1}}{{{n**2}}}\\log_a b"
    wrong3 = f"\\dfrac{{1}}{{{n}}} + {n}\\log_a b"
    de_bai = (
        f"Cho các số thực dương $a, b$ với $a \\neq 1$. Mệnh đề nào sau đây đúng?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix=f"\\log_{{a^{{{n}}}}}(ab) = ")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$\\log_{{a^{{{n}}}}}(ab)=\\dfrac{{1}}{{{n}}}\\log_a(ab)=\\dfrac{{1}}{{{n}}}(1+\\log_a b)"
        f"=\\dfrac{{1}}{{{n}}}+\\dfrac{{1}}{{{n}}}\\log_a b$."
    )
    return de_bai, dap_an, loi_giai, dict(n=str(n))


def verify_D06(params):
    n = sp.sympify(params["n"])
    av, bv = sp.Rational(7, 3), sp.Rational(11, 5)
    lhs = sp.log(av * bv, av ** n)
    rhs = sp.Rational(1, n) + sp.Rational(1, n) * sp.log(bv, av)
    return abs(float(lhs - rhs)) < 1e-9


# =====================================================================
# D13: log_c(k*a^p/b) = log_c(k) + p*log_c(a) - log_c(b)
# =====================================================================
def gen_D13(c, k, p):
    c, k, p = sp.Integer(c), sp.Integer(k), sp.Integer(p)
    logk = f"\\log_{{{c}}}{k}" if k != 1 else "0"
    correct = f"{logk}+{p}\\log_{{{c}}} a-\\log_{{{c}}} b" if k != 1 else f"{p}\\log_{{{c}}} a-\\log_{{{c}}} b"
    wrong1 = f"{logk}+{p}\\log_{{{c}}} a+\\log_{{{c}}} b" if k != 1 else f"{p}\\log_{{{c}}} a+\\log_{{{c}}} b"
    wrong2 = f"{logk}+\\dfrac{{1}}{{{p}}}\\log_{{{c}}} a-\\log_{{{c}}} b" if k != 1 else f"\\dfrac{{1}}{{{p}}}\\log_{{{c}}} a-\\log_{{{c}}} b"
    wrong3 = f"{p}({logk}+\\log_{{{c}}} a-\\log_{{{c}}} b)" if k != 1 else f"{p}(\\log_{{{c}}} a-\\log_{{{c}}} b)"
    frac = f"\\dfrac{{{k}a^{{{p}}}}}{{b}}" if k != 1 else f"\\dfrac{{a^{{{p}}}}}{{b}}"
    ka_p = f"{k}a^{{{p}}}" if k != 1 else f"a^{{{p}}}"
    de_bai = (
        f"Với các số thực dương $a, b$ bất kì. Mệnh đề nào dưới đây đúng?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix=f"\\log_{{{c}}}\\left({frac}\\right) = ")
    de_bai += "\n".join(lines)
    step2 = f"{logk}+{p}\\log_{{{c}}} a" if k != 1 else f"{p}\\log_{{{c}}} a"
    loi_giai = (
        f"$\\log_{{{c}}}\\left({frac}\\right)=\\log_{{{c}}}({ka_p})-\\log_{{{c}}} b"
        f"={step2}-\\log_{{{c}}} b$."
    )
    return de_bai, dap_an, loi_giai, dict(c=str(c), k=str(k), p=str(p))


def verify_D13(params):
    c, k, p = (sp.sympify(params[x]) for x in ("c", "k", "p"))
    av, bv = sp.Rational(5, 2), sp.Rational(9, 4)
    lhs = sp.log(k * av ** p / bv, c)
    rhs = sp.log(k, c) + p * sp.log(av, c) - sp.log(bv, c)
    return abs(float(lhs - rhs)) < 1e-9


# =====================================================================
# D36b: evaluate log_b(x^n) using log_b(x^n) = n log_b(x)
# =====================================================================
def gen_D36(base, n):
    base, n = sp.Integer(base), sp.Integer(n)
    correct = f"{n}\\log_{{{base}}} a"
    wrong1 = f"\\dfrac{{1}}{{{n}}}\\log_{{{base}}} a"
    wrong2 = f"{n}+\\log_{{{base}}} a"
    wrong3 = f"\\dfrac{{1}}{{{n}}}+\\log_{{{base}}} a"
    de_bai = f"Với $a$ là số thực dương tùy ý, $\\log_{{{base}}}(a^{{{n}}})$ bằng\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Ta có $\\log_{{{base}}}(a^{{{n}}})={n}\\log_{{{base}}} a$."
    return de_bai, dap_an, loi_giai, dict(base=str(base), n=str(n))


def gen_D36a(n):
    """Recognize the universally valid power rule in the source's statement-selection format."""
    n = sp.Integer(n)
    assert n > 1
    correct = f"\\log(a^{{{n}}})={n}\\log a"
    wrong1 = f"\\log(a^{{{n}}})=\\dfrac{{1}}{{{n}}}\\log a"
    wrong2 = f"\\log({n}a)={n}\\log a"
    wrong3 = f"\\log({n}a)=\\dfrac{{1}}{{{n}}}\\log a"
    de_bai = f"Với $a$ là số thực dương bất kì, mệnh đề nào dưới đây đúng?\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Theo công thức lôgarit của lũy thừa, $\\log(a^{{{n}}})={n}\\log a$. Chọn mệnh đề này."
    return de_bai, dap_an, loi_giai, dict(n=str(n))


def verify_D36a(params):
    n = int(sp.sympify(params["n"]))
    av = sp.Rational(7, 3)
    return abs(float(sp.log(av ** n, 10) - n * sp.log(av, 10))) < 1e-10


def verify_D36b(params):
    base, n = sp.sympify(params["base"]), sp.sympify(params["n"])
    av = sp.Rational(13, 4)
    lhs = sp.log(av ** n, base)
    rhs = n * sp.log(av, base)
    return abs(float(lhs - rhs)) < 1e-9


# =====================================================================
# D30: log_c(a * b^n) = log_c a + n log_c b
# =====================================================================
def gen_D30(c, n):
    c, n = sp.Integer(c), sp.Integer(n)
    correct = f"\\log_{{{c}}} a+{n}\\log_{{{c}}} b"
    wrong1 = f"{n}(\\log_{{{c}}} a+\\log_{{{c}}} b)"
    wrong2 = f"\\log_{{{c}}} a+\\dfrac{{1}}{{{n}}}\\log_{{{c}}} b"
    wrong3 = f"\\log_{{{c}}} a-{n}\\log_{{{c}}} b"
    de_bai = f"Với $a$ và $b$ là hai số thực dương tùy ý, $\\log_{{{c}}}(ab^{{{n}}})$ bằng\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"$\\log_{{{c}}}(ab^{{{n}}})=\\log_{{{c}}} a+\\log_{{{c}}} b^{{{n}}}=\\log_{{{c}}} a+{n}\\log_{{{c}}} b$."
    return de_bai, dap_an, loi_giai, dict(c=str(c), n=str(n))


def verify_D30(params):
    c, n = sp.sympify(params["c"]), sp.sympify(params["n"])
    av, bv = sp.Rational(3, 2), sp.Rational(7, 3)
    lhs = sp.log(av * bv ** n, c)
    rhs = sp.log(av, c) + n * sp.log(bv, c)
    return abs(float(lhs - rhs)) < 1e-9


# =====================================================================
# D54: ln(p*a) - ln(q*a) = ln(p/q)
# =====================================================================
def gen_D54(p, q):
    p, q = sp.Integer(p), sp.Integer(q)
    g = sp.gcd(p, q)
    p2, q2 = p // g, q // g
    correct = f"\\ln\\dfrac{{{p2}}}{{{q2}}}" if q2 != 1 else f"\\ln {p2}"
    wrong1 = f"\\ln\\dfrac{{{q2}}}{{{p2}}}" if p2 != 1 else f"\\ln\\dfrac{{{q2}}}{{1}}"
    wrong2 = f"\\ln({p}\\cdot{q}a^2)"
    wrong3 = "\\ln a"
    de_bai = f"Với $a$ là số thực dương tùy ý, $\\ln({p}a)-\\ln({q}a)$ bằng\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Ta có $\\ln({p}a)-\\ln({q}a)=\\ln\\left(\\dfrac{{{p}a}}{{{q}a}}\\right)={correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), q=str(q))


def verify_D54(params):
    p, q = sp.sympify(params["p"]), sp.sympify(params["q"])
    av = sp.Rational(11, 5)
    lhs = sp.log(p * av) - sp.log(q * av)
    rhs = sp.log(sp.Rational(p, q))
    return abs(float(lhs - rhs)) < 1e-9


# =====================================================================
# D59: log_{a^(1/k)} a = k
# =====================================================================
def gen_D59(k):
    k = sp.Integer(k)
    root = "\\sqrt{a}" if k == 2 else f"\\sqrt[{k}]{{a}}"
    correct, wrong1, wrong2, wrong3 = str(k), f"\\dfrac{{1}}{{{k}}}", str(-k), "0"
    de_bai = f"Cho $a$ là số thực dương khác 1. Tính $I=\\log_{{{root}}}a$.\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="I=")
    de_bai += "\n".join(lines)
    loi_giai = f"$\\log_{{{root}}}a=\\log_{{a^{{1/{k}}}}}a={k}\\log_a a={k}$."
    return de_bai, dap_an, loi_giai, dict(k=str(k))


def verify_D59(params):
    k = sp.sympify(params["k"])
    av = sp.Rational(7, 2)
    lhs = sp.log(av, av ** (sp.Rational(1, k)))
    return abs(float(lhs - k)) < 1e-9


# =====================================================================
# D60: log_a(b^p) + log_{a^m}(b^(m*p)) = 2p log_a b
# =====================================================================
def gen_D60(p, m):
    p, m = sp.Integer(p), sp.Integer(m)
    mp = m * p
    vals_num = utils.bump_until_distinct([sp.Integer(2 * p), p * p, p + m, sp.Rational(2 * p, m)])
    v0, v1, v2, v3 = vals_num
    correct = f"{latex(v0)}\\log_a b"
    wrong1 = f"{latex(v1)}\\log_a b"
    wrong2 = f"{latex(v2)}\\log_a b"
    wrong3 = f"{latex(v3)}\\log_a b"
    de_bai = (
        f"Với $a,b$ là các số thực dương tùy ý và $a$ khác 1, đặt "
        f"$P=\\log_a b^{{{p}}}+\\log_{{a^{{{m}}}}}b^{{{mp}}}$. Mệnh đề nào dưới đây đúng?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="P=")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Ta có $\\log_a b^{{{p}}}={p}\\log_a b$ và $\\log_{{a^{{{m}}}}}b^{{{mp}}}"
        f"=\\dfrac{{{mp}}}{{{m}}}\\log_a b={p}\\log_a b$. Do đó $P={2*p}\\log_a b$."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), m=str(m))


def verify_D60(params):
    p, m = sp.sympify(params["p"]), sp.sympify(params["m"])
    av, bv = sp.Rational(9, 4), sp.Rational(5, 3)
    lhs = sp.log(bv ** p, av) + sp.log(bv ** (m * p), av ** m)
    rhs = 2 * p * sp.log(bv, av)
    return abs(float(lhs - rhs)) < 1e-9


# =====================================================================
# D66: log_c(k*a) = log_c(k) + log_c(a)
# =====================================================================
def gen_D66(c, k):
    c, k = sp.Integer(c), sp.Integer(k)
    logk = sp.log(k, c)
    is_int = logk == sp.floor(logk) and logk.is_rational
    logk_str = latex(logk) if not (logk.is_Integer) else str(logk)
    correct = f"{logk_str}+\\log_{{{c}}} a"
    wrong1 = f"{k}\\log_{{{c}}} a"
    wrong2 = f"{logk_str}-\\log_{{{c}}} a"
    wrong3 = f"\\log_{{{c}}} a-{logk_str}" if logk_str != "0" else f"-\\log_{{{c}}}a"
    de_bai = f"Với $a$ là số thực dương tuỳ ý, $\\log_{{{c}}}({k}a)$ bằng\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Ta có $\\log_{{{c}}}({k}a)=\\log_{{{c}}}{k}+\\log_{{{c}}} a={logk_str}+\\log_{{{c}}} a$."
    return de_bai, dap_an, loi_giai, dict(c=str(c), k=str(k))


def verify_D66(params):
    c, k = sp.sympify(params["c"]), sp.sympify(params["k"])
    av = sp.Rational(17, 6)
    lhs = sp.log(k * av, c)
    rhs = sp.log(k, c) + sp.log(av, c)
    return abs(float(lhs - rhs)) < 1e-9


# =====================================================================
# D76: log_{a^n}(b) = (1/n) log_a(b)
# =====================================================================
def gen_D76(n):
    n = sp.Integer(n)
    correct = f"\\dfrac{{1}}{{{n}}}\\log_a b"
    wrong1 = f"{n}\\log_a b"
    wrong2 = f"{n}+\\log_a b"
    wrong3 = f"\\dfrac{{1}}{{{n}}}+\\log_a b"
    de_bai = (
        f"Với $a, b$ là các số thực dương tuỳ ý và $a \\neq 1$, $\\log_{{a^{{{n}}}}} b$ bằng\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Ta có $\\log_{{a^{{{n}}}}} b=\\dfrac{{1}}{{{n}}}\\log_a b$."
    return de_bai, dap_an, loi_giai, dict(n=str(n))


def verify_D76(params):
    n = sp.sympify(params["n"])
    av, bv = sp.Rational(5, 2), sp.Rational(11, 3)
    lhs = sp.log(bv, av ** n)
    rhs = sp.Rational(1, n) * sp.log(bv, av)
    return abs(float(lhs - rhs)) < 1e-9


# =====================================================================
# D81: log_a(a^(1/n)) = 1/n
# =====================================================================
def gen_D81(n):
    n = sp.Integer(n)
    root = "\\sqrt{a}" if n == 2 else f"\\sqrt[{n}]{{a}}"
    correct, wrong1, wrong2, wrong3 = f"\\dfrac{{1}}{{{n}}}", str(-n), str(n), f"-\\dfrac{{1}}{{{n}}}"
    de_bai = f"Cho $a>0$ và $a\\neq 1$, khi đó $\\log_a {root}$ bằng\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Ta có $\\log_a {root}=\\log_a a^{{1/{n}}}=\\dfrac{{1}}{{{n}}}$."
    return de_bai, dap_an, loi_giai, dict(n=str(n))


def verify_D81(params):
    n = sp.sympify(params["n"])
    av = sp.Rational(9, 2)
    lhs = sp.log(av ** (sp.Rational(1, n)), av)
    return abs(float(lhs - sp.Rational(1, n))) < 1e-9


# =====================================================================
# D90: coef * log_c(sqrt(a)) = (coef/2) log_c a
# =====================================================================
def gen_D90(coef, c):
    coef, c = sp.Integer(coef), sp.Integer(c)
    half = sp.Rational(coef, 2)
    log_name = "\\log" if c == 10 else f"\\log_{{{c}}}"
    correct = f"{latex(half)}{log_name} a"
    wrong1 = f"-{latex(half)}{log_name} a"
    wrong2 = f"-{coef}{log_name} a"
    wrong3 = f"{coef*2}{log_name} a"
    de_bai = f"Với $a$ là số thực dương tùy ý, ${coef}{log_name}\\sqrt{{a}}$ bằng\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Ta có ${coef}{log_name}\\sqrt a={coef}{log_name} a^{{1/2}}"
        f"={coef}\\cdot\\dfrac12{log_name} a={latex(half)}{log_name} a$."
    )
    return de_bai, dap_an, loi_giai, dict(coef=str(coef), c=str(c))


def verify_D90(params):
    coef, c = sp.sympify(params["coef"]), sp.sympify(params["c"])
    av = sp.Rational(13, 4)
    lhs = coef * sp.log(sp.sqrt(av), c)
    rhs = sp.Rational(coef, 2) * sp.log(av, c)
    return abs(float(lhs - rhs)) < 1e-9


# =====================================================================
GENERATORS = {
    "D06": (gen_D06, verify_D06, ["p006_q17"], [(n,) for n in (2, 3, 4, 5, 6)]),
    "D13": (gen_D13, verify_D13, ["p020_q16"],
            [(2, 2, 3), (3, 1, 2), (5, 3, 4), (2, 4, 2), (3, 5, 3), (4, 1, 3)]),
    "D36a": (gen_D36a, verify_D36a, ["p049_q10"],
             [(n,) for n in (2, 3, 4, 5, 6, 7)]),
    "D36b": (gen_D36, verify_D36b, ["p079_q10", "p094_q11", "p171_q05"],
             [(2, 2), (3, 4), (5, 3), (7, 2), (2, 5), (10, 3)]),
    "D30": (gen_D30, verify_D30, ["p065_q05"], [(2, 2), (3, 3), (5, 2), (10, 4), (7, 3), (2, 4)]),
    "D54": (gen_D54, verify_D54, ["p125_q28"], [(3, 2), (5, 3), (7, 4), (4, 3), (9, 5), (5, 2)]),
    "D59": (gen_D59, verify_D59, ["p138_q06"], [(3,), (4,), (5,), (6,), (7,), (8,)]),
    "D60": (gen_D60, verify_D60, ["p139_q15"],
            [(3, 2), (2, 3), (1, 4), (4, 2), (2, 5), (3, 3)]),
    "D66": (gen_D66, verify_D66, ["p154_q11"], [(3, 3), (2, 4), (5, 5), (2, 8), (10, 10), (3, 9)]),
    "D76": (gen_D76, verify_D76, ["p191_q12"], [(2,), (3,), (4,), (5,), (6,), (7,)]),
    "D81": (gen_D81, verify_D81, ["p208_q17"], [(3,), (2,), (4,), (5,), (6,), (7,)]),
    "D90": (gen_D90, verify_D90, ["p237_q17"],
            [(5, 10), (2, 3), (6, 5), (4, 2), (2, 10), (6, 3)]),
}

TEN_DANG_OVERRIDE = {
    "D36a": "Nhận biết mệnh đề đúng về lôgarit của lũy thừa",
    "D36b": "Tính lôgarit của lũy thừa bằng quy tắc đưa số mũ ra trước",
    "D06": "Nhận biết công thức đổi cơ số lôgarit",
    "D13": "Rút gọn biểu thức lôgarit chứa tích, thương và lũy thừa",
    "D30": "Rút gọn biểu thức lôgarit của một tích chứa lũy thừa",
    "D54": "Rút gọn hiệu hai lôgarit tự nhiên cùng cơ số",
    "D59": "Tính giá trị lôgarit có cơ số là căn bậc hai của biến",
    "D60": "Rút gọn tổng nhiều lôgarit cùng biến bằng đổi cơ số",
    "D66": "Tách lôgarit của một tích chứa hằng số thành tổng hai lôgarit",
    "D76": "Nhận biết công thức đổi cơ số lôgarit dạng log_{a^n} b",
    "D81": "Tính giá trị lôgarit của căn bậc ba của chính cơ số",
    "D90": "Rút gọn biểu thức lôgarit có hệ số nhân với lôgarit của căn bậc hai",
}


def expand_type(code, gen_fn, verify_fn, sampler, seed=0, target=90, max_tries=5000):
    rng = random.Random(seed)
    current = [r for r in ROWS if r["ma_dang"] == code]
    seen_params = {tuple(sorted((k,str(v)) for k,v in r["params"].items())) for r in current}
    seen_questions = {r["de_bai"] for r in current}
    seen_args = set()
    made = len(current)
    for _ in range(max_tries):
        if made >= target:
            break
        args = tuple(sampler(rng))
        if args in seen_args:
            continue
        seen_args.add(args)
        try:
            q, ans, sol, params = gen_fn(*args)
        except (AssertionError, ValueError, TypeError, ZeroDivisionError, OverflowError):
            continue
        key = tuple(sorted((k,str(v)) for k,v in params.items()))
        if key in seen_params or q in seen_questions:
            continue
        if code == "D59" and str(params.get("k")) == "2":
            continue
        if code == "D90" and str(params.get("coef")) == "4" and str(params.get("c")) == "10":
            continue
        opts = __import__("re").findall(r"(?m)^([A-D])\.\s*(.+)$", q)
        norm = [__import__("re").sub(r"[\s$.,]", "", v) for _,v in opts]
        if len(opts)!=4 or {c for c,_ in opts}!=set("ABCD") or len(set(norm))!=4:
            continue
        try:
            if not verify_fn(params):
                continue
        except Exception:
            continue
        add_row(code, TEN_DANG_OVERRIDE.get(code, code), GENERATORS[code][2][0], "chuan", q, ans, sol, params)
        seen_params.add(key); seen_questions.add(q); made+=1
    print(f"{code}: {made}/{target}")
    return made


def main():
    all_rows = []
    fail = []
    for ma_dang, (gen_fn, verify_fn, id_list, param_list) in GENERATORS.items():
        idx = 0
        for id_goc in id_list:
            for _ in range(6 // len(id_list) if len(id_list) <= 6 else 1):
                if idx >= len(param_list):
                    break
                p = param_list[idx]
                idx += 1
                de_bai, dap_an, loi_giai, params = gen_fn(*p)
                ok = verify_fn(params)
                if not ok:
                    fail.append((ma_dang, params))
                    continue
                add_row(ma_dang, TEN_DANG_OVERRIDE.get(ma_dang, ma_dang), id_goc, "chuan",
                        de_bai, dap_an, loi_giai, params)
        # dung het param_list con lai cho cau dau tien neu con du
        while idx < len(param_list):
            p = param_list[idx]
            idx += 1
            de_bai, dap_an, loi_giai, params = gen_fn(*p)
            ok = verify_fn(params)
            if not ok:
                fail.append((ma_dang, params))
                continue
            add_row(ma_dang, TEN_DANG_OVERRIDE.get(ma_dang, ma_dang), id_list[0], "chuan",
                    de_bai, dap_an, loi_giai, params)

    samplers = {
        "D06": lambda r: (r.randint(2, 500),),
        "D13": lambda r: (r.randint(2, 30), r.randint(1, 100), r.randint(2, 100)),
        "D36a": lambda r: (r.randint(2, 100),),
        "D36b": lambda r: (r.randint(2, 60), r.randint(2, 100)),
        "D30": lambda r: (r.randint(2, 60), r.randint(2, 100)),
        "D54": lambda r: (r.randint(1, 120), r.randint(1, 120)),
        "D59": lambda r: (r.randint(2, 500),),
        "D60": lambda r: (r.randint(2, 100), r.randint(2, 100)),
        "D66": lambda r: (r.randint(2, 40), r.randint(2, 100)),
        "D76": lambda r: (r.randint(2, 500),),
        "D81": lambda r: (r.randint(2, 500),),
        "D90": lambda r: (r.randint(1, 100), r.randint(2, 60)),
    }
    for code, (gen_fn, verify_fn, ids, _) in GENERATORS.items():
        code_num = int("".join(ch for ch in code[1:] if ch.isdigit()))
        expand_type(code, gen_fn, verify_fn, samplers[code], seed=code_num*97+15)

    with open("data/questions/mu_logarit_extraction/bien_the/batch_identities_A.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)

    with open("scripts/generate_questions/.tmp_batchA_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Tong so hang sinh: {len(ROWS)}\n")
        f.write(f"That bai verify: {len(fail)}\n")
        for ma_dang, params in fail:
            f.write(f"  {ma_dang}: {params}\n")


if __name__ == "__main__":
    main()
