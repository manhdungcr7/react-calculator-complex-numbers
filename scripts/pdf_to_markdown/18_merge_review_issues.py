import json

all_issues = []
for i in range(1, 5):
    with open(f'Danh_gia_chuyen_doi_markdown/data/review_issues_batch{i}.json', encoding='utf-8') as f:
        all_issues.extend(json.load(f))

with open('Danh_gia_chuyen_doi_markdown/data/all_review_issues.json', 'w', encoding='utf-8') as f:
    json.dump(all_issues, f, ensure_ascii=False, indent=2)

with open('Danh_gia_chuyen_doi_markdown/data/review_summary.txt', 'w', encoding='utf-8') as f:
    f.write(f'Tong so cau co van de: {len(all_issues)} / 120\n\n')
    for it in all_issues:
        f.write(f"STT {it['stt']} ({it['dinh_danh']}) - {it['loai_van_de']}\n")
        f.write(f"  {it['mo_ta']}\n\n")

print('total issues:', len(all_issues))
