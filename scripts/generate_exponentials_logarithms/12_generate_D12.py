"""
Sinh bien the D12 - Giai phuong trinh mu co ban dang a^f(x)=a^k, f(x) bac
nhat. 4 cau goc: p020_q13, p093_q03, p172_q13, p192_q13.

Cong thuc: a^(m*x + c) = N (voi N = a^k)  =>  x = (k - c) / m
"""
import json
import random
import re
import sys
from importlib import import_module

sys.path.insert(0, "scripts/generate_questions")
utils = import_module("10_common_utils")
latex = utils.latex
linear_expr_str = utils.linear_expr_str
bump_until_distinct = utils.bump_until_distinct

import sympy as sp

MA_DANG = "D12"
TEN_DANG = "Giai phuong trinh mu co ban dang a^f(x)=a^k, f(x) bac nhat"
SOURCE_IDS = ["p020_q13", "p093_q03", "p172_q13", "p192_q13"]


def mau_D12(a, m, c, k):
    a, m, c, k = sp.Integer(a), sp.Integer(m), sp.Integer(c), sp.Integer(k)
    N = a ** k
    correct = sp.Rational(k - c, m)
    wrong1 = sp.Rational(k + c, m)
    wrong2 = sp.Rational(N - c, m)
    wrong3 = sp.Rational(k, m) - c
    vals = bump_until_distinct([correct, wrong1, wrong2, wrong3])
    correct, wrong1, wrong2, wrong3 = vals

    expr = linear_expr_str(m, c)
    de_bai = f"Nghiệm của phương trình ${a}^{{{expr}}}={latex(N)}$ là\n\n"
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
        lines.append(f"{letter}. $x={latex(opts[idx])}$.")
    de_bai += "\n".join(lines)
    dap_an = f"{correct_letter}. $x={latex(correct)}$."
    loi_giai = (
        f"Ta có ${a}^{{{expr}}}={latex(N)}={a}^{{{k}}} "
        f"\\Leftrightarrow {expr}={k} \\Leftrightarrow x={latex(correct)}$."
    )
    return de_bai, dap_an, loi_giai, dict(a=str(a), m=str(m), c=str(c), k=str(k))


BUCKETS = {
    "he_so_x_bang_1": dict(m_choices=[1], c_range=(-6, 6)),
    "he_so_x_lon_hon_1": dict(m_choices=[2, 3], c_range=(-6, 6)),
    "dap_so_phan_so": dict(m_choices=[2, 3], c_range=(-6, 6)),
}
SO_BAN_MOI_BUCKET = 2


def gen_variants(id_goc, seed_base):
    rows = []
    rnd = random.Random(seed_base)
    for bucket_name, spec in BUCKETS.items():
        made = 0
        tries = 0
        seen = set()
        while made < SO_BAN_MOI_BUCKET and tries < 500:
            tries += 1
            a = rnd.choice([2, 3, 4, 5])
            m = rnd.choice(spec["m_choices"])
            c = utils.rrange(*spec["c_range"], exclude=set(), rnd=rnd)
            k = rnd.choice([1, 2, 3, 4])
            if bucket_name == "dap_so_phan_so":
                if (k - c) % m == 0:
                    continue
            else:
                if (k - c) % m != 0:
                    continue
            key = (a, m, c, k)
            if key in seen:
                continue
            seen.add(key)
            de_bai, dap_an, loi_giai, params = mau_D12(a, m, c, k)
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
    random.seed(1201)
    all_rows, seen_params, seen_questions = [], set(), set()
    attempts = 0
    while len(all_rows) < 90 and attempts < 500:
        source_id = SOURCE_IDS[attempts % len(SOURCE_IDS)]
        for row in gen_variants(source_id, seed_base=2000 + attempts):
            key = tuple(sorted(row["params"].items()))
            if key in seen_params or row["de_bai"] in seen_questions:
                continue
            ok, note = verifier.verify_D12(row["params"], row["dap_an"])
            if not ok:
                raise AssertionError(f"D12 independent verification failed: {row['params']} {note}")
            choices = re.findall(r"(?m)^([A-D])\.\s*(.+)$", row["de_bai"])
            normalized = [re.sub(r"[\s$.,]", "", text) for _, text in choices]
            if len(choices) != 4 or {c for c, _ in choices} != set("ABCD") or len(set(normalized)) != 4:
                continue
            seen_params.add(key); seen_questions.add(row["de_bai"]); all_rows.append(row)
            if len(all_rows) == 90:
                break
        attempts += 1
    print(f"D12: {len(all_rows)}/90 variants; attempts={attempts}")
    with open("data/questions/mu_logarit_extraction/bien_the/D12_bien_the.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=2)
