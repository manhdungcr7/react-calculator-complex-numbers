import re

with open('scratch/full_text.txt', encoding='utf-8') as f:
    lines = f.readlines()

page = 0
candidates = []
for i, line in enumerate(lines):
    m = re.match(r'--- PAGE (\d+) ---', line)
    if m:
        page = int(m.group(1))
        continue
    m = re.match(r'\s*Câu\s*(\d+):\s*(.*)', line)
    if m and 'số phức' in line.lower():
        candidates.append((page, i+1, m.group(1), line.strip()))

with open('scratch/candidates.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total candidates: {len(candidates)}\n')
    for c in candidates:
        f.write(f'{c}\n')
print(f'Total candidates: {len(candidates)}')
