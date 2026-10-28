# -*- coding: utf-8 -*-
"""Per-type breakdown: DUNG (correct) / SAI (wrong but answered) / KXD (no
letter extracted, usually because the model hit the token budget mid-think)."""
import pandas as pd

SRC = "data/results/qwen3_4b_zeroshot/full_dataset/ketqua_Qwen3-4B_zeroshot_mulogarit_full.csv"
OUT = "data/results/qwen3_4b_zeroshot/full_dataset/thong_ke_theo_dang.csv"


def main():
    df = pd.read_csv(SRC, encoding="utf-8-sig")
    df["model_chon"] = df["model_chon"].fillna("")
    df["kxd"] = df["model_chon"] == ""
    df["sai"] = (~df["DUNG"]) & (~df["kxd"])

    g = df.groupby("ma_dang").agg(
        tong=("STT", "count"),
        dung=("DUNG", "sum"),
        kxd=("kxd", "sum"),
    )
    g["sai"] = g["tong"] - g["dung"] - g["kxd"]
    g["ti_le_dung"] = (g["dung"] / g["tong"] * 100).round(1)
    g = g[["tong", "dung", "sai", "kxd", "ti_le_dung"]].sort_values("ti_le_dung")

    g.to_csv(OUT, encoding="utf-8-sig")

    print(f"Tong: {len(df)} cau, {len(g)} dang")
    print(f"  DUNG: {df['DUNG'].sum()}  SAI: {df['sai'].sum()}  KXD: {df['kxd'].sum()}")
    print()
    print(g.to_string())


if __name__ == "__main__":
    main()
