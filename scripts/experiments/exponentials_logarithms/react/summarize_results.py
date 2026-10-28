# -*- coding: utf-8 -*-
"""Summary of the Kaggle result files of the ReAct + Calculator runs (one csv per type)."""
import glob
import sys

import pandas as pd

folder = sys.argv[1] if len(sys.argv) > 1 else "data/results/react_calculator_qwen3_4b"
EXPECTED = ("D89 D84 D47 D75 D69 D57 D93 D52 D65 D78 D68 D56 D28 D46 D23 D88 D41 D16 D24 D25 D94 D83 D71 D29 D22 "
            "D40 D51 D45 D08 D17 D10").split()
rows, found = [], set()
for path in sorted(glob.glob(f"{folder}/d*_react_calculator_full90.csv")):
    df = pd.read_csv(path, encoding="utf-8-sig")
    ma = df["ma_dang"].iloc[0]
    found.add(ma)
    rows.append({"ma_dang": ma, "tong": len(df), "dung": int(df["DUNG"].sum()),
                 "sai": int(((df["model_chon"] != "") & ~df["DUNG"]).sum()),
                 "kxd": int((df["model_chon"].fillna("") == "").sum()),
                 "calls_tb": round(df["tool_calls"].mean(), 1), "loi_cu_phap": int(df["syntax_errors"].sum()),
                 "stop": dict(df["stop_reason"].value_counts())})
out = pd.DataFrame(rows)
pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 80)
print(out.to_string(index=False))
print("missing types:", [t for t in EXPECTED if t not in found])
print("total correct:", int(out["dung"].sum()), "of", int(out["tong"].sum()))
