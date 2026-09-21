"""Hàm tiện ích dùng chung cho tất cả script sinh câu hỏi (mọi dạng)."""
import random

import sympy as sp


def latex(expr):
    expr = sp.sympify(expr)
    s = sp.latex(sp.radsimp(sp.sqrtdenest(expr)) if expr.has(sp.sqrt) else expr)
    s = s.replace(r"\frac", r"\dfrac")
    return s


def latex_sq(expr):
    return f"\\left({latex(expr)}\\right)"


def _is_compound(expr):
    """True nếu expr là tổng nhiều hạng tử (vd 2-4*sqrt(11)), cần bọc ngoặc
    khi ghép vào biểu thức khác để tránh sai/lẫn dấu."""
    return isinstance(expr, sp.Add)


def signed_term(coef, symbol="i", show_one=False):
    if coef == 0:
        return ""
    if coef < 0:
        sign = "-"
        mag = -coef  # phủ định đúng theo biểu thức (phân phối dấu), không phải Abs() trên chuỗi
    else:
        sign = "+"
        mag = coef
    if mag == 1 and not show_one:
        mag_str = ""
    elif _is_compound(mag):
        mag_str = f"\\left({latex(mag)}\\right)"
    else:
        mag_str = latex(mag)
    return f"{sign}{mag_str}{symbol}"


def num_bare(coef):
    if _is_compound(coef):
        return f"\\left({latex(coef)}\\right)"
    return latex(coef)


def z_string(a, b):
    return f"{num_bare(a)}{signed_term(b)}"


def join_plus(s):
    """Ghép '+ s' vào 1 biểu thức latex trước đó, tránh lỗi '+-9' khi s tự
    mang dấu âm (trả về đúng '-9' thay vì '+-9')."""
    s = str(s)
    return s if s.startswith("-") else f"+{s}"


def assert_distinct(*vals):
    """Bảo đảm các phương án A/B/C/D không trùng nhau (bẫy lỗi kiểu sinh
    trùng đáp án đã gặp phải khi thí điểm)."""
    seen = []
    for v in vals:
        for s in seen:
            if sp.simplify(v - s) == 0:
                raise ValueError(f"Trùng phương án: {v} == {s}")
        seen.append(v)


def gen_integers(n, lo=-9, hi=9, seed=None, avoid_zero=True):
    rnd = random.Random(seed)
    seen = set()
    out = []
    tries = 0
    while len(out) < n and tries < 10000:
        tries += 1
        a = rnd.randint(lo, hi)
        b = rnd.randint(lo, hi)
        if avoid_zero and (a == 0 or b == 0):
            continue
        if (a, b) in seen:
            continue
        seen.add((a, b))
        out.append((sp.Integer(a), sp.Integer(b)))
    return out


def gen_rationals(n, seed=None):
    rnd = random.Random(seed)
    seen = set()
    out = []
    denoms = [2, 3, 4, 5]
    tries = 0
    while len(out) < n and tries < 10000:
        tries += 1
        dq = rnd.choice(denoms)
        dp = rnd.choice(denoms)
        num_a = rnd.choice([x for x in range(-11, 12) if x % dq != 0 and x != 0])
        num_b = rnd.choice([x for x in range(-11, 12) if x % dp != 0 and x != 0])
        a = sp.Rational(num_a, dq)
        b = sp.Rational(num_b, dp)
        if (a, b) in seen:
            continue
        seen.add((a, b))
        out.append((a, b))
    return out


def gen_irrationals(n, seed=None):
    rnd = random.Random(seed)
    seen = set()
    out = []
    radicands = [2, 3, 5, 6, 7, 10, 11]
    tries = 0
    while len(out) < n and tries < 10000:
        tries += 1
        which = rnd.choice(["a", "b", "both"])
        k1 = rnd.choice([x for x in range(-4, 5) if x != 0])
        k2 = rnd.choice([x for x in range(-4, 5) if x != 0])
        r1 = rnd.choice(radicands)
        r2 = rnd.choice(radicands)
        if which == "a":
            a = k1 * sp.sqrt(r1)
            b = sp.Integer(rnd.choice([x for x in range(-9, 10) if x != 0]))
        elif which == "b":
            a = sp.Integer(rnd.choice([x for x in range(-9, 10) if x != 0]))
            b = k1 * sp.sqrt(r1)
        else:
            a = k1 * sp.sqrt(r1)
            b = k2 * sp.sqrt(r2)
        key = (a, b)
        if key in seen:
            continue
        seen.add(key)
        out.append((a, b))
    return out


NUMBER_TYPES = [
    ("Số nguyên", gen_integers),
    ("Số hữu tỉ", gen_rationals),
    ("Số vô tỉ", gen_irrationals),
]


def build_rows_for_question(stt_goc, dang, mau_ta, template_fn, so_ban_moi_loai, seed_base):
    """Sinh `so_ban_moi_loai` bản cho mỗi loại số (nguyên/hữu tỉ/vô tỉ), gắn nhãn
    câu gốc STT. template_fn(a, b) -> (de_bai, dap_an, loi_giai)."""
    rows = []
    for loai_so, gen_fn in NUMBER_TYPES:
        seed = hash((stt_goc, loai_so, seed_base)) % (2**31)
        pairs = gen_fn(so_ban_moi_loai, seed=seed)
        for a, b in pairs:
            de_bai, dap_an, loi_giai = template_fn(a, b)
            rows.append({
                "stt_goc": stt_goc,
                "dang": dang,
                "mau_ta": mau_ta,
                "nguon": "Nhân bản",
                "loai_so": loai_so,
                "de_bai": de_bai,
                "dap_an": dap_an,
                "loi_giai": loi_giai,
                "params": {"a": str(a), "b": str(b)},
            })
    return rows
