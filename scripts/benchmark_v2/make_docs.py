import csv, random, collections, sys, re
sys.stdout.reconfigure(encoding='utf-8')
import frames as F
rows = list(csv.DictReader(open('F:/Math/data/questions/benchmark_so_phuc_v2_24dang_2160cau.csv', encoding='utf-8-sig')))
out = ['# Benchmark Số phức v2 – so sánh đề v1 và v2 (mẫu)\n',
       'Mỗi dạng lấy 4 câu ngẫu nhiên (cố định hạt giống), gồm cả ba mức thay đổi diễn đạt. Công thức, số và bốn phương án không đổi.\n']
by = collections.OrderedDict()
for r in rows: by.setdefault(r['ma_dang_bai_bao'], []).append(r)
for code, rs in by.items():
    out.append('\n## %s – %s\n' % (code, rs[0]['ten_dang']))
    rr = random.Random(11); pick = []
    for lv in '123':
        pick += rr.sample([r for r in rs if r['muc_dien_dat'] == lv], 1)
    pick += rr.sample(rs, 1)
    for r in pick:
        out.append('- **v1:** %s\n  **v2 (mức %s, %s):** %s\n' % (r['de_bai_v1'].partition('\n\nA.')[0].replace('\n', ' '), r['muc_dien_dat'], r['khung_cau'], r['de_bai'].partition('\n\nA.')[0].replace('\n', ' ')))
open('F:/Math/data/questions/benchmark_so_phuc_v2_mau_so_sanh.md', 'w', encoding='utf-8').write(''.join(out))
print('ok')
