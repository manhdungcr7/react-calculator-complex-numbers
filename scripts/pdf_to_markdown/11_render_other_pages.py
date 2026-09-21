import ast
import fitz
import os

selected = []
with open('Danh_gia_chuyen_doi_markdown/data/selected_other_topics.txt', encoding='utf-8') as f:
    lines = f.readlines()[2:]
for line in lines:
    line = line.strip()
    if not line:
        continue
    tup = ast.literal_eval(line)
    selected.append(tup)

pages = sorted(set(s[0] for s in selected))
print('unique pages:', len(pages), pages)

doc = fitz.open('DAP AN.pdf')
os.makedirs('Danh_gia_chuyen_doi_markdown/pages', exist_ok=True)
for p in pages:
    page = doc[p-1]
    pix = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2))
    pix.save(f'Danh_gia_chuyen_doi_markdown/pages/page_{p:03d}.png')
print('rendered', len(pages), 'pages')
