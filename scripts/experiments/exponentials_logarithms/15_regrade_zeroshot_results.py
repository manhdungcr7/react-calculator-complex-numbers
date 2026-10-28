# -*- coding: utf-8 -*-
"""Post-hoc re-grading of the Qwen3-4B zero-shot run.

The notebook's get_letter() (copied unchanged from the Complex Numbers
experiments) only recognises "Đáp án đúng: X" within 15 characters and
\\boxed{X}. Qwen3-4B frequently ends with \\boxed{\\text{X}} or
\\boxed{\\text{X. 20}}, which that regex misses, so those answers were
recorded as KXD. This script re-extracts the final letter with a wider
pattern and writes the result to NEW columns, leaving the original
model_chon / DUNG untouched so the original protocol stays reproducible.
"""
import re
import pandas as pd

SRC = "data/results/qwen3_4b_zeroshot/full_dataset/ketqua_Qwen3-4B_zeroshot_mulogarit_full.csv"
OUT = "data/results/qwen3_4b_zeroshot/full_dataset/ketqua_Qwen3-4B_zeroshot_mulogarit_full_regraded.csv"
OUT_STATS = "data/results/qwen3_4b_zeroshot/full_dataset/thong_ke_theo_dang_regraded.csv"

ORIGINAL_1 = re.compile(r"[Đđ]áp\s*án[^A-D]{0,15}([A-D])\b")
ORIGINAL_2 = re.compile(r"\\boxed\{([A-D])\}")
BOXED_TEXT = re.compile(r"\\boxed\{\s*(?:\\text\{\s*)?([A-D])\b")


def extract_original(after):
    m = ORIGINAL_1.findall(after)
    if m:
        return m[-1]
    m = ORIGINAL_2.findall(after)
    return m[-1] if m else ""


def extract_wide(after):
    letter = extract_original(after)
    if letter:
        return letter
    m = BOXED_TEXT.findall(after)
    return m[-1] if m else ""


def main():
    df = pd.read_csv(SRC, encoding="utf-8-sig")
    df["after"] = df["after"].fillna("")
    df["model_chon"] = df["model_chon"].fillna("")
    df["model_chon_moi"] = df["after"].map(extract_wide)

    # the wide extractor must agree with the original wherever the original found a letter
    both = df[(df["model_chon"] != "") & (df["model_chon_moi"] != "")]
    assert (both["model_chon"] == both["model_chon_moi"]).all()

    df["DUNG_moi"] = df["model_chon_moi"] == df["dap_an_dung"]
    df["kxd_moi"] = df["model_chon_moi"] == ""
    df["sai_moi"] = (~df["DUNG_moi"]) & (~df["kxd_moi"])
    df.to_csv(OUT, index=False, encoding="utf-8-sig")

    changed = df[df["model_chon"] != df["model_chon_moi"]]
    print(f"Cau doi ket qua sau khi mo rong bo trich xuat: {len(changed)}")
    print(changed.groupby("ma_dang").size().to_string())
    print(f"  trong do KXD -> DUNG: {int((changed['DUNG_moi']).sum())}, KXD -> SAI: {int((changed['sai_moi']).sum())}")

    print()
    print("Ket qua goc  : DUNG=%d SAI=%d KXD=%d" % (
        int(df["DUNG"].sum()), int(((~df["DUNG"]) & (df["model_chon"] != "")).sum()), int((df["model_chon"] == "").sum())))
    print("Ket qua moi  : DUNG=%d SAI=%d KXD=%d" % (
        int(df["DUNG_moi"].sum()), int(df["sai_moi"].sum()), int(df["kxd_moi"].sum())))

    g = df.groupby("ma_dang").agg(tong=("STT", "count"), dung=("DUNG_moi", "sum"), kxd=("kxd_moi", "sum"))
    g["sai"] = g["tong"] - g["dung"] - g["kxd"]
    g["ti_le_dung"] = (g["dung"] / g["tong"] * 100).round(1)
    g = g[["tong", "dung", "sai", "kxd", "ti_le_dung"]].sort_values("ti_le_dung")
    g.to_csv(OUT_STATS, encoding="utf-8-sig")
    print()
    print("So dang chua dat 100% (sau cham lai):", int((g["dung"] < g["tong"]).sum()))


if __name__ == "__main__":
    main()
