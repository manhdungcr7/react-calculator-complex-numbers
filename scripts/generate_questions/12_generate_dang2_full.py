"""Sinh đầy đủ Dạng 2 (Biểu diễn hình học số phức) — 9 câu gốc, mỗi câu 4
bản/loại số (nguyên, hữu tỉ, vô tỉ) = 12 bản/câu, tổng 9*12 = 108 câu."""
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

SO_BAN_MOI_LOAI = 4
DANG = "Dạng 2 - Biểu diễn hình học"


def diem(x, y):
    return f"({latex(x)};{latex(y)})"


# --- STT20/28/63: điểm biểu diễn của z=a+bi có tọa độ là -------------------
def mau_diem_bieu_dien(a, b):
    if a == b or a == -b or b == 0:
        b = b + 1
    if a == b or a == -b:
        b = b + 1
    vals = [(a, b), (-a, b), (b, a), (a, -b)]  # index0=dap an dung C, giu co dinh
    for i in range(1, 4):
        while any(vals[i] == vals[j] for j in range(i)):
            vals[i] = (vals[i][0] + 1, vals[i][1])
    (a_c, b_c), a_pt, b_pt, d_pt = vals
    de_bai = (
        f"Trên mặt phẳng tọa độ, điểm biểu diễn số phức $z={z_string(a, b)}$ có tọa độ là\n\n"
        f"A. ${diem(*a_pt)}$.\n"
        f"B. ${diem(*b_pt)}$.\n"
        f"C. ${diem(a_c, b_c)}$.\n"
        f"D. ${diem(*d_pt)}$."
    )
    dap_an = f"C. ${diem(a_c, b_c)}$."
    loi_giai = f"Điểm biểu diễn số phức $z={z_string(a, b)}$ có tọa độ là ${diem(a, b)}$."
    return de_bai, dap_an, loi_giai


# --- STT24/47: M(p,q) biểu diễn z. Phần thực của z bằng ---------------------
def mau_M_phan_thuc(p, q):
    vals = [p, q, -p, -q]  # index0=dap an dung, giu co dinh
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    p_disp, q_disp, np_disp, nq_disp = vals
    de_bai = (
        f"Trên mặt phẳng tọa độ, biết ${diem(p, q)}$ là điểm biểu diễn số phức $z$. Phần thực của $z$ bằng\n\n"
        f"A. ${latex(q_disp)}$.\n"
        f"B. ${latex(np_disp)}$.\n"
        f"C. ${latex(nq_disp)}$.\n"
        f"D. ${latex(p_disp)}$."
    )
    dap_an = f"D. ${latex(p_disp)}$."
    loi_giai = (
        f"Ta có ${diem(p, q)}$ là điểm biểu diễn số phức $z={z_string(p, q)}$. "
        f"Do đó, phần thực của $z$ là ${latex(p)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT51: M(p,q) là điểm biểu diễn của số phức nào sau đây ---------------
def mau_M_la_so_phuc_nao(p, q):
    de_bai = (
        f"Trong mặt phẳng tọa độ $Oxy$, điểm ${diem(p, q)}$ là điểm biểu diễn của số phức nào sau đây?\n\n"
        f"A. $z_1={z_string(p, -q)}$.\n"
        f"B. $z_2={z_string(-p, q)}$.\n"
        f"C. $z_3={z_string(-p, -q)}$.\n"
        f"D. $z_4={z_string(p, q)}$."
    )
    dap_an = f"D. $z_4={z_string(p, q)}$."
    loi_giai = f"Điểm ${diem(p, q)}$ biểu diễn cho số phức $z_4={z_string(p, q)}$."
    return de_bai, dap_an, loi_giai


# --- STT17: z=(a+bi)^2, điểm biểu diễn -------------------------------------
def mau_binh_phuong(a, b):
    val = sp.expand((a + b * sp.I) ** 2)
    re_v, im_v = sp.re(val), sp.im(val)
    p_pt, n_pt, m_pt = (im_v, re_v), (re_v, -im_v), (-re_v, im_v)
    correct_pt = (re_v, im_v)
    if p_pt == correct_pt or p_pt == n_pt or p_pt == m_pt:
        p_pt = (im_v + 1, re_v)
    if n_pt == correct_pt or n_pt == m_pt:
        n_pt = (re_v, -im_v - 1)
    if m_pt == correct_pt:
        m_pt = (-re_v - 1, im_v)
    de_bai = (
        f"Trên mặt phẳng tọa độ, điểm biểu diễn số phức $z = ({z_string(a, b)})^2$ là điểm nào dưới đây?\n\n"
        f"A. $P{diem(*p_pt)}$.\n"
        f"B. $Q{diem(re_v, im_v)}$.\n"
        f"C. $N{diem(*n_pt)}$.\n"
        f"D. $M{diem(*m_pt)}$."
    )
    dap_an = f"B. $Q{diem(re_v, im_v)}$."
    loi_giai = (
        f"Ta có: $z = ({z_string(a,b)})^2 = {z_string(re_v, im_v)}$.\n"
        f"Vậy, điểm biểu diễn số phức $z$ là $Q{diem(re_v, im_v)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT37: z=a+bi. w=iz. điểm biểu diễn w ---------------------------------
def mau_w_iz(a, b):
    w = sp.expand((a + b * sp.I) * sp.I)
    re_w, im_w = sp.re(w), sp.im(w)
    q_pt, m_pt, p_pt = (im_w, re_w), (a, b), (-im_w, re_w)
    correct_pt = (re_w, im_w)
    if q_pt == correct_pt or q_pt == m_pt or q_pt == p_pt:
        q_pt = (im_w + 1, re_w)
    if m_pt == correct_pt or m_pt == p_pt:
        m_pt = (a, b + 1)
    if p_pt == correct_pt:
        p_pt = (-im_w - 1, re_w)
    de_bai = (
        f"Cho số phức $z={z_string(a, b)}$. Điểm nào dưới đây là điểm biểu diễn của số phức $w=iz$ "
        f"trên mặt phẳng tọa độ?\n\n"
        f"A. $Q{diem(*q_pt)}$.\n"
        f"B. $N{diem(re_w, im_w)}$.\n"
        f"C. $M{diem(*m_pt)}$.\n"
        f"D. $P{diem(*p_pt)}$."
    )
    dap_an = f"B. $N{diem(re_w, im_w)}$."
    loi_giai = f"$w=iz={z_string(re_w, im_w)}$. Điểm biểu diễn số phức $w$ là $N{diem(re_w, im_w)}$."
    return de_bai, dap_an, loi_giai


# --- STT44: z1,z2. điểm biểu diễn của 2z1+z2 --------------------------------
def mau_2z1_z2(pair1, pair2):
    a, b = pair1
    c, d = pair2
    re_v, im_v = 2 * a + c, 2 * b + d
    correct_pt = (re_v, im_v)
    a_pt, b_pt, d_pt = (im_v, re_v), (re_v, -im_v), (-re_v, im_v)
    if a_pt == correct_pt or a_pt == b_pt or a_pt == d_pt:
        a_pt = (im_v + 1, re_v)
    if b_pt == correct_pt or b_pt == d_pt:
        b_pt = (re_v, -im_v - 1)
    if d_pt == correct_pt:
        d_pt = (-re_v - 1, im_v)
    de_bai = (
        f"Cho hai số phức $z_1={z_string(a, b)}$ và $z_2={z_string(c, d)}$. Trên mặt phẳng tọa độ $Oxy$, "
        f"điểm biểu diễn số phức $2z_1+z_2$ có tọa độ là\n\n"
        f"A. ${diem(*a_pt)}$.\n"
        f"B. ${diem(*b_pt)}$.\n"
        f"C. ${diem(re_v, im_v)}$.\n"
        f"D. ${diem(*d_pt)}$."
    )
    dap_an = f"C. ${diem(re_v, im_v)}$."
    loi_giai = (
        f"Ta có $2z_1+z_2 = {z_string(2*a, 2*b)}{join_plus(z_string(c, d))}={z_string(re_v, im_v)}$.\n"
        f"Vậy điểm biểu diễn số phức $2z_1+z_2$ có tọa độ là ${diem(re_v, im_v)}$."
    )
    return de_bai, dap_an, loi_giai


def gen_pairs_two(gen_fn, n, seed):
    p1 = gen_fn(n, seed=seed)
    p2 = gen_fn(n, seed=seed + 999983)
    return list(zip(p1, p2))


all_rows = []

single_param_map = [
    (20, mau_diem_bieu_dien), (28, mau_diem_bieu_dien), (63, mau_diem_bieu_dien),
    (24, mau_M_phan_thuc), (47, mau_M_phan_thuc),
    (51, mau_M_la_so_phuc_nao),
    (17, mau_binh_phuong),
    (37, mau_w_iz),
]

for stt_goc, fn in single_param_map:
    all_rows.extend(build_rows_for_question(
        stt_goc, DANG, fn.__name__, fn, SO_BAN_MOI_LOAI, seed_base=stt_goc
    ))

for stt_goc, fn in [(44, mau_2z1_z2)]:
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

print("Tong so cau sinh ra (Dang 2):", len(all_rows))
with open("Sinh_them_cau_hoi/data/dang2_full.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False, indent=2)
