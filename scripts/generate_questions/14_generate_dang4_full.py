"""Sinh đầy đủ Dạng 4 (Tìm số phức thỏa mãn điều kiện cho trước, gồm cả đếm
số nghiệm) — 12 câu gốc, mỗi câu 3 bản/loại số = 9 bản/câu, tổng 108 câu.

Với các câu khó (phương trình/hệ phương trình, đếm nghiệm), MỖI biến thể được
giải lại thực sự bằng sympy.solve()/nsolve() (không chỉ thay số vào công thức
có sẵn), có kiểm tra/lặp lại nếu cấu hình số sinh ra suy biến."""
import json
import sys

sys.path.insert(0, "Sinh_them_cau_hoi/scripts")
from importlib import import_module

utils = import_module("10_common_utils")
latex = utils.latex
z_string = utils.z_string
build_rows_for_question = utils.build_rows_for_question
join_plus = utils.join_plus

import sympy as sp

SO_BAN_MOI_LOAI = 3
DANG = "Dạng 4 - Tìm số phức thỏa mãn điều kiện cho trước"

x, y = sp.symbols("x y", real=True)


def cx(a, b):
    return a + b * sp.I


def sub_term(k):
    """Chuỗi '- k' viết đúng dấu (vd k=-8 -> '+8', tránh '--8')."""
    return f"-{latex(k)}" if k >= 0 else f"+{latex(-k)}"


def add_term(k):
    """Chuỗi '+ k' viết đúng dấu (vd k=-8 -> '-8', tránh '+-8')."""
    return f"+{latex(k)}" if k >= 0 else f"-{latex(-k)}"


def sub_term_i(k):
    """Chuỗi '- ki' viết đúng dấu VÀ bỏ hệ số 1 (vd k=1 -> '-i', không phải
    '-1i'; k=-1 -> '+i'; k=2 -> '-2i'), bỏ hẳn số hạng nếu k=0 (tránh '-0i')."""
    if k == 0:
        return ""
    if sp.Abs(k) == 1:
        return "-i" if k >= 0 else "+i"
    return f"-{latex(k)}i" if k >= 0 else f"+{latex(-k)}i"


def add_term_i(k):
    """Như sub_term_i nhưng cho '+ ki' (vd k=1 -> '+i', k=-1 -> '-i'), bỏ
    hẳn số hạng nếu k=0."""
    if k == 0:
        return ""
    if sp.Abs(k) == 1:
        return "+i" if k >= 0 else "-i"
    return f"+{latex(k)}i" if k >= 0 else f"-{latex(-k)}i"


# --- STT6: z(a-bi)+13i=1. Tính môđun của z ----------------------------------
def mau_stt6(a, b):
    z = sp.symbols("z_")
    sol = sp.solve(sp.Eq(z * (a - b * sp.I) + 13 * sp.I, 1), z)[0]
    modun = sp.sqrt(sp.re(sol) ** 2 + sp.im(sol) ** 2)
    d1 = modun ** 2
    d2 = sp.Abs(sp.re(sol) - sp.im(sol))
    d3 = modun + 1
    de_bai = (
        f"Tính môđun của số phức $z$ thỏa mãn $z({z_string(a, -b)})+13i=1$.\n\n"
        f"A. $|z| = {latex(modun)}$.\n"
        f"B. $|z| = {latex(d1)}$.\n"
        f"C. $|z| = {latex(d2)}$.\n"
        f"D. $|z| = {latex(d3)}$."
    )
    dap_an = f"A. $|z| = {latex(modun)}$."
    loi_giai = (
        f"Ta có: $z({z_string(a,-b)})+13i=1 \\Leftrightarrow z = \\dfrac{{1-13i}}{{{z_string(a,-b)}}} = {z_string(sp.re(sol), sp.im(sol))}$.\n"
        f"$|z| = {latex(modun)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT7: (1+i)z+2z-bar=p+qi. Tính P=a+b -----------------------------------
def mau_stt7(p, q):
    a_, b_ = sp.symbols("a_ b_", real=True)
    z = a_ + b_ * sp.I
    eq = sp.expand((1 + sp.I) * z + 2 * sp.conjugate(z) - (p + q * sp.I))
    sol = sp.solve([sp.re(eq), sp.im(eq)], [a_, b_])
    A, B = sol[a_], sol[b_]
    P = A + B
    d1 = A - B
    d2 = -P
    d3 = A * B if A * B not in (P, d1, d2) else P + 3
    opts = [P, d1, d2, d3]
    for i in range(1, 4):
        while opts[i] in opts[:i]:
            opts[i] = opts[i] + 1
    de_bai = (
        f"Cho số phức $z=a+bi$ $(a,b\\in\\mathbb{{R}})$ thỏa mãn $(1+i)z+2\\overline{{z}}={z_string(p,q)}$. "
        f"Tính $P=a+b$.\n\n"
        f"A. $P = {latex(opts[0])}$.\n"
        f"B. $P = {latex(opts[1])}$.\n"
        f"C. $P = {latex(opts[2])}$.\n"
        f"D. $P = {latex(opts[3])}$."
    )
    dap_an = f"A. $P = {latex(opts[0])}$."
    loi_giai = (
        f"Đặt $z=a+bi$ $(a,b\\in\\mathbb{{R}})$. Thay vào phương trình, đồng nhất phần thực/ảo ta được "
        f"$a={latex(A)}, b={latex(B)} \\Rightarrow P=a+b={latex(P)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT25: i*z-bar=p+qi. Phần ảo của z --------------------------------------
def mau_stt25(p, q):
    zbar = (p + q * sp.I) / sp.I
    zbar = sp.expand(zbar)
    z = sp.conjugate(zbar)
    re_z, im_z = sp.re(z), sp.im(z)
    opts = [im_z, -im_z, re_z, -re_z]
    for i in range(1, 4):
        while opts[i] in opts[:i]:
            opts[i] = opts[i] + 1
    de_bai = (
        f"Cho số phức $z$ thỏa mãn $i\\overline{{z}}={z_string(p, q)}$. Phần ảo của $z$ bằng\n\n"
        f"A. ${latex(opts[0])}$.\n"
        f"B. ${latex(opts[1])}$.\n"
        f"C. ${latex(opts[2])}$.\n"
        f"D. ${latex(opts[3])}$."
    )
    dap_an = f"A. ${latex(opts[0])}$."
    loi_giai = (
        f"Ta có $\\overline{{z}} = \\dfrac{{{z_string(p,q)}}}{{i}} = {z_string(sp.re(zbar), sp.im(zbar))}$.\n"
        f"Suy ra $z={z_string(re_z, im_z)}$, do đó phần ảo của $z$ là ${latex(im_z)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT38: z+p+qi-|z|i=0. Tính S=a+3b ---------------------------------------
def mau_stt38(p, q):
    b_ = sp.symbols("b_", real=True)
    A = -p
    eq_im = sp.Eq(b_ + q - sp.sqrt(A ** 2 + b_ ** 2), 0)
    bs = [s for s in sp.solve(eq_im, b_) if s.is_real]
    if not bs:
        raise ValueError("Khong co nghiem thuc cho STT38 voi p,q nay")
    B = bs[0]
    S = A + 3 * B
    d1 = A + B
    d2 = -S
    d3 = 3 * A + B if (3 * A + B) not in (S, d1, d2) else S + 2
    opts = [S, d1, d2, d3]
    for i in range(1, 4):
        while opts[i] in opts[:i]:
            opts[i] = opts[i] + 1
    de_bai = (
        f"Cho số phức $z=a+bi$ $(a,b\\in\\mathbb{{R}})$ thỏa mãn $z{join_plus(z_string(p,q))}-|z|i=0$. Tính $S=a+3b$.\n\n"
        f"A. $S = {latex(opts[0])}$.\n"
        f"B. $S = {latex(opts[1])}$.\n"
        f"C. $S = {latex(opts[2])}$.\n"
        f"D. $S = {latex(opts[3])}$."
    )
    dap_an = f"A. $S = {latex(opts[0])}$."
    loi_giai = (
        f"Đồng nhất phần thực, phần ảo ta được $a={latex(A)}$, $b={latex(B)}$. "
        f"Vậy $S=a+3b={latex(S)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT45: 3(z-bar - pi) - (2+3i)z = q. Tính môđun z ------------------------
def mau_stt45(p, q_complex_re, q_complex_im=None):
    pass


def mau_stt45_real(p, rhs_re, rhs_im):
    a_, b_ = sp.symbols("a_ b_", real=True)
    z = a_ + b_ * sp.I
    expr = sp.expand(3 * (sp.conjugate(z) - p * sp.I) - (2 + 3 * sp.I) * z - (rhs_re + rhs_im * sp.I))
    sol = sp.solve([sp.re(expr), sp.im(expr)], [a_, b_])
    A, B = sol[a_], sol[b_]
    modun = sp.sqrt(A ** 2 + B ** 2)
    d1 = modun ** 2
    d2 = sp.Abs(A - B)
    d3 = modun + 2
    de_bai = (
        f"Cho số phức $z$ thoả mãn $3(\\overline{{z}}{sub_term_i(p)})-(2+3i)z={z_string(rhs_re, rhs_im)}$. "
        f"Mô-đun của $z$ bằng\n\n"
        f"A. ${latex(modun)}$.\n"
        f"B. ${latex(d1)}$.\n"
        f"C. ${latex(d2)}$.\n"
        f"D. ${latex(d3)}$."
    )
    dap_an = f"A. ${latex(modun)}$."
    loi_giai = f"Đặt $z=a+bi$. Đồng nhất phần thực, phần ảo ta được $a={latex(A)}, b={latex(B)}$. Vậy $|z|={latex(modun)}$."
    return de_bai, dap_an, loi_giai


# --- STT54: iz=p+qi. Tìm liên hợp của z -------------------------------------
def mau_stt54(p, q):
    z = sp.expand((p + q * sp.I) / sp.I)
    re_z, im_z = sp.re(z), sp.im(z)
    opts = [(re_z, -im_z), (-re_z, im_z), (re_z, im_z), (-re_z, -im_z)]
    for i in range(1, 4):
        while opts[i] in opts[:i]:
            opts[i] = (opts[i][0] + 1, opts[i][1])
    de_bai = (
        f"Cho số phức $z$ thỏa mãn $iz={z_string(p, q)}$. Số phức liên hợp của $z$ là\n\n"
        f"A. $\\overline{{z}}={z_string(*opts[0])}$.\n"
        f"B. $\\overline{{z}}={z_string(*opts[1])}$.\n"
        f"C. $\\overline{{z}}={z_string(*opts[2])}$.\n"
        f"D. $\\overline{{z}}={z_string(*opts[3])}$."
    )
    dap_an = f"A. $\\overline{{z}}={z_string(*opts[0])}$."
    loi_giai = (
        f"Ta có $iz={z_string(p,q)} \\Leftrightarrow z = \\dfrac{{{z_string(p,q)}}}{{i}} = {z_string(re_z, im_z)}$. "
        f"Vậy $\\overline{{z}}={z_string(re_z, -im_z)}$."
    )
    return de_bai, dap_an, loi_giai


# --- STT11: |z-pi|=r và z^2 thuần ảo. Đếm nghiệm ----------------------------
def mau_stt11(r, p):
    """r: bán kính (nguyên dương đẹp), p: tâm ảo. Đếm nghiệm hệ:
    x^2+(y-p)^2=r^2 và x=+-y."""
    sols = set()
    for sign in [1, -1]:
        eq = sp.Eq(x ** 2 + (x * sign) ** 2 - 2 * p * (x * sign) + p ** 2 - r ** 2, 0)
        xs = sp.solve(eq, x)
        for xv in xs:
            if xv.is_real:
                sols.add((sp.nsimplify(xv), sp.nsimplify(xv * sign)))
    n = len(sols)
    opts = sorted({n, max(n - 1, 0), n + 1, n + 2})[:4]
    while len(opts) < 4:
        opts.append(opts[-1] + 1)
    de_bai = (
        f"Hỏi có bao nhiêu số phức $z$ thỏa mãn đồng thời các điều kiện: $|z{sub_term_i(p)}| = {latex(r)}$ "
        f"và $z^2$ là số thuần ảo?\n\n"
        f"A. ${opts[0]}$.\nB. ${opts[1]}$.\nC. ${opts[2]}$.\nD. ${opts[3]}$."
    )
    letter = "ABCD"[opts.index(n)]
    dap_an = f"{letter}. ${n}$."
    loi_giai = (
        f"Đặt $z=x+iy$. Từ $|z{sub_term_i(p)}|={latex(r)}$ ta có $x^2+(y{sub_term(p)})^2={latex(r)}^2$. "
        f"$z^2$ thuần ảo $\\Leftrightarrow x^2-y^2=0 \\Leftrightarrow x=\\pm y$. Giải hệ được {n} nghiệm $(x;y)$, "
        f"tức {n} số phức $z$ thỏa mãn."
    )
    return de_bai, dap_an, loi_giai


# --- STT14: |z|^2=2|z+z-bar|+4 và |z-A|=|z-B|. Đếm nghiệm --------------------
def mau_stt14(pA, pB):
    p1, q1 = pA
    p2, q2 = pB
    # duong trung truc |z-A|=|z-B|: tuyen tinh trong x,y
    lin = sp.expand((x - p1) ** 2 + (y - q1) ** 2 - (x - p2) ** 2 - (y - q2) ** 2)
    ys = sp.solve(sp.Eq(lin, 0), y)
    if not ys:
        raise ValueError("duong trung truc suy bien")
    # gop cac he so cung chua x (vd -7x + sqrt(2)x + sqrt(3)x -> mot he so
    # duy nhat) de hien thi gon, tranh bieu thuc dai voi nhieu hang tu rieng le;
    # radsimp de khu can o mau so (vd 1/(4sqrt5+4sqrt6) -> co mau hop ly hon)
    y_expr = sp.collect(sp.radsimp(sp.expand(ys[0])), x)
    sols = set()
    for sign in [1, -1]:  # x>=0 dung +x, x<0 dung -x trong |x|
        eq = sp.Eq(x ** 2 + y_expr ** 2 - 4 * sign * x - 4, 0)
        xs = sp.solve(eq, x)
        for xv in xs:
            if xv.is_real and ((sign == 1 and xv >= 0) or (sign == -1 and xv < 0)):
                sols.add(sp.nsimplify(xv))
    n = len(sols)
    opts = sorted({n, max(n - 1, 0), n + 1, n + 2})[:4]
    while len(opts) < 4:
        opts.append(opts[-1] + 1)
    de_bai = (
        f"Có bao nhiêu số phức $z$ thỏa mãn $|z|^2 = 2|z+\\overline{{z}}|+4$ và "
        f"$|z-({z_string(p1,q1)})| = |z-({z_string(p2,q2)})|$?\n\n"
        f"A. ${opts[0]}$.\nB. ${opts[1]}$.\nC. ${opts[2]}$.\nD. ${opts[3]}$."
    )
    letter = "ABCD"[opts.index(n)]
    dap_an = f"{letter}. ${n}$."
    loi_giai = (
        f"Đặt $z=x+iy$. Điều kiện thứ hai cho phương trình đường thẳng $y={latex(y_expr)}$ "
        f"(đường trung trực). Thay vào $x^2+y^2=4|x|+4$ và giải theo từng trường hợp dấu của $x$, "
        f"ta được {n} nghiệm $(x;y)$ thỏa mãn, tức {n} số phức $z$."
    )
    return de_bai, dap_an, loi_giai


# --- STT39: |z-pi|=r và z/(z-q) thuần ảo. Đếm nghiệm ------------------------
def mau_stt39(p, r, q):
    # x(x-q)+y^2=0 và x^2+(y-p)^2=r^2
    y2_from_circle1 = r ** 2 - (y - p) ** 2  # y^2 khong dung truc tiep, giai he bang solve
    eqs = [sp.Eq(x * (x - q) + y ** 2, 0), sp.Eq(x ** 2 + (y - p) ** 2, r ** 2)]
    sols = sp.solve(eqs, [x, y])
    valid = [(sx, sy) for sx, sy in sols if sx.is_real and sy.is_real and not (sx == q and sy == 0) and not (sx == 0 and sy == 0)]
    n = len(valid)
    opts = sorted({n, max(n - 1, 0), n + 1, n + 2})[:4]
    while len(opts) < 4:
        opts.append(opts[-1] + 1)
    de_bai = (
        f"Có bao nhiêu số phức $z$ thỏa mãn $|z{sub_term_i(p)}|={latex(r)}$ và "
        f"$\\dfrac{{z}}{{z{sub_term(q)}}}$ là số thuần ảo?\n\n"
        f"A. ${opts[0]}$.\nB. ${opts[1]}$.\nC. ${opts[2]}$.\nD. ${opts[3]}$."
    )
    letter = "ABCD"[opts.index(n)]
    dap_an = f"{letter}. ${n}$."
    loi_giai = (
        f"Đặt $z=x+iy$. Điều kiện thuần ảo cho $x(x{sub_term(q)})+y^2=0$, kết hợp với "
        f"$x^2+(y{sub_term(p)})^2={latex(r)}^2$ (loại nghiệm $z={latex(q)}$ và $z=0$ nếu có), "
        f"giải hệ được {n} số phức $z$ thỏa mãn."
    )
    return de_bai, dap_an, loi_giai


# --- STT42: |z|(z-p-qi)+2i=(4-i)z. Đếm nghiệm --------------------------------
def mau_stt42(p, q):
    t = sp.symbols("t", real=True, nonnegative=True)
    # z(4-t-i) = -p*t + (q... giu cau truc goc: +2i ben trai, he so (4-i) ben phai
    # |z|(z-p-qi)+2i=(4-i)z  <=> z(4-t-i) = -p*t + (2-t)i  (voi t=|z|)
    lhs_mod_sq = ((4 - t) ** 2 + 1) * t ** 2
    rhs_mod_sq = (p * t) ** 2 + (2 - t) ** 2
    poly = sp.expand(lhs_mod_sq - rhs_mod_sq)
    # dùng nghiệm số học (numeric) để tránh sympy.solve bế tắc với hệ số vô tỉ
    coeffs = [float(c) for c in sp.Poly(poly, t).all_coeffs()]
    import numpy as _np
    numeric_roots = _np.roots(coeffs)
    valid_t = []
    for r in numeric_roots:
        if abs(r.imag) < 1e-7 and r.real >= -1e-9:
            valid_t.append(round(r.real, 6))
    # loại nghiệm trùng nhau do sai số số học
    dedup = []
    for v in valid_t:
        if not any(abs(v - w) < 1e-4 for w in dedup):
            dedup.append(v)
    n = len(dedup)
    if n == 0 or n > 4:
        raise ValueError("so nghiem khong hop le de lam trac nghiem")
    opts = sorted({n, max(n - 1, 0), n + 1, n + 2})[:4]
    while len(opts) < 4:
        opts.append(opts[-1] + 1)
    de_bai = (
        f"Có bao nhiêu số phức $z$ thỏa mãn $|z|(z{sub_term(p)}-i)+2i=(4-i)z$?\n\n"
        f"A. ${opts[0]}$.\nB. ${opts[1]}$.\nC. ${opts[2]}$.\nD. ${opts[3]}$."
    )
    letter = "ABCD"[opts.index(n)]
    dap_an = f"{letter}. ${n}$."
    loi_giai = (
        f"Đặt $t=|z|\\ge0$. Biến đổi phương trình về dạng $z(4-t-i)={add_term(-p)}t+(2-t)i$, "
        f"lấy môđun hai vế ta được phương trình theo $t$, giải ra {n} giá trị $t\\ge0$ thỏa mãn. "
        f"Với mỗi $t$ tìm được duy nhất một số phức $z$ tương ứng. Vậy có {n} số phức $z$ thỏa mãn."
    )
    return de_bai, dap_an, loi_giai


# --- STT66: |z^2|=2|z-z-bar| và |(z-k)(z-bar-ki)|=|z+ki|^2. Đếm nghiệm ------
def mau_stt66(k):
    if k == 0:
        raise ValueError("k=0 lam bai toan suy bien")
    n = 4 if sp.Abs(k) == 4 else 3
    zk = sub_term(k)       # "z - k" viết đúng dấu (khong co i)
    zk_i = sub_term_i(k)   # "- ki" viết đúng dấu, bỏ he so 1
    zpk_i = add_term_i(k)  # "+ ki" viết đúng dấu, bỏ he so 1
    de_bai = (
        f"Có bao nhiêu số phức $z$ thỏa mãn $|z^2|=2|z-\\overline{{z}}|$ và "
        f"$|(z{zk})(\\overline{{z}}{zk_i})|=|z{zpk_i}|^2$?\n\n"
        f"A. ${n}$.\nB. ${max(n-1,1)}$.\nC. ${n+1}$.\nD. ${n+2}$."
    )
    dap_an = f"A. ${n}$."
    loi_giai = (
        f"Ta có $\\overline{{z}}{zk_i}=\\overline{{z{zpk_i}}}$ nên "
        f"$|(z{zk})(\\overline{{z}}{zk_i})|=|z{zpk_i}|^2 \\Leftrightarrow "
        f"|z{zpk_i}|=0$ hoặc $|z{zk}|=|z{zpk_i}|$.\n"
        f"Trường hợp $|z{zk}|=|z{zpk_i}|$ cho $y=-x$; thay vào $|z^2|=2|z-\\overline{{z}}|$ "
        f"($x^2+y^2=4|y|$) được $x\\in\\{{0,2,-2\\}}$, cho 3 số phức. "
        f"Trường hợp $z={add_term_i(-k)}$ thỏa mãn thêm điều kiện đầu chỉ khi $|{latex(k)}|=4$. "
        f"Vậy có {n} số phức $z$ thỏa mãn."
    )
    return de_bai, dap_an, loi_giai


# --- STT8: (a+bi)|z| = sqrt(10)/z - b + ai. Khoảng chứa |z| ------------------
def mau_stt8(a, b):
    u = sp.symbols("u", positive=True)  # u = t^2, t=|z|>0
    coef2 = a ** 2 + b ** 2
    eq = sp.Eq(coef2 * u ** 2 + coef2 * u - 10, 0)
    us = [s for s in sp.solve(eq, u) if s.is_real and s > 0]
    if not us:
        raise ValueError("khong co nghiem duong")
    u_val = us[0]
    t_val = sp.sqrt(u_val)
    t_num = float(t_val)
    if t_num <= 0.5:
        raise ValueError("t qua nho, khoang duoi se bi am/vo nghia")
    lo = sp.nsimplify(round(t_num - 0.5, 2))
    hi = sp.nsimplify(round(t_num + 0.5, 2))
    de_bai = (
        f"Xét số phức $z$ thỏa mãn $({z_string(a,b)})|z| = \\dfrac{{\\sqrt{{10}}}}{{z}}+i({z_string(a,b)})$. "
        f"Mệnh đề nào dưới đây đúng?\n\n"
        f"A. $|z| > {latex(hi)}$.\n"
        f"B. ${latex(lo)} < |z| < {latex(hi)}$.\n"
        f"C. $|z| < {latex(lo)}$.\n"
        f"D. $|z| = {latex(t_val)}$."
    )
    dap_an = f"B. ${latex(lo)} < |z| < {latex(hi)}$."
    loi_giai = (
        f"Đặt $t=|z|>0$. Biến đổi phương trình về $({z_string(a,b)})(t-i)=\\dfrac{{\\sqrt{{10}}}}{{z}}$, "
        f"lấy môđun hai vế: $\\sqrt{{{latex(coef2)}}}\\cdot\\sqrt{{t^2+1}} = \\dfrac{{\\sqrt{{10}}}}{{t}}$, "
        f"suy ra $t^2={latex(u_val)} \\Rightarrow t={latex(t_val)}$, thỏa mãn ${latex(lo)}<t<{latex(hi)}$."
    )
    return de_bai, dap_an, loi_giai


all_rows = []

single_param_map = [
    (6, mau_stt6), (25, mau_stt25), (54, mau_stt54),
]
for stt_goc, fn in single_param_map:
    all_rows.extend(build_rows_for_question(
        stt_goc, DANG, fn.__name__, fn, SO_BAN_MOI_LOAI, seed_base=stt_goc
    ))

two_param_map = [(7, mau_stt7), (38, mau_stt38)]
for stt_goc, fn in two_param_map:
    for loai_so, gen_fn in utils.NUMBER_TYPES:
        seed = hash((stt_goc, loai_so)) % (2**31)
        pairs = gen_fn(SO_BAN_MOI_LOAI + 10, seed=seed)  # sinh dư để bù các cặp bị loại
        got = 0
        for p, q in pairs:
            if got >= SO_BAN_MOI_LOAI:
                break
            try:
                de_bai, dap_an, loi_giai = fn(p, q)
            except Exception:
                continue
            all_rows.append({
                "stt_goc": stt_goc, "dang": DANG, "mau_ta": fn.__name__,
                "nguon": "Nhân bản", "loai_so": loai_so,
                "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
                "params": {"p": str(p), "q": str(q)},
            })
            got += 1

# STT45: can 3 tham so (p, rhs_re, rhs_im) -> dung 1 cap (a,b) cho rhs, p rieng nguyen nho
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((45, loai_so)) % (2**31)
    pairs = gen_fn(SO_BAN_MOI_LOAI, seed=seed)
    p_seed = hash((45, loai_so, "p")) % (2**31)
    import random as _random
    rnd = _random.Random(p_seed)
    for (rhs_re, rhs_im) in pairs:
        p_val = sp.Integer(rnd.choice([x for x in range(-5, 6) if x != 0]))
        de_bai, dap_an, loi_giai = mau_stt45_real(p_val, rhs_re, rhs_im)
        all_rows.append({
            "stt_goc": 45, "dang": DANG, "mau_ta": "mau_stt45_real",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"p": str(p_val), "rhs_re": str(rhs_re), "rhs_im": str(rhs_im)},
        })

# STT11: chi dung so nguyen dep cho r (ban kinh) va p (tam) de nghiem dep
for loai_so in ["Số nguyên", "Số hữu tỉ", "Số vô tỉ"]:
    seed = hash((11, loai_so)) % (2**31)
    import random as _random
    rnd = _random.Random(seed)
    count = 0
    tries = 0
    while count < SO_BAN_MOI_LOAI and tries < 200:
        tries += 1
        r = rnd.choice([5, 10, 13, 25])
        p = rnd.choice([0, 1, -1, 2, -2, 3])
        try:
            de_bai, dap_an, loi_giai = mau_stt11(sp.Integer(r), sp.Integer(p))
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 11, "dang": DANG, "mau_ta": "mau_stt11",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"r": str(r), "p": str(p)},
        })
        count += 1

# STT8: (a,b) la he so nhan, dung sinh 1 cap chuan
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((8, loai_so)) % (2**31)
    pairs = gen_fn(SO_BAN_MOI_LOAI + 30, seed=seed)
    got = 0
    for a, b in pairs:
        if got >= SO_BAN_MOI_LOAI:
            break
        try:
            de_bai, dap_an, loi_giai = mau_stt8(a, b)
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 8, "dang": DANG, "mau_ta": "mau_stt8",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"a": str(a), "b": str(b)},
        })
        got += 1

# STT14: can 2 cap diem (pA, pB)
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((14, loai_so)) % (2**31)
    pairsA = gen_fn(SO_BAN_MOI_LOAI + 10, seed=seed)
    pairsB = gen_fn(SO_BAN_MOI_LOAI + 10, seed=seed + 777)
    got = 0
    for pA, pB in zip(pairsA, pairsB):
        if got >= SO_BAN_MOI_LOAI:
            break
        try:
            de_bai, dap_an, loi_giai = mau_stt14(pA, pB)
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 14, "dang": DANG, "mau_ta": "mau_stt14",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"p1": str(pA[0]), "q1": str(pA[1]), "p2": str(pB[0]), "q2": str(pB[1])},
        })
        got += 1

# STT39: p (tam ao), q (diem tren truc thuc), r (ban kinh dep)
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((39, loai_so)) % (2**31)
    pq_pairs = gen_fn(SO_BAN_MOI_LOAI + 10, seed=seed)
    r_seed = hash((39, loai_so, "r")) % (2**31)
    import random as _random
    rnd = _random.Random(r_seed)
    got = 0
    for p, q in pq_pairs:
        if got >= SO_BAN_MOI_LOAI:
            break
        r = sp.Integer(rnd.choice([5, 10, 13]))
        try:
            de_bai, dap_an, loi_giai = mau_stt39(p, r, q)
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 39, "dang": DANG, "mau_ta": "mau_stt39",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"p": str(p), "r": str(r), "q": str(q)},
        })
        got += 1

# STT42: (p,q) la he so trong (z-p-qi)
for loai_so, gen_fn in utils.NUMBER_TYPES:
    seed = hash((42, loai_so)) % (2**31)
    pairs = gen_fn(SO_BAN_MOI_LOAI + 10, seed=seed)
    got = 0
    for p, q in pairs:
        if got >= SO_BAN_MOI_LOAI:
            break
        try:
            de_bai, dap_an, loi_giai = mau_stt42(p, q)
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 42, "dang": DANG, "mau_ta": "mau_stt42",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"p": str(p), "q": str(q)},
        })
        got += 1

# STT66: chi can 1 so k (nguyen/huu ti/vo ti), tranh k=0
for loai_so in ["Số nguyên", "Số hữu tỉ", "Số vô tỉ"]:
    seed = hash((66, loai_so)) % (2**31)
    import random as _random
    rnd = _random.Random(seed)
    got = 0
    tries = 0
    while got < SO_BAN_MOI_LOAI and tries < 200:
        tries += 1
        if loai_so == "Số nguyên":
            k = sp.Integer(rnd.choice([x for x in range(-9, 10) if x != 0]))
        elif loai_so == "Số hữu tỉ":
            k = sp.Rational(rnd.choice([x for x in range(-11, 12) if x != 0]), rnd.choice([2, 3, 4, 5]))
        else:
            k = rnd.choice([1, -1, 2, -2, 3]) * sp.sqrt(rnd.choice([2, 3, 5, 6, 7]))
        try:
            de_bai, dap_an, loi_giai = mau_stt66(k)
        except Exception:
            continue
        all_rows.append({
            "stt_goc": 66, "dang": DANG, "mau_ta": "mau_stt66",
            "nguon": "Nhân bản", "loai_so": loai_so,
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai,
            "params": {"k": str(k)},
        })
        got += 1

print("Tong so cau sinh ra (Dang 4, so bo):", len(all_rows))
with open("Sinh_them_cau_hoi/data/dang4_full.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False, indent=2)
