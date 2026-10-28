# -*- coding: utf-8 -*-
"""D49 (tach hieu) va D20 (luy thua cua luy thua) - 2 dang don gian con sot."""
import json
import re
import random
import sys
from importlib import import_module

sys.path.insert(0, "scripts/generate_questions")
utils = import_module("10_common_utils")
latex = utils.latex
render_mc = utils.render_mc
bump_until_distinct = utils.bump_until_distinct

import sympy as sp

ROWS = []


def add_row(ma_dang, ten_dang, id_goc, de_bai, dap_an, loi_giai, params):
    ROWS.append({
        "id_goc": id_goc, "ma_dang": ma_dang, "ten_dang": ten_dang,
        "nguon": "Nhân bản", "loai_bien_the": "chuan",
        "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai, "params": params,
    })


# ===================== D49: log_c(a/k) = log_c a - log_c k ==================
def gen_D49(c, k):
    c, k = sp.Integer(c), sp.Integer(k)
    # Preserve readable change-of-base notation; SymPy can expand some
    # integer logarithms into unwieldy products of radicals.
    logk_str = f"\\dfrac{{\\log({k})}}{{\\log({c})}}"
    correct = f"\\log_{{{c}}} a-\\left({logk_str}\\right)"
    wrong1 = f"\\log_{{{c}}} a+\\left({logk_str}\\right)"
    wrong2 = f"\\left({logk_str}\\right)-\\log_{{{c}}} a"
    wrong3 = f"\\log_{{{c}}} a-{k}"
    de_bai = f"Với mọi số thực $a$ dương, $\\log_{{{c}}}\\dfrac{{a}}{{{k}}}$ bằng\n\n"
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = f"Ta có $\\log_{{{c}}}\\dfrac{{a}}{{{k}}}=\\log_{{{c}}} a-\\log_{{{c}}}{k}=\\log_{{{c}}} a-\\left({logk_str}\\right)$."
    return de_bai, dap_an, loi_giai, dict(c=str(c), k=str(k))


def verify_D49(params):
    c, k = sp.sympify(params["c"]), sp.sympify(params["k"])
    av = sp.Rational(11, 3)
    lhs = sp.log(av / k, c)
    rhs = sp.log(av, c) - sp.log(k, c)
    return abs(float(lhs - rhs)) < 1e-9


# ===================== D20: log_{a^(1/m)} a^n = n*m =========================
def gen_D20(m, n):
    m, n = sp.Integer(m), sp.Integer(n)
    val = n * m
    root = "\\sqrt{a}" if m == 2 else f"\\sqrt[{m}]{{a}}"
    vals = bump_until_distinct([val, sp.Rational(n, m), m + n, n - m if n != m else n + m + 1])
    correct, wrong1, wrong2, wrong3 = (latex(v) for v in vals)
    de_bai = (
        f"Cho $a$ là số thực dương, $a\\neq 1$ và $P=\\log_{{{root}}} a^{{{n}}}$. "
        f"Mệnh đề nào dưới đây là đúng?\n\n"
    )
    lines, dap_an = render_mc([correct, wrong1, wrong2, wrong3], 0, prefix="P=")
    de_bai += "\n".join(lines)
    loi_giai = f"Ta có $P=\\log_{{a^{{1/{m}}}}}a^{{{n}}}=\\dfrac{{{n}}}{{1/{m}}}\\log_a a={val}$."
    return de_bai, dap_an, loi_giai, dict(m=str(m), n=str(n))


def verify_D20(params):
    m, n = sp.sympify(params["m"]), sp.sympify(params["n"])
    av = sp.Rational(13, 5)
    lhs = sp.log(av ** n, av ** (sp.Rational(1, m)))
    return abs(float(lhs - n * m)) < 1e-9


def expand_type(ma_dang, ten_dang, id_goc, gen_fn, verify_fn, sampler,
                verify_answer_count=False, target=90, max_tries=20000, seed=0):
    rng = random.Random(seed)
    seen_params, seen_questions = set(), set()
    made = 0
    for _ in range(max_tries):
        if made >= target:
            break
        args = sampler(rng)
        try:
            de_bai, dap_an, loi_giai, params = gen_fn(*args)
        except (AssertionError, ValueError, ZeroDivisionError):
            continue
        key = tuple(sorted(params.items()))
        if key in seen_params or de_bai in seen_questions:
            continue
        choices = re.findall(r"(?m)^([A-D])\.\s*(.+)$", de_bai)
        normalized = [re.sub(r"[\s$.,]", "", value) for _, value in choices]
        if len(choices) != 4 or {c for c, _ in choices} != set("ABCD") or len(set(normalized)) != 4:
            continue
        try:
            if verify_answer_count:
                match = re.search(r"\$\s*(-?\d+)\s*\$", dap_an)
                if not match or not verify_fn(params, int(match.group(1))):
                    continue
            elif not verify_fn(params):
                continue
        except Exception:
            continue
        add_row(ma_dang, ten_dang, id_goc, de_bai, dap_an, loi_giai, params)
        seen_params.add(key); seen_questions.add(de_bai); made += 1
    print(f"{ma_dang}: {made}/{target}")
    return made


def main():
    ROWS.clear()
    expand_type("D49", "Expand a logarithm of a quotient as a difference", "p110_q17",
                gen_D49, verify_D49, lambda r: (r.randint(2, 30), r.randint(2, 100)), seed=4901)
    expand_type("D20", "Evaluate a logarithm whose base and argument are powers of the same number", "p033_q13",
                gen_D20, verify_D20, lambda r: (r.randint(2, 12), r.randint(1, 30)), seed=2001)
    with open("data/questions/mu_logarit_extraction/bien_the/batch_identities_C.json", "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
