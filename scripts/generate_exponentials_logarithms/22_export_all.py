# -*- coding: utf-8 -*-
"""
Gop TOAN BO cau goc (107 cau, sau khi loai D31/D32) + bien the da sinh (pilot D01/D12/D18/D53 +
batch A/B/C) thanh 1 file CSV/Excel. Chi xuat neu moi bien the da qua kiem
tra doc lap tuong ung (khong kiem tra lai o day, cac script sinh da lam).
"""
import json

import pandas as pd

# D31 and D32 were dropped (see 23b_exclude_types.py); never export them again.
EXCLUDED_TYPES = {"D31", "D32"}

df_goc = pd.read_csv(
    "data/questions/mu_logarit_extraction/Mu_Logarit_107_cau_phan_dang.csv",
    encoding="utf-8-sig",
)

rows = []
for _, r in df_goc.iterrows():
    rows.append({
        "Mã dạng": r["Ma dang"],
        "Nguồn": "Câu gốc",
        "id_goc": r["id"],
        "Loại biến thể": "",
        "Đề bài": r["De bai"],
        "Đáp án đúng": r["Dap an dung"],
        "Lời giải": "",
    })

BIEN_THE_FILES = [
    "data/questions/mu_logarit_extraction/bien_the/D01_bien_the.json",
    "data/questions/mu_logarit_extraction/bien_the/D12_bien_the.json",
    "data/questions/mu_logarit_extraction/bien_the/D18_bien_the.json",
    "data/questions/mu_logarit_extraction/bien_the/D53_bien_the.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_identities_A.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_identities_B.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_basic_eq.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_counting.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_identities_C.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_round2.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_round3.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_round4.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_round5.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_round6.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_round7.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_round8.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_round9.json",
    "data/questions/mu_logarit_extraction/bien_the/batch_round10.json",
]

for path in BIEN_THE_FILES:
    with open(path, encoding="utf-8") as f:
        items = json.load(f)
    for it in items:
        if it["ma_dang"] in EXCLUDED_TYPES:
            continue
        rows.append({
            "Mã dạng": it["ma_dang"],
            "Nguồn": "Nhân bản",
            "id_goc": it["id_goc"],
            "Loại biến thể": it.get("loai_bien_the", ""),
            "Đề bài": it["de_bai"],
            "Đáp án đúng": it["dap_an"],
            "Lời giải": it["loi_giai"],
        })

df = pd.DataFrame(rows)
df.insert(0, "STT", range(1, len(df) + 1))

out_base = "data/questions/mu_logarit_extraction/bien_the/Mu_Logarit_bien_the_full"
df.to_csv(f"{out_base}.csv", index=False, encoding="utf-8-sig")
df.to_excel(f"{out_base}.xlsx", index=False)

with open("scripts/generate_questions/.tmp_export_all_output.txt", "w", encoding="utf-8") as f:
    f.write(f"Tong so dong: {len(df)}\n")
    f.write(f"So dang co bien the: {df[df['Nguồn']=='Nhân bản']['Mã dạng'].nunique()}\n")
    f.write(f"So dang tong cong trong bo cau hoi: {df['Mã dạng'].nunique()}\n")
    f.write(str(df["Nguồn"].value_counts()) + "\n")
