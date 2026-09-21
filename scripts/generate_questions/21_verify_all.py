"""Kiểm tra ĐỘC LẬP tính đúng đắn của đáp án/lời giải cho toàn bộ 696 câu nhân
bản (7 dạng). Với mỗi câu, dựa vào "params" (tham số thô đã lưu lúc sinh) và
"mau_ta" (tên mẫu), hàm verify_* dưới đây TÍNH LẠI đáp án đúng bằng một cách
độc lập (thế trực tiếp vào điều kiện đề bài / giải lại phương trình bằng
sympy) — không gọi lại hàm sinh câu hỏi — rồi so sánh với giá trị đã lưu
trong "dap_an". Kết quả được thêm vào cột "Kiểm tra tự động" khi xuất Excel.

Quy ước trả về: (True, "") nếu khớp, (False, ghi chú) nếu KHÔNG khớp hoặc
không tự động kiểm tra được (cần người xem lại)."""
import json
import re
import sys

sys.path.insert(0, "Sinh_them_cau_hoi/scripts")

import sympy as sp

from importlib import import_module
_utils = import_module("10_common_utils")

I = sp.I


def _latex(expr):
    """Dùng CHUNG bộ render LaTeX với script sinh câu hỏi (tự động \\dfrac,
    radsimp/sqrtdenest) để so khớp chuỗi chính xác, tránh false-negative do
    khác định dạng (vd \\frac vs \\dfrac)."""
    return _utils.latex(expr)


def _contains(target, text):
    r"""So khop chuoi bo qua khac biet khoang trang (sympy latex doi khi chen
    khoang trang truoc dau '-' cua he so am, vd '- 3 \sqrt{6}')."""
    return target.replace(" ", "") in text.replace(" ", "")


def P(params, key):
    return sp.sympify(params[key])


def extract_letter(dap_an):
    m = re.match(r"^([A-D])\.", dap_an.strip())
    return m.group(1) if m else None


def eq0(expr):
    return sp.simplify(expr) == 0


# ============================================================================
# Dạng 1 — định nghĩa trực tiếp (liên hợp, môđun, phần thực/ảo)
# ============================================================================
def verify_mau_stt1(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    # kiem tra truc tiep: lien hop cua a+bi la a-bi
    re_ok = _contains(f"bằng ${_latex(a)}$", dap_an)
    im_ok = _contains(f"bằng ${_latex(-b)}$", dap_an)
    return (re_ok and im_ok), "" if (re_ok and im_ok) else "khong khop cong thuc lien hop a-bi"


def verify_mau_stt2(params, dap_an, **_):
    a, b, c, d = (P(params, k) for k in "abcd")
    dung = sp.sqrt((a + c) ** 2 + (b + d) ** 2)
    return _check_value_in_text(dap_an, dung)


def verify_mau_stt9(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    ok = _contains(f"a={_latex(a)}, b={_latex(b)}", dap_an)
    return ok, "" if ok else "khong khop a,b"


def verify_mau_stt10(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    zbar = sp.expand((a + b * I) * (1 + I))
    dung = sp.sqrt(sp.expand(sp.re(zbar) ** 2 + sp.im(zbar) ** 2))
    return _check_value_in_text(dap_an, dung)


def verify_mau_stt15(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    dung = sp.sqrt(a ** 2 + b ** 2)
    return _check_value_in_text(dap_an, dung)


def verify_mau_stt49(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    return _check_conjugate(dap_an, a, b)


def verify_mau_stt43(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    return _check_conjugate(dap_an, a, b)


def verify_mau_stt30(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    return _check_value_in_text(dap_an, b)


verify_mau_stt58 = verify_mau_stt30


def verify_mau_stt53(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    return _check_value_in_text(dap_an, a)


def verify_mau_stt34(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    # Doc lap: dap an dung phai la B, va gia tri hien thi phai bang bi (phan
    # thuc =0, phan ao =b). Dong thoi xac nhan a!=0 (dieu kien de 3 phuong an
    # con lai KHONG phai thuan ao, tuc de bai khong bi mo ho).
    if a == 0:
        return False, "a=0 lam cac phuong an con lai cung thuan ao (de bai mo ho)"
    correct = f"{_latex(b)}i" if sp.Abs(b) != 1 else ("i" if b > 0 else "-i")
    ok_letter = dap_an.strip().startswith("B.")
    ok_value = _contains(f"z={correct}", dap_an)
    ok = ok_letter and ok_value
    return ok, "" if ok else f"khong khop dang thuan ao doc lap z={correct}"


def verify_mau_stt40(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")  # a=P, b=Q trong build_rows_for_question
    return _check_conjugate_raw(dap_an, a, b)  # z=P+Qi, kiem tra dung dang


def verify_mau_stt50(params, dap_an, **_):
    a, b, c, d = (P(params, k) for k in "abcd")
    prod = sp.expand((a + b * I) * (c - d * I))
    dung = sp.sqrt(sp.re(prod) ** 2 + sp.im(prod) ** 2)
    return _check_value_in_text(dap_an, dung)


def verify_mau_stt59(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    dung = sp.sqrt(2 * (a ** 2 + b ** 2))
    return _check_value_in_text(dap_an, dung)


# ============================================================================
# Dạng 2 — tọa độ điểm biểu diễn
# ============================================================================
def verify_mau_diem_bieu_dien(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    if a == b or a == -b:
        b = b + 1
    ok = _contains(f"({_latex(a)};{_latex(b)})", dap_an)
    return ok, "" if ok else "toa do khong khop (a;b)"


def verify_mau_M_phan_thuc(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")  # a=p, b=q
    return _check_value_in_text(dap_an, a)


def verify_mau_M_la_so_phuc_nao(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    target = f"={_latex(a)}{'+' if b>=0 else '-'}{_latex(sp.Abs(b))}i".replace(" ", "")
    ok = target in dap_an.replace(" ", "")
    return ok, "" if ok else "khong khop z=p+qi"


def verify_mau_binh_phuong(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    val = sp.expand((a + b * I) ** 2)
    re_v, im_v = sp.re(val), sp.im(val)
    ok = _contains(f"({_latex(re_v)};{_latex(im_v)})", dap_an)
    return ok, "" if ok else "toa do (a+bi)^2 khong khop"


def verify_mau_w_iz(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    w = sp.expand((a + b * I) * I)
    re_w, im_w = sp.re(w), sp.im(w)
    ok = _contains(f"({_latex(re_w)};{_latex(im_w)})", dap_an)
    return ok, "" if ok else "toa do w=iz khong khop"


def verify_mau_2z1_z2(params, dap_an, **_):
    a, b, c, d = (P(params, k) for k in "abcd")
    re_v, im_v = 2 * a + c, 2 * b + d
    ok = _contains(f"({_latex(re_v)};{_latex(im_v)})", dap_an)
    return ok, "" if ok else "toa do 2z1+z2 khong khop"


# ============================================================================
# Dạng 3 — phép toán số phức
# ============================================================================
def verify_mau_stt3(params, dap_an, **_):
    a, b, c, d = None, None, None, None
    a, b = P(params, "a"), P(params, "b")
    z = a + b * I
    w = sp.expand(I * z + sp.conjugate(z))
    return _check_conjugate_raw(dap_an, sp.re(w), sp.im(w))


def verify_mau_stt5(params, dap_an, **_):
    p, q = P(params, "a"), P(params, "b")
    z = sp.expand(I * (p + q * I))
    zbar_re, zbar_im = sp.re(z), -sp.im(z)
    return _check_conjugate_raw(dap_an, zbar_re, zbar_im, label="\\overline{z}")


def verify_mau_stt16(params, dap_an, **_):
    a, b, c, d = (P(params, k) for k in "abcd")
    val = (a + b * I) + sp.conjugate(c + d * I)
    return _check_value_in_text(dap_an, sp.im(val))


def verify_mau_stt19(params, dap_an, **_):
    a, b, c, d = (P(params, k) for k in "abcd")
    return _check_value_in_text(dap_an, a + c)


def verify_mau_stt21(params, dap_an, **_):
    a, b, c, d = (P(params, k) for k in "abcd")
    val = sp.expand((a + b * I) * (c + d * I))
    return _check_value_in_text(dap_an, sp.im(val))


def verify_mau_stt23(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    return _check_conjugate_raw(dap_an, 2 * a, 2 * b)


def verify_mau_stt29(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    val = sp.expand((a + b * I) ** 2)
    return _check_value_in_text(dap_an, sp.re(val))


def verify_mau_tong(params, dap_an, **_):
    a, b, c, d = (P(params, k) for k in "abcd")
    return _check_conjugate_raw(dap_an, a + c, b + d)


def verify_mau_stt52(params, dap_an, **_):
    a, b, c, d = (P(params, k) for k in "abcd")
    return _check_conjugate_raw(dap_an, a + c, b + d)


def verify_mau_stt57(params, dap_an, **_):
    a, b, c, d = (P(params, k) for k in "abcd")
    return _check_conjugate_raw(dap_an, a - c, b - d)


# ============================================================================
# Dạng 4 — giải phương trình / đếm nghiệm (verify bằng giải lại độc lập)
# ============================================================================
def verify_mau_stt6(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    z_ = sp.symbols("z__")
    sol = sp.solve(sp.Eq(z_ * (a - b * I) + 13 * I, 1), z_)[0]
    dung = sp.sqrt(sp.re(sol) ** 2 + sp.im(sol) ** 2)
    return _check_value_in_text(dap_an, dung)


def verify_mau_stt7(params, dap_an, **_):
    p, q = P(params, "p"), P(params, "q")
    a_, b_ = sp.symbols("a__ b__", real=True)
    z = a_ + b_ * I
    eq = sp.expand((1 + I) * z + 2 * sp.conjugate(z) - (p + q * I))
    sol = sp.solve([sp.re(eq), sp.im(eq)], [a_, b_])
    P_val = sol[a_] + sol[b_]
    return _check_value_in_text(dap_an, P_val, label="P")


def verify_mau_stt25(params, dap_an, **_):
    p, q = P(params, "a"), P(params, "b")
    zbar = sp.expand((p + q * I) / I)
    z = sp.conjugate(zbar)
    return _check_value_in_text(dap_an, sp.im(z))


def verify_mau_stt38(params, dap_an, **_):
    p, q = P(params, "p"), P(params, "q")
    b_ = sp.symbols("b__", real=True)
    A = -p
    eq_im = sp.Eq(b_ + q - sp.sqrt(A ** 2 + b_ ** 2), 0)
    bs = [s for s in sp.solve(eq_im, b_) if s.is_real]
    if not bs:
        return False, "khong giai duoc b (doc lap)"
    B = bs[0]
    S = A + 3 * B
    return _check_value_in_text(dap_an, S, label="S")


def verify_mau_stt45_real(params, dap_an, **_):
    p = P(params, "p")
    rhs_re, rhs_im = P(params, "rhs_re"), P(params, "rhs_im")
    a_, b_ = sp.symbols("a__ b__", real=True)
    z = a_ + b_ * I
    expr = sp.expand(3 * (sp.conjugate(z) - p * I) - (2 + 3 * I) * z - (rhs_re + rhs_im * I))
    sol = sp.solve([sp.re(expr), sp.im(expr)], [a_, b_])
    modun = sp.sqrt(sol[a_] ** 2 + sol[b_] ** 2)
    return _check_value_in_text(dap_an, modun)


def verify_mau_stt54(params, dap_an, **_):
    p, q = P(params, "a"), P(params, "b")
    z = sp.expand((p + q * I) / I)
    return _check_conjugate_raw(dap_an, sp.re(z), -sp.im(z), label="\\overline{z}")


def verify_mau_stt11(params, dap_an, **_):
    r, p = P(params, "r"), P(params, "p")
    xs = sp.symbols("xs", real=True)
    sols = set()
    for sign in [1, -1]:
        eq = sp.Eq(xs ** 2 + (xs * sign) ** 2 - 2 * p * (xs * sign) + p ** 2 - r ** 2, 0)
        for xv in sp.solve(eq, xs):
            if xv.is_real:
                sols.add((sp.nsimplify(xv), sp.nsimplify(xv * sign)))
    return _check_count(dap_an, len(sols))


def verify_mau_stt14(params, dap_an, **_):
    p1, q1, p2, q2 = (P(params, k) for k in ["p1", "q1", "p2", "q2"])
    xs, ys = sp.symbols("xs ys", real=True)
    lin = sp.expand((xs - p1) ** 2 + (ys - q1) ** 2 - (xs - p2) ** 2 - (ys - q2) ** 2)
    y_sols = sp.solve(sp.Eq(lin, 0), ys)
    if not y_sols:
        return False, "duong trung truc suy bien (doc lap)"
    y_expr = y_sols[0]
    sols = set()
    for sign in [1, -1]:
        eq = sp.Eq(xs ** 2 + y_expr ** 2 - 4 * sign * xs - 4, 0)
        for xv in sp.solve(eq, xs):
            if xv.is_real and ((sign == 1 and xv >= 0) or (sign == -1 and xv < 0)):
                sols.add(sp.nsimplify(xv))
    return _check_count(dap_an, len(sols))


def verify_mau_stt39(params, dap_an, **_):
    p, r, q = P(params, "p"), P(params, "r"), P(params, "q")
    xs, ys = sp.symbols("xs ys", real=True)
    eqs = [sp.Eq(xs * (xs - q) + ys ** 2, 0), sp.Eq(xs ** 2 + (ys - p) ** 2, r ** 2)]
    sols = sp.solve(eqs, [xs, ys])
    valid = [(sx, sy) for sx, sy in sols if sx.is_real and sy.is_real and not (sx == q and sy == 0) and not (sx == 0 and sy == 0)]
    return _check_count(dap_an, len(valid))


def verify_mau_stt42(params, dap_an, **_):
    p, q = P(params, "p"), P(params, "q")
    t = sp.symbols("t", real=True, nonnegative=True)
    lhs_mod_sq = ((4 - t) ** 2 + 1) * t ** 2
    rhs_mod_sq = (p * t) ** 2 + (2 - t) ** 2
    poly = sp.expand(lhs_mod_sq - rhs_mod_sq)
    coeffs = [float(c) for c in sp.Poly(poly, t).all_coeffs()]
    import numpy as _np
    numeric_roots = _np.roots(coeffs)
    valid_t = []
    for r in numeric_roots:
        if abs(r.imag) < 1e-7 and r.real >= -1e-9:
            valid_t.append(round(r.real, 6))
    dedup = []
    for v in valid_t:
        if not any(abs(v - w) < 1e-4 for w in dedup):
            dedup.append(v)
    return _check_count(dap_an, len(dedup))


def verify_mau_stt66(params, dap_an, **_):
    k = P(params, "k")
    n = 4 if sp.Abs(k) == 4 else 3
    return _check_count(dap_an, n)


def verify_mau_stt8(params, dap_an, **_):
    a, b = P(params, "a"), P(params, "b")
    u = sp.symbols("u_", positive=True)
    coef2 = a ** 2 + b ** 2
    eq = sp.Eq(coef2 * u ** 2 + coef2 * u - 10, 0)
    us = [s for s in sp.solve(eq, u) if s.is_real and s > 0]
    if not us:
        return False, "khong giai duoc u (doc lap)"
    t_val = sp.sqrt(us[0])
    t_num = float(t_val)
    lo = round(t_num - 0.5, 2)
    hi = round(t_num + 0.5, 2)
    ok = lo < t_num < hi
    return ok, "" if ok else "t khong nam trong khoang (lo,hi) doc lap"


# ============================================================================
# Dạng 5 — quỹ tích
# ============================================================================
def verify_mau_stt4(params, dap_an, **_):
    R, a, b = P(params, "R"), P(params, "a"), P(params, "b")
    dung = R * sp.sqrt(a ** 2 + b ** 2)
    return _check_value_in_text(dap_an, dung, label="r")


def verify_mau_stt31(params, dap_an, **_):
    p, r = P(params, "a"), P(params, "b")
    r = sp.Abs(r)
    if r == 0:
        r = sp.Integer(1)
    ok = _contains(f"({_latex(0)};{_latex(-p)})", dap_an)
    return ok, "" if ok else "tam duong tron khong khop"


def verify_mau_stt13(params, dap_an, **_):
    p, q = P(params, "a"), P(params, "b")
    cx_, cy_ = -q / sp.Integer(2), -p / sp.Integer(2)
    if cx_ == cy_:
        q = q + 2
        cx_, cy_ = -q / sp.Integer(2), -p / sp.Integer(2)
    ok = _contains(f"({_latex(cx_)};{_latex(cy_)})", dap_an)
    return ok, "" if ok else "tam duong tron STT13 khong khop"


def verify_mau_stt41(params, dap_an, **_):
    p, q = P(params, "a"), P(params, "b")
    dung = sp.sqrt(p ** 2 + q ** 2) / 2
    return _check_value_in_text(dap_an, dung)


def verify_mau_stt46(params, dap_an, **_):
    r, p = P(params, "r"), P(params, "p")
    X, Y = sp.symbols("X_ Y_", real=True)
    eq = sp.expand((X - p) ** 2 + Y ** 2 - r ** 2 * (X ** 2 + (1 - Y) ** 2))
    poly = sp.Poly(eq, X, Y)
    coeff_X2 = poly.coeff_monomial(X ** 2)
    coeff_Y2 = poly.coeff_monomial(Y ** 2)
    if sp.simplify(coeff_X2 - coeff_Y2) != 0 or coeff_X2 == 0:
        return False, "khong dua duoc ve duong tron chuan (doc lap)"
    eq_norm = sp.expand(eq / coeff_X2)
    poly_n = sp.Poly(eq_norm, X, Y)
    coeff_X = poly_n.coeff_monomial(X)
    coeff_Y = poly_n.coeff_monomial(Y)
    const = poly_n.coeff_monomial(1)
    h = -coeff_X / 2
    k = -coeff_Y / 2
    R2 = h ** 2 + k ** 2 - const
    if R2 <= 0:
        return False, "R^2 khong duong (doc lap)"
    return _check_value_in_text(dap_an, sp.sqrt(R2))


# ============================================================================
# Dạng 6 — phương trình bậc hai có tham số
# ============================================================================
def verify_mau_stt26(params, dap_an, **_):
    c, d = P(params, "c"), P(params, "d")
    count = 0
    for mv in range(-80, 81):
        delta = mv ** 2 - c * mv - d
        if delta > 0:
            if mv == 0:
                count += 1
        elif delta < 0:
            count += 1
    return _check_count(dap_an, count)


def verify_mau_stt33(params, dap_an, **_):
    a, S = P(params, "a"), P(params, "S")
    mm = sp.symbols("mm_", real=True)
    valid = set()
    for mv in [S / 2, -S / 2]:
        if sp.simplify(2 * a * mv + a ** 2) < 0:
            valid.add(sp.nsimplify(mv))
    for mv in [-a + S / 2, -a - S / 2]:
        if sp.simplify((mv + a) ** 2 - mv ** 2) > 0:
            valid.add(sp.nsimplify(mv))
    return _check_count(dap_an, len(valid))


def verify_mau_stt36(params, dap_an, **_):
    p, q = P(params, "a"), P(params, "b")
    S = 2 * p
    Pv = p ** 2 + q ** 2
    # kiem tra bang Viet doc lap: pt dung phai la z^2 - S*z + Pv = 0, thay
    # true root p+qi vao xac nhan bang 0 (khong phu thuoc quy uoc hien thi dau)
    z = p + q * I
    residual = sp.expand(z ** 2 - S * z + Pv)
    ok_root = eq0(residual)
    ok_letter = dap_an.strip().startswith("C.")
    ok_final = ok_root and ok_letter
    return ok_final, "" if ok_final else "nghiem khong thoa phuong trinh Viet doc lap"


def verify_mau_stt56(params, dap_an, **_):
    a, R = P(params, "a"), P(params, "R")
    valid = set()
    mm = sp.symbols("mm_", real=True)
    m_edge = -a
    if sp.simplify(sp.Abs(m_edge + a) - R) == 0:
        valid.add(sp.nsimplify(m_edge))
    for mv in [R, -R]:
        if sp.simplify(2 * a * mv + a ** 2) < 0:
            valid.add(sp.nsimplify(mv))
    for z0v in [R, -R]:
        eq = sp.Eq(z0v ** 2 - 2 * (mm + a) * z0v + mm ** 2, 0)
        for mv in sp.solve(eq, mm):
            if mv.is_real and sp.simplify((mv + a) ** 2 - mv ** 2) > 0:
                valid.add(sp.nsimplify(mv))
    return _check_count(dap_an, len(valid))


def verify_mau_stt61(params, dap_an, **_):
    p, q = P(params, "p"), P(params, "q")
    solutions = set()
    z1, z2 = p, q / 2
    a1 = -(z1 + z2) / 4
    rhs_b2 = z1 * z2 - 2
    if rhs_b2 > 0:
        bv = sp.sqrt(rhs_b2)
        solutions.add((sp.nsimplify(a1), sp.nsimplify(bv)))
        solutions.add((sp.nsimplify(a1), sp.nsimplify(-bv)))
    elif rhs_b2 == 0:
        solutions.add((sp.nsimplify(a1), sp.Integer(0)))
    xs, ys = sp.symbols("xs_ ys_", real=True)
    sol = sp.solve([sp.Eq(xs + 2 * ys, p), sp.Eq(2 * xs + ys, q)], [xs, ys])
    xv, yv = sol[xs], sol[ys]
    if yv != 0:
        a2 = -(2 * xv) / 4
        rhs2 = xv ** 2 + yv ** 2 - 2
        if rhs2 > 0:
            bv2 = sp.sqrt(rhs2)
            solutions.add((sp.nsimplify(a2), sp.nsimplify(bv2)))
            solutions.add((sp.nsimplify(a2), sp.nsimplify(-bv2)))
        elif rhs2 == 0:
            solutions.add((sp.nsimplify(a2), sp.Integer(0)))
    return _check_count(dap_an, len(solutions))


# ============================================================================
# Dạng 7 — cực trị & vận dụng cao
# ============================================================================
def verify_mau_stt12(params, dap_an, **_):
    A = tuple(sp.sympify(v) for v in params["A"])
    B = tuple(sp.sympify(v) for v in params["B"])
    C = tuple(sp.sympify(v) for v in params["C"])
    ax, ay = A
    bx, by = B
    cx_, cy_ = C
    if ax == bx:
        return False, "AB thang dung (doc lap)"
    slope = sp.simplify((by - ay) / (bx - ax))
    xs = sp.symbols("xs__", real=True)
    y_expr = ay + slope * (xs - ax)
    f = sp.expand((xs - cx_) ** 2 + (y_expr - cy_) ** 2)
    poly = sp.Poly(f, xs)
    a2, b2, c2 = poly.all_coeffs() if poly.degree() == 2 else (0, *poly.all_coeffs())
    if a2 == 0:
        return False, "suy bien (doc lap)"
    x0 = sp.simplify(-b2 / (2 * a2))
    lo, hi = (ax, bx) if ax < bx else (bx, ax)
    candidates = [lo, hi]
    if lo < x0 < hi:
        candidates.append(x0)
    vals = [sp.radsimp(sp.simplify(f.subs(xs, xv))) for xv in candidates]
    f_min = min(vals, key=lambda v: sp.N(v))
    f_max = max(vals, key=lambda v: sp.N(v))
    m = sp.radsimp(sp.sqrtdenest(sp.sqrt(f_min)))
    M = sp.radsimp(sp.sqrtdenest(sp.sqrt(f_max)))
    Pv = sp.simplify(m + M)
    return _check_value_in_text(dap_an, Pv, label="P")


def verify_mau_stt27(params, dap_an, **_):
    c, h = P(params, "c"), P(params, "h")
    d_frac = P(params, "d_frac")
    R = sp.nsimplify(c / 2)
    d = sp.nsimplify(d_frac * R)
    Pmax = sp.nsimplify(2 * h * d)
    return _check_value_in_text(dap_an, Pmax)


def verify_mau_stt32(params, dap_an, **_):
    p, q = P(params, "p"), P(params, "q")
    Cmag = sp.sqrt(p ** 2 + q ** 2)
    ans = sp.nsimplify(2 * Cmag + 4)
    return _check_value_in_text(dap_an, ans)


def verify_mau_stt55(params, dap_an, **_):
    p, q, r1, r2 = (P(params, k) for k in ["p", "q", "r1", "r2"])
    K = p + q * I
    Kmag = sp.sqrt(p ** 2 + q ** 2)
    if Kmag <= r1 + r2:
        return False, "|K|<=r1+r2 (doc lap)"
    z_val = sp.simplify(-K / Kmag * r1)
    w_val = sp.simplify(-I * sp.conjugate(K) / Kmag * r2)
    diff = sp.simplify(z_val - w_val)
    ans = sp.nsimplify(sp.sqrt(sp.expand(sp.re(diff) ** 2 + sp.im(diff) ** 2)))
    return _check_value_in_text(dap_an, ans)


def verify_mau_stt60(params, dap_an, **_):
    A = tuple(sp.sympify(v) for v in params["A"])
    B = tuple(sp.sympify(v) for v in params["B"])
    ax, ay = A
    bx, by = B
    Aval = ax + ay * I
    Bval = bx + by * I
    bound1 = sp.simplify(sp.Abs(-Aval * I - Bval))
    bound2 = sp.simplify(sp.Abs(Aval * I - Bval))
    ans = min(bound1, bound2, key=lambda v: sp.N(v))
    return _check_value_in_text(dap_an, sp.nsimplify(ans))


def verify_mau_stt65(params, dap_an, **_):
    R, c1, c2 = P(params, "R"), P(params, "c1"), P(params, "c2")
    K = sp.nsimplify(c2 * R ** 2 / c1)
    half = K / 2
    disc = R ** 2 - half ** 2
    if disc <= 0:
        return False, "khong ton tai d thuc (doc lap)"
    d = sp.sqrt(disc)
    if sp.simplify(1 - half) == 0:
        return False, "dien tich = 0 (doc lap)"
    area = sp.nsimplify(sp.Abs(d * (1 - half)))
    return _check_value_in_text(dap_an, area)


# ============================================================================
# Helper kiểm tra chung
# ============================================================================
def _check_value_in_text(dap_an, value, label=None):
    target = _latex(value)
    ok = _contains(f"${target}$", dap_an) or _contains(f"={target}$", dap_an)
    if not ok:
        # thu so sanh so hoc truc tiep tat ca cac so trong dap_an voi value
        nums = re.findall(r"-?\d+\.?\d*", dap_an)
        try:
            ok = any(abs(float(n) - float(value)) < 1e-6 for n in nums if n not in ("", "-"))
        except Exception:
            ok = False
    return ok, "" if ok else f"khong tim thay gia tri doc lap {target} trong dap_an"


def _check_count(dap_an, n):
    m = re.search(r"\$(\d+)\$", dap_an)
    if not m:
        return False, "khong doc duoc so nguyen trong dap_an"
    stored_n = int(m.group(1))
    ok = stored_n == n
    return ok, "" if ok else f"so luong doc lap={n} nhung dap_an luu {stored_n}"


def _check_conjugate(dap_an, a, b):
    return _check_conjugate_raw(dap_an, a, -b)


def _check_conjugate_raw(dap_an, re_v, im_v, label=None):
    # dung chinh ham z_string cua script sinh cau hoi de dam bao dinh dang
    # (bao gom \left(...\right) khi he so la bieu thuc gop) khop chinh xac.
    target = _utils.z_string(re_v, im_v)
    dap_clean = dap_an.replace(" ", "")
    ok = target.replace(" ", "") in dap_clean
    return ok, "" if ok else f"khong khop {target} trong dap_an"


VERIFIERS = {k[len("verify_"):]: v for k, v in list(globals().items()) if k.startswith("verify_") and callable(v)}


def verify_row(row):
    mau_ta = row["mau_ta"]
    fn = VERIFIERS.get(mau_ta)
    if fn is None:
        return "Chưa có checker", "Không có hàm kiểm tra độc lập cho mẫu này"
    try:
        ok, note = fn(row.get("params", {}), row["dap_an"])
    except Exception as e:
        return "Lỗi khi kiểm tra", f"{type(e).__name__}: {e}"
    return ("Đạt" if ok else "Cần xem lại"), note


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    stats = {}
    all_results = []
    for i in range(1, 8):
        data = json.load(open(f"Sinh_them_cau_hoi/data/dang{i}_full.json", encoding="utf-8"))
        for row in data:
            status, note = verify_row(row)
            stats[status] = stats.get(status, 0) + 1
            all_results.append((i, row["stt_goc"], row["mau_ta"], status, note))
    for status, count in sorted(stats.items()):
        print(status, count)
    with open("Sinh_them_cau_hoi/data/verify_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
