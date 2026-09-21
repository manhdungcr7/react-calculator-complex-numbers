import ast
from collections import defaultdict

candidates = []
with open('Danh_gia_chuyen_doi_markdown/data/other_topics_candidates.txt', encoding='utf-8') as f:
    lines = f.readlines()[2:]
for line in lines:
    line = line.strip()
    if not line:
        continue
    tup = ast.literal_eval(line)
    page, num, topic, has_hv, text = tup
    if has_hv:
        continue
    candidates.append((page, num, topic, text))

already_used = set()
with open('Danh_gia_chuyen_doi_markdown/data/selected_other_topics.txt', encoding='utf-8') as f:
    for line in f.readlines()[2:]:
        line = line.strip()
        if not line:
            continue
        page, num, topic, text = ast.literal_eval(line)
        already_used.add((page, num))

remaining = [c for c in candidates if (c[0], c[1]) not in already_used]
by_topic = defaultdict(list)
for c in remaining:
    by_topic[c[2]].append(c)

counts = {'Hàm số - Đạo hàm - Khảo sát': 4, 'Tích phân - Nguyên hàm': 3,
          'Hình giải tích Oxyz': 3, 'Hình học không gian': 3}

selected = []
for topic, n in counts.items():
    items = by_topic.get(topic, [])
    step = max(1, len(items) // n)
    picked = items[::step][:n]
    selected.extend(picked)

selected = selected[:13]
selected.sort(key=lambda x: (x[0], int(x[1])))

with open('Danh_gia_chuyen_doi_markdown/data/selected_13_more.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total selected: {len(selected)}\n\n')
    for s in selected:
        f.write(f'{s}\n')

print('selected', len(selected))
