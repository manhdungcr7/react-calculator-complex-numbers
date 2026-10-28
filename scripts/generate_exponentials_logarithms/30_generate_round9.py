# -*- coding: utf-8 -*-
"""Generate and independently verify numerical variants for D84."""
import json
import mpmath as mp
import re
import sys
from pathlib import Path
from importlib import import_module

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts/generate_questions"))
utils = import_module("10_common_utils")
render_mc = utils.render_mc

SOURCE_ID = "p216_q45"
TYPE_NAME = "Đếm số nguyên một biến sao cho tồn tại biến kia thỏa phương trình mũ bằng xét hàm đơn điệu"


def gen_D84(U):
    U = int(U)
    assert 3 <= U <= 93 and U != 4
    C = 3 * U
    # h(y)=y-log_3(1+y/3) is strictly increasing for y>=1. Count
    # positive integer y by the endpoint condition h(y)<3U-1.
    from fractions import Fraction
    # Exact equivalent of h(y)<3U-1; avoid floating-point boundary decisions.
    positive_count = sum(
        1 for y in range(1, 4 * U + 1)
        if Fraction(1) + Fraction(y, 3) > Fraction(3) ** (y - 3 * U + 1)
    )
    count = positive_count + 2  # y=-1,-2 work; y=0 does not.
    choices = [str(count), str(count + 1), str(count - 1), str(count + 2)]
    choice_lines, answer = render_mc(choices, 0)
    question = (
        f"Có bao nhiêu số nguyên $y$ tồn tại sao cho "
        f"$x\\in\\left(\\dfrac{{1}}{{3}};{U}\\right)$ thỏa mãn "
        f"$27^{{3x^2+xy}}=(1+xy)27^{{{C}x}}$?\n\n" + "\n".join(choice_lines)
    )
    solution = (
        f"Đặt $g_y(x)=3x-{C}-\\dfrac{{\\log_{{27}}(1+xy)}}x+y$. Với $y\\ge1$, "
        "phương trình tương đương $g_y(x)=0$. Ta có "
        "$g_y'(x)=3+\\dfrac{\\ln(1+xy)}{x^2\\ln27}-"
        "\\dfrac{y}{x(1+xy)\\ln27}>3-\\dfrac1{x^2\\ln27}"
        ">=3-\\dfrac3{\\ln3}>0$, nên $g_y$ đồng biến trên "
        f"$[1/3;{U}]$. Tại $x={U}$, $g_y({U})=y-"
        f"\\dfrac{{\\log_{{27}}(1+{U}y)}}{{{U}}}>0$, vì "
        "$\\ln(1+u)<u$ và $\\ln27>1$. Do đó phương trình có nghiệm "
        f"trong khoảng mở khi và chỉ khi $g_y(1/3)<0$, tức là "
        f"$h(y)=y-\\log_3(1+y/3)<{C-1}$. Hàm $h$ đồng biến với $y\\ge1$ vì $h'(y)=1-1/((y+3)\\ln3)>0$. "
        f"V\u00ec $h$ \u0111\u1ed3ng bi\u1ebfn, ki\u1ec3m tra hai s\u1ed1 nguy\u00ean k\u1ec1 ng\u01b0\u1ee1ng: "
        f"$h({positive_count})<{C-1}\\le h({positive_count+1})$, t\u01b0\u01a1ng \u0111\u01b0\u01a1ng "
        f"$1+{positive_count}/3>3^{{{positive_count}-{C-1}}}$ v\u00e0 "
        f"$1+({positive_count+1})/3\\le3^{{{positive_count+1}-{C-1}}}$. "
        f"Do \u0111\u00f3 c\u00e1c s\u1ed1 nguy\u00ean d\u01b0\u01a1ng th\u1ecfa m\u00e3n l\u00e0 $y=1,\\ldots,{positive_count}$, g\u1ed3m "
        f"${positive_count}$ gi\u00e1 tr\u1ecb.\n\n"
        "Nếu $y\\le-3$ thì $x>1/3$ kéo theo $1+xy<0$, không thể thỏa mãn. "
        f"Với $y=0$, phương trình tương đương $3x(x-{U})=0$, chỉ có $x=0$ "
        f"hoặc $x={U}$, đều không thuộc khoảng mở. Với $y=-1$ và $y=-2$, "
        "xét $F_y(x)=27^{3x^2+(y-"
        f"{C})x}}-(1+xy)$ trên $(1/3,-1/y)$. Trên khoảng này, "
        f"$F_y'(x)=27^{{3x^2+(y-{C})x}}\\ln27(6x+y-{C})-y>0$: "
        f"với $y=-1$, số hạng âm có độ lớn nhỏ hơn "
        f"$27^{{-{U}}}\\ln27\\cdot{C-1}<1$; với $y=-2$, số hạng âm có độ lớn nhỏ hơn "
        f"$27^{{-{U}-1/3}}\\ln27\\cdot{C}<2$. Do đó $F_y$ đồng biến. "
        f"Tại $x=1/3$, $F_y(x)<0$; "
        "khi $x$ tiến đến $-1/y$ từ bên trái, $F_y(x)$ tiến đến một giá trị "
        "dương. Theo định lý giá trị trung gian, mỗi giá trị $y=-1,-2$ đều "
        f"cho một nghiệm. Tổng cộng có ${count}$ giá trị nguyên của $y$."
    )
    return question, answer, solution, {"U": U, "C": C, "count": count}


def verify_D84(params, observed_count=None):
    """Exact integer checks plus analytic monotonicity/end-point arguments."""
    from fractions import Fraction
    U, C, expected = (int(params[k]) for k in ("U", "C", "count"))
    if C != 3 * U or not (3 <= U <= 93 and U != 4):
        return False
    if observed_count is not None and expected != observed_count:
        return False

    # For y>=1, the equation has an interior root exactly when
    # h(y)=y-log_3(1+y/3)<3U-1. Since h is strictly increasing,
    # failure at y=4U excludes every larger integer. Compare the equivalent
    # powers as exact rationals, not rounded logarithms.
    def positive_y_works(y):
        return Fraction(1) + Fraction(y, 3) > Fraction(3) ** (y - 3 * U + 1)
    positive_y = [y for y in range(1, 4 * U + 1) if positive_y_works(y)]
    if positive_y_works(4 * U):
        return False

    # For y=-1,-2, the equation function is strictly increasing on its
    # admissible interval. Its left endpoint is negative (checked exactly),
    # and its right limit is positive. The derivative's negative term is
    # bounded respectively by 26(3U-1)/27^U and 26(3U)/3^(3U+1), using
    # ln(27)<26; these exact inequalities certify F'_y>0 throughout.
    if not (26 * (3 * U - 1) < 27 ** U):
        return False
    if not (26 * 3 * U < 2 * 3 ** (3 * U + 1)):
        return False
    for y in (-1, -2):
        exponent3 = 1 + y - C  # 27^((1+y-C)/3) = 3^(1+y-C)
        left_power = Fraction(3) ** exponent3
        if not left_power < Fraction(1) + Fraction(y, 3):
            return False
    # y=0 gives only x=0 and x=U, both outside the open interval;
    # y<=-3 violates 1+xy>0 for x>1/3.
    return len(positive_y) + 2 == expected


def audit_choices(rows):
    for row in rows:
        choices = re.findall(r"(?m)^([A-D])\.\s*(.+)$", row["de_bai"])
        if len(choices) != 4 or {letter for letter, _ in choices} != set("ABCD"):
            raise AssertionError("Each question must have one choice A-D")
        normalized = [re.sub(r"[\s$.,]", "", value) for _, value in choices]
        if len(set(normalized)) != 4:
            raise AssertionError("Duplicate answer choices")


def main():
    rows = []
    for U in range(3, 94):
        if U == 4:
            continue
        question, answer, solution, params = gen_D84(U)
        if not verify_D84(params):
            raise AssertionError(f"Independent check failed: {params}")
        rows.append({
            "id_goc": SOURCE_ID,
            "ma_dang": "D84",
            "ten_dang": TYPE_NAME,
            "nguon": "Nhân bản",
            "loai_bien_the": "chuan",
            "de_bai": question,
            "dap_an": answer,
            "loi_giai": solution,
            "params": {k: str(v) for k, v in params.items()},
        })
    audit_choices(rows)
    path = REPO / "data/questions/mu_logarit_extraction/bien_the/batch_round9.json"
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated and independently verified {len(rows)} D84 variants")


if __name__ == "__main__":
    main()
