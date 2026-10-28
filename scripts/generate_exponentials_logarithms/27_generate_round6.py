# -*- coding: utf-8 -*-
"""Round 6: D79 (cong thuc dong dua tren nguong x^2-x<threshold, thay vi do
luoi tren y khong bi chan - chinh xac va nhanh hon nhieu)."""
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

ROWS = []


def add_row(ma_dang, ten_dang, id_goc, de_bai, dap_an, loi_giai, params):
    def repair(text):
        if isinstance(text, str):
            try:
                return text.encode("cp1252").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                return text
        return text
    de_bai, dap_an, loi_giai = map(repair, (de_bai, dap_an, loi_giai))
    ROWS.append({
        "id_goc": id_goc, "ma_dang": ma_dang, "ten_dang": ten_dang,
        "nguon": "Nhân bản", "loai_bien_the": "chuan",
        "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai, "params": params,
    })


# ===================== D79: dem x sao cho <=N0 gia tri y thoa log_p(x^2+y)>=log_q(x+y)
def gen_D79(p, q, N0):
    p, q, N0 = sp.Integer(p), sp.Integer(q), sp.Integer(N0)
    assert p > q
    r = sp.log(p, q)
    threshold = (N0 + 1) ** r - (N0 + 1)
    xv = sp.Symbol("xv", real=True)
    sol = sp.solve_univariate_inequality(xv ** 2 - xv < threshold, xv, relational=False)
    assert isinstance(sol, sp.Interval)
    lo_i, hi_i = int(sp.ceiling(sol.start)), int(sp.floor(sol.end))
    assert lo_i <= hi_i
    count = hi_i - lo_i + 1
    assert 5 < count < 300
    correct = str(count)
    vals = bump_until_distinct([sp.Integer(count), count + 1, count - 1, count + 2])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    de_bai = (
        f"Có bao nhiêu số nguyên $x$ sao cho ứng với mỗi $x$ có không quá {N0} số nguyên $y$ thỏa mãn "
        f"$\\log_{{{p}}}(x^2+y)\\ge \\log_{{{q}}}(x+y)$?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    threshold_str = latex(threshold) if threshold.is_rational else f"({N0+1})^{{\\log_{{{q}}}{p}}}-{N0+1}"
    threshold_eq = "="
    loi_giai = (
        f"Điều kiện $x+y>0, x^2+y>0$. Đặt $t=x+y$ ($t\\ge1$ do $x,y$ nguyên). Bất phương trình "
        f"$\\Leftrightarrow x^2-x\\ge t^{{\\log_{{{q}}}{p}}}-t=f(t)$, với $f$ đồng biến trên $[1;+\\infty)$. "
        f"Có không quá {N0} số nguyên $y$ (tức $t$) thỏa mãn khi $x^2-x<f({N0+1}){threshold_eq}{threshold_str}$. "
        f"Giải ra $x\\in\\{{{lo_i},\\ldots,{hi_i}\\}}$, có ${count}$ số nguyên $x$."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), q=str(q), N0=str(N0), lo_i=str(lo_i), hi_i=str(hi_i))


def verify_D79(params):
    p, q, N0, lo_i, hi_i = (sp.sympify(params[k]) for k in ("p", "q", "N0", "lo_i", "hi_i"))
    p, q, N0 = float(p), float(q), int(N0)
    # kiem tra doc lap: voi vai x quanh bien (trong va ngoai [lo_i,hi_i]), dem SO Y truc tiep
    # (bang dinh nghia goc, khong dung cong thuc nguong) va so sanh voi <=N0 hay khong.
    import math

    def count_y_for_x(xv, y_search=400):
        c = 0
        for yv in range(-y_search, y_search):
            s = xv + yv
            if s <= 0 or xv ** 2 + yv <= 0:
                continue
            lhs = math.log(xv ** 2 + yv, p)
            rhs = math.log(s, q)
            if lhs >= rhs:
                c += 1
                if c > N0 + 2:
                    break
        return c

    test_xs = [int(lo_i), int(hi_i), int(lo_i) - 1, int(hi_i) + 1, (int(lo_i) + int(hi_i)) // 2]
    for xv in test_xs:
        c = count_y_for_x(xv)
        should_be_le = lo_i <= xv <= hi_i
        is_le = c <= N0
        if should_be_le != is_le:
            return False
    return True


# ===================== D89: count positive integers y for which a real x in (lo,hi) exists.
# Solve the equation as a quadratic in y. For x>1 it has exactly one positive
# root psi(x). Keep only tuples for which interval arithmetic certifies psi'>0
# on every subinterval, so endpoint counting is mathematically justified.
def _d89_psi(x, A, B, C):
    import mpmath as mp
    d = mp.exp(x) - B*x*x - C
    disc = d*d + 4*x*A*(x-1)*mp.exp(x)
    return (-d + mp.sqrt(disc))/(2*x)


def _d89_certify_increasing(A, B, C, lo, hi, max_depth=9):
    import mpmath as mp
    mp.iv.dps = 50
    pending = [(float(lo), float(hi), 0)]
    lower_bounds = []
    while pending:
        left, right, depth = pending.pop()
        x = mp.iv.mpf([left, right])
        ex = mp.iv.exp(x)
        d = ex - B*x*x - C
        disc = d*d + 4*x*A*(x-1)*ex
        if disc.a > 0:
            y = (-d + mp.iv.sqrt(disc))/(2*x)
            fx = (A*x-y)*ex - y*y + 2*B*x*y
            if fx.a > 0:
                lower_bounds.append(fx.a/mp.iv.sqrt(disc).b)
                continue
        if depth >= max_depth:
            return None
        mid = (left + right)/2
        if mid == left or mid == right:
            return None
        pending.append((left, mid, depth+1))
        pending.append((mid, right, depth+1))
    if not lower_bounds:
        return None
    return min(lower_bounds)


def gen_D89(A, B, C, lo, hi):
    import mpmath as mp
    A, B, C, lo, hi = map(int, (A, B, C, lo, hi))
    assert A > 0 and B >= 0 and C >= 0 and lo >= 2 and hi > lo
    derivative_lower = _d89_certify_increasing(A, B, C, lo, hi)
    assert derivative_lower is not None and derivative_lower > 0
    mp.mp.dps = 60
    yl, yh = _d89_psi(mp.mpf(lo), A, B, C), _d89_psi(mp.mpf(hi), A, B, C)
    margin = min(abs(yl-mp.nint(yl)), abs(yh-mp.nint(yh)))
    assert yl > 0 and yh > yl and margin > mp.mpf('1e-8')
    first, last = int(mp.floor(yl))+1, int(mp.ceil(yh))-1
    count = last-first+1
    assert 5 < count < 40
    correct = str(count)
    vals = bump_until_distinct([sp.Integer(count), count+1, count-1, count+2])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    Bx2 = f"{B}x^2" if B != 1 else "x^2"
    Cterm = f"-{C}" if C else ""
    question = (f"C\u00f3 bao nhi\u00eau s\u1ed1 nguy\u00ean d\u01b0\u01a1ng $y$ \u0111\u1ec3 t\u1ed3n t\u1ea1i s\u1ed1 th\u1ef1c "
                f"$x\\in({lo};{hi})$ th\u1ecfa m\u00e3n "
                f"${A}(x-1)e^x=y(e^x+xy-{Bx2}{Cterm})$?\n\n")
    lines, answer = render_mc([correct, wrong1, wrong2, wrong3], 0)
    question += "\n".join(lines)
    d_expr = f"e^x-{Bx2}{Cterm}"
    solution = (
        f"Xem ph\u01b0\u01a1ng tr\u00ecnh nh\u01b0 ph\u01b0\u01a1ng tr\u00ecnh b\u1eadc hai theo $y$: "
        f"$xy^2+({d_expr})y-{A}(x-1)e^x=0$. V\u1edbi $x\\in({lo};{hi})$ v\u00e0 $x>1$, "
        f"t\u00edch hai nghi\u1ec7m \u00e2m n\u00ean ph\u01b0\u01a1ng tr\u00ecnh c\u00f3 \u0111\u00fang m\u1ed9t nghi\u1ec7m d\u01b0\u01a1ng "
        f"$y=\\psi(x)=\\dfrac{{-D(x)+\\sqrt{{D(x)^2+4\\cdot x\\cdot {A}(x-1)e^x}}}}{{2x}}$, "
        f"trong \u0111\u00f3 $D(x)={d_expr}$. D\u00f9ng \u0111\u1ea1o h\u00e0m \u1ea9n cho "
        f"$F(x,y)={A}(x-1)e^x-y(e^x+xy-{Bx2}{Cterm})=0$: "
        f"$F_y=-\\sqrt{{D(x)^2+4\\cdot x\\cdot {A}(x-1)e^x}}<0$ v\u00e0 "
        f"$F_x=({A}x-y)e^x-y^2+{2*B}xy$. Ki\u1ec3m tra b\u1eb1ng s\u1ed1 h\u1ecdc kho\u1ea3ng tr\u00ean to\u00e0n "
        f"$({lo};{hi})$ cho $\\psi'(x)=F_x/\\sqrt{{D(x)^2+4\\cdot x\\cdot {A}(x-1)e^x}}>0$ "
        f"(c\u1eadn d\u01b0\u1edbi \u0111\u01b0\u1ee3c ch\u1ee9ng nh\u1eadn l\u00e0 {float(derivative_lower.a):.6g}); do \u0111\u00f3 $\\psi$ t\u0103ng nghi\u00eam ng\u1eb7t. "
        f"T\u1ea1i hai \u0111\u1ea7u m\u00fat, $\\psi({lo})\\approx {mp.nstr(yl,12)}$ v\u00e0 "
        f"$\\psi({hi})\\approx {mp.nstr(yh,12)}$, \u0111\u1ec1u kh\u00f4ng nguy\u00ean. V\u00ec kho\u1ea3ng c\u1ee7a $x$ l\u00e0 kho\u1ea3ng m\u1edf, "
        f"c\u00e1c gi\u00e1 tr\u1ecb nguy\u00ean d\u01b0\u01a1ng c\u00f3 th\u1ec3 nh\u1eadn \u0111\u01b0\u1ee3c l\u00e0 ${first},\\ldots,{last}$. "
        f"V\u1eady c\u00f3 {count} gi\u00e1 tr\u1ecb."
    )
    params = dict(A=A, B=B, C=C, lo=lo, hi=hi, found_lo=first, found_hi=last,
                  psi_lo=str(yl), psi_hi=str(yh), derivative_lower=str(derivative_lower.a))
    return question, answer, solution, params


def verify_D89(params):
    import mpmath as mp
    A, B, C, lo, hi = [int(params[k]) for k in ("A", "B", "C", "lo", "hi")]
    lower = _d89_certify_increasing(A, B, C, lo, hi)
    if lower is None or lower <= 0:
        return False
    mp.mp.dps = 60
    yl, yh = _d89_psi(mp.mpf(lo), A, B, C), _d89_psi(mp.mpf(hi), A, B, C)
    if min(abs(yl-mp.nint(yl)), abs(yh-mp.nint(yh))) <= mp.mpf('1e-8'):
        return False
    first, last = int(mp.floor(yl))+1, int(mp.ceil(yh))-1
    return (first == int(params["found_lo"]) and last == int(params["found_hi"])
            and first <= last and int(params["found_hi"])-int(params["found_lo"])+1 > 5)

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
    for p, q, N0 in [(4, 3, 242), (9, 5, 300), (4, 3, 100), (3, 2, 150), (8, 5, 200)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D79(p, q, N0)
        except (AssertionError, TypeError):
            continue
        if verify_D79(params):
            add_row("D79", "Đếm số nguyên một biến sao cho số giá trị nguyên biến kia thỏa mãn bất phương "
                            "trình lôgarit không vượt một ngưỡng", "p204_q49", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D79", params))

    for A, B, C, lo, hi in []:
        try:
            de_bai, dap_an, loi_giai, params = gen_D89(A, B, C, lo, hi)
        except AssertionError:
            continue
        if verify_D89(params):
            add_row("D89", "Đếm số nguyên dương một biến sao cho tồn tại biến kia thỏa mãn phương trình "
                            "chứa hàm mũ e^x", "p230_q45", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D89", params))

    expand_type("D79", "Count integers satisfying a logarithmic inequality threshold", "p204_q49",
                gen_D79, verify_D79,
                lambda r: (lambda p, q: (p, q if q < p else p-1, r.randint(20, 500)))(r.randint(3, 30), r.randint(2, 29)), seed=7901)
    expand_type("D89", "Count positive integer parameters for an exponential equation", "p230_q45",
                gen_D89, verify_D89,
                lambda r: (r.randint(1, 15), r.randint(1, 12), r.randint(0, 30),
                           (lo := r.randint(2, 8)), lo + r.randint(2, 12)), seed=8901)

    with open("data/questions/mu_logarit_extraction/bien_the/batch_round6.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)

    with open("scripts/generate_questions/.tmp_round6_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Tong so hang sinh: {len(ROWS)}\n")
        f.write(f"That bai verify: {len(fails)}\n")
        for ma_dang, params in fails:
            f.write(f"  {ma_dang}: {params}\n")


if __name__ == "__main__":
    main()
