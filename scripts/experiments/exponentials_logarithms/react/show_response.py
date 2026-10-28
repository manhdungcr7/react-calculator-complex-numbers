# -*- coding: utf-8 -*-
"""Print the beginning of one model response (full_text) of a Kaggle result file.

    python scripts/experiments/react/show_response.py D57 7 [n_chars] [folder]
"""
import sys

import pandas as pd

ma, stt = sys.argv[1], int(sys.argv[2])
n = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
folder = sys.argv[4] if len(sys.argv) > 4 else "data/results/react_calculator_qwen3_4b"
df = pd.read_csv(f"{folder}/{ma.lower()}_react_calculator_full90.csv", encoding="utf-8-sig")
row = df[df["STT"] == stt].iloc[0]
print(row["full_text"][:n])
