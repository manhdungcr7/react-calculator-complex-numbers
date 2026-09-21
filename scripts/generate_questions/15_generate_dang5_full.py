"""Sinh đầy đủ Dạng 5 (Tập hợp điểm biểu diễn số phức - quỹ tích đường tròn)
— 5 câu gốc, mỗi câu 6 bản/loại số = 18 bản/câu, tổng 5*18 = 90 câu."""
import json
import sys

sys.path.insert(0, "Sinh_them_cau_hoi/scripts")
from importlib import import_module

utils = import_module("10_common_utils")
latex = utils.latex
z_string = utils.z_string
build_rows_for_question = utils.build_rows_for_question

import sympy as sp

SO_BAN_MOI_LOAI = 6
DANG = "Dạng 5 - Tập hợp điểm biểu diễn (quỹ tích)"

xr, yr = sp.symbols("xr yr", real=True)


def sub_term(k):
    return f"-{latex(k)}" if k >= 0 else f"+{latex(-k)}"


def add_term(k):
    return f"+{latex(k)}" if k >= 0 else f"-{latex(-k)}"


def add_term_i(k):
    """Như add_term nhưng bỏ hệ số 1 trước i (vd k=1 -> '+i', k=-1 -> '-i'),
    bỏ hẳn số hạng nếu k=0."""
    if k == 0:
        return ""
    if sp.Abs(k) == 1:
        return "+i" if k >= 0 else "-i"
    return f"+{latex(k)}i" if k >= 0 else f"-{latex(-k)}i"


def diem(px, py):
    return f"({latex(px)};{latex(py)})"


# --- STT4: |z|=R. w=(a+bi)z+(c+di). Bán kính đường tròn của w --------------
def mau_stt4(R, pair_ab):
    a, b = pair_ab
    radius = R * sp.sqrt(a ** 2 + b ** 2)
    vals = [radius, R * (a ** 2 + b ** 2), sp.sqrt(a ** 2 + b ** 2), radius ** 2]  # index0 giu co dinh
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    radius, d1, d2, d3 = vals
    de_bai = (
        f"Cho số phức $z$ thỏa mãn $|z| = {latex(R)}$. Biết rằng tập hợp các điểm biểu diễn các số phức "
        f"$w = ({z_string(a,b)})z+i$ là một đường tròn. Tính bán kính $r$ của đường tròn đó.\n\n"
        f"A. $r = {latex(d2)}$.\n"
        f"B. $r = {latex(radius)}$.\n"
        f"C. $r = {latex(d1)}$.\n"
        f"D. $r = {latex(d3)}$."
    )
    dap_an = f"B. $r = {latex(radius)}$."
    loi_giai = (
        f"Ta có $w=({z_string(a,b)})z+i \\Leftrightarrow z=\\dfrac{{w-i}}{{{z_string(a,b)}}}$. "
        f"Do $|z|={latex(R)}$ nên tập hợp điểm biểu diễn $w$ là đường tròn bán kính "
        f"$r = {latex(R)}\\cdot|{z_string(a,b)}| = {latex(radius)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT31: |z+pi|=r. Tâm đường tròn -----------------------------------------
def mau_stt31(p, r):
    r = sp.Abs(r)
    if r == 0:
        r = sp.Integer(1)
    center = (0, -p)
    opts = [diem(0, p), diem(p, 0), diem(0, -p), diem(-p, 0)]
    de_bai = (
        f"Trên mặt phẳng tọa độ, biết tập hợp điểm biểu diễn các số phức $z$ thỏa mãn $|z{add_term_i(p)}|={latex(r)}$ "
        f"là một đường tròn. Tâm của đường tròn đó có tọa độ là\n\n"
        f"A. ${opts[0]}$.\nB. ${opts[1]}$.\nC. ${opts[2]}$.\nD. ${opts[3]}$."
    )
    dap_an = f"C. ${opts[2]}$."
    loi_giai = (
        f"Gọi $z=x+yi$. Ta có $|z{add_term_i(p)}|={latex(r)} \\Leftrightarrow x^2+(y{add_term(p)})^2={latex(r)}^2$. "
        f"Vậy tập hợp điểm biểu diễn là đường tròn tâm $I{diem(0,-p)}$ bán kính $R={latex(r)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT13: (z+pi)(z-bar+q) thuần ảo. Tâm đường tròn -------------------------
def mau_stt13(p, q):
    # x^2+qx+y^2+py=0 -> tam (-q/2,-p/2)
    cx_, cy_ = -q / sp.Integer(2), -p / sp.Integer(2)
    if cx_ == cy_:
        q = q + 2
        cx_, cy_ = -q / sp.Integer(2), -p / sp.Integer(2)
    opts = [diem(cy_, cx_), diem(cx_, -cy_), diem(-cx_, cy_), diem(cx_, cy_)]
    de_bai = (
        f"Xét các số phức $z$ thỏa mãn $(z{add_term_i(p)})(\\overline{{z}}{add_term(q)})$ là số thuần ảo. "
        f"Biết rằng tập hợp tất cả các điểm biểu diễn của $z$ là một đường tròn, tâm của đường tròn đó có tọa độ là\n\n"
        f"A. ${opts[0]}$.\nB. ${opts[1]}$.\nC. ${opts[2]}$.\nD. ${opts[3]}$."
    )
    dap_an = f"D. ${diem(cx_, cy_)}$."
    loi_giai = (
        f"Giả sử $z=a+bi$. Khai triển $(z{add_term_i(p)})(\\overline{{z}}{add_term(q)})$ và cho phần thực bằng 0, "
        f"ta được $(a{sub_term(-cx_)})^2+(b{sub_term(-cy_)})^2={latex(cx_**2+cy_**2)}$, "
        f"nên tập hợp điểm biểu diễn là đường tròn tâm $I{diem(cx_,cy_)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT41: (z-bar+pi)(z-q) thuần ảo. Bán kính đường tròn --------------------
def mau_stt41(p, q):
    radius = sp.sqrt(p ** 2 + q ** 2) / 2
    vals = [radius, sp.sqrt(p ** 2 + q ** 2), radius ** 2 * 4, sp.Abs(p) + sp.Abs(q)]  # index0 co dinh
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    radius, d1, d2, d3 = vals
    de_bai = (
        f"Xét các số phức $z$ thỏa mãn $(\\overline{{z}}{add_term_i(p)})(z{sub_term(q)})$ là số thuần ảo. "
        f"Trên mặt phẳng tọa độ, tập hợp tất cả các điểm biểu diễn các số phức $z$ là một đường tròn có bán kính bằng\n\n"
        f"A. ${latex(d2)}$.\n"
        f"B. ${latex(d3)}$.\n"
        f"C. ${latex(d1)}$.\n"
        f"D. ${latex(radius)}$."
    )
    dap_an = f"D. ${latex(radius)}$."
    raw_form = f"\\dfrac{{\\sqrt{{{latex(p**2+q**2)}}}}}{{2}}"
    simplified = latex(radius)
    ket_qua = raw_form if raw_form.replace(" ", "") == simplified.replace(" ", "") else f"{raw_form} = {simplified}"
    loi_giai = (
        f"Giả sử $z=x+yi$. Khai triển và cho phần thực của $(\\overline{{z}}{add_term_i(p)})(z{sub_term(q)})$ bằng 0, "
        f"ta được phương trình đường tròn có bán kính $R={ket_qua}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT46: |z|=r. w=(p+iz)/(1+z). Bán kính đường tròn -----------------------
def mau_stt46(r, p):
    X, Y = sp.symbols("X Y", real=True)
    eq = sp.expand((X - p) ** 2 + Y ** 2 - r ** 2 * (X ** 2 + (1 - Y) ** 2))
    poly = sp.Poly(eq, X, Y)
    coeff_X2 = poly.coeff_monomial(X ** 2)
    coeff_Y2 = poly.coeff_monomial(Y ** 2)
    if sp.simplify(coeff_X2 - coeff_Y2) != 0 or coeff_X2 == 0:
        raise ValueError("khong dua duoc ve duong tron chuan (r=1 hoac suy bien)")
    eq_norm = sp.expand(eq / coeff_X2)
    poly_n = sp.Poly(eq_norm, X, Y)
    coeff_X = poly_n.coeff_monomial(X)
    coeff_Y = poly_n.coeff_monomial(Y)
    const = poly_n.coeff_monomial(1)
    h = -coeff_X / 2
    k = -coeff_Y / 2
    R2 = h ** 2 + k ** 2 - const
    if R2 <= 0:
        raise ValueError("R^2 khong duong")
    radius = sp.sqrt(R2)
    vals = [radius, R2, radius * 2, sp.Abs(h) + sp.Abs(k)]  # index0 co dinh
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    radius, d1, d2, d3 = vals
    de_bai = (
        f"Xét số phức $z$ thỏa mãn $|z|={latex(r)}$. Trên mặt phẳng tọa độ $Oxy$, tập hợp điểm biểu diễn các số phức "
        f"$w=\\dfrac{{{latex(p)}+iz}}{{1+z}}$ là một đường tròn có bán kính bằng\n\n"
        f"A. ${latex(d3)}$.\n"
        f"B. ${latex(d1)}$.\n"
        f"C. ${latex(d2)}$.\n"
        f"D. ${latex(radius)}$."
    )
    dap_an = f"D. ${latex(radius)}$."
    loi_giai = (
        f"Đặt $w=X+Yi$. Từ $w=\\dfrac{{{latex(p)}+iz}}{{1+z}}$ suy ra $z=\\dfrac{{w{sub_term(p)}}}{{i-w}}$, "
        f"lấy môđun và thay $|z|={latex(r)}$, biến đổi được phương trình đường tròn với bán kính $R={latex(radius)}$."
    )
    return de_bai, dap_an, loi_giai


all_rows = []

single_map = [(31, mau_stt31), (13, mau_stt13), (41, mau_stt41)]
for stt_goc, fn in single_map:
    all_rows.extend(build_rows_for_question(
        stt_goc, DANG, fn.__name__, fn, SO_BAN_MOI_LOAI, seed_base=stt_goc
    ))

# STT4: can R (so) va (a,b) cap rieng
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((4, loai_so)) % (2**31)
    R_seed = hash((4, loai_so, "R")) % (2**31)
    pairs = gen_fn(SO_BAN_MOI_LOAI, seed=seed)
    import random as _random
    rnd = _random.Random(R_seed)
    for a, b in pairs:
        R = sp.Integer(rnd.choice([1, 2, 3, 4, 5]))
        de_bai, dap_an, loi_giai = mau_stt4(R, (a, b))
        all_rows.append({
            "stt_goc": 4, "dang": DANG, "mau_ta": "mau_stt4",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"R": str(R), "a": str(a), "b": str(b)},
        })

# STT46: can r (theo loai so) va p (so nguyen nho co dinh kieu)
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((46, loai_so)) % (2**31)
    got = 0
    tries = 0
    import random as _random
    rnd = _random.Random(seed)
    while got < SO_BAN_MOI_LOAI and tries < 300:
        tries += 1
        if loai_so == "Số nguyên":
            r_val = sp.Integer(rnd.choice([2, 3, 4, 5]))
        elif loai_so == "Số hữu tỉ":
            r_val = sp.Rational(rnd.choice([3, 5, 7, 9]), rnd.choice([2, 3]))
        else:
            r_val = sp.sqrt(rnd.choice([2, 3, 5, 6, 7]))
        p_val = sp.Integer(rnd.choice([1, 2, 3, -1, -2]))
        try:
            de_bai, dap_an, loi_giai = mau_stt46(r_val, p_val)
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 46, "dang": DANG, "mau_ta": "mau_stt46",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"r": str(r_val), "p": str(p_val)},
        })
        got += 1

print("Tong so cau sinh ra (Dang 5):", len(all_rows))
with open("Sinh_them_cau_hoi/data/dang5_full.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False, indent=2)
