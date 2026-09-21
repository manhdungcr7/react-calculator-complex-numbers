import json
import pandas as pd

df = pd.read_excel('Danh_gia_chuyen_doi_markdown/Bang_danh_gia_chuyen_doi_markdown.xlsx')

# map dinh danh -> trang, duong dan anh
records = []
for _, r in df.iterrows():
    dinh_danh = r['Định danh']
    if dinh_danh.startswith('SP-'):
        # vd: "SP-01 (Trang 10 - Câu 29)"
        inside = dinh_danh.split('(')[1].rstrip(')')
        trang = int(inside.split('Trang')[1].split('-')[0].strip())
        img_dir = 'scratch/pages'
    else:
        inside = dinh_danh.split('(')[1].rstrip(')')
        trang = int(inside.split('Trang')[1].split('-')[0].strip())
        img_dir = 'Danh_gia_chuyen_doi_markdown/pages'
    img_path = f'{img_dir}/page_{trang:03d}.png'
    records.append({
        'stt': int(r['STT']),
        'dinh_danh': dinh_danh,
        'chu_de': r['Chủ đề'],
        'trang': trang,
        'anh': img_path,
        'de_bai': r['Đề bài (chuyển đổi)'],
        'dap_an': r['Đáp án (chuyển đổi)'],
        'loi_giai': r['Lời giải (chuyển đổi)'],
    })

with open('Danh_gia_chuyen_doi_markdown/data/review_export.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)
print('exported', len(records))
