"""
Sinh đầy đủ Dạng 1 (Xác định phần thực, phần ảo, liên hợp, môđun) — mỗi câu
gốc trong 17 câu đều có 2 bản/loại số (nguyên, hữu tỉ, vô tỉ) = 6 bản/câu,
tổng 17*6 = 102 câu.
"""
import json
import sys

sys.path.insert(0, "Sinh_them_cau_hoi/scripts")
from importlib import import_module

utils = import_module("10_common_utils")
latex = utils.latex
latex_sq = utils.latex_sq
signed_term = utils.signed_term
num_bare = utils.num_bare
z_string = utils.z_string
build_rows_for_question = utils.build_rows_for_question
assert_distinct = utils.assert_distinct
join_plus = utils.join_plus

import sympy as sp

SO_BAN_MOI_LOAI = 2
DANG = "Dạng 1 - Xác định phần thực, phần ảo, liên hợp, môđun"


# --- STT1: Cho z=a+bi. Tìm phần thực/ảo của z-bar ---------------------------
def mau_stt1(a, b):
    de_bai = (
        f"Cho số phức $z = {z_string(a, b)}$. Tìm phần thực và phần ảo của số phức $\\overline{{z}}$.\n\n"
        f"A. Phần thực bằng ${latex(-a)}$ và phần ảo bằng ${latex(b)}i$.\n"
        f"B. Phần thực bằng ${latex(-a)}$ và phần ảo bằng ${latex(b)}$.\n"
        f"C. Phần thực bằng ${latex(a)}$ và phần ảo bằng ${latex(-b)}i$.\n"
        f"D. Phần thực bằng ${latex(a)}$ và phần ảo bằng ${latex(-b)}$."
    )
    dap_an = f"D. Phần thực bằng ${latex(a)}$ và phần ảo bằng ${latex(-b)}$."
    loi_giai = (
        f"Từ $z = {z_string(a, b)}$ suy ra $\\overline{{z}} = {z_string(a, -b)}$. "
        f"Nên phần thực của $\\overline{{z}}$ bằng ${latex(a)}$ và phần ảo của $\\overline{{z}}$ bằng ${latex(-b)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT2: z1,z2 cho trước. Tính môđun của z1+z2 ----------------------------
def mau_stt2(pair1, pair2):
    a, b = pair1
    c, d = pair2
    dung = sp.sqrt((a + c) ** 2 + (b + d) ** 2)
    d1 = (a + c) ** 2 + (b + d) ** 2
    d2 = sp.sqrt((a - c) ** 2 + (b - d) ** 2)
    d3 = sp.sqrt(a ** 2 + b ** 2) + sp.sqrt(c ** 2 + d ** 2)
    if sp.simplify(d3 - dung) == 0 or sp.simplify(d3 - d2) == 0 or sp.simplify(d3 - d1) == 0:
        d3 = d3 + 1
    assert_distinct(dung, d1, d2, d3)
    de_bai = (
        f"Cho hai số phức $z_1 = {z_string(a, b)}$ và $z_2 = {z_string(c, d)}$. "
        f"Tính môđun của số phức $z_1+z_2$.\n\n"
        f"A. $|z_1+z_2| = {latex(dung)}$.\n"
        f"B. $|z_1+z_2| = {latex(d1)}$.\n"
        f"C. $|z_1+z_2| = {latex(d2)}$.\n"
        f"D. $|z_1+z_2| = {latex(d3)}$."
    )
    dap_an = f"A. $|z_1+z_2| = {latex(dung)}$."
    loi_giai = (
        f"Ta có $z_1+z_2 = {z_string(a + c, b + d)} \\Rightarrow "
        f"|z_1+z_2| = \\sqrt{{{latex_sq(a+c)}^2+{latex_sq(b+d)}^2}} = {latex(dung)}$."
    )
    return de_bai, dap_an, loi_giai


def gen_pairs_two(gen_fn, n, seed):
    p1 = gen_fn(n, seed=seed)
    p2 = gen_fn(n, seed=seed + 999983)
    return list(zip(p1, p2))


# --- STT9: Kí hiệu a,b là phần thực/ảo của z. Tìm a,b -----------------------
def mau_stt9(a, b):
    opts = [(-a, -b), (-a, b), (a, -b), (a, b)]
    assert len(set(opts)) == 4, f"Trung phuong an STT9: a={a}, b={b}"
    de_bai = (
        f"Kí hiệu $a, b$ lần lượt là phần thực và phần ảo của số phức ${z_string(a, b)}$. Tìm $a, b$.\n\n"
        f"A. $a={latex(-a)}, b={latex(-b)}$.\n"
        f"B. $a={latex(-a)}, b={latex(b)}$.\n"
        f"C. $a={latex(a)}, b={latex(-b)}$.\n"
        f"D. $a={latex(a)}, b={latex(b)}$."
    )
    dap_an = f"D. $a={latex(a)}, b={latex(b)}$."
    loi_giai = (
        f"Số phức ${z_string(a, b)}$ có phần thực và phần ảo lần lượt là ${latex(a)}$ và ${latex(b)}$. "
        f"Vậy, $a={latex(a)}, b={latex(b)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT10: z-bar=(a+bi)(1+i). Tính môđun của z -----------------------------
def mau_stt10(a, b):
    dung = sp.sqrt(2 * (a ** 2 + b ** 2))
    d1 = sp.sqrt(a ** 2 + b ** 2)
    d2 = sp.sqrt(2) * (a ** 2 + b ** 2)
    d3 = 2 * sp.sqrt(a ** 2 + b ** 2)
    vals = [dung, d1, d2, d3]
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    dung, d1, d2, d3 = vals
    zbar_val = sp.expand((a + b * sp.I) * (1 + sp.I))
    de_bai = (
        f"Tính môđun của số phức $z$ biết $\\overline{{z}} = ({z_string(a, b)})(1+i)$.\n\n"
        f"A. $|z| = {latex(d2)}$.\n"
        f"B. $|z| = {latex(d1)}$.\n"
        f"C. $|z| = {latex(dung)}$.\n"
        f"D. $|z| = {latex(d3)}$."
    )
    dap_an = f"C. $|z| = {latex(dung)}$."
    re_z, im_z = sp.re(zbar_val), sp.im(zbar_val)
    loi_giai = (
        f"Ta có $\\overline{{z}} = ({z_string(a, b)})(1+i) = {z_string(re_z, im_z)} "
        f"\\Rightarrow |\\overline{{z}}| = {latex(dung)} \\Rightarrow |z| = {latex(dung)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT15: Môđun của (a+bi) bằng (không có nhãn z=) ------------------------
def mau3_core(a, b):
    modun = sp.sqrt(a ** 2 + b ** 2)
    d1 = a ** 2 + b ** 2
    if a ** 2 == b ** 2:
        d2 = sp.sqrt(a ** 2 + 2 * sp.Abs(a * b))
        d3 = a ** 2 + 2 * sp.Abs(a * b)
    else:
        d2 = sp.sqrt(sp.Abs(a ** 2 - b ** 2))
        d3 = sp.Abs(a ** 2 - b ** 2)
    vals = [modun, d1, d2, d3]
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    modun, d1, d2, d3 = vals
    return modun, d1, d2, d3


def mau_stt15(a, b):
    modun, d1, d2, d3 = mau3_core(a, b)
    de_bai = (
        f"Môđun của số phức ${z_string(a, b)}$ bằng\n\n"
        f"A. ${latex(d1)}$.\n"
        f"B. ${latex(modun)}$.\n"
        f"C. ${latex(d3)}$.\n"
        f"D. ${latex(d2)}$."
    )
    dap_an = f"B. ${latex(modun)}$."
    loi_giai = f"Ta có: $|{z_string(a,b)}| = \\sqrt{{{latex_sq(a)}^2+{latex_sq(b)}^2}} = {latex(modun)}$."
    return de_bai, dap_an, loi_giai


# --- STT18/49: Số phức liên hợp của z=a+bi là -------------------------------
def mau_stt49(a, b):
    de_bai = (
        f"Số phức liên hợp của số phức $z={z_string(a, b)}$ là\n\n"
        f"A. $\\overline{{z}}={z_string(-a, -b)}$.\n"
        f"B. $\\overline{{z}}={z_string(-a, b)}$.\n"
        f"C. $\\overline{{z}}={z_string(a, b)}$.\n"
        f"D. $\\overline{{z}}={z_string(a, -b)}$."
    )
    dap_an = f"D. $\\overline{{z}}={z_string(a, -b)}$."
    loi_giai = f"Ta có số phức liên hợp của số phức $z={z_string(a, b)}$ là $\\overline{{z}}={z_string(a, -b)}$."
    return de_bai, dap_an, loi_giai


# --- STT43: Số phức liên hợp của (a+bi) là (không có nhãn z=) --------------
def mau_stt43(a, b):
    de_bai = (
        f"Số phức liên hợp của số phức ${z_string(a, b)}$ là\n\n"
        f"A. ${z_string(-a, b)}$.\n"
        f"B. ${z_string(-a, -b)}$.\n"
        f"C. ${z_string(a, b)}$.\n"
        f"D. ${z_string(a, -b)}$."
    )
    dap_an = f"D. ${z_string(a, -b)}$."
    loi_giai = f"Số phức liên hợp của số phức ${z_string(a, b)}$ là ${z_string(a, -b)}$."
    return de_bai, dap_an, loi_giai


# --- STT30/58: Phần ảo của z=a+bi (là/bằng) --------------------------------
def mau_phan_ao(a, b, verb="là"):
    vals = [b, -b, a, -a]
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    b_disp, nb_disp, a_disp, na_disp = vals
    de_bai = (
        f"Phần ảo của số phức $z={z_string(a, b)}$ {verb}\n\n"
        f"A. ${latex(b_disp)}$.\n"
        f"B. ${latex(nb_disp)}$.\n"
        f"C. ${latex(a_disp)}$.\n"
        f"D. ${latex(na_disp)}$."
    )
    dap_an = f"A. ${latex(b_disp)}$."
    loi_giai = f"Phần ảo của số phức $z={z_string(a, b)}$ {verb} ${latex(b)}$."
    return de_bai, dap_an, loi_giai


def mau_stt30(a, b):
    return mau_phan_ao(a, b, verb="là")


def mau_stt58(a, b):
    return mau_phan_ao(a, b, verb="bằng")


# --- STT53: Phần thực của z=a+bi bằng --------------------------------------
def mau_stt53(a, b):
    # dap an dung (C=a) giu nguyen, chi bump cac phuong an nhieu neu trung
    vals = [a, -b, b, -a]  # index0=dap an dung, giu co dinh
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    a_disp, nb_disp, b_disp, na_disp = vals
    de_bai = (
        f"Phần thực của số phức $z={z_string(a, b)}$ bằng\n\n"
        f"A. ${latex(nb_disp)}$.\n"
        f"B. ${latex(b_disp)}$.\n"
        f"C. ${latex(a_disp)}$.\n"
        f"D. ${latex(na_disp)}$."
    )
    dap_an = f"C. ${latex(a_disp)}$."
    loi_giai = f"Phần thực của số phức $z={z_string(a, b)}$ bằng ${latex(a)}$."
    return de_bai, dap_an, loi_giai


# --- STT34: Số phức nào dưới đây là số thuần ảo? ---------------------------
def mau_stt34(a, b):
    # a,b dùng làm 2 hệ số khác 0 để tạo 3 phương án "không thuần ảo",
    # b dùng làm hệ số ảo cho phương án thuần ảo đúng.
    correct_coef = b
    wrong1 = z_string(a, b)  # có phần thực -> không thuần ảo
    wrong2 = num_bare(a)  # số thực thuần túy -> không thuần ảo
    wrong3 = z_string(a, -b)
    correct = f"{latex(correct_coef)}i" if sp.Abs(correct_coef) != 1 else ("i" if correct_coef > 0 else "-i")
    de_bai = (
        f"Số phức nào dưới đây là số thuần ảo?\n\n"
        f"A. $z={wrong1}$.\n"
        f"B. $z={correct}$.\n"
        f"C. $z={wrong2}$.\n"
        f"D. $z={wrong3}$."
    )
    dap_an = f"B. $z={correct}$."
    loi_giai = "Số phức là số thuần ảo nếu phần thực bằng $0$."
    return de_bai, dap_an, loi_giai


# --- STT40: Số phức có phần thực bằng P và phần ảo bằng Q là ---------------
def mau_stt40(P, Q):
    if P == Q or P == -Q:
        Q = Q + 1 if Q + 1 != P and Q + 1 != -P else Q + 2
    de_bai = (
        f"Số phức có phần thực bằng ${latex(P)}$ và phần ảo bằng ${latex(Q)}$ là\n\n"
        f"A. ${z_string(P, Q)}$.\n"
        f"B. ${z_string(Q, -P)}$.\n"
        f"C. ${z_string(P, -Q)}$.\n"
        f"D. ${z_string(Q, P)}$."
    )
    dap_an = f"A. ${z_string(P, Q)}$."
    loi_giai = f"Số phức có phần thực bằng ${latex(P)}$ và phần ảo bằng ${latex(Q)}$ là $z = {z_string(P, Q)}$."
    return de_bai, dap_an, loi_giai


# --- STT50: z=a+bi, w=c+di. Môđun của z*w-bar bằng --------------------------
def mau_stt50(pair1, pair2):
    a, b = pair1
    c, d = pair2
    # z * conj(w)
    prod = sp.expand((a + b * sp.I) * (c - d * sp.I))
    re_p, im_p = sp.re(prod), sp.im(prod)
    modun = sp.sqrt(re_p ** 2 + im_p ** 2)
    d1 = re_p ** 2 + im_p ** 2
    if re_p == 0 or im_p == 0 or re_p ** 2 == im_p ** 2:
        d2 = sp.sqrt(re_p ** 2 + 2 * sp.Abs(re_p * im_p) + 1)
        d3 = re_p ** 2 + 2 * sp.Abs(re_p * im_p) + 1
    else:
        d2 = sp.sqrt(sp.Abs(re_p ** 2 - im_p ** 2))
        d3 = sp.Abs(re_p ** 2 - im_p ** 2)
    vals = [modun, d1, d2, d3]
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    modun, d1, d2, d3 = vals
    de_bai = (
        f"Cho hai số phức $z={z_string(a, b)}$ và $w={z_string(c, d)}$. "
        f"Môđun của số phức $z\\cdot\\overline{{w}}$ bằng\n\n"
        f"A. ${latex(d1)}$.\n"
        f"B. ${latex(d3)}$.\n"
        f"C. ${latex(d2)}$.\n"
        f"D. ${latex(modun)}$."
    )
    dap_an = f"D. ${latex(modun)}$."
    loi_giai = (
        f"Ta có $z\\cdot\\overline{{w}}=({z_string(a,b)})({z_string(c,-d)})={z_string(re_p, im_p)}$.\n"
        f"Vậy $|z\\cdot\\overline{{w}}|=|{z_string(re_p, im_p)}|={latex(modun)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT59: z=a+bi. Môđun của (1+i)z bằng -----------------------------------
def mau_stt59(a, b):
    dung = sp.sqrt(2 * (a ** 2 + b ** 2))
    d1 = sp.sqrt(a ** 2 + b ** 2)
    d2 = sp.sqrt(2) * (a ** 2 + b ** 2)
    d3 = 2 * sp.sqrt(a ** 2 + b ** 2)
    vals = [dung, d1, d2, d3]
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    dung, d1, d2, d3 = vals
    prod = sp.expand((1 + sp.I) * (a + b * sp.I))
    re_p, im_p = sp.re(prod), sp.im(prod)
    de_bai = (
        f"Cho số phức $z={z_string(a, b)}$, môđun của số phức $(1+i)z$ bằng\n\n"
        f"A. ${latex(d2)}$.\n"
        f"B. ${latex(d1)}$.\n"
        f"C. ${latex(d3)}$.\n"
        f"D. ${latex(dung)}$."
    )
    dap_an = f"D. ${latex(dung)}$."
    loi_giai = (
        f"Ta có $(1+i)z=(1+i)({z_string(a,b)})={z_string(re_p, im_p)}$.\n"
        f"Do đó môđun của $(1+i)z$ là $|{z_string(re_p, im_p)}|={latex(dung)}$."
    )
    return de_bai, dap_an, loi_giai


# ---------------------------------------------------------------------------
all_rows = []

single_param_map = [
    (1, mau_stt1), (9, mau_stt9), (10, mau_stt10), (15, mau_stt15),
    (18, mau_stt49), (22, mau_stt15), (30, mau_stt30), (34, mau_stt34),
    (43, mau_stt43), (49, mau_stt49), (53, mau_stt53), (58, mau_stt58),
    (59, mau_stt59), (62, mau_stt15),
]

for stt_goc, fn in single_param_map:
    all_rows.extend(build_rows_for_question(
        stt_goc, DANG, fn.__name__, fn, SO_BAN_MOI_LOAI, seed_base=stt_goc
    ))

# STT40 dùng 2 tham số P,Q nhưng vẫn 1 cặp (a,b)-like -> tái dùng khung sẵn có
all_rows.extend(build_rows_for_question(
    40, DANG, "mau_stt40", mau_stt40, SO_BAN_MOI_LOAI, seed_base=40
))

# STT2 và STT50 cần 2 cặp số (z1,z2) hoặc (z,w) -> xử lý riêng
for stt_goc, fn in [(2, mau_stt2), (50, mau_stt50)]:
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

print("Tong so cau sinh ra (Dang 1):", len(all_rows))
with open("Sinh_them_cau_hoi/data/dang1_full.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False, indent=2)
