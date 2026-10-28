# -*- coding: utf-8 -*-
"""Combines GPT-4o/Gemini/Qwen3-4B zero-shot results on the 107 retained
source questions into one table with DUNG/SAI/KXD per model, plus overall
tallies."""
import pandas as pd

GOC = "data/questions/mu_logarit_extraction/Mu_Logarit_107_cau_goc.csv"
MOHINH = "data/questions/mu_logarit_extraction/Mu_Logarit_107_cau_goc_ket_qua_mo_hinh.csv"
QWEN = "data/results/qwen3_4b_zeroshot/ketqua_Qwen3-4B_think_mulogarit107.csv"
PHAN_DANG = "data/questions/mu_logarit_extraction/Mu_Logarit_107_cau_phan_dang.csv"

OUT_CSV = "data/results/So_sanh_3_mo_hinh_107_cau_goc.csv"
OUT_XLSX = "data/results/So_sanh_3_mo_hinh_107_cau_goc.xlsx"


def normalize(label, chosen):
    """Map a model's raw status to DUNG / SAI / KXD."""
    chosen = str(chosen).strip()
    if chosen == "" or chosen.lower() == "nan" or chosen not in ("A", "B", "C", "D"):
        return "KXD"
    label = str(label).strip().lower()
    if "đúng" in label or label == "dung":
        return "DUNG"
    if "sai" in label:
        return "SAI"
    return "KXD"


def main():
    mohinh = pd.read_csv(MOHINH, encoding="utf-8")
    qwen = pd.read_csv(QWEN, encoding="utf-8")
    phan_dang = pd.read_csv(PHAN_DANG, encoding="utf-8")

    id_col = mohinh.columns[0]  # BOM-prefixed 'id' column
    mohinh = mohinh.rename(columns={id_col: "id"})
    qwen_id_col = qwen.columns[0]
    qwen = qwen.rename(columns={qwen_id_col: "id"})

    merged = mohinh[["id", "dap_an"]].merge(
        qwen[["id", "qwen_chon", "ket_qua"]], on="id", how="left"
    )
    merged = merged.merge(
        mohinh[["id", "ChatGPT chọn", "ChatGPT đúng/sai", "Gemini chọn", "Gemini đúng/sai"]],
        on="id", how="left",
    )
    merged = merged.merge(
        phan_dang[["id", "Ma dang", "Ten dang"]], on="id", how="left"
    )

    merged["GPT-4o"] = [normalize(l, c) for l, c in zip(merged["ChatGPT đúng/sai"], merged["ChatGPT chọn"])]
    merged["Gemini"] = [normalize(l, c) for l, c in zip(merged["Gemini đúng/sai"], merged["Gemini chọn"])]
    merged["Qwen3-4B"] = [normalize(l, c) for l, c in zip(merged["ket_qua"], merged["qwen_chon"])]

    out = merged[["id", "Ma dang", "Ten dang", "dap_an", "ChatGPT chọn", "GPT-4o",
                  "Gemini chọn", "Gemini", "qwen_chon", "Qwen3-4B"]].rename(columns={
        "dap_an": "dap_an_dung", "ChatGPT chọn": "GPT-4o_chon",
        "Gemini chọn": "Gemini_chon", "qwen_chon": "Qwen3-4B_chon",
    })
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    out.to_excel(OUT_XLSX, index=False)

    print(f"Tong so cau: {len(out)}")
    for model in ("GPT-4o", "Gemini", "Qwen3-4B"):
        counts = out[model].value_counts()
        dung = counts.get("DUNG", 0)
        sai = counts.get("SAI", 0)
        kxd = counts.get("KXD", 0)
        print(f"  {model}: DUNG={dung}  SAI={sai}  KXD={kxd}  ({dung/len(out)*100:.1f}% dung)")


if __name__ == "__main__":
    main()
