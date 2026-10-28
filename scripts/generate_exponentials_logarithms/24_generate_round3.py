# -*- coding: utf-8 -*-
"""
Round 3: sinh bien the bang cach "thiet ke NGUOC tu dieu kien dau bang/diem
toi han" thay vi tim cong thuc thuan chieu — ap dung cho cac dang GTNN/GTLN
truoc day bi xep vao nhom kho (D10, D68, D94, D46). Chon truoc he so lien
quan toi diem dat cuc tri/dau bang, sau do TINH RA diem do bang cong thuc
dai so (khong do/thu), roi kiem tra doc lap rang diem do thoa dung dinh
nghia goc cua bai toan.
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

x, y, m = sp.symbols("x y m", real=True)
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


# ===================== D10: y=ln(x^2+e^2)-mx+1 dong bien tren R ============
def gen_D10(e):
    e = sp.Integer(e)
    ans = sp.Rational(-1, e)
    correct = f"\\left(-\\infty;{latex(ans)}\\right]"
    wrong1 = f"\\left(-\\infty;{latex(-ans)}\\right)"
    wrong2 = f"\\left[{latex(ans)};{latex(-ans)}\\right]"
    wrong3 = f"\\left[{latex(-ans)};+\\infty\\right)"
    de_bai = (
        f"Tìm tập hợp tất cả các giá trị của tham số thực $m$ để hàm số "
        f"$y = \\ln(x^2+{e**2}) - mx + 1$ đồng biến trên khoảng $(-\\infty; +\\infty)$.\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    min_str = "1" if e == 1 else f"\\dfrac{{1}}{{{e}}}"
    loi_giai = (
        f"$y'=\\dfrac{{2x}}{{x^2+{e**2}}}-m\\ge0,\\forall x \\Leftrightarrow m\\le\\min g(x)$ với "
        f"$g(x)=\\dfrac{{2x}}{{x^2+{e**2}}}$. $g'(x)=0\\Leftrightarrow x=\\pm{e}$. "
        f"$\\min g(x)=g(-{e})=-{min_str}$. Vậy $m\\le-{min_str}$."
    )
    return de_bai, dap_an, loi_giai, dict(e=str(e))


def verify_D10(params):
    e = sp.sympify(params["e"])
    g = 2 * x / (x ** 2 + e ** 2)
    gp = sp.diff(g, x)
    crit = sp.solve(sp.Eq(gp, 0), x)
    min_val = min(g.subs(x, c) for c in crit)
    return sp.simplify(min_val - sp.Rational(-1, e)) == 0


# ===================== D68: thiet ke nguoc tu A,B,C,E ========================
def gen_D68(A, B, C, E):
    A, B, C, E = (sp.Integer(v) for v in (A, B, C, E))
    k = sp.Rational(A, B)
    a0 = sp.Rational(C + E * k, 2 * A * B * k)
    b0 = k * a0
    N1 = (A * a0) ** 2 + (B * b0) ** 2 + 1
    N3 = 2 * A * B * a0 * b0 + 1
    D1 = C * a0 + E * b0 + 1
    assert N1 == N3 == D1 and N1 > 1 and a0 > 0 and b0 > 0
    ans = a0 + 2 * b0
    Aa = "a" if A == 1 else f"{A}a"
    Bb = "b" if B == 1 else f"{B}b"
    Cc = "" if C == 0 else (f"{C}a+" if C != 1 else "a+")
    Ee = "b" if E == 1 else f"{E}b"
    de_bai = (
        f"Cho $a>0,b>0$ thỏa mãn\n"
        f"$$\\log_{{{Cc}{Ee}+1}}(({Aa})^2+({Bb})^2+1)+\\log_{{{2*A*B}ab+1}}({Cc}{Ee}+1)=2.$$\n"
        f"Giá trị của $a+2b$ bằng\n\n"
    )
    correct = latex(ans)
    wrong1 = latex(ans + 1)
    wrong2 = latex(2 * ans)
    wrong3 = latex(a0 + b0)
    vals = bump_until_distinct([ans, ans + 1, 2 * ans, a0 + b0])
    correct, wrong1, wrong2, wrong3 = (latex(v) for v in vals)
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Áp dụng Cô-si: $({Aa})^2+({Bb})^2+1\\ge {2*A*B}ab+1$. Dấu \"=\" khi ${Aa}={Bb}$. "
        f"Kết hợp với dấu \"=\" ở bước Cô-si thứ hai (hai lôgarit nghịch đảo bằng 1) ta được hệ "
        f"$\\begin{{cases}}{Aa}={Bb}\\\\{Cc}{Ee}+1={2*A*B}ab+1\\end{{cases}} "
        f"\\Rightarrow a={latex(a0)}, b={latex(b0)}$. Vậy $a+2b={correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(A=str(A), B=str(B), C=str(C), E=str(E))


def verify_D68(params):
    A, B, C, E = (sp.sympify(params[k]) for k in ("A", "B", "C", "E"))
    k_ratio = sp.Rational(A, B)
    a0 = sp.Rational(C + E * k_ratio, 2 * A * B * k_ratio)
    b0 = k_ratio * a0
    D1v = C * a0 + E * b0 + 1
    N1v = (A * a0) ** 2 + (B * b0) ** 2 + 1
    N3v = 2 * A * B * a0 * b0 + 1
    lhs = sp.log(N1v, D1v) + sp.log(D1v, N3v)
    return abs(float(lhs - 2)) < 1e-9


# ===================== D94: tim GTLN P=x^2+y^2+c1 x+c2 y voi x^2+y^2<=N ====
def gen_D94(N, c1, c2):
    N, c1, c2 = sp.Integer(N), sp.Integer(c1), sp.Integer(c2)
    bound = sp.sqrt((c1 ** 2 + c2 ** 2) * N)
    assert bound == sp.floor(bound) and bound > 0
    bound = sp.Integer(bound)
    Pmax = N + bound
    x_star = sp.simplify(c1 * sp.sqrt(N) / sp.sqrt(c1 ** 2 + c2 ** 2))
    y_star = sp.simplify(c2 * sp.sqrt(N) / sp.sqrt(c1 ** 2 + c2 ** 2))
    x_term = ("" if c1 == 1 else "-" if c1 == -1 else str(c1)) + "x"
    y_magnitude = "y" if abs(c2) == 1 else f"{abs(c2)}y"
    linear_expr = f"{x_term} {'+' if c2 > 0 else '-'} {y_magnitude}"
    correct = str(Pmax)
    wrong1, wrong2, wrong3 = str(N), str(2 * N), str(Pmax - 2 * bound)
    vals = bump_until_distinct([Pmax, N, 2 * N, Pmax - 2 * bound])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    c1_disp = "" if abs(c1) == 1 else str(abs(c1))
    c2_disp = "" if abs(c2) == 1 else str(abs(c2))
    c2_str = (f"+{c1_disp}x" if c1 > 0 else f"-{c1_disp}x")
    c2_str += f"+{c2_disp}y" if c2 > 0 else f"-{c2_disp}y"
    de_bai = (
        f"Xét tất cả các số thực $x, y$ sao cho $a^{{4x-\\log_5(a^2)}}\\le 25^{{{N}-y^2}}$ với mọi số thực "
        f"dương $a$. Giá trị lớn nhất của biểu thức $P=x^2+y^2{c2_str}$ bằng\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"\u0110\u1eb7t $t=\\log_5 a$. L\u1ea5y l\u00f4garit c\u01a1 s\u1ed1 5 hai v\u1ebf, ta \u0111\u01b0\u1ee3c "
        f"$4xt-2t^2\\le2({N}-y^2)$ v\u1edbi m\u1ecdi $t$. V\u1ebf tr\u00e1i \u0111\u1ea1t gi\u00e1 tr\u1ecb l\u1edbn nh\u1ea5t $2x^2$ t\u1ea1i $t=x$, "
        f"n\u00ean \u0111i\u1ec1u ki\u1ec7n t\u01b0\u01a1ng \u0111\u01b0\u01a1ng $x^2+y^2\\le{N}$. Theo Bunhiac\u00f4pxki, "
        f"$({linear_expr})^2\\le({c1**2+c2**2})(x^2+y^2)\\le({c1**2+c2**2})\\cdot{N}={bound**2}$, "
        f"suy ra $P\\le{N}+{bound}={Pmax}$. D\u1ea5u b\u1eb1ng x\u1ea3y ra khi "
        f"$(x,y)=({sp.latex(x_star)},{sp.latex(y_star)})$, khi \u0111\u00f3 "
        f"$x^2+y^2={N}$ v\u00e0 ${linear_expr}={bound}$. V\u1eady $P_{{\\max}}={Pmax}$."
    )
    return de_bai, dap_an, loi_giai, dict(N=str(N), c1=str(c1), c2=str(c2))


def verify_D94(params):
    N, c1, c2 = (sp.sympify(params[k]) for k in ("N", "c1", "c2"))
    # kiem tra doc lap bang toi uu so hoc truc tiep tren duong tron x^2+y^2=N
    theta = sp.Symbol("theta", real=True)
    xe = sp.sqrt(N) * sp.cos(theta)
    ye = sp.sqrt(N) * sp.sin(theta)
    expr = xe ** 2 + ye ** 2 + c1 * xe + c2 * ye
    expr = sp.simplify(expr)
    vals = [expr.subs(theta, sp.Rational(i, 100) * sp.pi) for i in range(0, 200)]
    numeric_max = max(float(v) for v in vals)
    bound = sp.sqrt((c1 ** 2 + c2 ** 2) * N)
    expected = float(N + bound)
    return abs(numeric_max - expected) < 0.05


def gen_D46(k_val, c):
    k_val, c = sp.Integer(k_val), sp.Integer(c)
    t = sp.Symbol("t", positive=True)
    x_expr = sp.Rational(1, k_val) * (1 + t)
    y_expr = sp.Rational(1, k_val) * (1 + 1 / t)
    P = x_expr + c * y_expr
    Pd = sp.diff(P, t)
    crit = [cr for cr in sp.solve(sp.Eq(Pd, 0), t) if cr.is_real and cr > 0]
    assert len(crit) == 1
    t0 = crit[0]
    Pmin = sp.simplify(P.subs(t, t0))
    Pmin_f = float(Pmin)
    lo = sp.floor(Pmin_f * 2) / 2
    if lo == Pmin_f:
        lo -= sp.Rational(1, 2)
    hi = lo + sp.Rational(1, 2)
    assert lo < Pmin_f < hi
    correct = f"\\left[{latex(lo)};{latex(hi)}\\right)"
    others = []
    step = sp.Rational(1, 2)
    cur = hi
    while len(others) < 3:
        others.append(f"\\left[{latex(cur)};{latex(cur+step)}\\right)")
        cur += step
    de_bai = (
        f"Xét các số thực dương $a,b,x,y$ thỏa mãn $a,b>1$ và $a^x=b^y=(ab)^{{1/{k_val}}}$. "
        f"Giá trị nhỏ nhất của biểu thức $P=x+{c}y$ thuộc tập nào dưới đây?\n\n"
    )
    lines, dap_an = render_mc([correct] + others, 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Đặt $t=\\log_a b>0$. $x=\\dfrac{{1}}{{{k_val}}}(1+t)$, $y=\\dfrac1{{{k_val}}}\\left(1+\\dfrac1t\\right)$. "
        f"$P=x+{c}y$ đạt cực tiểu tại $t={latex(t0)}$, $P_{{\\min}}={latex(Pmin)}\\approx{Pmin_f:.3f}$, "
        f"thuộc ${correct}$."
    )
    return de_bai, dap_an, loi_giai, dict(k_val=str(k_val), c=str(c))


def verify_D46(params):
    k_val, c = sp.sympify(params["k_val"]), sp.sympify(params["c"])
    t = sp.Symbol("t", positive=True)
    x_expr = sp.Rational(1, k_val) * (1 + t)
    y_expr = sp.Rational(1, k_val) * (1 + 1 / t)
    P = x_expr + c * y_expr
    vals = [P.subs(t, sp.Rational(i, 100)) for i in range(1, 2000)]
    numeric_min = min(float(v) for v in vals)
    Pd = sp.diff(P, t)
    crit = [cr for cr in sp.solve(sp.Eq(Pd, 0), t) if cr.is_real and cr > 0]
    Pmin_analytic = float(P.subs(t, crit[0]))
    return abs(numeric_min - Pmin_analytic) < 0.01


def expand_type(code, name, source_id, gen, verify, sampler, seed=0, target=90, max_tries=5000):
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
    fails += try_add("D10", "Tìm tham số để hàm số chứa lôgarit tự nhiên đơn điệu trên R", "p018_q09",
                      gen_D10, verify_D10, [(v,) for v in (1, 2, 3, 4, 5, 6)])

    for A, B, C, E in [(5, 1, 10, 3), (2, 1, 4, 3), (3, 2, 6, 2), (1, 1, 3, 1), (3, 1, 6, 2), (2, 1, 8, 1)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D68(A, B, C, E)
        except AssertionError:
            continue
        if verify_D68(params):
            add_row("D68", "Tìm giá trị biểu thức từ hệ hai đẳng thức lôgarit-mũ bằng bất đẳng thức Cô-si",
                     "p161_q37", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D68", params))

    d94_candidates = [(10, 1, -3), (13, 2, -3), (16, 3, -4), (17, 1, -4), (18, 3, -3), (20, 1, -2)]
    for N, c1, c2 in d94_candidates:
        try:
            de_bai, dap_an, loi_giai, params = gen_D94(N, c1, c2)
        except AssertionError:
            continue
        if verify_D94(params):
            add_row("D94", "Tìm giá trị lớn nhất của biểu thức hai biến từ điều kiện đúng với mọi tham số bằng bất đẳng thức Cauchy-Schwarz",
                     "p243_q44", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D94", params))

    for k_val, c in [(2, 2), (3, 2), (2, 3), (4, 2), (2, 4), (3, 3)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D46(k_val, c)
        except AssertionError:
            continue
        if verify_D46(params):
            add_row("D46", "Tìm giá trị nhỏ nhất của biểu thức mũ-lôgarit qua ẩn phụ t=log_a b", "p105_q47",
                     de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D46", params))

    expand_type("D10", "Monotonicity of a logarithmic function", "p018_q09", gen_D10, verify_D10,
                lambda r: (r.randint(1, 500),), seed=1001)
    expand_type("D68", "Evaluate an expression under logarithmic equalities", "p161_q37", gen_D68, verify_D68,
                lambda r: tuple(r.randint(1, 40) for _ in range(4)), seed=6801)
    expand_type("D94", "Maximize a quadratic expression under a disk constraint", "p243_q44", gen_D94,
                verify_D94, lambda r: (None, (c1 := r.randint(1, 40)), (c2 := r.randint(1, 40)))
                if False else (lambda c1, c2: (c1*c1+c2*c2, c1, c2))(r.randint(1,40),r.randint(1,40)), seed=9401)
    expand_type("D46", "Locate the minimum of an exponential-logarithmic expression", "p105_q47",
                gen_D46, verify_D46, lambda r: (r.randint(1, 100), r.randint(1, 100)), seed=4601)

    with open("data/questions/mu_logarit_extraction/bien_the/batch_round3.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)

    with open("scripts/generate_questions/.tmp_round3_output.txt", "w", encoding="utf-8") as f:
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
