# -*- coding: utf-8 -*-
"""Robustness check: the model may write the commands with different spacing or with ^ for powers.
Each command of the method is replayed with (a) all spaces removed and (b) '**' written as '^', and the matched
letter must not change."""
import importlib
import json
import sys

sys.path.insert(0, "scripts/experiments/react")
import calculator_backend as backend  # noqa: E402
import framework as fw  # noqa: E402

TYPES = ("D89 D84 D47 D75 D69 D57 D93 D52 D65 D78 D68 D56 D28 D46 D23 D88 D41 D16 D24 D25 D94 D83 D71 D29 D22 D40 "
         "D51 D45 D08 D17 D10").split()
data = json.load(open("scripts/experiments/plan_solve_prompts_mulogarit_merged.json", encoding="utf-8"))


def run(dang, cmds):
    calc = backend.Calculator(free_unknowns=dang.FREE_UNKNOWNS)
    for c in cmds:
        _, err = calc.evaluate(c)
        if err:
            return None, err
    return [k for k in "ABCD" if bool(calc.ns[f"test_{k}"])], None


bad = 0
for ma in TYPES:
    dang = importlib.import_module(f"dang_{ma}")
    for rec in data[ma][::9]:                       # 10 questions per type
        cmds = fw.full_program(dang, rec["de_bai_mcq"])
        base, _ = run(dang, cmds)
        for name, f in (("no spaces", lambda c: c.replace(" ", "")), ("caret", lambda c: c.replace("**", "^"))):
            got, err = run(dang, [f(c) for c in cmds])
            if got != base:
                bad += 1
                print(f"{ma} STT {rec['STT']} [{name}] -> {got} {err}")
                break
print("variants that changed the result:", bad)
