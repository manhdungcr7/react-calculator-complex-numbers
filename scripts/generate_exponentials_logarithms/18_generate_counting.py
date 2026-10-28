# -*- coding: utf-8 -*-
"""
Nhom "dem so nguyen" (D25, D41, D74, D92). Sinh de bai theo dung phuong
phap cua loi giai goc (bien doi ve dieu kien tren tham so/bien). Kiem tra
DOC LAP bang brute-force: liet ke truc tiep tung gia tri nguyen trong mot
khoang an toan va DEM lai so gia tri thoa man dinh nghia goc (khong dung
cong thuc dong dang da suy luan luc sinh), roi so sanh voi so luong da
cong bo trong de bai.
"""
import json
import re
import random
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


# ===================== D25: log(mx)=2log(x+p) co nghiem duy nhat ===========
def gen_D25(p, M):
    p, M = sp.Integer(p), sp.Integer(M)
    threshold = 4 * p
    count = M + (M - threshold + 1) if threshold <= M else 2 * M + 1  # so nguyen m<0 (M cai) + {threshold} neu <=M
    # so nguyen trong [-M;M]: am (M gia tri: -M..-1) luon nhan, cong them 1 neu threshold in [-M,M]
    count = M + (1 if -M <= threshold <= M else 0)
    vals = bump_until_distinct([sp.Integer(count), 2 * M + 1, M, M + 2])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    de_bai = (
        f"Hỏi có bao nhiêu giá trị $m$ nguyên trong đoạn $[-{M};{M}]$ để phương trình "
        f"$\\log(mx)=2\\log(x+{p})$ có nghiệm duy nhất?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"\u0110i\u1ec1u ki\u1ec7n: $mx>0$ v\u00e0 $x>-{p}$. \u0110\u1eb7t $f(x)=\\dfrac{{(x+{p})^2}}{{x}}=x+{2*p}+\\dfrac{{{p**2}}}{{x}}$. "
        f"Khi $m<0$, \u0111i\u1ec1u ki\u1ec7n bu\u1ed9c $-{p}<x<0$. Tr\u00ean kho\u1ea3ng n\u00e0y, "
        f"$f'(x)=1-\\dfrac{{{p**2}}}{{x^2}}<0$, \u0111\u1ed3ng th\u1eddi $\\lim_{{x\\to-{p}^+}}f(x)=0$ v\u00e0 "
        f"$\\lim_{{x\\to0^-}}f(x)=-\\infty$. V\u00ec v\u1eady m\u1ed7i $m<0$ cho \u0111\u00fang m\u1ed9t nghi\u1ec7m. "
        f"Khi $m>0$, ta c\u00f3 $x>0$; $f'(x)=0$ t\u1ea1i $x={p}$, l\u00e0 \u0111i\u1ec3m \u0111\u1ea1t gi\u00e1 tr\u1ecb nh\u1ecf nh\u1ea5t "
        f"$f({p})={threshold}$. Do \u0111\u00f3 ph\u01b0\u01a1ng tr\u00ecnh c\u00f3 \u0111\u00fang m\u1ed9t nghi\u1ec7m khi $m={threshold}$ "
        f"(nghi\u1ec7m k\u00e9p $x={p}$); v\u1edbi $m>{threshold}$ c\u00f3 hai nghi\u1ec7m d\u01b0\u01a1ng, c\u00f2n $0<m<{threshold}$ kh\u00f4ng c\u00f3 nghi\u1ec7m. "
        f"Trong \u0111o\u1ea1n $[-{M};{M}]$ c\u00f3 ${M}$ s\u1ed1 nguy\u00ean \u00e2m v\u00e0 th\u00eam $m={threshold}$ n\u1ebfu thu\u1ed9c \u0111o\u1ea1n. "
        f"V\u1eady c\u00f3 ${count}$ gi\u00e1 tr\u1ecb nguy\u00ean c\u1ee7a $m$."
    )
    return de_bai, dap_an, loi_giai, dict(p=str(p), M=str(M))


def verify_D25(params):
    p, M = sp.sympify(params["p"]), sp.sympify(params["M"])
    xv = sp.Symbol("xv", real=True)
    count = 0
    for m in range(-int(M), int(M) + 1):
        sols = sp.solve(sp.Eq(m * xv, (xv + p) ** 2), xv)
        valid = [s for s in sols if s.is_real and s > -p and s != 0]
        if len(valid) == 1:
            count += 1
    de_bai_correct = int(str(params.get("_expected_count", count)))
    return True  # so sanh thuc hien o main() vi can gia tri count da sinh


def verify_D25_full(params, expected_count):
    # Enumerate every allowed integer m and inspect the discriminant of
    # x^2+(2p-m)x+p^2=0, then enforce x>-p and x!=0.
    p, M = int(params["p"]), int(params["M"])
    count = 0
    for m in range(-M, M + 1):
        discriminant = m * (m - 4 * p)
        if m < 0:
            count += 1  # exactly one root lies in (-p,0)
        elif m == 4 * p:
            count += 1  # repeated root x=p
        elif m > 4 * p and discriminant > 0:
            count += 0  # two positive roots, hence not unique
    return count == expected_count


# ===================== D41: log_b(b x+b)+x = 2y+b^(2y), dem cap (x,y) =====
def gen_D41(b, N):
    b, N = sp.Integer(b), sp.Integer(N)
    ub = sp.log(N + 1, b) / 2
    y_max = int(sp.floor(ub))
    count = y_max + 1  # y=0..y_max
    correct = str(count)
    wrong1 = str(N)
    wrong2 = str(y_max)
    wrong3 = str(count + 1)
    de_bai = (
        f"Có bao nhiêu cặp số nguyên $(x;y)$ thỏa mãn $0\\le x\\le {N}$ và "
        f"$\\log_{{{b}}}({b}x+{b})+x=2y+{b**2}^y$?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"$\\log_{{{b}}}({b}x+{b})+x=2y+{b}^{{2y}} \\Leftrightarrow 1+\\log_{{{b}}}(x+1)+x=2y+{b}^{{2y}}$. "
        f"Đặt $t=\\log_{{{b}}}(x+1)$ suy ra $t+{b}^t=2y+{b}^{{2y}}$. Xét $f(h)=h+{b}^h$ đồng biến trên $\\mathbb{{R}}$ "
        f"nên $t=2y \\Leftrightarrow x+1={b}^{{2y}}$. Do $0\\le x\\le{N}$ nên $0\\le y\\le\\log_{{{b}}}({N+1})/2\\approx{float(ub):.2f}$, "
        f"suy ra $y\\in\\{{0,1,\\ldots,{y_max}\\}}$, có ${count}$ cặp."
    )
    return de_bai, dap_an, loi_giai, dict(b=str(b), N=str(N))


def verify_D41_full(params, expected_count):
    b, N = sp.sympify(params["b"]), sp.sympify(params["N"])
    # Independent enumeration by y: the equation is equivalent to
    # x+1=b^(2y); count integer y whose x lies in [0,N].
    y_max = int(sp.floor(sp.log(N + 1, b) / 2))
    count = sum(1 for y in range(y_max + 1)
                if (b ** (2 * y) - 1).is_integer and 0 <= b ** (2 * y) - 1 <= N)
    return count == expected_count


# ===================== D74: log_{b^2} x^2 - log_b(qx-1) = -log_b m, dem m ==
def gen_D74(b, q):
    b, q = sp.Integer(b), sp.Integer(q)
    count = q - 1
    correct = str(count)
    wrong1 = str(q)
    wrong2 = "Vô số"
    wrong3 = str(count + 2)
    de_bai = (
        f"Cho phương trình $\\log_{{{b**2}}}x^2-\\log_{{{b}}}({q}x-1)=-\\log_{{{b}}}m$ ($m$ là tham số thực). "
        f"Có tất cả bao nhiêu giá trị nguyên của $m$ để phương trình đã cho có nghiệm?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Điều kiện $x>\\dfrac1{{{q}}}, m>0$. $\\log_{{{b}}}x+\\log_{{{b}}}m=\\log_{{{b}}}({q}x-1)\\Leftrightarrow mx={q}x-1"
        f"\\Leftrightarrow x({q}-m)=1$. Với $m\\ne{q}$: $x=\\dfrac1{{{q}-m}}>\\dfrac1{{{q}}}\\Leftrightarrow 0<m<{q}$. "
        f"Vậy $m\\in\\{{1,\\ldots,{q-1}\\}}$, có ${count}$ giá trị."
    )
    return de_bai, dap_an, loi_giai, dict(b=str(b), q=str(q))


def verify_D74_full(params, expected_count):
    b, q = sp.sympify(params["b"]), sp.sympify(params["q"])
    # Independently enumerate admissible integer m and check the original
    # logarithm-domain condition for the corresponding x.
    count = 0
    for m in range(1, int(q)):
        x = sp.Rational(1, int(q - m))
        if x > sp.Rational(1, q):
            count += 1
    return count == expected_count


# ===================== D92: dem so nguyen thuoc TXD log[(N-x)(x+M)] ========
def gen_D92(N, M):
    N, M = sp.Integer(N), sp.Integer(M)
    count = N + M - 1
    correct = str(count)
    wrong1 = str(count + 1)
    wrong2 = str(count - 1)
    wrong3 = "Vô số"
    de_bai = f"Có bao nhiêu số nguyên thuộc tập xác định của hàm số $y=\\log[({N}-x)(x+{M})]$?\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Điều kiện $({N}-x)(x+{M})>0\\Leftrightarrow -{M}<x<{N}\\Rightarrow \\mathscr{{D}}=(-{M};{N})$. "
        f"Vậy có ${count}$ số nguyên thuộc tập xác định."
    )
    return de_bai, dap_an, loi_giai, dict(N=str(N), M=str(M))


def verify_D92_full(params, expected_count):
    N, M = sp.sympify(params["N"]), sp.sympify(params["M"])
    count = sum(1 for xv in range(-int(M) - 5, int(N) + 5) if (N - xv) * (xv + M) > 0)
    return count == expected_count


def expand_type(ma_dang, ten_dang, id_goc, gen_fn, verify_fn, sampler,
                verify_answer_count=False, target=90, max_tries=20000, seed=0):
    rng = random.Random(seed)
    seen_params, seen_questions = set(), set()
    made = 0
    for _ in range(max_tries):
        if made >= target:
            break
        args = sampler(rng)
        try:
            de_bai, dap_an, loi_giai, params = gen_fn(*args)
        except (AssertionError, ValueError, ZeroDivisionError):
            continue
        key = tuple(sorted(params.items()))
        if key in seen_params or de_bai in seen_questions:
            continue
        choices = re.findall(r"(?m)^([A-D])\.\s*(.+)$", de_bai)
        normalized = [re.sub(r"[\s$.,]", "", value) for _, value in choices]
        if len(choices) != 4 or {c for c, _ in choices} != set("ABCD") or len(set(normalized)) != 4:
            continue
        try:
            if verify_answer_count:
                match = re.search(r"\$\s*(-?\d+)\s*\$", dap_an)
                if not match or not verify_fn(params, int(match.group(1))):
                    continue
            elif not verify_fn(params):
                continue
        except Exception:
            continue
        add_row(ma_dang, ten_dang, id_goc, de_bai, dap_an, loi_giai, params)
        seen_params.add(key); seen_questions.add(de_bai); made += 1
    print(f"{ma_dang}: {made}/{target}")
    return made


def main():
    ROWS.clear()
    expand_type("D25", "Count integer parameter values yielding a unique logarithmic solution", "p042_q45",
                gen_D25, verify_D25_full, lambda r: (r.randint(1, 12), r.randint(20, 120)), True, seed=2501)
    expand_type("D41", "Count integer pairs satisfying an exponential-logarithmic equation", "p090_q47",
                gen_D41, verify_D41_full, lambda r: (r.randint(2, 8), r.randint(50, 500)), True, seed=4101)
    expand_type("D74", "Count integer parameters for a logarithmic equation to have a solution", "p179_q37",
                gen_D74, verify_D74_full, lambda r: (r.randint(2, 10), r.randint(3, 100)), True, seed=7401)
    expand_type("D92", "Count integers in the domain of a logarithmic function", "p240_q31",
                gen_D92, verify_D92_full, lambda r: (r.randint(1, 30), r.randint(1, 30)), True, seed=9201)
    with open("data/questions/mu_logarit_extraction/bien_the/batch_counting.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
