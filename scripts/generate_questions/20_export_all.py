"""Gộp toàn bộ câu gốc (66) + câu nhân bản (các dạng) thành 1 file Excel/CSV
với các cột: STT, Dạng, Nguồn (Câu gốc/Nhân bản), STT câu gốc tương ứng,
Loại số (chỉ có với câu nhân bản), Đề bài, Đáp án đúng, Lời giải, và cột
"Nhận xét" (câu nhân bản phải Đạt kiểm tra sympy độc lập — xem 21_verify_all.py
— script sẽ raise lỗi và KHÔNG xuất file nếu có câu chưa đạt).
"""
import json
import sys

sys.path.insert(0, "Sinh_them_cau_hoi/scripts")
from importlib import import_module

import pandas as pd

verify = import_module("21_verify_all")

sys.stdout.reconfigure(encoding="utf-8")

DANG_MAP = {
    1: "Dạng 1 - Xác định phần thực, phần ảo, liên hợp, môđun",
    2: "Dạng 2 - Biểu diễn hình học",
    3: "Dạng 3 - Phép toán số phức",
    4: "Dạng 4 - Tìm số phức thỏa mãn điều kiện cho trước",
    5: "Dạng 5 - Tập hợp điểm biểu diễn (quỹ tích)",
    6: "Dạng 6 - Phương trình bậc hai có tham số",
    7: "Dạng 7 - Cực trị & vận dụng cao",
}

STT_GOC_THEO_DANG = {
    1: [1, 2, 9, 10, 15, 18, 22, 30, 34, 40, 43, 49, 50, 53, 58, 59, 62],
    2: [17, 20, 24, 28, 37, 44, 47, 51, 63],
    3: [3, 5, 16, 19, 21, 23, 29, 35, 48, 52, 57, 64],
    4: [6, 7, 8, 11, 14, 25, 38, 39, 42, 45, 54, 66],
    5: [4, 13, 31, 41, 46],
    6: [26, 33, 36, 56, 61],
    7: [12, 27, 32, 55, 60, 65],
}

df_goc = pd.read_excel("So_phuc_60_mau.xlsx")
stt_to_dang = {}
for dang_so, stts in STT_GOC_THEO_DANG.items():
    for s in stts:
        stt_to_dang[s] = DANG_MAP[dang_so]

rows = []
for _, r in df_goc.iterrows():
    stt = int(r["STT"])
    rows.append({
        "Dạng": stt_to_dang.get(stt, "Chưa phân loại"),
        "Nguồn": "Câu gốc",
        "STT câu gốc": stt,
        "Loại số": "",
        "Đề bài": r["Đề bài"],
        "Đáp án đúng": r["Đáp án đúng"],
        "Lời giải": r["Lời giải (theo tài liệu)"],
        "Nhận xét": "Đạt",
        "Ghi chú kiểm tra": "",
    })

# Câu nhân bản từng dạng (nạp dần khi đã sinh xong)
GENERATED_FILES = [
    ("Sinh_them_cau_hoi/data/dang1_full.json", 1),
    ("Sinh_them_cau_hoi/data/dang2_full.json", 2),
    ("Sinh_them_cau_hoi/data/dang3_full.json", 3),
    ("Sinh_them_cau_hoi/data/dang4_full.json", 4),
    ("Sinh_them_cau_hoi/data/dang5_full.json", 5),
    ("Sinh_them_cau_hoi/data/dang6_full.json", 6),
    ("Sinh_them_cau_hoi/data/dang7_full.json", 7),
]

for path, dang_so in GENERATED_FILES:
    try:
        with open(path, encoding="utf-8") as f:
            items = json.load(f)
    except FileNotFoundError:
        continue
    for it in items:
        status, note = verify.verify_row(it)
        if status != "Đạt":
            raise RuntimeError(
                f"STT_goc={it['stt_goc']} mau={it['mau_ta']} loai_so={it['loai_so']} "
                f"khong dat kiem tra ({status}: {note}) - dung xuat file cho den khi sua xong"
            )
        rows.append({
            "Dạng": DANG_MAP[dang_so],
            "Nguồn": "Nhân bản",
            "STT câu gốc": it["stt_goc"],
            "Loại số": it["loai_so"],
            "Đề bài": it["de_bai"],
            "Đáp án đúng": it["dap_an"],
            "Lời giải": it["loi_giai"],
            "Nhận xét": "Đạt",
            "Ghi chú kiểm tra": note,
        })

df = pd.DataFrame(rows)
df.insert(0, "STT", range(1, len(df) + 1))

df.to_excel("Sinh_them_cau_hoi/So_phuc_day_du.xlsx", index=False)
df.to_csv("Sinh_them_cau_hoi/So_phuc_day_du.csv", index=False, encoding="utf-8-sig")
print("Tong so dong:", len(df))
print(df["Dạng"].value_counts())
print(df["Nguồn"].value_counts())
print(df["Nhận xét"].value_counts())
