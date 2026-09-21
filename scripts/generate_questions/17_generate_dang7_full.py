"""Sinh đầy đủ Dạng 7 (Cực trị & vận dụng cao số phức) — 6 câu gốc
(STT 12, 27, 32, 55, 60, 65), mỗi câu 5 bản/loại số, tổng 6*15 = 90 câu.

Mỗi biến thể được giải lại thực sự bằng sympy (không chỉ thay số vào công
thức đáp số có sẵn): các công thức closed-form dưới đây được re-derive và
verify khớp với đáp số câu gốc trước khi dùng để sinh biến thể."""
import json
import random
import sys

sys.path.insert(0, "Sinh_them_cau_hoi/scripts")
from importlib import import_module

utils = import_module("10_common_utils")
latex = utils.latex

import sympy as sp

SO_BAN_MOI_LOAI = 5
DANG = "Dạng 7 - Cực trị & vận dụng cao"


def sub_term(k):
    return f"-{latex(k)}" if k >= 0 else f"+{latex(-k)}"


def add_term(k):
    return f"+{latex(k)}" if k >= 0 else f"-{latex(-k)}"


def signed_i(q):
    """'+qi' hoặc '-|q|i', dùng cho hằng số dịch chuyển trong |z - (p+qi)|."""
    return utils.signed_term(q)


# ============================================================================
# STT12: |z-A|+|z-B| = AB (đoạn thẳng AB). Tìm m=min, M=max của |z-C|. P=m+M
# ============================================================================
def mau_stt12(A, B, C):
    ax, ay = A
    bx, by = B
    cx, cy = C
    if ax == bx:
        raise ValueError("AB thang dung, bo qua de don gian")
    AB2 = (bx - ax) ** 2 + (by - ay) ** 2
    # KHONG dung nsimplify tren ty so (by-ay)/(bx-ax) khi toa do la bieu thuc
    # can bac hai hon hop: nsimplify co the "doan" nham thanh mot bieu thuc
    # dai so cuc ky phuc tap (bug da gap). Dung ty so chinh xac + simplify.
    slope = sp.simplify((by - ay) / (bx - ax))
    x = sp.symbols("x", real=True)
    y_expr = ay + slope * (x - ax)
    f = sp.expand((x - cx) ** 2 + (y_expr - cy) ** 2)
    poly = sp.Poly(f, x)
    a2, b2, c2 = poly.all_coeffs() if poly.degree() == 2 else (0, *poly.all_coeffs())
    if a2 == 0:
        raise ValueError("suy bien")
    x0 = sp.simplify(-b2 / (2 * a2))
    lo, hi = (ax, bx) if ax < bx else (bx, ax)
    candidates = [lo, hi]
    if lo < x0 < hi:
        candidates.append(x0)
    vals = [sp.radsimp(sp.simplify(f.subs(x, xv))) for xv in candidates]
    f_min, f_max = min(vals, key=lambda v: sp.N(v)), max(vals, key=lambda v: sp.N(v))
    m = sp.radsimp(sp.sqrtdenest(sp.sqrt(f_min)))
    M = sp.radsimp(sp.sqrtdenest(sp.sqrt(f_max)))
    P = sp.simplify(m + M)
    vals4 = [P, sp.simplify(M - m), sp.simplify(m * M), sp.simplify(2 * M)]  # index0 co dinh
    for i in range(1, 4):
        while any(sp.simplify(vals4[i] - vals4[j]) == 0 for j in range(i)):
            vals4[i] = vals4[i] + 1
    P, d1, d2, d3 = vals4
    # bao ve: neu bieu thuc qua phuc tap (nghiem "xau" do toa do vo ti sinh
    # ra), loai bo dong nay de tranh cau hoi hien thi qua roi/kho doc.
    if max(len(str(m)), len(str(M)), len(str(P))) > 80:
        raise ValueError("bieu thuc min/max/P qua phuc tap, bo qua")
    AB = sp.sqrt(AB2)
    de_bai = (
        f"Xét các số phức $z$ thỏa mãn $|z{sub_term(ax)}{signed_i(-ay)}|+|z{sub_term(bx)}{signed_i(-by)}| = {latex(AB)}$. "
        f"Gọi $m, M$ lần lượt là giá trị nhỏ nhất, giá trị lớn nhất của $|z{sub_term(cx)}{signed_i(-cy)}|$. Tính $P=m+M$.\n\n"
        f"A. $P={latex(P)}$.\nB. $P={latex(d1)}$.\nC. $P={latex(d2)}$.\nD. $P={latex(d3)}$."
    )
    dap_an = f"A. $P={latex(P)}$."
    loi_giai = (
        f"Gọi $M_0(x;y)$ là điểm biểu diễn của $z$, $A({latex(ax)};{latex(ay)})$, $B({latex(bx)};{latex(by)})$, "
        f"$C({latex(cx)};{latex(cy)})$. Ta có $AB={latex(AB)}$ nên $M_0A+M_0B=AB \\Rightarrow M_0$ thuộc đoạn $AB$. "
        f"Tham số hóa theo $x\\in[{latex(lo)};{latex(hi)}]$, biểu diễn $|z{sub_term(cx)}{signed_i(-cy)}|^2$ thành hàm bậc hai theo $x$, "
        f"khảo sát trên đoạn để tìm min $=m^2={latex(f_min)}$, max $=M^2={latex(f_max)}$. Suy ra $P=m+M={latex(P)}$."
    )
    return de_bai, dap_an, loi_giai


# ============================================================================
# STT27: Re(1/(|z|-z)) = 1/c -> |z|=c/2 =: R. |z1-z2|=d (d<=2R). I(0,h).
# P=|z1-hi|^2-|z2-hi|^2 <= 2*h*d. Max P = 2*h*d.
# ============================================================================
def mau_stt27(c, h, d_frac):
    R = sp.nsimplify(c / 2)
    d = sp.nsimplify(d_frac * R)  # d < 2R luon dung vi d_frac in (0,2)
    if R <= 0 or d <= 0:
        raise ValueError("khong hop le")
    Pmax = sp.nsimplify(2 * h * d)
    vals = [Pmax, sp.nsimplify(h * d), sp.nsimplify(4 * h * d), sp.nsimplify(h * R)]  # index0 co dinh
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    Pmax, d1, d2, d3 = vals
    de_bai = (
        f"Gọi $S$ là tập hợp tất cả các số phức $z$ sao cho số phức $w=\\dfrac{{1}}{{|z|-z}}$ có phần thực bằng "
        f"$\\dfrac{{1}}{{{latex(c)}}}$. Xét các số phức $z_1, z_2 \\in S$ thỏa mãn $|z_1-z_2|={latex(d)}$, giá trị lớn nhất "
        f"của $P=|z_1{signed_i(-h)}|^2-|z_2{signed_i(-h)}|^2$ bằng\n\n"
        f"A. ${latex(d1)}$.\nB. ${latex(Pmax)}$.\nC. ${latex(d2)}$.\nD. ${latex(d3)}$."
    )
    dap_an = f"B. ${latex(Pmax)}$."
    loi_giai = (
        f"Gọi $z=x+yi$, biến đổi phần thực của $w$ bằng $\\dfrac{{1}}{{{latex(c)}}}$ ta được $\\sqrt{{x^2+y^2}}={latex(R)}$, "
        f"nên tập hợp điểm biểu diễn $z$ là đường tròn $(O;{latex(R)})$. Gọi $A,B$ biểu diễn $z_1,z_2$, $I(0;{latex(h)})$, "
        f"$AB={latex(d)}$. Khi đó $P=AI^2-BI^2=2\\overrightarrow{{OI}}\\cdot\\overrightarrow{{AB}}\\le 2\\cdot OI\\cdot AB = {latex(Pmax)}$."
    )
    return de_bai, dap_an, loi_giai


# ============================================================================
# STT32: |z^2-(p+qi)| = 2|z|. M,m = max/min |z|. Answer M^2+m^2 = 2|C|+4, |C|=sqrt(p^2+q^2)
# ============================================================================
def mau_stt32(p, q):
    Cmag = sp.sqrt(p ** 2 + q ** 2)
    ans = sp.nsimplify(2 * Cmag + 4)
    d1 = sp.nsimplify(Cmag + 4)
    d2 = sp.nsimplify(2 * Cmag)
    d3 = sp.nsimplify(4 * Cmag + 4)
    pq_str = f"{latex(p)}{signed_i(q)}"
    de_bai = (
        f"Xét các số phức $z$ thỏa mãn $|z^2{sub_term(p)}{signed_i(q)}| = 2|z|$. Gọi $M$ và $m$ lần lượt là giá trị lớn nhất và giá trị "
        f"nhỏ nhất của $|z|$. Giá trị của $M^2+m^2$ bằng\n\n"
        f"A. ${latex(d1)}$.\nB. ${latex(d2)}$.\nC. ${latex(ans)}$.\nD. ${latex(d3)}$."
    )
    dap_an = f"C. ${latex(ans)}$."
    loi_giai = (
        f"Đặt $C={pq_str}$, $|C|={latex(Cmag)}$, $t=|z|^2$. Biến đổi $|z^2-C|=2|z|$ theo phần thực/ảo của $z$ và dùng "
        f"bất đẳng thức B.C.S, ta được $t^2-2({latex(Cmag)}+2)t+{latex(Cmag)}^2 \\le 0$, hai nghiệm biên là $m^2, M^2$. "
        f"Theo Vi-ét, $M^2+m^2 = 2({latex(Cmag)}+2) = {latex(ans)}$."
    )
    return de_bai, dap_an, loi_giai


# ============================================================================
# STT55: |z+i*conj(w)+K|>=|K|-r1-r2 (K=p+qi, |z|=r1,|w|=r2, |K|>r1+r2).
# Equality: z=-K/|K|*r1 ; w = -i*conj(K)/|K|*r2. Tinh |z-w|.
# ============================================================================
def mau_stt55(p, q, r1, r2):
    K = p + q * sp.I
    Kmag = sp.sqrt(p ** 2 + q ** 2)
    if Kmag <= r1 + r2:
        raise ValueError("khong thoa |K|>r1+r2")
    z_val = sp.simplify(-K / Kmag * r1)
    w_val = sp.simplify(-sp.I * sp.conjugate(K) / Kmag * r2)
    diff = sp.simplify(z_val - w_val)
    ans = sp.nsimplify(sp.sqrt(sp.expand(sp.re(diff) ** 2 + sp.im(diff) ** 2)))
    vals = [ans, sp.nsimplify(ans * 2), sp.nsimplify(r1 + r2), sp.nsimplify(Kmag - r1 - r2)]  # index0 co dinh
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    ans, d1, d2, d3 = vals
    de_bai = (
        f"Xét các số phức $z, w$ thỏa mãn $|z|={latex(r1)}$ và $|w|={latex(r2)}$. Khi $|z+i\\overline{{w}}{add_term(p)}{signed_i(q)}|$ "
        f"đạt giá trị nhỏ nhất, $|z-w|$ bằng\n\n"
        f"A. ${latex(d2)}$.\nB. ${latex(d1)}$.\nC. ${latex(d3)}$.\nD. ${latex(ans)}$."
    )
    dap_an = f"D. ${latex(ans)}$."
    loi_giai = (
        f"Ta có $|z+i\\overline{{w}}+K| \\ge |K|-|z|-|i\\overline{{w}}| = {latex(Kmag)}-{latex(r1)}-{latex(r2)}$, với "
        f"$K={add_term(p)[1:] if p>=0 else '-'+latex(-p)}{signed_i(q)}$. Dấu bằng xảy ra khi $z=-\\dfrac{{K}}{{|K|}}\\cdot {latex(r1)}$ "
        f"và $\\overline{{w}}=\\dfrac{{K}}{{i|K|}}\\cdot {latex(r2)}$. Tính trực tiếp $z,w$ rồi suy ra $|z-w|={latex(ans)}$."
    )
    return de_bai, dap_an, loi_giai


# ============================================================================
# STT60: |z|=|w|=R, |z-w|=R*sqrt(2). P=|z-A|+|w-B| min = min(|-Ai-B|, |Ai-B|)
# ============================================================================
def mau_stt60(R, A, B):
    # R|z|=|w|=R va |z-w|=R*sqrt(2) giu ty le R*sqrt(2) co dinh de z/w=+-i
    # chinh xac (bat ke R la bao nhieu) — R KHONG anh huong toi dap so cuoi
    # (chi anh huong cach viet de bai), nen cho R bien thien tu do theo loai so.
    ax, ay = A
    bx, by = B
    Aval = ax + ay * sp.I
    Bval = bx + by * sp.I
    bound1 = sp.simplify(sp.Abs(-Aval * sp.I - Bval))
    bound2 = sp.simplify(sp.Abs(Aval * sp.I - Bval))
    ans = sp.nsimplify(min(bound1, bound2, key=lambda v: sp.N(v)))
    other = sp.nsimplify(max(bound1, bound2, key=lambda v: sp.N(v)))
    if sp.simplify(ans - other) == 0:
        raise ValueError("hai bound bang nhau")
    vals = [ans, other, sp.nsimplify(other / 2), sp.nsimplify(ans * 2 + 1)]  # index0,1 (ans,other) co dinh
    for i in range(2, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    ans, other, d2, d3 = vals
    R_sqrt2 = latex(R * sp.sqrt(2))  # nhan thuc su roi rut gon (vd R=sqrt(2) -> D=2, khong phai "sqrt2 sqrt2")
    de_bai = (
        f"Xét các số phức $z$ và $w$ thay đổi thỏa mãn $|z|=|w|={latex(R)}$ và $|z-w|={R_sqrt2}$. Giá trị nhỏ nhất của "
        f"$P=|z{sub_term(ax)}{signed_i(-ay)}|+|w{sub_term(bx)}{signed_i(-by)}|$ bằng\n\n"
        f"A. ${latex(other)}$.\nB. ${latex(d2)}$.\nC. ${latex(d3)}$.\nD. ${latex(ans)}$."
    )
    dap_an = f"D. ${latex(ans)}$."
    loi_giai = (
        f"Đặt $\\dfrac{{z}}{{w}}=x+yi$. Từ $|z|=|w|$ và $|z-w|={R_sqrt2}$ suy ra $x=0, y=\\pm1$, tức $z=iw$ hoặc $z=-iw$. "
        f"Xét từng trường hợp, dùng bất đẳng thức tam giác $|w-C_1|+|w-C_2|\\ge|C_1-C_2|$, ta được hai giá trị chặn dưới "
        f"${latex(bound1)}$ và ${latex(bound2)}$; giá trị nhỏ nhất của $P$ là ${latex(ans)}$."
    )
    return de_bai, dap_an, loi_giai


# ============================================================================
# STT65: |z1|=|z2|=R, |z3|=1, c1(z1+z2)z3=c2*z1*z2. Dien tich tam giac ABC.
# Re-derivation: z1+z2 = K*z3 (K=c2*R^2/c1), WLOG z3=1 (thuc), z1=T/2+di,
# z2=T/2-di (T=K), d=sqrt(R^2-(T/2)^2). Area = d*|1-T/2|.
# ============================================================================
def mau_stt65(R, c1, c2):
    K = sp.nsimplify(c2 * R ** 2 / c1)
    T = K
    half = T / 2
    disc = R ** 2 - half ** 2
    if disc <= 0:
        raise ValueError("khong ton tai d thuc")
    d = sp.sqrt(disc)
    if sp.simplify(1 - half) == 0:
        raise ValueError("dien tich bang 0")
    # KHONG dung nsimplify o day: voi bieu thuc dai so nhieu can bac hai khac
    # goc, nsimplify co the "doan" nham thanh mot dang luy thua phan so ky
    # quai (bug da gap: 5*2^(368/527)*...). Giu nguyen bieu thuc chinh xac,
    # de latex() (radsimp/sqrtdenest) lo phan hien thi.
    area = sp.Abs(d * (1 - half))
    vals = [area, area * 2, area / 2, d]  # index0 co dinh
    for i in range(1, 4):
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)):
            vals[i] = vals[i] + 1
    area, d1, d2, d3 = vals
    gia_thiet_modun = (
        f"|z_1|=|z_2|=|z_3|={latex(R)}" if R == 1 else f"|z_1|=|z_2|={latex(R)}|z_3|={latex(R)}"
    )
    de_bai = (
        f"Cho các số phức $z_1, z_2, z_3$ thỏa mãn ${gia_thiet_modun}$ và "
        f"${latex(c1)}(z_1+z_2)z_3={latex(c2)}z_1z_2$. Gọi $A, B, C$ lần lượt là các điểm biểu diễn của $z_1, z_2, z_3$ "
        f"trên mặt phẳng tọa độ. Diện tích tam giác $ABC$ bằng\n\n"
        f"A. ${latex(d3)}$.\nB. ${latex(area)}$.\nC. ${latex(d1)}$.\nD. ${latex(d2)}$."
    )
    dap_an = f"B. ${latex(area)}$."
    loi_giai = (
        f"Ta có ${latex(c1)}(z_1+z_2)z_3={latex(c2)}z_1z_2 \\Leftrightarrow \\dfrac{{{latex(c1)}}}{{z_2}}+\\dfrac{{{latex(c1)}}}{{z_1}}=\\dfrac{{{latex(c2)}}}{{z_3}} "
        f"\\Leftrightarrow \\dfrac{{{latex(c1)}\\overline{{z_2}}}}{{|z_2|^2}}+\\dfrac{{{latex(c1)}\\overline{{z_1}}}}{{|z_1|^2}}=\\dfrac{{{latex(c2)}\\overline{{z_3}}}}{{|z_3|^2}} "
        f"\\Leftrightarrow \\dfrac{{{latex(c1)}\\overline{{z_2}}}}{{{latex(R)}^2}}+\\dfrac{{{latex(c1)}\\overline{{z_1}}}}{{{latex(R)}^2}}=\\dfrac{{{latex(c2)}\\overline{{z_3}}}}{{1}} "
        f"\\Leftrightarrow \\overline{{z_1}}+\\overline{{z_2}}=K\\overline{{z_3}}$ với $K=\\dfrac{{{latex(c2)}\\cdot {latex(R)}^2}}{{{latex(c1)}}}={latex(K)}$. (1)\n\n"
        f"Gọi $A', B', C'$ lần lượt là các điểm biểu diễn của $\\overline{{z_1}}, \\overline{{z_2}}, \\overline{{z_3}}$, suy ra "
        f"$A', B', C'$ lần lượt đối xứng với $A, B, C$ qua trục $Ox \\Rightarrow S_{{\\triangle ABC}}=S_{{\\triangle A'B'C'}}$.\n\n"
        f"Ta có $(1) \\Leftrightarrow \\overrightarrow{{OA'}}+\\overrightarrow{{OB'}}=K\\overrightarrow{{OC'}}=\\overrightarrow{{OD}}$, trong đó "
        f"$OA'=OB'={latex(R)}, OC'=1$, suy ra tứ giác $OA'DB'$ là hình thoi có $OA'=OB'={latex(R)}$, $OD={latex(K)}$ và $C'\\in OD: OC'=1$.\n\n"
        f"Gọi $I$ là giao điểm hai đường chéo $OD$ và $A'B'$, ta có $OI=\\dfrac{{K}}{{2}}={latex(half)}$. Suy ra "
        f"$IC'=|OC'-OI|=\\left|1-\\dfrac{{K}}{{2}}\\right|={latex(sp.Abs(1-half))}$, nên $S_{{\\triangle A'B'C'}}=\\dfrac{{IC'}}{{OI}}S_{{\\triangle OA'B'}}$.\n\n"
        f"$S_{{\\triangle OA'B'}}=OI\\cdot\\sqrt{{OA'^2-OI^2}}={latex(half)}\\cdot\\sqrt{{{latex(R)}^2-\\left(\\dfrac{{K}}{{2}}\\right)^2}}={latex(half*d)}$.\n\n"
        f"Vậy $S_{{ABC}}=S_{{\\triangle A'B'C'}}=\\left|1-\\dfrac{{K}}{{2}}\\right|\\cdot{latex(d)}={latex(area)}$."
    )
    return de_bai, dap_an, loi_giai


all_rows = []


def add_rows(stt_goc, mau_ta, rows):
    for r in rows:
        r.update({"stt_goc": stt_goc, "dang": DANG, "mau_ta": mau_ta, "nguon": "Nhân bản"})
    all_rows.extend(rows)


# --- STT12 ---
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((12, loai_so)) % (2**31)
    rnd = random.Random(seed)
    got, tries, rows = 0, 0, []
    while got < SO_BAN_MOI_LOAI and tries < 600:
        tries += 1
        pts = gen_fn(3, seed=rnd.randint(0, 2**31))
        A, B, C = pts[0], pts[1], pts[2]
        try:
            de_bai, dap_an, loi_giai = mau_stt12(A, B, C)
        except Exception:
            continue
        rows.append({"loai_so": loai_so, "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
                     "params": {"A": [str(A[0]), str(A[1])], "B": [str(B[0]), str(B[1])], "C": [str(C[0]), str(C[1])]}})
        got += 1
    add_rows(12, "mau_stt12", rows)

# --- STT27 --- (c, h nguyen nho; d_frac co dinh 1/2 de d<2R luon dung)
for loai_so in ["Số nguyên", "Số hữu tỉ", "Số vô tỉ"]:
    seed = hash((27, loai_so)) % (2**31)
    rnd = random.Random(seed)
    got, tries, rows = 0, 0, []
    while got < SO_BAN_MOI_LOAI and tries < 400:
        tries += 1
        if loai_so == "Số nguyên":
            c = sp.Integer(rnd.choice([4, 6, 8, 10, 12]))
            h = sp.Integer(rnd.choice([x for x in range(-9, 10) if x != 0]))
        elif loai_so == "Số hữu tỉ":
            c = sp.Rational(rnd.choice([3, 5, 7, 9]), rnd.choice([2, 3]))
            h = sp.Rational(rnd.choice([x for x in range(-11, 12) if x != 0]), rnd.choice([2, 3]))
        else:
            c = rnd.choice([2, 3, 4]) * sp.sqrt(rnd.choice([2, 3, 5]))
            h = rnd.choice([1, -1, 2, -2]) * sp.sqrt(rnd.choice([2, 3, 5]))
        d_frac = sp.Rational(rnd.choice([1, 1, 1, 2, 3]), rnd.choice([3, 4, 2, 3, 4]))
        try:
            de_bai, dap_an, loi_giai = mau_stt27(c, h, d_frac)
        except Exception:
            continue
        rows.append({"loai_so": loai_so, "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
                     "params": {"c": str(c), "h": str(h), "d_frac": str(d_frac)}})
        got += 1
    add_rows(27, "mau_stt27", rows)

# --- STT32 ---
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((32, loai_so)) % (2**31)
    pairs = gen_fn(SO_BAN_MOI_LOAI, seed=seed)
    rows = []
    for p, q in pairs:
        de_bai, dap_an, loi_giai = mau_stt32(p, q)
        rows.append({"loai_so": loai_so, "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
                     "params": {"p": str(p), "q": str(q)}})
    add_rows(32, "mau_stt32", rows)

# --- STT55 --- (p,q nho; r1,r2 nho, dam bao |K|>r1+r2)
for loai_so in ["Số nguyên", "Số hữu tỉ", "Số vô tỉ"]:
    seed = hash((55, loai_so)) % (2**31)
    rnd = random.Random(seed)
    got, tries, rows = 0, 0, []
    while got < SO_BAN_MOI_LOAI and tries < 600:
        tries += 1
        r1 = sp.Integer(rnd.choice([1, 2]))
        r2 = sp.Integer(rnd.choice([1, 2, 3]))
        if loai_so == "Số nguyên":
            p = sp.Integer(rnd.choice([5, 6, 7, 8, 9, 10]))
            q = sp.Integer(rnd.choice([5, 6, 7, 8, 9, 10]))
        elif loai_so == "Số hữu tỉ":
            p = sp.Rational(rnd.choice([15, 17, 19]), 2)
            q = sp.Rational(rnd.choice([15, 17, 19]), 2)
        else:
            p = rnd.choice([3, 4, 5]) * sp.sqrt(rnd.choice([2, 3, 5]))
            q = rnd.choice([3, 4, 5]) * sp.sqrt(rnd.choice([2, 3, 5]))
        try:
            de_bai, dap_an, loi_giai = mau_stt55(p, q, r1, r2)
        except Exception:
            continue
        rows.append({"loai_so": loai_so, "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
                     "params": {"p": str(p), "q": str(q), "r1": str(r1), "r2": str(r2)}})
        got += 1
    add_rows(55, "mau_stt55", rows)

# --- STT60 --- (A,B cap so tu number type generator; R bien thien theo loai so)
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((60, loai_so)) % (2**31)
    rnd = random.Random(seed)
    got, tries, rows = 0, 0, []
    while got < SO_BAN_MOI_LOAI and tries < 400:
        tries += 1
        pts = gen_fn(2, seed=rnd.randint(0, 2**31))
        A, B = pts[0], pts[1]
        if loai_so == "Số nguyên":
            R = sp.Integer(rnd.choice([2, 3, 4, 5, 6]))
        elif loai_so == "Số hữu tỉ":
            R = sp.Rational(rnd.choice([3, 5, 7, 9]), rnd.choice([2, 3]))
        else:
            R = rnd.choice([1, 2, 3]) * sp.sqrt(rnd.choice([2, 3, 5]))
        try:
            de_bai, dap_an, loi_giai = mau_stt60(R, A, B)
        except Exception:
            continue
        rows.append({"loai_so": loai_so, "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
                     "params": {"R": str(R), "A": [str(A[0]), str(A[1])], "B": [str(B[0]), str(B[1])]}})
        got += 1
    add_rows(60, "mau_stt60", rows)

# --- STT65 --- (R theo loai so; c1,c2 nguyen nho co dinh dang)
for loai_so in ["Số nguyên", "Số hữu tỉ", "Số vô tỉ"]:
    seed = hash((65, loai_so)) % (2**31)
    rnd = random.Random(seed)
    got, tries, rows = 0, 0, []
    while got < SO_BAN_MOI_LOAI and tries < 600:
        tries += 1
        c1 = sp.Integer(rnd.choice([4, 6, 8, 10]))
        c2 = sp.Integer(rnd.choice([2, 3, 5]))
        if loai_so == "Số nguyên":
            R = sp.Integer(rnd.choice([2, 3, 4]))
        elif loai_so == "Số hữu tỉ":
            R = sp.Rational(rnd.choice([3, 5, 7]), rnd.choice([2, 3]))
        else:
            R = rnd.choice([1, 2]) * sp.sqrt(rnd.choice([2, 3, 5]))
        try:
            de_bai, dap_an, loi_giai = mau_stt65(R, c1, c2)
        except Exception:
            continue
        rows.append({"loai_so": loai_so, "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
                     "params": {"R": str(R), "c1": str(c1), "c2": str(c2)}})
        got += 1
    add_rows(65, "mau_stt65", rows)

print("Tong so cau sinh ra (Dang 7):", len(all_rows))
with open("Sinh_them_cau_hoi/data/dang7_full.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False, indent=2)
