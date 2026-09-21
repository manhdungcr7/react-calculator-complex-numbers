import ast

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

# group by topic, pick spread evenly (every ~4th item per topic) up to target count
from collections import defaultdict
by_topic = defaultdict(list)
for c in candidates:
    by_topic[c[2]].append(c)

target_per_topic = 8
selected = []
for topic, items in by_topic.items():
    step = max(1, len(items) // target_per_topic)
    picked = items[::step][:target_per_topic]
    selected.extend(picked)

selected.sort(key=lambda x: (x[0], int(x[1])))

with open('Danh_gia_chuyen_doi_markdown/data/selected_other_topics.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total selected: {len(selected)}\n\n')
    for s in selected:
        f.write(f'{s}\n')

print('selected', len(selected))
for topic in by_topic:
    cnt = sum(1 for s in selected if s[2]==topic)
    print(topic, cnt)
