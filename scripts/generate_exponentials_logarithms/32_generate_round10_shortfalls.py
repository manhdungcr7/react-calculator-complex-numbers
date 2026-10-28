# -*- coding: utf-8 -*-
"""Add independently verified numerical variants for D43 and D51."""
import importlib.util
import json
import random
import re
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/questions/mu_logarit_extraction/bien_the"
OUT = DATA / "batch_round10.json"


def load_module(filename):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


basic = load_module("17_generate_basic_eq.py")
utils = basic.utils


def question_signature(text):
    stem, _, choices = text.partition("\n\n")
    options = re.findall(r"(?m)^([A-D])\.\s*(.+)$", choices)
    normalize = lambda value: re.sub(r"\s+", "", value.strip().strip("$."))
    return normalize(stem), tuple(sorted(normalize(value) for _, value in options))


def question_rows(code):
    rows = []
    for path in sorted(DATA.glob("*.json")):
        if path == OUT:
            continue
        rows.extend(row for row in json.loads(path.read_text(encoding="utf-8"))
                    if row.get("ma_dang") == code)
    return rows


def check_choices(row):
    choices = re.findall(r"(?m)^([A-D])\.\s*(.+)$", row["de_bai"])
    assert len(choices) == 4 and {letter for letter, _ in choices} == set("ABCD")
    assert len({re.sub(r"[\s$.,]", "", value) for _, value in choices}) == 4
    letter = row["dap_an"][:1]
    assert next(line for line in row["de_bai"].splitlines() if line.startswith(letter + ". ")) == row["dap_an"]


def verify_D43(row):
    k = sp.Rational(row["params"]["k"])
    x = sp.Symbol("x", positive=True)
    solution = sp.solve_univariate_inequality(sp.log(x, 10) >= k, x, relational=False)
    expected = sp.Interval(10 ** k, sp.oo)
    assert solution == expected
    value_tex = utils.latex(10 ** k)
    expected_text = f"[{value_tex};+\\infty)"
    chosen = row["dap_an"].split("$", 1)[1].rsplit("$", 1)[0]
    assert expected_text in chosen
    check_choices(row)
    return True


def verify_D51(row):
    p = row["params"]
    u, v, c, d = (int(p[key]) for key in ("u", "v", "c", "d"))
    F, D, N = (int(p[key]) for key in ("F", "D", "N"))
    assert 4 * c == 2 ** u + 2 ** v and d == 2 ** (u + v) and 2 <= u < v <= N
    assert 10 ** D // F == N and 10 ** D % F == 0
    # Count the integers directly from the generated inequality.
    actual = 0
    for xv in range(1, N + 1):
        sqrt_defined = F * xv <= 10 ** D
        polynomial = 4 ** xv - c * 2 ** (xv + 2) + d
        if sqrt_defined and (polynomial >= 0 or xv == N):
            actual += 1
    expected = u + N - v + 1
    assert actual == expected
    answer_value = int(re.findall(r"-?\d+", row["dap_an"])[-1])
    assert answer_value == actual
    check_choices(row)
    return True


def make_D51(u, v, F=2, D=3):
    assert 2 <= u < v <= 14
    N, rem = divmod(10 ** D, F)
    assert rem == 0 and N >= v
    c = (2 ** u + 2 ** v) // 4
    d = 2 ** (u + v)
    count = u + N - v + 1
    vals = utils.bump_until_distinct([sp.Integer(count), sp.Integer(count + 1),
                                      sp.Integer(count - 1), sp.Integer(N)])
    lines, answer = utils.render_mc([str(value) for value in vals], 0)
    question = (
        f"C\u00f3 bao nhi\u00eau s\u1ed1 nguy\u00ean $x$ th\u1ecfa m\u00e3n "
        f"$(4^x-{c}\\cdot2^{{x+2}}+{d})\\sqrt{{{D}-\\log({F}x)}}\\ge0$?\n\n"
        + "\n".join(lines)
    )
    solution = (
        f"\u0110i\u1ec1u ki\u1ec7n x\u00e1c \u0111\u1ecbnh: $0<x\\le {N}$. "
        f"\u0110\u1eb7t $t=2^x>0$, ta c\u00f3 "
        f"$4^x-{c}\\cdot2^{{x+2}}+{d}=t^2-(2^{{{u}}}+2^{{{v}}})t+2^{{{u+v}}}="
        f"(t-2^{{{u}}})(t-2^{{{v}}})$. V\u00ec $t=2^x$ t\u0103ng, b\u1ea5t ph\u01b0\u01a1ng tr\u00ecnh "
        f"t\u01b0\u01a1ng \u0111\u01b0\u01a1ng $x\\le {u}$ ho\u1eb7c $x\\ge {v}$. "
        f"C\u0103n th\u1ee9c d\u01b0\u01a1ng khi $x<{N}$; t\u1ea1i $x={N}$, \u0111a th\u1ee9c d\u01b0\u01a1ng v\u00ec ${N}\\ge {v}$. "
        f"Do \u0111\u00f3, k\u1ebft h\u1ee3p \u0111i\u1ec1u ki\u1ec7n x\u00e1c \u0111\u1ecbnh, c\u00e1c s\u1ed1 nguy\u00ean th\u1ecfa m\u00e3n "
        f"l\u00e0 $1,\\ldots,{u}$ v\u00e0 ${v},\\ldots,{N}$, c\u00f3 ${u}+({N}-{v}+1)={count}$ s\u1ed1."
    )
    row = {
        "id_goc": "p115_q39", "ma_dang": "D51",
        "ten_dang": "\u0110\u1ebfm s\u1ed1 nguy\u00ean th\u1ecfa b\u1ea5t ph\u01b0\u01a1ng tr\u00ecnh m\u0169-l\u00f4garit-c\u0103n ph\u1ee9c h\u1ee3p",
        "nguon": "Nh\u00e2n b\u1ea3n", "loai_bien_the": "chuan",
        "de_bai": question, "dap_an": answer, "loi_giai": solution,
        "params": {"u": str(u), "v": str(v), "c": str(c), "d": str(d),
                   "F": str(F), "D": str(D), "N": str(N), "expected": str(count)},
    }
    assert verify_D51(row)
    return row


def main():
    random.seed(510430)
    old43 = question_rows("D43")
    old51 = question_rows("D51")
    originals = {json.loads(line)["id"]: json.loads(line)["de_bai"]
                 for line in (ROOT / "data/questions/mu_logarit_extraction/Mu_Logarit_110_cau_goc.jsonl").read_text(encoding="utf-8").splitlines()}
    seen43 = {question_signature(row["de_bai"]) for row in old43} | {question_signature(originals["p095_q16"])}
    seen43_k = {sp.Rational(row["params"]["k"]) for row in old43}
    seen51 = {question_signature(row["de_bai"]) for row in old51} | {question_signature(originals["p115_q39"])}
    new_rows = []

    # Keep the threshold in [-10, 10] and represent it exactly.
    ks = [sp.Rational(n) for n in range(-10, 11)]
    ks += [sp.Rational(n, 2) for n in range(-19, 20) if n % 2]
    ks += [sp.Rational(n, 3) for n in range(-29, 30) if n % 3]
    ks += [sp.Rational(n, 4) for n in range(-39, 40) if n % 2]
    ks += [sp.Rational(n, 5) for n in range(-49, 50) if n % 5]
    ks = list(dict.fromkeys(ks))
    for k in ks:
        if len(old43) + sum(row["ma_dang"] == "D43" for row in new_rows) >= 90:
            break
        if k in seen43_k:
            continue
        generated = basic.gen_D43(k)
        row = {
            "id_goc": "p095_q16", "ma_dang": "D43",
            "ten_dang": "Gi\u1ea3i b\u1ea5t ph\u01b0\u01a1ng tr\u00ecnh l\u00f4garit c\u01a1 b\u1ea3n (l\u00f4garit th\u1eadp ph\u00e2n)",
            "nguon": "Nh\u00e2n b\u1ea3n", "loai_bien_the": "chuan",
            "de_bai": generated[0], "dap_an": generated[1],
            "loi_giai": generated[2], "params": generated[3],
        }
        signature = question_signature(row["de_bai"])
        if signature in seen43:
            continue
        assert verify_D43(row)
        seen43.add(signature)
        seen43_k.add(k)
        new_rows.append(row)
    added43 = sum(row["ma_dang"] == "D43" for row in new_rows)
    assert len(old43) + added43 == 90, (len(old43), added43)

    pairs = [(u, v) for u in range(2, 9) for v in range(u + 2, 15)]
    added51 = 0
    for u, v in pairs:
        if len(old51) + added51 >= 90:
            break
        row = make_D51(u, v)
        signature = question_signature(row["de_bai"])
        if signature in seen51:
            continue
        seen51.add(signature)
        new_rows.append(row)
        added51 += 1
    assert len(old51) + added51 == 90, (len(old51), added51)
    assert len(new_rows) == added43 + added51
    OUT.write_text(json.dumps(new_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"D43: {len(old43)} + {added43} = 90; D51: {len(old51)} + {added51} = 90")
    print(f"Wrote {len(new_rows)} independently verified rows to {OUT}")


if __name__ == "__main__":
    main()
