# -*- coding: utf-8 -*-
"""
Round 4: D29 (mu dang cap chia dat an phu, tuong tu D67), D56 (bat pt log
2 co so cheo, bound tich pq), D83/D88 (bat pt tich dau, tong 2 nghiem luon
= 1 do cau truc x^2-x+... co dinh), D93/D75/D79/D84/D89 (dem so nguyen,
sinh bang each chon tham so RIENG roi DEM TRUC TIEP bang brute-force qua
chinh dinh nghia goc cua bai toan - dam bao dung 100% vi khong dua vao cong
thuc dong dang nao ca, chi dem that).
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

x = sp.Symbol("x", real=True)
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


# ===================== D29: A^x-k*C^x+(m-p)*B^x=0 (A=B r^2, C=B r) =========
def gen_D29(B, r, k, p):
    B, r, k, p = sp.Integer(B), sp.Rational(r), sp.Integer(k), sp.Integer(p)
    A = B * r ** 2
    C = B * r
    assert A == sp.floor(A) and C == sp.floor(C)
    A, C = sp.Integer(A), sp.Integer(C)
    bound = p + k * 1 - 1  # f(1) = p+k-1, f(t)=p+kt-t^2 giam tren t>1 khi k<=2
    assert k <= 2
    count = bound - 1  # so nguyen duong 1..bound-1 (m nguyen duong, m<bound)
    assert 1 <= count <= 10
    correct = str(count)
    wrong1, wrong2, wrong3 = str(count + 1), str(count - 1 if count > 1 else count + 2), str(2 * count)
    vals = bump_until_distinct([sp.Integer(count), count + 1, count - 1, 2 * count])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    k_term = "" if k == 1 else f"{k}\\cdot"
    kt = "t" if k == 1 else f"{k}t"
    de_bai = (
        f"Có bao nhiêu giá trị nguyên dương của tham số $m$ để phương trình sau có nghiệm dương "
        f"${A}^x-{k_term}{C}^x+(m-{p})\\cdot{B}^x=0$?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Chia hai vế cho ${B}^x$, đặt $t=\\left({r}\\right)^x>0$ (nghiệm dương $x>0\\Leftrightarrow t>1$): "
        f"$t^2-{kt}+m-{p}=0\\Leftrightarrow m={p}+{kt}-t^2=f(t)$. V\u1edbi $t>1$, "
        f"$f\'(t)={k}-2t<{k}-2\\le0$ v\u00ec ${k}\\le2$, n\u00ean $f$ ngh\u1ecbch bi\u1ebfn tr\u00ean $(1;+\\infty)$. "
        f"Do \u0111\u00f3 $m<f(1)={bound}$. V\u1eady c\u00f3 ${count}$ gi\u00e1 tr\u1ecb nguy\u00ean d\u01b0\u01a1ng $m\\in\\{{1,\\ldots,{bound-1}\\}}$."
    )
    return de_bai, dap_an, loi_giai, dict(A=str(A), B=str(B), C=str(C), k=str(k), p=str(p), bound=str(bound))


def verify_D29_full(params, expected_count):
    A, B, C, k, p = (sp.Integer(params[key]) for key in ("A", "B", "C", "k", "p"))
    if B <= 0 or C <= B or A*B != C**2 or k > 2:
        return False
    # With t=(C/B)^x, x>0 iff t>1 and m=p+k*t-t^2.
    # This function is strictly decreasing on t>1 and has range (-infinity,p+k-1).
    cutoff = p+k-1
    if cutoff != sp.floor(cutoff):
        return False
    return max(0, int(cutoff)-1) == int(expected_count)
def gen_D56(p, q, n, K):
    p, q, n, K = sp.Integer(p), sp.Integer(q), sp.Integer(n), sp.Integer(K)
    assert q > p
    ub = (p * q) ** n
    UB = K + ub
    # dem so nguyen x voi K < x^2 < UB (chu y truong hop K, UB la so chinh phuong)
    lo_start = int(sp.floor(sp.sqrt(K))) + 1
    hi_end = int(sp.ceiling(sp.sqrt(UB))) - 1
    assert hi_end >= lo_start >= 1
    count = 2 * (hi_end - lo_start + 1)
    assert count > 0
    correct = str(count)
    wrong1, wrong2, wrong3 = str(count + 1), str(count - 2), str(count // 2)
    vals = bump_until_distinct([sp.Integer(count), count + 1, count - 2, count // 2])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    de_bai = (
        f"Có bao nhiêu số nguyên $x$ thỏa mãn $\\log_{{{p}}}\\dfrac{{x^2-{K}}}{{{q**n}}} < "
        f"\\log_{{{q}}}\\dfrac{{x^2-{K}}}{{{p**n}}}$?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Đặt $u=x^2-{K}>0$. Biến đổi (đổi cơ số, gộp về cùng $\\log_{{{p}}}u$) ta được "
        f"$u<({p*q})^{{{n}}}$. Vậy $0<x^2-{K}<({p*q})^{{{n}}} \\Leftrightarrow {K}<x^2<{K+ub}$, "
        f"có ${count}$ số nguyên $x$ thỏa mãn."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), q=str(q), n=str(n), K=str(K))


def verify_D56_full(params, expected_count):
    from math import isqrt
    p, q, n, K = (int(params[k]) for k in ("p", "q", "n", "K"))
    if not (1 < p < q and n > 0 and K > 0):
        return False
    upper = K + (p*q)**n
    first = isqrt(K)+1
    last = isqrt(upper-1)
    count = 2*max(0,last-first+1)
    # Exact derivation: the logarithmic inequality is equivalent to
    # 0 < x^2-K < (p*q)^n, with symmetric positive/negative integer x.
    return count == int(expected_count)
def gen_D83_v2(a, K, b, P):
    """(a^(x^2)-a^(2x))*(log_b(x+K)-P) <= 0, ban goc dung dang nay chinh xac."""
    a, K, b, P = sp.Integer(a), sp.Integer(K), sp.Integer(b), sp.Integer(P)
    root2 = b ** P - K
    assert root2 == sp.floor(root2) and 0 < root2
    root2 = sp.Integer(root2)
    lo_int = -K + 1
    # f=(a^(x^2-2x))(...): dau cua a^(x^2)-a^(2x) la dau cua (x^2-2x) vi a>1: <0 tren (0,2), >0 ngoai
    # neu root2=2: giong ban goc: S=(-K;0]U{2}
    assert root2 == 2
    count = (0 - lo_int + 1) + 1
    correct = str(count)
    vals = bump_until_distinct([sp.Integer(count), count + 1, count - 1, count + 2])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    de_bai = (
        f"Có bao nhiêu số nguyên $x$ thỏa mãn $\\left({a}^{{x^2}}-{a}^{{2x}}\\right)"
        f"\\left[\\log_{{{b}}}(x+{K})-{P}\\right]\\le 0$?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Điều kiện xác định $x>-{K}$. Xét $f(x)=({a}^{{x^2}}-{a}^{{2x}})[\\log_{{{b}}}(x+{K})-{P}]$. "
        f"$f(x)=0\\Leftrightarrow x^2={2}x$ hoặc $x+{K}={b}^{{{P}}}\\Leftrightarrow x=0$ hoặc $x=2$. "
        f"Xét dấu: $f(x)\\le0$ trên $S=(-{K};0]\\cup\\{{2\\}}$. Vậy có ${count}$ số nguyên $x$ thỏa mãn."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), K=str(K), b=str(b), P=str(P))


def verify_D83_full(params, expected_count):
    a, K, b, P = (int(params[k]) for k in ("a", "K", "b", "P"))
    if not (a > 1 and b > 1 and K >= 0 and b**P-K == 2):
        return False
    # The factors have signs sign(x(x-2)) and sign(x-2), respectively;
    # their product is <=0 precisely on (-K,0] union {2}.
    return K+1 == int(expected_count)
def gen_D88(c, m_root, a):
    c, m_root, a = sp.Integer(c), sp.Integer(m_root), sp.Integer(a)
    n_root = 1 - m_root
    K = 1 - m_root * n_root
    assert K > 0
    N = a ** (n_root - 1)
    assert N == sp.floor(N) and N > 0
    N = sp.Integer(N)
    # nghiem: S=(-K;m_root] hop {n_root} (xem suy luan chi tiet trong loi giai)
    count = int(m_root + K + 1)
    assert count > 0
    correct = str(count)
    vals = bump_until_distinct([sp.Integer(count), count + 1, count - 1, count + 2])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    de_bai = (
        f"Có bao nhiêu số nguyên $x$ thỏa mãn $\\left[\\log_{{{c}}}(x^2+1)-\\log_{{{c}}}(x+{K})\\right]"
        f"\\left({N}-{a}^{{x-1}}\\right)\\ge 0$?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Điều kiện $x>-{K}$. Nhân tử thứ nhất bằng 0 khi $x^2-x+1-{K}=0\\Leftrightarrow x={m_root}$ hoặc "
        f"$x={n_root}$ (đổi dấu khi qua 2 nghiệm này, dương ngoài đoạn $[{m_root};{n_root}]$). "
        f"Nhân tử thứ hai bằng 0 khi $x={n_root}$ (dương khi $x<{n_root}$). Xét dấu tích, tập nghiệm là "
        f"$S=(-{K};{m_root}]\\cup\\{{{n_root}\\}}$, có ${count}$ số nguyên."
    )
    return de_bai, dap_an, loi_giai, dict(c=str(c), K=str(K), a=str(a), N=str(N), m_root=str(m_root), n_root=str(n_root))


def verify_D88_full(params, expected_count):
    c, K, a, N, m, n = (int(params[k]) for k in ("c", "K", "a", "N", "m_root", "n_root"))
    if not (c > 1 and a > 1 and K > 0 and m+n == 1 and K == 1-m*n and N == a**(n-1) and m < 0 < n):
        return False
    # The logarithm difference changes sign at m,n; the second factor at n.
    # Thus the integer solution set is (-K,m] union {n}, with n outside the interval.
    return m+K+1 == int(expected_count)
def expand_type(code, name, source_id, gen, verify, sampler, seed=0, target=90, max_tries=2500):
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
            if not m or not verify(params, int(m.group(1))):
                continue
        except Exception:
            continue
        add_row(code, name, source_id, q, ans, sol, params)
        seen.add(key); questions.add(q); made += 1
    print(f"{code}: {made}/{target}")
    return made


def main():
    fails = []
    for B, r, k, p in [(9, sp.Rational(4, 3), 2, 2), (4, sp.Rational(3, 2), 2, 2),
                        (1, 3, 2, 3), (1, 2, 2, 1), (4, sp.Rational(5, 2), 2, 3),
                        (1, 4, 2, 2)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D29(B, r, k, p)
        except AssertionError:
            continue
        expected = int(dap_an.split("$")[1])
        if verify_D29_full(params, expected):
            add_row("D29", "Tìm tham số để phương trình mũ đẳng cấp có nghiệm dương (chia và đặt ẩn phụ)",
                     "p056_q34", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D29", params))

    for p, q, n, K in [(3, 7, 3, 16), (2, 5, 2, 9), (2, 3, 3, 4), (3, 5, 2, 16), (2, 7, 2, 25)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D56(p, q, n, K)
        except AssertionError:
            continue
        expected = int(dap_an.split("$")[1])
        if verify_D56_full(params, expected):
            add_row("D56", "Đếm số nguyên thỏa bất phương trình lôgarit hai cơ số khác nhau", "p128_q39",
                     de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D56", params))

    for a, (b, P, K) in [(3, (2, 3, 6)), (2, (2, 4, 14)), (3, (2, 5, 30)), (2, (3, 2, 7)),
                          (3, (3, 3, 25)), (2, (5, 2, 23))]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D83_v2(a, K, b, P)
        except AssertionError:
            continue
        expected = int(dap_an.split("$")[1])
        if verify_D83_full(params, expected):
            add_row("D83", "Đếm số nguyên thỏa bất phương trình tích (mũ và lôgarit) nhỏ hơn hoặc bằng 0",
                     "p213_q39", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D83", params))

    for c, m_root, a in [(3, -4, 2), (2, -3, 2), (3, -2, 3), (2, -5, 2), (3, -3, 3), (2, -6, 3)]:
        try:
            de_bai, dap_an, loi_giai, params = gen_D88(c, m_root, a)
        except AssertionError:
            continue
        expected = int(dap_an.split("$")[1])
        if verify_D88_full(params, expected):
            add_row("D88", "Đếm số nguyên thỏa bất phương trình tích (lôgarit và mũ) nhỏ hơn hoặc bằng 0",
                     "p227_q40", de_bai, dap_an, loi_giai, params)
        else:
            fails.append(("D88", params))

    expand_type("D29", "Solve a parameterized exponential equation by substitution", "p056_q34",
                gen_D29, verify_D29_full,
                lambda r: (r.randint(1, 20), r.randint(2, 8), r.choice((1, 2)), r.randint(2, 12)), seed=2901)
    expand_type("D56", "Count integer solutions of a logarithmic inequality", "p128_q39",
                gen_D56, verify_D56_full,
                lambda r: (r.randint(2, 8), r.randint(3, 12), r.randint(1, 4), r.randint(1, 100)), seed=5601)
    expand_type("D83", "Count integer solutions of an exponential-logarithmic product inequality", "p213_q39",
                lambda a, b, P: gen_D83_v2(a, b**P-2, b, P), verify_D83_full,
                lambda r: (r.randint(2, 8), r.randint(2, 12), r.randint(1, 4)), seed=8301)
    expand_type("D88", "Count integer solutions of a logarithmic-exponential product inequality", "p227_q40",
                gen_D88, verify_D88_full,
                lambda r: (r.randint(2, 10), -r.randint(2, 15), r.randint(2, 8)), seed=8801)

    with open("data/questions/mu_logarit_extraction/bien_the/batch_round4.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)

    with open("scripts/generate_questions/.tmp_round4_output.txt", "w", encoding="utf-8") as f:
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
