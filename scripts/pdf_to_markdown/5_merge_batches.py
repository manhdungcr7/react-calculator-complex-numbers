import json
import pandas as pd

all_items = []
for b in ['batch1', 'batch2', 'batch3']:
    with open(f'scratch/{b}.json', encoding='utf-8') as f:
        all_items.extend(json.load(f))

# fix known error: trang 40, cau 39 -> dap_an should be C (4 so phuc), solution says 4
for item in all_items:
    if item['trang'] == 40 and item['cau'] == 39:
        item['dap_an'] = 'C. 4.'

# sort by page then cau
all_items.sort(key=lambda x: (x['trang'], x['cau']))

rows = []
for i, item in enumerate(all_items, start=1):
    rows.append({
        'STT': i,
        'Bài (Trang - Câu)': f"Trang {item['trang']} - Câu {item['cau']}",
        'Đề bài': item['de_bai'],
        'Đáp án đúng': item['dap_an'],
        'Lời giải (theo tài liệu)': item['loi_giai'],
        'Lời giải ChatGPT': '',
        'Nhận xét ChatGPT': '',
        'Lời giải Gemini': '',
        'Nhận xét Gemini': '',
        'Lời giải Qwen': '',
        'Nhận xét Qwen': '',
    })

df = pd.DataFrame(rows)
df.to_excel('So_phuc_60_mau.xlsx', index=False)
df.to_csv('So_phuc_60_mau.csv', index=False, encoding='utf-8-sig')
print('Total rows:', len(df))
