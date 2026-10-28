# -*- coding: utf-8 -*-
"""
Merges the per-type CSVs downloaded from the 10 Kaggle Qwen3-4B zero-shot
runs (one zip per GROUP_ID, each containing <ma_dang>_zeroshot_full90_Qwen3-4B.csv
files) into one combined results file, then prints the overall and
per-type accuracy.
"""
import glob
import os
import pandas as pd

EXTRACTED_DIR = "data/results/qwen3_4b_zeroshot/full_dataset/_extracted"
OUT_CSV = "data/results/qwen3_4b_zeroshot/full_dataset/ketqua_Qwen3-4B_zeroshot_mulogarit_full.csv"
EXPECTED_TYPES = 89  # D31 and D32 were dropped
EXCLUDED_TYPES = {"D31", "D32"}
EXPECTED_PER_TYPE = 90


def main():
    paths = sorted(glob.glob(f"{EXTRACTED_DIR}/*/*_zeroshot_full90_Qwen3-4B.csv"))
    print(f"Tim thay {len(paths)} file CSV")

    dfs = []
    for p in paths:
        df = pd.read_csv(p, encoding="utf-8-sig")
        df["_src_file"] = os.path.basename(p)
        dfs.append(df)

    full = pd.concat(dfs, ignore_index=True)
    full = full[~full["ma_dang"].isin(EXCLUDED_TYPES)].reset_index(drop=True)
    full.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    print(f"Da gop {len(full)} cau vao {OUT_CSV}")

    counts = full["ma_dang"].value_counts()
    print(f"\nSo dang: {len(counts)} (ky vong {EXPECTED_TYPES})")
    bad = counts[counts != EXPECTED_PER_TYPE]
    if len(bad):
        print("Dang khong du 90 cau:")
        print(bad)
    else:
        print(f"Tat ca dang deu co du {EXPECTED_PER_TYPE} cau.")

    dup = full["ma_dang"].astype(str) + "|" + full["STT"].astype(str)
    n_dup = dup.duplicated().sum()
    print(f"\nSo dong trung (ma_dang+STT trung nhau): {n_dup}")

    print("\n" + "=" * 70)
    print(f"KET QUA TONG (ZERO-SHOT, Qwen3-4B, {len(full)} cau, {len(counts)} dang):")
    print(f"  Dung: {full['DUNG'].sum()} / {len(full)} ({full['DUNG'].mean()*100:.2f}%)")
    n_het_ngan_sach = full["het_ngan_sach"].sum() if "het_ngan_sach" in full.columns else None
    if n_het_ngan_sach is not None:
        print(f"  Cham gioi han token (het_ngan_sach=True): {n_het_ngan_sach} ({n_het_ngan_sach/len(full)*100:.2f}%)")
    print("=" * 70)

    per_type = full.groupby("ma_dang")["DUNG"].agg(["sum", "count", "mean"]).sort_values("mean")
    per_type.columns = ["dung", "tong", "ti_le"]
    print("\n--- Theo dang (sap xep tang dan ti le dung) ---")
    print(per_type.to_string(float_format=lambda v: f"{v*100:.1f}%" if v <= 1 else str(v)))


if __name__ == "__main__":
    main()
