"""Sinh đầy đủ Dạng 3 (Phép toán số phức) — 12 câu gốc, mỗi câu 3 bản/loại số
(nguyên, hữu tỉ, vô tỉ) = 9 bản/câu, tổng 12*9 = 108 câu."""
import json
import sys

sys.path.insert(0, "Sinh_them_cau_hoi/scripts")
from importlib import import_module

utils = import_module("10_common_utils")
latex = utils.latex
z_string = utils.z_string
build_rows_for_question = utils.build_rows_for_question
assert_distinct = utils.assert_distinct
join_plus = utils.join_plus

import sympy as sp

SO_BAN_MOI_LOAI = 3
DANG = "Dạng 3 - Phép toán số phức"


def cx(a, b):
    return a + b * sp.I


def parts(expr):
    return sp.re(expr), sp.im(expr)


def _bump(v, k):
    if isinstance(v, tuple):
        return (v[0] + k, v[1])
    return v + k


def safe4(vals):
    """Đảm bảo 4 giá trị (mỗi giá trị có thể là số hoặc cặp (re,im)) khác nhau từng đôi."""
    vals = list(vals)
    for i in range(len(vals)):
        tries = 0
        while any(vals[i] == vals[j] for j in range(i)) and tries < 20:
            vals[i] = _bump(vals[i], 1)
            tries += 1
    return vals


# --- STT3: z=a+bi. w=iz+z-bar -----------------------------------------------
def mau_stt3(a, b):
    z = cx(a, b)
    w = sp.expand(sp.I * z + sp.conjugate(z))
    re_w, im_w = parts(w)
    opts = safe4([(re_w, im_w), (re_w, -im_w), (-re_w, -im_w), (-re_w, im_w)])
    de_bai = (
        f"Cho số phức $z={z_string(a, b)}$. Tìm số phức $w=iz+\\overline{{z}}$.\n\n"
        f"A. $w={z_string(*opts[1])}$.\n"
        f"B. $w={z_string(*opts[0])}$.\n"
        f"C. $w={z_string(*opts[2])}$.\n"
        f"D. $w={z_string(*opts[3])}$."
    )
    dap_an = f"B. $w={z_string(*opts[0])}$."
    loi_giai = f"$w = i({z_string(a,b)}){join_plus(z_string(a,-b))} = {z_string(re_w, im_w)}$."
    return de_bai, dap_an, loi_giai


# --- STT5: z=i(p+qi). Tìm liên hợp -----------------------------------------
def mau_stt5(p, q):
    z = sp.expand(sp.I * (p + q * sp.I))
    re_z, im_z = parts(z)
    opts = safe4([(re_z, -im_z), (-re_z, im_z), (re_z, im_z), (-re_z, -im_z)])
    de_bai = (
        f"Tìm số phức liên hợp của số phức $z = i({z_string(p, q)})$.\n\n"
        f"A. $\\overline{{z}} = {z_string(*opts[0])}$.\n"
        f"B. $\\overline{{z}} = {z_string(*opts[1])}$.\n"
        f"C. $\\overline{{z}} = {z_string(*opts[2])}$.\n"
        f"D. $\\overline{{z}} = {z_string(*opts[3])}$."
    )
    dap_an = f"A. $\\overline{{z}} = {z_string(*opts[0])}$."
    loi_giai = f"Ta có $z = i({z_string(p,q)}) = {z_string(re_z, im_z)} \\Rightarrow \\overline{{z}} = {z_string(re_z, -im_z)}$."
    return de_bai, dap_an, loi_giai


# --- STT16: z1,z2. Phần ảo của z1+z2-bar -------------------------------------
def mau_stt16(pair1, pair2):
    a, b = pair1
    c, d = pair2
    val = cx(a, b) + sp.conjugate(cx(c, d))
    re_v, im_v = parts(val)
    opts = safe4([im_v, -im_v, re_v, -re_v])
    de_bai = (
        f"Cho hai số phức $z_1 = {z_string(a, b)}$ và $z_2 = {z_string(c, d)}$. "
        f"Phần ảo của số phức $z_1+\\overline{{z_2}}$ bằng\n\n"
        f"A. ${latex(opts[1])}$.\n"
        f"B. ${latex(opts[3])}$.\n"
        f"C. ${latex(opts[0])}$.\n"
        f"D. ${latex(opts[2])}$."
    )
    dap_an = f"C. ${latex(opts[0])}$."
    loi_giai = (
        f"Ta có: $z_1+\\overline{{z_2}} = {z_string(a,b)}{join_plus(z_string(c,-d))} = {z_string(re_v, im_v)}$. "
        f"Phần ảo của số phức $z_1+\\overline{{z_2}}$ là ${latex(im_v)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT19: z1,z2. Phần thực của z1+z2 --------------------------------------
def mau_stt19(pair1, pair2):
    a, b = pair1
    c, d = pair2
    re_v, im_v = a + c, b + d
    opts = safe4([re_v, im_v, -re_v, -im_v])
    de_bai = (
        f"Cho hai số phức $z_1 = {z_string(a, b)}$ và $z_2 = {z_string(c, d)}$. "
        f"Phần thực của số phức $z_1+z_2$ bằng\n\n"
        f"A. ${latex(opts[1])}$.\n"
        f"B. ${latex(opts[0])}$.\n"
        f"C. ${latex(opts[2])}$.\n"
        f"D. ${latex(opts[3])}$."
    )
    dap_an = f"B. ${latex(opts[0])}$."
    loi_giai = (
        f"Ta có $z_1+z_2 = {z_string(re_v, im_v)}$.\n"
        f"Phần thực của số phức $z_1+z_2$ bằng ${latex(re_v)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT21: z1,z2. Phần ảo của z1*z2 ----------------------------------------
def mau_stt21(pair1, pair2):
    a, b = pair1
    c, d = pair2
    val = sp.expand(cx(a, b) * cx(c, d))
    re_v, im_v = parts(val)
    re_v_distractor = re_v
    if re_v_distractor == im_v or re_v_distractor == -im_v:
        re_v_distractor = re_v_distractor + 1  # chỉ đổi phương án nhiễu A, không đụng đáp án đúng D hay lời giải
    de_bai = (
        f"Cho hai số phức $z_1 = {z_string(a, b)}$ và $z_2 = {z_string(c, d)}$. "
        f"Phần ảo của số phức $z_1z_2$ bằng\n\n"
        f"A. ${latex(re_v_distractor)}$.\n"
        f"B. ${latex(im_v)}i$.\n"
        f"C. ${latex(-im_v)}$.\n"
        f"D. ${latex(im_v)}$."
    )
    dap_an = f"D. ${latex(im_v)}$."
    loi_giai = (
        f"Ta có $z_1z_2 = ({z_string(a,b)})({z_string(c,d)}) = {z_string(re_v, im_v)}$.\n"
        f"Suy ra phần ảo của $z_1z_2$ bằng ${latex(im_v)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT23: z=a+bi. 2z bằng --------------------------------------------------
def mau_stt23(a, b):
    re_v, im_v = 2 * a, 2 * b
    opts = safe4([(re_v, im_v), (re_v, -im_v), (a, im_v), (-re_v, im_v)])
    de_bai = (
        f"Cho số phức $z={z_string(a, b)}$, khi đó $2z$ bằng\n\n"
        f"A. ${z_string(*opts[1])}$.\n"
        f"B. ${z_string(*opts[0])}$.\n"
        f"C. ${z_string(*opts[2])}$.\n"
        f"D. ${z_string(*opts[3])}$."
    )
    dap_an = f"B. ${z_string(*opts[0])}$."
    loi_giai = f"Ta có $2z = 2({z_string(a,b)}) = {z_string(re_v, im_v)}$."
    return de_bai, dap_an, loi_giai


# --- STT29: z=a+bi. Phần thực của z^2 ---------------------------------------
def mau_stt29(a, b):
    val = sp.expand(cx(a, b) ** 2)
    re_v, im_v = parts(val)
    opts = safe4([re_v, im_v, -re_v, -im_v])
    de_bai = (
        f"Cho số phức $z={z_string(a, b)}$, phần thực của số phức $z^2$ bằng\n\n"
        f"A. ${latex(opts[0])}$.\n"
        f"B. ${latex(opts[1])}$.\n"
        f"C. ${latex(opts[2])}$.\n"
        f"D. ${latex(opts[3])}$."
    )
    dap_an = f"A. ${latex(opts[0])}$."
    loi_giai = (
        f"Ta có $z^2 = ({z_string(a,b)})^2 = {z_string(re_v, im_v)}$ "
        f"nên phần thực của số phức $z^2$ bằng ${latex(re_v)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT35/48/64: z1,z2. z=z1+z2 (giống hệt cấu trúc) -----------------------
def mau_tong(pair1, pair2):
    a, b = pair1
    c, d = pair2
    re_v, im_v = a + c, b + d
    opts = safe4([(re_v, im_v), (a, im_v), (-re_v, im_v), (re_v, -im_v)])
    de_bai = (
        f"Cho hai số phức $z_1 = {z_string(a, b)}$ và $z_2 = {z_string(c, d)}$. "
        f"Tìm số phức $z=z_1+z_2$.\n\n"
        f"A. $z={z_string(*opts[0])}$.\n"
        f"B. $z={z_string(*opts[1])}$.\n"
        f"C. $z={z_string(*opts[2])}$.\n"
        f"D. $z={z_string(*opts[3])}$."
    )
    dap_an = f"A. $z={z_string(*opts[0])}$."
    loi_giai = f"Ta có $z = {z_string(a,b)}{join_plus(z_string(c,d))} = {z_string(re_v, im_v)}$."
    return de_bai, dap_an, loi_giai


# --- STT52: z,w. z+w bằng ----------------------------------------------------
def mau_stt52(pair1, pair2):
    a, b = pair1
    c, d = pair2
    re_v, im_v = a + c, b + d
    opts = safe4([(re_v, im_v), (a, im_v), (-re_v, -im_v), (re_v, -im_v)])
    de_bai = (
        f"Cho hai số phức $z={z_string(a, b)}$ và $w={z_string(c, d)}$. Số phức $z+w$ bằng\n\n"
        f"A. ${z_string(*opts[0])}$.\n"
        f"B. ${z_string(*opts[1])}$.\n"
        f"C. ${z_string(*opts[2])}$.\n"
        f"D. ${z_string(*opts[3])}$."
    )
    dap_an = f"A. ${z_string(*opts[0])}$."
    loi_giai = f"Ta có $z+w={z_string(a,b)}{join_plus(z_string(c,d))}={z_string(re_v, im_v)}$."
    return de_bai, dap_an, loi_giai


# --- STT57: z,w. z-w bằng ----------------------------------------------------
def mau_stt57(pair1, pair2):
    a, b = pair1
    c, d = pair2
    re_v, im_v = a - c, b - d
    opts = safe4([(re_v, im_v), (a, im_v), (-re_v, -im_v), (re_v, -im_v)])
    de_bai = (
        f"Cho hai số phức $z={z_string(a, b)}$ và $w={z_string(c, d)}$. Số phức $z-w$ bằng\n\n"
        f"A. ${z_string(*opts[0])}$.\n"
        f"B. ${z_string(*opts[1])}$.\n"
        f"C. ${z_string(*opts[2])}$.\n"
        f"D. ${z_string(*opts[3])}$."
    )
    dap_an = f"A. ${z_string(*opts[0])}$."
    loi_giai = f"Ta có $z-w={z_string(a,b)}-({z_string(c,d)})={z_string(re_v, im_v)}$."
    return de_bai, dap_an, loi_giai


def gen_pairs_two(gen_fn, n, seed):
    p1 = gen_fn(n, seed=seed)
    p2 = gen_fn(n, seed=seed + 999983)
    return list(zip(p1, p2))


all_rows = []

single_param_map = [(3, mau_stt3), (5, mau_stt5), (23, mau_stt23), (29, mau_stt29)]
for stt_goc, fn in single_param_map:
    all_rows.extend(build_rows_for_question(
        stt_goc, DANG, fn.__name__, fn, SO_BAN_MOI_LOAI, seed_base=stt_goc
    ))

two_param_map = [
    (16, mau_stt16), (19, mau_stt19), (21, mau_stt21),
    (35, mau_tong), (48, mau_tong), (64, mau_tong),
    (52, mau_stt52), (57, mau_stt57),
]
for stt_goc, fn in two_param_map:
    for loai_so, gen_fn in utils.NUMBER_TYPES:
        seed = hash((stt_goc, loai_so, "pairs")) % (2**31)
        pairs = gen_pairs_two(gen_fn, SO_BAN_MOI_LOAI, seed)
        for p1, p2 in pairs:
            de_bai, dap_an, loi_giai = fn(p1, p2)
            all_rows.append({
                "stt_goc": stt_goc, "dang": DANG, "mau_ta": fn.__name__,
                "nguon": "Nhân bản", "loai_so": loai_so,
                "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
                "params": {"a": str(p1[0]), "b": str(p1[1]), "c": str(p2[0]), "d": str(p2[1])},
            })

print("Tong so cau sinh ra (Dang 3):", len(all_rows))
with open("Sinh_them_cau_hoi/data/dang3_full.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False, indent=2)
