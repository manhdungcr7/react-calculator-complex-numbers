"""
Gộp 66 câu số phức (đã có, từ So_phuc_60_mau.xlsx) + 41 câu chủ đề khác
(mới transcribe) thành 1 bảng đánh giá chất lượng chuyển đổi Markdown/LaTeX,
theo đúng yêu cầu của thầy:
    - Định danh câu hỏi
    - Chủ đề
    - Đề bài (chuyển đổi)
    - Đáp án (chuyển đổi)
    - Lời giải (chuyển đổi)
    - Nhận xét của A   (để trống, 1 bạn tự điền)
    - Nhận xét của B   (để trống, bạn kia tự điền)
    - Ghi chú lỗi chuyển sang markdown (để trống, ghi lại lỗi phát hiện được,
      KHÔNG sửa nội dung trong bảng này — giữ nguyên bản để đánh giá công cụ)
"""

import json

import pandas as pd

rows = []

# --- 66 câu số phức đã có sẵn ---
df_sp = pd.read_excel("So_phuc_60_mau.xlsx")
for _, r in df_sp.iterrows():
    rows.append({
        "Định danh": f"SP-{int(r['STT']):02d} ({r['Bài (Trang - Câu)']})",
        "Chủ đề": "Số phức",
        "Đề bài (chuyển đổi)": r["Đề bài"],
        "Đáp án (chuyển đổi)": r["Đáp án đúng"],
        "Lời giải (chuyển đổi)": r["Lời giải (theo tài liệu)"],
        "Nhận xét A": "",
        "Nhận xét B": "",
        "Ghi chú lỗi chuyển markdown": "",
    })

# --- 41 câu chủ đề khác ---
other = []
for b in ["batch1", "batch2", "batch3", "batch4"]:
    with open(f"Danh_gia_chuyen_doi_markdown/data/transcribe_{b}.json", encoding="utf-8") as f:
        other.extend(json.load(f))

# map lại chủ đề dựa theo (trang, cau) đã chọn ban đầu
topic_map = {}
import ast
for fname in ["selected_other_topics.txt", "selected_13_more.txt"]:
    with open(f"Danh_gia_chuyen_doi_markdown/data/{fname}", encoding="utf-8") as f:
        for line in f.readlines()[2:]:
            line = line.strip()
            if not line:
                continue
            page, cau, topic, _ = ast.literal_eval(line)
            topic_map[(page, int(cau))] = topic

for i, item in enumerate(other, start=1):
    topic = topic_map.get((item["trang"], item["cau"]), "Khác")
    rows.append({
        "Định danh": f"KT-{i:02d} (Trang {item['trang']} - Câu {item['cau']})",
        "Chủ đề": topic,
        "Đề bài (chuyển đổi)": item["de_bai"],
        "Đáp án (chuyển đổi)": item["dap_an"],
        "Lời giải (chuyển đổi)": item["loi_giai"],
        "Nhận xét A": "",
        "Nhận xét B": "",
        "Ghi chú lỗi chuyển markdown": "",
    })

df = pd.DataFrame(rows)
df.insert(0, "STT", range(1, len(df) + 1))

out_xlsx = "Danh_gia_chuyen_doi_markdown/Bang_danh_gia_chuyen_doi_markdown.xlsx"
out_csv = "Danh_gia_chuyen_doi_markdown/Bang_danh_gia_chuyen_doi_markdown.csv"
df.to_excel(out_xlsx, index=False)
df.to_csv(out_csv, index=False, encoding="utf-8-sig")

print("Tổng số mẫu:", len(df))
print("Theo chủ đề:")
print(df["Chủ đề"].value_counts())
