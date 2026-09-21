"""
Tìm thêm các câu hỏi thuộc chủ đề KHÁC (không phải số phức) trong DAP AN.pdf,
để gộp với 66 câu số phức đã có, đủ >100 mẫu cho bảng đánh giá chất lượng
chuyển đổi Markdown/LaTeX theo yêu cầu của thầy.
"""
import re

with open('scratch/full_text.txt', encoding='utf-8') as f:
    lines = f.readlines()

# các trang đã dùng cho 66 câu số phức -> tránh trùng để đa dạng chủ đề
used_pages = {10,11,24,25,31,40,44,72,73,80,84,96,97,100,108,109,110,113,114,116,
              121,123,127,130,132,137,138,141,142,144,148,153,160,168,169,171,176,
              177,184,190,193,195,208,209,210,211,214,215,217,220,222,225,229,232,
              237,239,244,245}

TOPIC_KEYWORDS = {
    'Hàm số - Đạo hàm - Khảo sát': ['đồng biến', 'nghịch biến', 'cực trị', 'tiệm cận', 'đạo hàm'],
    'Tích phân - Nguyên hàm': ['tích phân', 'nguyên hàm'],
    'Mũ - Logarit': ['logarit', 'phương trình mũ', 'bất phương trình mũ'],
    'Hình học không gian': ['thể tích khối', 'khối chóp', 'khối lăng trụ', 'khối hộp'],
    'Hình giải tích Oxyz': ['mặt phẳng', 'mặt cầu', 'đường thẳng d', 'vectơ pháp tuyến', 'Oxyz'],
    'Xác suất - Tổ hợp': ['xác suất', 'tổ hợp', 'chỉnh hợp'],
    'Cấp số': ['cấp số cộng', 'cấp số nhân'],
}

page = 0
all_cau_idx = []
candidates = []
for i, line in enumerate(lines):
    m = re.match(r'--- PAGE (\d+) ---', line)
    if m:
        page = int(m.group(1))
        continue
    m = re.match(r'\s*Câu\s*(\d+):\s*(.*)', line)
    if m:
        all_cau_idx.append(i)
        if page in used_pages:
            continue
        if 'số phức' in line.lower():
            continue
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(kw.lower() in line.lower() for kw in keywords):
                candidates.append((page, i, m.group(1), topic, line.strip()))
                break

# check hinh ve trong block cua tung candidate
out = []
for page, i, num, topic, text in candidates:
    nexts = [x for x in all_cau_idx if x > i]
    end = min(nexts) if nexts else i + 40
    block = ''.join(lines[i:end])
    has_hv = 'hình vẽ' in block.lower()
    out.append((page, num, topic, has_hv, text[:100]))

with open('Danh_gia_chuyen_doi_markdown/data/other_topics_candidates.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total candidates: {len(out)}\n\n')
    for o in out:
        f.write(f'{o}\n')

print('done', len(out))
