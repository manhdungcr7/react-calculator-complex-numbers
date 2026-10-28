# -*- coding: utf-8 -*-
"""Round 7: D17 (thiet ke nguoc chon t roi suy k2, giong D68/D94)."""
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

ROWS = []


def add_row(ma_dang, ten_dang, id_goc, de_bai, dap_an, loi_giai, params):
    ROWS.append({
        "id_goc": id_goc, "ma_dang": ma_dang, "ten_dang": ten_dang,
        "nguon": "Nhân bản", "loai_bien_the": "chuan",
        "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai, "params": params,
    })


# ===================== D17: P=k1(1+t)^2+k2/t, t=log_{a/b}b, chon t truoc ===
def gen_D17(k1, t_num, t_den):
    k1 = sp.Integer(k1)
    t0 = sp.Rational(t_num, t_den)
    k2 = 2 * k1 * t0 ** 2 * (1 + t0)
    assert k2 == sp.floor(k2) and k2 > 0
    k2 = sp.Integer(k2)
    t = sp.Symbol("t", positive=True)
    P = k1 * (1 + t) ** 2 + k2 / t
    Pmin = P.subs(t, t0)
    assert Pmin == sp.floor(Pmin) and Pmin > 0
    Pmin = sp.Integer(Pmin)
    k1_disp = "" if k1 == 1 else str(k1)
    de_bai = (
        f"Xét các số thực $a, b$ thỏa mãn $a>b>1$. Tìm giá trị nhỏ nhất $P_{{\\min}}$ của biểu thức "
        f"$P = \\log^2_{{\\frac{{a}}{{b}}}}(a^{{{2*k1 if False else 2}}}) + {k2}\\log_b\\left(\\dfrac{{a}}{{b}}\\right)$"
        if k1 == 1 else
        f"Xét các số thực $a, b$ thỏa mãn $a>b>1$. Tìm giá trị nhỏ nhất $P_{{\\min}}$ của biểu thức "
        f"$P = {k1}\\log^2_{{\\frac{{a}}{{b}}}}(a) + {k2}\\log_b\\left(\\dfrac{{a}}{{b}}\\right)$"
    )
    de_bai = (
        f"Xét các số thực $a, b$ thỏa mãn $a>b>1$. Tìm giá trị nhỏ nhất $P_{{\\min}}$ của biểu thức "
        f"$P = {k1_disp}\\log^2_{{\\frac{{a}}{{b}}}}a + {k2}\\log_b\\left(\\dfrac{{a}}{{b}}\\right)$.\n\n"
    )
    correct = f"P_{{\\min}}={Pmin}"
    wrong1 = f"P_{{\\min}}={Pmin+1}"
    wrong2 = f"P_{{\\min}}={Pmin-1}"
    wrong3 = f"P_{{\\min}}={2*Pmin}"
    vals = bump_until_distinct([Pmin, Pmin + 1, Pmin - 1, 2 * Pmin])
    v0, v1, v2, v3 = vals
    correct, wrong1, wrong2, wrong3 = (f"P_{{\\min}}={v}" for v in (v0, v1, v2, v3))
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Đặt $t=\\log_{{a/b}}b>0$. Ta có $\\log_{{a/b}}a=1+t$ và $\\log_b(a/b)=\\dfrac1t$, nên "
        f"$P={k1_disp}(1+t)^2+\\dfrac{{{k2}}}{{t}}=f(t)$. Xét $f'(t)={2*k1}(1+t)-\\dfrac{{{k2}}}{{t^2}}$, "
        f"$f'(t)=0$ tại $t={latex(t0)}$ (nghiệm dương duy nhất). $f\\left({latex(t0)}\\right)={Pmin}$ là giá "
        f"trị nhỏ nhất. Vậy $P_{{\\min}}={Pmin}$."
    )
    return de_bai, dap_an, loi_giai, dict(k1=str(k1), k2=str(k2), t0=str(t0))


def verify_D17(params):
    k1, k2, t0 = (float(sp.sympify(params[k])) for k in ("k1", "k2", "t0"))
    claimed = k1 * (1 + t0) ** 2 + k2 / t0
    samples = [k1 * (1 + i/1000.0) ** 2 + k2 / (i/1000.0)
               for i in range(1, 5000, 5)]
    sampled_min = min(samples)
    return abs(sampled_min - claimed) < 0.05 and claimed <= sampled_min + 1e-6


def gen_D65(b, C, m, n):
    b, C, m, n = sp.Integer(b), sp.Integer(C), sp.Integer(m), sp.Integer(n)
    K = 1 + b * C
    xv = sp.Symbol("xv", positive=True)
    yv_expr = (b * C - m * xv) / (b * xv + n)
    P = xv + yv_expr
    Pd = sp.diff(P, xv)
    crit = [c for c in sp.solve(sp.Eq(sp.numer(sp.together(Pd)), 0), xv) if c.is_real and c > 0]
    assert len(crit) == 1
    x0 = crit[0]
    y0 = yv_expr.subs(xv, x0)
    assert y0 > 0
    Pmin = sp.simplify(sp.radsimp(P.subs(xv, x0)))
    assert Pmin.is_real and not Pmin.is_rational  # dang can dep nhu ban goc
    correct = latex(Pmin)
    wrong1 = latex(-Pmin)
    wrong2 = latex(Pmin + 1)
    wrong3 = latex(2 * Pmin)
    vals_ok = len({correct, wrong1, wrong2, wrong3}) == 4
    assert vals_ok
    my_str = f"{m}x" if m != 1 else "x"
    ny_str = f"{n}y" if n != 1 else "y"
    de_bai = (
        f"Xét các số thực dương $x,y$ thỏa mãn $\\log_{{{b}}}\\dfrac{{{C}-xy}}{{{my_str}+{ny_str}}}="
        f"{b}xy+{my_str}+{ny_str}-{K}$. Tìm giá trị nhỏ nhất $P_{{\\min}}$ của $P=x+y$.\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="P_{\\min}=")
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Xét $f(t)=\\log_{{{b}}}t+t$ đồng biến trên $(0;+\\infty)$. Biến đổi giả thiết về dạng "
        f"$f\\left({b}({C}-xy)\\right)=f({my_str}+{ny_str})$, suy ra ${b}({C}-xy)={my_str}+{ny_str}"
        f"\\Rightarrow y=\\dfrac{{{b*C}-{my_str}}}{{{b}x+{n}}}$ (với $0<x<{latex(sp.Rational(b*C,m)) if m!=0 else C}$ để $y>0$). "
        f"Khảo sát $P=x+y$ theo $x$ trên miền này, đạt giá trị nhỏ nhất tại $x={latex(x0)}$, "
        f"$P_{{\\min}}={correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(b=str(b), C=str(C), m=str(m), n=str(n))


def verify_D65(params):
    b, C, m, n = (float(sp.sympify(params[k])) for k in ("b", "C", "m", "n"))
    x_hi = b * C / m if m > 0 else 100.0
    samples = []
    for i in range(1, 2000):
        xv = (i / 2000.0) * x_hi
        yv = (b * C - m * xv) / (b * xv + n)
        if xv > 0 and yv > 0:
            samples.append(xv + yv)
    if not samples:
        return False
    # Independent dense numeric search over the positive feasible interval.
    x0 = (math.sqrt(m*n + b*b*C) - n) / b
    y0 = (b*C - m*x0) / (b*x0 + n)
    claimed_numeric_min = x0 + y0
    return y0 > 0 and abs(min(samples) - claimed_numeric_min) < 0.02


def expand_type(code, name, source_id, gen, verify, sampler, seed=0, target=90, max_tries=5000):
    rng = random.Random(seed)
    current = [r for r in ROWS if r["ma_dang"] == code]
    seen = {tuple(sorted(r["params"].items())) for r in current}
    questions = {r["de_bai"] for r in current}
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
            if not verify(params):
                continue
        except Exception:
            continue
        add_row(code, name, source_id, q, ans, sol, params)
        seen.add(key); questions.add(q); made += 1
    print(f"{code}: {made}/{target}")
    return made


def main():
    fails = []
    candidates = [(1, 1, 1), (2, 1, 1), (3, 1, 1), (4, 1, 2), (5, 1, 1), (6, 1, 1), (7, 1, 1),
                  (1, 2, 1), (2, 2, 1), (3, 2, 1)]
    for k1, t_num, t_den in candidates:
        try:
            de_bai, dap_an, loi_giai, params = gen_D17(k1, t_num, t_den)
        except AssertionError:
            continue
        if verify_D17(params):
            add_row("D17", "Tìm giá trị nhỏ nhất của biểu thức lôgarit bằng đặt ẩn phụ và khảo sát hàm",
                     "p021_q21", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D17", params))

    for b, C, m, n in [(3, 1, 1, 2), (2, 1, 1, 1), (3, 2, 1, 3), (2, 2, 1, 2), (3, 1, 2, 1)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D65(b, C, m, n)
        except AssertionError:
            continue
        if verify_D65(params):
            add_row("D65", "Tìm giá trị nhỏ nhất của biểu thức hai biến từ phương trình lôgarit bằng hàm "
                            "đặc trưng", "p148_q47", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D65", params))

    expand_type("D17", "Minimize a logarithmic expression by substitution", "p021_q21",
                gen_D17, verify_D17, lambda r: (r.randint(1, 50), r.randint(1, 30), 1), seed=1701)
    expand_type("D65", "Minimize a two-variable expression under a logarithmic constraint", "p148_q47",
                gen_D65, verify_D65,
                lambda r: (r.randint(2, 12), r.randint(1, 40), r.randint(1, 40), r.randint(1, 40)), seed=6501)

    with open("data/questions/mu_logarit_extraction/bien_the/batch_round7.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)

    with open("scripts/generate_questions/.tmp_round7_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Tong so hang sinh: {len(ROWS)}\n")
        f.write(f"That bai verify: {len(fails)}\n")
        for ma_dang, params in fails:
            f.write(f"  {ma_dang}: {params}\n")


if __name__ == "__main__":
    main()
