"""
Gop cau goc (15 cau, D01/D12/D18/D53) + bien the da sinh thanh 1 file
CSV/Excel. Dung lai 20_verify_pilot.py de kiem tra doc lap; KHONG xuat file
neu co bat ky cau nao chua dat.
"""
import json
import sys
from importlib import import_module

import pandas as pd

verify = import_module("20_verify_pilot")
sys.path.insert(0, "scripts/generate_questions")

GOC_IDS = {
    "D01": ["p006_q12", "p079_q06", "p109_q10", "p191_q08", "p210_q27"],
    "D12": ["p020_q13", "p093_q03", "p172_q13", "p192_q13"],
    "D18": ["p031_q02", "p111_q22", "p121_q02"],
    "D53": ["p006_q14", "p124_q21", "p221_q08", "p236_q12"],
}

df_goc = pd.read_csv(
    "data/questions/mu_logarit_extraction/Mu_Logarit_110_cau_phan_dang.csv",
    encoding="utf-8-sig",
)

rows = []
for ma_dang, ids in GOC_IDS.items():
    for id_goc in ids:
        r = df_goc[df_goc["id"] == id_goc].iloc[0]
        rows.append({
            "Mã dạng": ma_dang,
            "Nguồn": "Câu gốc",
            "id_goc": id_goc,
            "Loại biến thể": "",
            "Đề bài": r["De bai"],
            "Đáp án đúng": r["Dap an dung"],
            "Lời giải": "",
            "Kiểm tra độc lập": "Đạt (câu gốc)",
        })

BIEN_THE_FILES = [
    "data/questions/mu_logarit_extraction/bien_the/D01_bien_the.json",
    "data/questions/mu_logarit_extraction/bien_the/D12_bien_the.json",
    "data/questions/mu_logarit_extraction/bien_the/D18_bien_the.json",
    "data/questions/mu_logarit_extraction/bien_the/D53_bien_the.json",
]

for path in BIEN_THE_FILES:
    with open(path, encoding="utf-8") as f:
        items = json.load(f)
    for it in items:
        status, note = verify.verify_row(it)
        if status != "Đạt":
            raise RuntimeError(
                f"id_goc={it['id_goc']} ma_dang={it['ma_dang']} params={it['params']} "
                f"khong dat kiem tra ({status}: {note}) - dung xuat file cho den khi sua xong"
            )
        rows.append({
            "Mã dạng": it["ma_dang"],
            "Nguồn": "Nhân bản",
            "id_goc": it["id_goc"],
            "Loại biến thể": it["loai_bien_the"],
            "Đề bài": it["de_bai"],
            "Đáp án đúng": it["dap_an"],
            "Lời giải": it["loi_giai"],
            "Kiểm tra độc lập": "Đạt",
        })

df = pd.DataFrame(rows)
df.insert(0, "STT", range(1, len(df) + 1))

out_base = "data/questions/mu_logarit_extraction/bien_the/Mu_Logarit_thi_diem_4dang_bien_the"
df.to_csv(f"{out_base}.csv", index=False, encoding="utf-8-sig")
df.to_excel(f"{out_base}.xlsx", index=False)

with open("scripts/generate_questions/.tmp_export_output.txt", "w", encoding="utf-8") as f:
    f.write(f"Tong so dong: {len(df)}\n")
    f.write(str(df["Mã dạng"].value_counts()) + "\n")
    f.write(str(df["Nguồn"].value_counts()) + "\n")
