import json

d = json.load(open('Danh_gia_chuyen_doi_markdown/data/review_export.json', encoding='utf-8'))
d.sort(key=lambda r: r['stt'])

n = len(d)
batch_size = 30
batches = [d[i:i+batch_size] for i in range(0, n, batch_size)]

for i, batch in enumerate(batches, start=1):
    stts = [r['stt'] for r in batch]
    imgs = sorted(set(r['anh'] for r in batch))
    with open(f'Danh_gia_chuyen_doi_markdown/data/review_batch{i}_info.txt', 'w', encoding='utf-8') as f:
        f.write(f'STT range: {stts}\n\n')
        f.write('Images:\n')
        for img in imgs:
            f.write(f'F:\Math\{img.replace("/", chr(92))}\n')
    print(f'batch{i}: {len(stts)} items, {len(imgs)} unique images')
