"""
Sinh bien the D18 - Dao ham ham so logarit co ban y=log_a x.
3 cau goc: p031_q02, p111_q22, p121_q02.

Cong thuc: y=log_a(x) => y' = 1/(x ln a)
"""
import json
import random
import re
import sys
from importlib import import_module

sys.path.insert(0, "scripts/generate_questions")
utils = import_module("10_common_utils")
latex = utils.latex

import sympy as sp

MA_DANG = "D18"
TEN_DANG = "Dao ham ham so logarit co ban y=log_a x"
SOURCE_IDS = ["p031_q02", "p111_q22", "p121_q02"]

x = sp.Symbol("x", positive=True)


def mau_D18(a):
    a = sp.Integer(a)
    ln_a = sp.log(a)
    ten_ham = "log x" if a == 10 else f"\\log_{{{a}}} x"
    de_bai = (
        f"Trên khoảng $(0;+\\infty)$, đạo hàm của hàm số $y={ten_ham}$ là\n\n"
    )
    correct = f"y'=\\dfrac{{1}}{{x\\ln {a}}}"
    wrong1 = f"y'=\\dfrac{{\\ln {a}}}{{x}}"
    wrong2 = "y'=\\dfrac{1}{x}"
    wrong3 = f"y'=\\dfrac{{1}}{{{a}x}}"
    opts = [correct, wrong1, wrong2, wrong3]
    letters = ["A", "B", "C", "D"]
    order = [0, 1, 2, 3]
    random.shuffle(order)
    lines = []
    correct_letter = None
    for pos, idx in enumerate(order):
        letter = letters[pos]
        if idx == 0:
            correct_letter = letter
        lines.append(f"{letter}. ${opts[idx]}$.")
    de_bai += "\n".join(lines)
    dap_an = f"{correct_letter}. ${correct}$."
    loi_giai = (
        f"Áp dụng công thức $(\\log_a x)' = \\dfrac{{1}}{{x\\ln a}}$ với $a={a}$, "
        f"ta có $y'=\\dfrac{{1}}{{x\\ln {a}}}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a))


BUCKETS = {
    "co_so_nho": [2, 3],
    "co_so_trung_binh": [4, 5, 6, 7],
    "co_so_lon": [8, 9, 10, 11],
}
SO_BAN_MOI_BUCKET = 2


def gen_variants(id_goc, seed_base):
    rows = []
    rnd = random.Random(seed_base)
    for bucket_name, choices in BUCKETS.items():
        made = 0
        tries = 0
        seen = set()
        while made < SO_BAN_MOI_BUCKET and tries < 200:
            tries += 1
            a = rnd.choice(choices)
            if a in seen:
                continue
            seen.add(a)
            de_bai, dap_an, loi_giai, params = mau_D18(a)
            rows.append({
                "id_goc": id_goc,
                "ma_dang": MA_DANG,
                "ten_dang": TEN_DANG,
                "nguon": "Nhân bản",
                "loai_bien_the": bucket_name,
                "de_bai": de_bai,
                "dap_an": dap_an,
                "loi_giai": loi_giai,
                "params": params,
            })
            made += 1
    return rows


if __name__ == "__main__":
    verifier = import_module("20_verify_pilot")
    random.seed(1801)
    all_rows = []
    for a in range(2, 92):
        id_goc = SOURCE_IDS[(a - 2) % len(SOURCE_IDS)]
        de_bai, dap_an, loi_giai, params = mau_D18(a)
        row = {"id_goc": id_goc, "ma_dang": MA_DANG, "ten_dang": TEN_DANG,
               "nguon": "Nh??n b???n", "loai_bien_the": "co_so_nguyen",
               "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai, "params": params}
        ok, note = verifier.verify_D18(params, dap_an)
        if not ok:
            raise AssertionError(f"D18 independent verification failed: {params} {note}")
        choices = re.findall(r"(?m)^([A-D])\.\s*(.+)$", de_bai)
        normalized = [re.sub(r"[\s$.,]", "", text) for _, text in choices]
        if len(choices) != 4 or {c for c, _ in choices} != set("ABCD") or len(set(normalized)) != 4:
            raise AssertionError(f"D18 answer-choice collision at {params}")
        all_rows.append(row)
    assert len({r["de_bai"] for r in all_rows}) == 90
    print(f"D18: {len(all_rows)}/90 variants; integer base a=2..91")
    with open("data/questions/mu_logarit_extraction/bien_the/D18_bien_the.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=2)
