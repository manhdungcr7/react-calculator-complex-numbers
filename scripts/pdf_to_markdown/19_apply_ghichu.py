import json
import pandas as pd

df = pd.read_excel('Danh_gia_chuyen_doi_markdown/Bang_danh_gia_chuyen_doi_markdown.xlsx')
issues = json.load(open('Danh_gia_chuyen_doi_markdown/data/all_review_issues.json', encoding='utf-8'))

df['Ghi chú lỗi chuyển markdown'] = df['Ghi chú lỗi chuyển markdown'].astype(object)
for it in issues:
    idx = df[df['STT'] == it['stt']].index[0]
    ghi_chu = f"[{it['loai_van_de']}] {it['mo_ta']}"
    df.at[idx, 'Ghi chú lỗi chuyển markdown'] = ghi_chu

out_xlsx = 'Danh_gia_chuyen_doi_markdown/Bang_danh_gia_chuyen_doi_markdown_v2.xlsx'
out_csv = 'Danh_gia_chuyen_doi_markdown/Bang_danh_gia_chuyen_doi_markdown.csv'
df.to_excel(out_xlsx, index=False)
df.to_csv(out_csv, index=False, encoding='utf-8-sig')
print('updated', len(issues), 'rows, saved to', out_xlsx)
