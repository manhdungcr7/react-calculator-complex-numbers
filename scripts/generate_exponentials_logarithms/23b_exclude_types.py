# -*- coding: utf-8 -*-
"""
Removes the excluded problem types (D31, D32) from the retained question
set and every derived file. Both types were dropped after a Qwen3-4B
zero-shot audit found generator-introduced defects (D31: two answer
options that are the same set; D32: variants where two options are
numerically equal), and from then on they are treated as non-existent.

Source-question files go 110 -> 107 questions and are written under the
Mu_Logarit_107_* names (the Mu_Logarit_112_* files stay as the
pre-exclusion snapshots kept for provenance). Run from the repo root.
"""
import json
import os

import pandas as pd

EXCLUDED = {"D31", "D32"}
Q = "data/questions/mu_logarit_extraction"
R = "data/results"


def git_rm(path):
    if os.path.exists(path):
        os.system(f'git rm -q -f "{path}"')


def main():
    phan = pd.read_csv(f"{Q}/Mu_Logarit_110_cau_phan_dang.csv", encoding="utf-8-sig")
    removed_ids = set(phan.loc[phan["Ma dang"].isin(EXCLUDED), "id"])
    print("source questions removed:", sorted(removed_ids))
    assert len(removed_ids) == 3

    # --- classification table (csv / jsonl / xlsx) ---
    keep = phan[~phan["Ma dang"].isin(EXCLUDED)].copy()
    keep["STT"] = range(1, len(keep) + 1)
    keep.to_csv(f"{Q}/Mu_Logarit_107_cau_phan_dang.csv", index=False, encoding="utf-8-sig")
    keep.to_excel(f"{Q}/Mu_Logarit_107_cau_phan_dang.xlsx", index=False)
    with open(f"{Q}/Mu_Logarit_110_cau_phan_dang.jsonl", encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    rows = [r for r in rows if r["Ma dang"] not in EXCLUDED]
    for i, r in enumerate(rows, start=1):
        r["STT"] = i
    with open(f"{Q}/Mu_Logarit_107_cau_phan_dang.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("phan_dang rows:", len(keep), len(rows))

    # --- source questions (csv / jsonl / xlsx) ---
    # the csv/xlsx identify a question as "Trang N - Cau M" (id p0NN_q0MM)
    labels = set()
    for i in removed_ids:
        page, num = i.split("_")
        labels.add((int(page[1:]), int(num[1:])))
    goc = pd.read_csv(f"{Q}/Mu_Logarit_110_cau_goc.csv", encoding="utf-8-sig")
    label_col = goc.columns[1]
    parsed = goc[label_col].str.extract(r"(\d+)\D+(\d+)").astype(int)
    drop = [(a, b) in labels for a, b in zip(parsed[0], parsed[1])]
    assert sum(drop) == 3, sum(drop)
    goc = goc[[not d for d in drop]].copy()
    goc["STT"] = range(1, len(goc) + 1)
    goc.to_csv(f"{Q}/Mu_Logarit_107_cau_goc.csv", index=False, encoding="utf-8-sig")
    goc.to_excel(f"{Q}/Mu_Logarit_107_cau_goc.xlsx", index=False)
    with open(f"{Q}/Mu_Logarit_110_cau_goc.jsonl", encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    rows = [r for r in rows if r["id"] not in removed_ids]
    with open(f"{Q}/Mu_Logarit_107_cau_goc.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("cau_goc rows:", len(goc), len(rows))

    # --- GPT-4o / Gemini answers on the source questions ---
    mh = pd.read_csv(f"{Q}/Mu_Logarit_110_cau_goc_ket_qua_mo_hinh.csv", encoding="utf-8-sig")
    mh = mh[~mh["id"].isin(removed_ids)]
    mh.to_csv(f"{Q}/Mu_Logarit_107_cau_goc_ket_qua_mo_hinh.csv", index=False, encoding="utf-8-sig")
    print("ket_qua_mo_hinh rows:", len(mh))

    # --- Qwen3-4B zero-shot on the source questions ---
    qw = pd.read_csv(f"{R}/qwen3_4b_zeroshot/ketqua_Qwen3-4B_think_mulogarit110.csv", encoding="utf-8-sig")
    qw = qw[~qw["id"].isin(removed_ids)]
    qw.to_csv(f"{R}/qwen3_4b_zeroshot/ketqua_Qwen3-4B_think_mulogarit107.csv", index=False, encoding="utf-8-sig")
    print("qwen 107 rows:", len(qw))

    # --- generated variants ---
    for fn in ("batch_basic_eq.json", "batch_identities_B.json"):
        p = f"{Q}/bien_the/{fn}"
        items = json.load(open(p, encoding="utf-8"))
        kept = [it for it in items if it["ma_dang"] not in EXCLUDED]
        json.dump(kept, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(fn, len(items), "->", len(kept))

    # --- Qwen3-4B zero-shot on the full variant set + stats ---
    base = f"{R}/qwen3_4b_zeroshot/full_dataset"
    full = pd.read_csv(f"{base}/ketqua_Qwen3-4B_zeroshot_mulogarit_full.csv", encoding="utf-8-sig")
    full = full[~full["ma_dang"].isin(EXCLUDED)]
    full.to_csv(f"{base}/ketqua_Qwen3-4B_zeroshot_mulogarit_full.csv", index=False, encoding="utf-8-sig")
    print("full results rows:", len(full))
    for fn in ("thong_ke_theo_dang.csv", "thong_ke_theo_dang_regraded.csv"):
        st = pd.read_csv(f"{base}/{fn}", encoding="utf-8-sig", index_col=0)
        st = st[~st.index.isin(EXCLUDED)]
        st.to_csv(f"{base}/{fn}", encoding="utf-8-sig")
        print(fn, len(st))

    # --- retire the 110-question files (112 snapshots stay) ---
    for ext in ("csv", "jsonl", "xlsx"):
        git_rm(f"{Q}/Mu_Logarit_110_cau_goc.{ext}")
        git_rm(f"{Q}/Mu_Logarit_110_cau_phan_dang.{ext}")
    git_rm(f"{Q}/Mu_Logarit_110_cau_goc_ket_qua_mo_hinh.csv")
    git_rm(f"{R}/qwen3_4b_zeroshot/ketqua_Qwen3-4B_think_mulogarit110.csv")
    git_rm(f"{R}/So_sanh_3_mo_hinh_110_cau_goc.csv")
    git_rm(f"{R}/So_sanh_3_mo_hinh_110_cau_goc.xlsx")


if __name__ == "__main__":
    main()
