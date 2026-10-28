# -*- coding: utf-8 -*-
"""Print the wrong questions of one type with the tool log and the program the method expects.

    python scripts/experiments/react/show_fail.py D40 [max_questions] [folder]
"""
import importlib
import json
import sys

import pandas as pd

sys.path.insert(0, "scripts/experiments/react")
import framework as fw  # noqa: E402

ma = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 6
folder = sys.argv[3] if len(sys.argv) > 3 else "data/results/react_calculator_qwen3_4b"
df = pd.read_csv(f"{folder}/{ma.lower()}_react_calculator_full90.csv", encoding="utf-8-sig")
data = json.load(open("scripts/experiments/plan_solve_prompts_mulogarit_merged.json", encoding="utf-8"))[ma]
dang = importlib.import_module(f"dang_{ma}")
bad = df[~df["DUNG"]]
print(f"{ma}: {len(bad)} wrong of {len(df)}")
for _, r in bad.head(limit).iterrows():
    rec = next(x for x in data if x["STT"] == r["STT"])
    print("=" * 100)
    print("STT", r["STT"], "key", r["dap_an_dung"], "model", r["model_chon"], "calls", r["tool_calls"], "errors", r["syntax_errors"], r["stop_reason"])
    print(rec["de_bai_mcq"])
    print("--- expected commands:")
    for c in fw.full_program(dang, rec["de_bai_mcq"]):
        print("   ", c)
    print("--- model tool log:")
    for part in str(r["tool_log"]).split(" | "):
        print("   ", part[:260])
    tail = str(r["full_text"])
    print("--- last 500 chars of the response:")
    print(tail[-500:])
