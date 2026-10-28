# -*- coding: utf-8 -*-
"""
Prepares the merged JSON used by the Qwen3-4B zero-shot full-90 Kaggle
notebooks, following the exact same record shape used for the Complex
Numbers (so_phuc) zero-shot experiments: one JSON file, keyed by Ma dang,
each value a list of records with STT / ma_dang / dap_an_letter / de_bai_mcq.

Only the generated variants are included (Nguon == "Nhan ban"), not the
110 retained source questions, matching the so_phuc "full90" convention
(each type contributes its 90 variants, not the original question).
"""
import json
import re
import pandas as pd

SRC = "data/questions/mu_logarit_extraction/bien_the/Mu_Logarit_bien_the_full.csv"
OUT_MERGED = "scripts/experiments/plan_solve_prompts_mulogarit_merged.json"
OUT_SPLIT_INFO = "scripts/experiments/mulogarit_group_split.json"
N_GROUPS = 10


def extract_letter(dap_an_dung):
    m = re.match(r"\s*([A-D])\b", str(dap_an_dung))
    return m.group(1) if m else ""


def main():
    df = pd.read_csv(SRC)
    df = df[df["Nguồn"] == "Nhân bản"].reset_index(drop=True)

    grouped = {}
    for ma_dang, sub in df.groupby("Mã dạng"):
        records = []
        for i, d in enumerate(sub.to_dict("records"), start=1):
            records.append({
                "STT": i,
                "ma_dang": ma_dang,
                "dap_an_letter": extract_letter(d["Đáp án đúng"]),
                "de_bai_mcq": d["Đề bài"],
            })
        grouped[ma_dang] = records

    with open(OUT_MERGED, "w", encoding="utf-8") as f:
        json.dump(grouped, f, ensure_ascii=False)

    types = sorted(grouped.keys(), key=lambda s: (len(s), s))
    counts = {t: len(grouped[t]) for t in types}
    total = sum(counts.values())
    print(f"Tong so dang: {len(types)}, tong so cau: {total}")
    bad = [t for t, c in counts.items() if c != 90]
    print("Dang khong du 90:", bad if bad else "khong co")

    # Split into N_GROUPS roughly-equal, contiguous groups by TYPE COUNT (not
    # question count) so each Kaggle account loads the model once and runs a
    # comparable number of types; 91 types / 10 groups ~= 9 types/group.
    sizes = [len(types) // N_GROUPS + (1 if i < len(types) % N_GROUPS else 0) for i in range(N_GROUPS)]
    groups = []
    idx = 0
    for s in sizes:
        groups.append(types[idx:idx + s])
        idx += s

    split_info = {f"group{i+1}": g for i, g in enumerate(groups)}
    with open(OUT_SPLIT_INFO, "w", encoding="utf-8") as f:
        json.dump(split_info, f, ensure_ascii=False, indent=2)

    for name, g in split_info.items():
        n_q = sum(counts[t] for t in g)
        print(f"{name}: {len(g)} dang ({g[0]}..{g[-1]}), {n_q} cau")


if __name__ == "__main__":
    main()
