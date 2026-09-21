"""Sinh đầy đủ Dạng 6 (Phương trình bậc hai có tham số trên tập số phức) —
5 câu gốc (STT 26, 33, 36, 56, 61), mỗi câu 6 bản/loại số, tổng 5*18 = 90 câu.

Mỗi biến thể được giải lại thực sự bằng sympy theo đúng phương pháp (biện luận
theo dấu Delta', dùng Viet, giải hệ) của lời giải gốc — không chỉ thay số vào
công thức đáp số có sẵn."""
import json
import random
import sys

sys.path.insert(0, "Sinh_them_cau_hoi/scripts")
from importlib import import_module

utils = import_module("10_common_utils")
latex = utils.latex
build_rows_for_question = utils.build_rows_for_question

import sympy as sp

SO_BAN_MOI_LOAI = 6
DANG = "Dạng 6 - Phương trình bậc hai có tham số"


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


# ============================================================================
# STT26: z^2 - 2mz + (c*m + d) = 0. Đếm SỐ NGUYÊN m để |z1| = |z2|
# (Delta' = m^2 - cm - d; Delta'>0: can m=0; Delta'<0: luon thoa)
# ============================================================================
def mau_stt26(c, d):
    count = 0
    for mv in range(-80, 81):
        delta = mv ** 2 - c * mv - d
        if delta > 0:
            if mv == 0:
                count += 1
        elif delta < 0:
            count += 1
    n = count
    if n < 1 or n > 12:
        raise ValueError("so luong khong hop ly")
    opts = sorted({n, max(n - 1, 0), n + 1, n + 2})[:4]
    while len(opts) < 4:
        opts.append(opts[-1] + 1)
    de_bai = (
        f"Trên tập hợp các số phức, xét phương trình $z^2-2mz{add_term(c)}m{add_term(d)}=0$ "
        f"($m$ là tham số thực). Có bao nhiêu giá trị nguyên của $m$ để phương trình đó có hai nghiệm "
        f"phân biệt $z_1, z_2$ thỏa mãn $|z_1| = |z_2|$?\n\n"
        f"A. ${opts[0]}$.\nB. ${opts[1]}$.\nC. ${opts[2]}$.\nD. ${opts[3]}$."
    )
    letter = "ABCD"[opts.index(n)]
    dap_an = f"{letter}. ${n}$."
    loi_giai = (
        f"Ta có $\\Delta' = m^2{sub_term(c)}m{sub_term(d)}$.\n\n"
        f"Nếu $\\Delta'>0$ thì phương trình có hai nghiệm thực. Khi đó $|z_1|=|z_2| \\Leftrightarrow z_1=-z_2 "
        f"\\Leftrightarrow z_1+z_2=0 \\Leftrightarrow m=0$ (nhận nếu thỏa $\\Delta'(0)>0$).\n\n"
        f"Nếu $\\Delta'<0$ thì phương trình có hai nghiệm phức liên hợp nên luôn có $|z_1|=|z_2|$.\n\n"
        f"Đếm trực tiếp các giá trị nguyên $m$ thỏa mãn hai trường hợp trên, ta được {n} giá trị."
    )
    return de_bai, dap_an, loi_giai


# ============================================================================
# STT33: z^2 - 2(m+a)z + m^2 = 0. Đếm số giá trị m để |z1|+|z2| = S
# ============================================================================
def mau_stt33(a, S):
    mm = sp.symbols("mm", real=True)
    valid = set()

    # TH1: Delta' < 0 -> z1,z2 lien hop, z1*z2 = m^2 = |z1|^2 -> |z1|=|m|
    # |z1|+|z2| = 2|m| = S -> m = +-S/2
    for mv in [S / 2, -S / 2]:
        delta_val = 2 * a * mv + a ** 2
        if sp.simplify(delta_val) < 0:
            valid.add(sp.nsimplify(mv))

    # TH2: Delta' >= 0 -> hai nghiem thuc, (|z1|+|z2|)^2 = 4(m+a)^2 (vi z1*z2=m^2>=0)
    # |z1|+|z2| = 2|m+a| = S -> m = -a +- S/2
    for mv in [-a + S / 2, -a - S / 2]:
        delta_val = sp.simplify((mv + a) ** 2 - mv ** 2)
        if delta_val > 0:
            valid.add(sp.nsimplify(mv))

    n = len(valid)
    if n < 1 or n > 4:
        raise ValueError("so nghiem khong hop le")
    opts = sorted({n, max(n - 1, 0), n + 1, n + 2})[:4]
    while len(opts) < 4:
        opts.append(opts[-1] + 1)
    de_bai = (
        f"Trên tập hợp số phức, xét phương trình $z^2-2(m{add_term(a)})z+m^2=0$ ($m$ là tham số thực). "
        f"Có bao nhiêu giá trị của $m$ để phương trình đó có hai nghiệm phân biệt $z_1, z_2$ thỏa mãn "
        f"$|z_1|+|z_2|={latex(S)}$?\n\n"
        f"A. ${opts[0]}$.\nB. ${opts[1]}$.\nC. ${opts[2]}$.\nD. ${opts[3]}$."
    )
    letter = "ABCD"[opts.index(n)]
    dap_an = f"{letter}. ${n}$."
    loi_giai = (
        f"Ta có $\\Delta'=(m{add_term(a)})^2-m^2$.\n\n"
        f"TH1: $\\Delta'<0$. Khi đó $z_1=\\overline{{z_2}}$, suy ra $2|z_1|=|z_1|+|z_2|={latex(S)} "
        f"\\Rightarrow |z_1|={latex(S/2)} \\Rightarrow m^2=z_1z_2=|z_1|^2 \\Rightarrow m=\\pm{latex(S/2)}$, "
        f"kết hợp điều kiện $\\Delta'<0$ để chọn nghiệm phù hợp.\n\n"
        f"TH2: $\\Delta'\\ge0$. Khi đó $z_1+z_2=2(m{add_term(a)})$, $z_1z_2=m^2$, nên "
        f"$(|z_1|+|z_2|)^2=(z_1+z_2)^2-2z_1z_2+2|z_1z_2|=4(m{add_term(a)})^2$, suy ra "
        f"$|m{add_term(a)}|={latex(S/2)} \\Rightarrow m=-({latex(a)})\\pm{latex(S/2)}$, kết hợp điều kiện "
        f"$\\Delta'\\ge0$ để chọn nghiệm phù hợp.\n\n"
        f"Tổng hợp cả hai trường hợp (loại nghiệm trùng nếu có), ta được {n} giá trị $m$ thỏa mãn."
    )
    return de_bai, dap_an, loi_giai


# ============================================================================
# STT36: viết pt bậc 2 nhận z=p+qi và p-qi làm nghiệm
# ============================================================================
def mau_stt36(p, q):
    S = 2 * p
    P = p ** 2 + q ** 2
    correct = f"z^2{sub_term(S)}z{add_term(P)}=0"
    d1 = f"z^2{add_term(S)}z{sub_term(P)}=0"
    d2 = f"z^2{sub_term(S)}z{sub_term(P)}=0"
    d3 = f"z^2{add_term(S)}z{add_term(P)}=0"
    z_p = f"{latex(p)}{add_term_i(q)}"
    z_m = f"{latex(p)}{add_term_i(-q)}"
    de_bai = (
        f"Phương trình nào dưới đây nhận hai số phức $z={z_p}$ và ${z_m}$ là nghiệm?\n\n"
        f"A. ${d1}$.\nB. ${d2}$.\nC. ${correct}$.\nD. ${d3}$."
    )
    dap_an = f"C. ${correct}$."
    loi_giai = (
        f"Áp dụng định lý Vi-ét: tổng hai số phức là ${latex(S)}$, tích của chúng là ${latex(P)}$ "
        f"$\\Rightarrow$ hai số phức là nghiệm của phương trình ${correct}$."
    )
    return de_bai, dap_an, loi_giai


# ============================================================================
# STT56: z^2 - 2(m+a)z + m^2 = 0. Đếm số giá trị m để pt có nghiệm z0, |z0|=R
# ============================================================================
def mau_stt56(a, R):
    valid = set()
    mm = sp.symbols("mm", real=True)

    # TH1: Delta'=0 -> nghiem kep z0=m+a, tai m=-a
    m_edge = -a
    z0 = m_edge + a
    if sp.simplify(sp.Abs(z0) - R) == 0:
        valid.add(sp.nsimplify(m_edge))

    # TH2: Delta'<0 -> z0 phuc, |z0|=|m| -> m=+-R (can Delta'<0)
    for mv in [R, -R]:
        delta_val = sp.simplify(2 * a * mv + a ** 2)
        if delta_val < 0:
            valid.add(sp.nsimplify(mv))

    # TH3: Delta'>0 -> z0 la nghiem thuc = +-R, the vao pt goc giai m
    for z0v in [R, -R]:
        eq = sp.Eq(z0v ** 2 - 2 * (mm + a) * z0v + mm ** 2, 0)
        for mv in sp.solve(eq, mm):
            if mv.is_real:
                delta_val = sp.simplify((mv + a) ** 2 - mv ** 2)
                if delta_val > 0:
                    valid.add(sp.nsimplify(mv))

    n = len(valid)
    if n < 1 or n > 5:
        raise ValueError("so nghiem khong hop le")
    opts = sorted({n, max(n - 1, 0), n + 1, n + 2})[:4]
    while len(opts) < 4:
        opts.append(opts[-1] + 1)
    de_bai = (
        f"Trên tập hợp các số phức, xét phương trình $z^2-2(m{add_term(a)})z+m^2=0$ ($m$ là tham số thực). "
        f"Có bao nhiêu giá trị của $m$ để phương trình đó có nghiệm $z_0$ thỏa mãn $|z_0|={latex(R)}$?\n\n"
        f"A. ${opts[0]}$.\nB. ${opts[1]}$.\nC. ${opts[2]}$.\nD. ${opts[3]}$."
    )
    letter = "ABCD"[opts.index(n)]
    dap_an = f"{letter}. ${n}$."
    loi_giai = (
        f"Ta có $\\Delta'=(m{add_term(a)})^2-m^2$.\n\n"
        f"TH1: $\\Delta'=0$: nghiệm kép $z_0=m{add_term(a)}$, kiểm tra điều kiện $|z_0|={latex(R)}$.\n\n"
        f"TH2: $\\Delta'<0$: $z_0$ phức, $|z_0|=|m|={latex(R)} \\Rightarrow m=\\pm{latex(R)}$, kiểm tra lại $\\Delta'<0$.\n\n"
        f"TH3: $\\Delta'>0$: $z_0=\\pm{latex(R)}$ là nghiệm thực, thế vào phương trình gốc để giải $m$, kiểm tra lại $\\Delta'>0$.\n\n"
        f"Tổng hợp cả ba trường hợp (loại nghiệm trùng nếu có), ta được {n} giá trị $m$ thỏa mãn."
    )
    return de_bai, dap_an, loi_giai


# ============================================================================
# STT61: z^2 + 4az + (b^2+2) = 0. Đếm số cặp (a;b) để z1+2i*z2 = p+qi
# ============================================================================
def mau_stt61(p, q):
    solutions = set()

    # TH1: z1, z2 thuc. z1+2i*z2=p+qi -> z1=p, z2=q/2
    z1, z2 = p, q / 2
    a1 = -(z1 + z2) / 4
    rhs_b2 = z1 * z2 - 2
    if rhs_b2 > 0:
        b_val = sp.sqrt(rhs_b2)
        solutions.add((sp.nsimplify(a1), sp.nsimplify(b_val)))
        solutions.add((sp.nsimplify(a1), sp.nsimplify(-b_val)))
    elif rhs_b2 == 0:
        solutions.add((sp.nsimplify(a1), sp.Integer(0)))

    # TH2: z1=x+yi, z2=x-yi (y != 0). x+2y=p, 2x+y=q
    x, y = sp.symbols("x y", real=True)
    sol = sp.solve([sp.Eq(x + 2 * y, p), sp.Eq(2 * x + y, q)], [x, y])
    xv, yv = sol[x], sol[y]
    if yv != 0:
        a2 = -(2 * xv) / 4
        rhs_b2_2 = xv ** 2 + yv ** 2 - 2
        if rhs_b2_2 > 0:
            b_val2 = sp.sqrt(rhs_b2_2)
            solutions.add((sp.nsimplify(a2), sp.nsimplify(b_val2)))
            solutions.add((sp.nsimplify(a2), sp.nsimplify(-b_val2)))
        elif rhs_b2_2 == 0:
            solutions.add((sp.nsimplify(a2), sp.Integer(0)))

    n = len(solutions)
    if n < 1 or n > 4:
        raise ValueError("so cap khong hop le")
    opts = sorted({n, max(n - 1, 0), n + 1, n + 2})[:4]
    while len(opts) < 4:
        opts.append(opts[-1] + 1)
    de_bai = (
        f"Trên tập hợp các số phức, xét phương trình $z^2+4az+b^2+2=0$ ($a, b$ là các tham số thực). "
        f"Có bao nhiêu cặp số thực $(a;b)$ sao cho phương trình đó có hai nghiệm $z_1, z_2$ thỏa mãn "
        f"$z_1+2iz_2={z_string_pq(p,q)}$?\n\n"
        f"A. ${opts[0]}$.\nB. ${opts[1]}$.\nC. ${opts[2]}$.\nD. ${opts[3]}$."
    )
    letter = "ABCD"[opts.index(n)]
    dap_an = f"{letter}. ${n}$."
    loi_giai = (
        f"TH1: $z_1,z_2$ là hai nghiệm thực. Từ $z_1+2iz_2={z_string_pq(p,q)}$ suy ra $z_1={latex(p)}$, "
        f"$z_2={latex(q/2)}$. Theo Vi-ét, $-4a=z_1+z_2$ và $b^2+2=z_1z_2$, giải ra $(a;b)$ nếu tồn tại.\n\n"
        f"TH2: $z_1,z_2$ là hai nghiệm phức liên hợp, đặt $z_1=x+yi$, $z_2=x-yi$. Từ "
        f"$z_1+2iz_2={z_string_pq(p,q)}$, cân bằng phần thực/ảo ta được hệ phương trình bậc nhất theo $x,y$, "
        f"giải ra $x,y$ rồi suy ra $(a;b)$ qua Vi-ét (nếu $y\\ne0$ và $b^2\\ge0$).\n\n"
        f"Tổng hợp cả hai trường hợp, ta được {n} cặp $(a;b)$ thỏa mãn."
    )
    return de_bai, dap_an, loi_giai


def z_string_pq(p, q):
    return f"{latex(p)}{add_term_i(q)}"


# ============================================================================
# Sinh toàn bộ
# ============================================================================
all_rows = []

# STT36: dung build_rows_for_question chuan (template (a,b))
all_rows.extend(build_rows_for_question(36, DANG, "mau_stt36", mau_stt36, SO_BAN_MOI_LOAI, seed_base=36))

# STT26: (c,d) tu sinh, ep dieu kien hop ly
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((26, loai_so)) % (2**31)
    rnd = random.Random(seed)
    got, tries = 0, 0
    while got < SO_BAN_MOI_LOAI and tries < 500:
        tries += 1
        if loai_so == "Số nguyên":
            c = sp.Integer(rnd.choice([x for x in range(-9, 10) if x != 0]))
            d = sp.Integer(rnd.choice([x for x in range(-9, 10) if x != 0]))
        elif loai_so == "Số hữu tỉ":
            c = sp.Rational(rnd.choice([x for x in range(-9, 10) if x != 0]), rnd.choice([2, 3]))
            d = sp.Rational(rnd.choice([x for x in range(-9, 10) if x != 0]), rnd.choice([2, 3]))
        else:
            c = rnd.choice([1, -1, 2, -2]) * sp.sqrt(rnd.choice([2, 3, 5]))
            d = rnd.choice([1, -1, 2, -2]) * sp.sqrt(rnd.choice([2, 3, 5]))
        try:
            de_bai, dap_an, loi_giai = mau_stt26(c, d)
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 26, "dang": DANG, "mau_ta": "mau_stt26",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"c": str(c), "d": str(d)},
        })
        got += 1

# STT33: a (nguyen nho), S (duong, theo loai so)
for loai_so in ["Số nguyên", "Số hữu tỉ", "Số vô tỉ"]:
    seed = hash((33, loai_so)) % (2**31)
    rnd = random.Random(seed)
    got, tries = 0, 0
    while got < SO_BAN_MOI_LOAI and tries < 500:
        tries += 1
        a = sp.Integer(rnd.choice([x for x in range(-4, 5) if x != 0]))
        if loai_so == "Số nguyên":
            S = sp.Integer(rnd.choice([2, 4, 6, 8]))
        elif loai_so == "Số hữu tỉ":
            S = sp.Rational(rnd.choice([3, 5, 7, 9]), rnd.choice([2, 3]))
        else:
            S = rnd.choice([1, 2]) * sp.sqrt(rnd.choice([2, 3, 5]))
        try:
            de_bai, dap_an, loi_giai = mau_stt33(a, S)
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 33, "dang": DANG, "mau_ta": "mau_stt33",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"a": str(a), "S": str(S)},
        })
        got += 1

# STT56: a (nguyen nho), R (duong, theo loai so)
for loai_so in ["Số nguyên", "Số hữu tỉ", "Số vô tỉ"]:
    seed = hash((56, loai_so)) % (2**31)
    rnd = random.Random(seed)
    got, tries = 0, 0
    while got < SO_BAN_MOI_LOAI and tries < 500:
        tries += 1
        a = sp.Integer(rnd.choice([x for x in range(-4, 5) if x != 0]))
        if loai_so == "Số nguyên":
            R = sp.Integer(rnd.choice([3, 4, 5, 6, 7]))
        elif loai_so == "Số hữu tỉ":
            R = sp.Rational(rnd.choice([5, 7, 9, 11]), rnd.choice([2, 3]))
        else:
            R = rnd.choice([1, 2, 3]) * sp.sqrt(rnd.choice([2, 3, 5]))
        try:
            de_bai, dap_an, loi_giai = mau_stt56(a, R)
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 56, "dang": DANG, "mau_ta": "mau_stt56",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"a": str(a), "R": str(R)},
        })
        got += 1

# STT61: (p,q) tu sinh theo loai so, gioi han nho de b^2 hop ly hon
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((61, loai_so)) % (2**31)
    pairs = gen_fn(SO_BAN_MOI_LOAI + 20, seed=seed)
    got = 0
    for p, q in pairs:
        if got >= SO_BAN_MOI_LOAI:
            break
        try:
            de_bai, dap_an, loi_giai = mau_stt61(p, q)
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 61, "dang": DANG, "mau_ta": "mau_stt61",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"p": str(p), "q": str(q)},
        })
        got += 1
    if got < SO_BAN_MOI_LOAI:
        raise RuntimeError(f"STT61 khong du mau cho loai_so={loai_so}, moi co {got}")

print("Tong so cau sinh ra (Dang 6):", len(all_rows))
with open("Sinh_them_cau_hoi/data/dang6_full.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False, indent=2)
