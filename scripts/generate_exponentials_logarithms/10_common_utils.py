"""Ham tien ich dung chung cho cac script sinh bien the Mu-Logarit."""
import random

import sympy as sp


def latex(expr):
    expr = sp.sympify(expr)
    s = sp.latex(expr)
    s = s.replace(r"\frac", r"\dfrac")
    return s


def assert_distinct(*vals):
    """Bao dam 4 phuong an A/B/C/D khong trung nhau."""
    seen = []
    for v in vals:
        for s in seen:
            if sp.simplify(v - s) == 0:
                raise ValueError(f"Trung phuong an: {v} == {s}")
        seen.append(v)


def bump_until_distinct(vals):
    """vals[0] la dap an dung, giu nguyen. Cong dan 1 vao vals[1:] neu trung
    voi bat ky gia tri nao truoc do, cho den khi tat ca phan biet."""
    vals = list(vals)
    for i in range(1, len(vals)):
        tries = 0
        while any(sp.simplify(vals[i] - vals[j]) == 0 for j in range(i)) and tries < 50:
            vals[i] = vals[i] + 1
            tries += 1
    return vals


def linear_expr_str(m, c, var="x"):
    """Chuoi latex cho m*var + c, vd '2x-1', 'x+4', '3x'."""
    m = sp.sympify(m)
    c = sp.sympify(c)
    coef = "" if m == 1 else (f"{latex(m)}" if m != -1 else "-")
    s = f"{coef}{var}" if m != 0 else ""
    if c != 0:
        sign = "+" if c > 0 else "-"
        s += f"{sign}{latex(sp.Abs(c))}"
    return s


def rrange(lo, hi, exclude=(0,), rnd=None):
    rnd = rnd or random
    while True:
        v = rnd.randint(lo, hi)
        if v not in exclude:
            return v


def render_mc(opt_strs, correct_index, prefix=""):
    """opt_strs: list 4 chuoi latex (khong bao gom $...$). correct_index: vi
    tri (0-3) cua dap an dung trong opt_strs TRUOC KHI xao tron. Tra ve
    (danh_sach_dong_ABCD, dap_an_dung_chuoi, correct_letter) sau khi xao tron
    ngau nhien vi tri hien thi."""
    letters = ["A", "B", "C", "D"]
    order = [0, 1, 2, 3]
    random.shuffle(order)
    lines = []
    correct_letter = None
    correct_str = None
    for pos, idx in enumerate(order):
        letter = letters[pos]
        if idx == correct_index:
            correct_letter = letter
            correct_str = opt_strs[idx]
        lines.append(f"{letter}. ${prefix}{opt_strs[idx]}$.")
    dap_an = f"{correct_letter}. ${prefix}{correct_str}$."
    return lines, dap_an
