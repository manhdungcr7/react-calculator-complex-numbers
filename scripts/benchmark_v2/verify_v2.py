# Kiểm tra độc lập file v2 so với v1 (không dùng lại dữ liệu trong lúc sinh)
import csv, re, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
import build_v2 as B
v1 = list(csv.DictReader(open(B.V1, encoding='utf-8-sig')))
v2 = list(csv.DictReader(open(B.OUT, encoding='utf-8-sig')))
assert len(v1) == len(v2) == 2160
bad = 0
same_cols = ['stt','ma_dang_bai_bao','ma_dang_du_lieu','bien_the','stt_cau_goc','van_de','ten_dang','muc_do','loai_so','dap_an_dung','dap_an_day_du','tham_so']
for a, b in zip(v1, v2):
    for c in same_cols:
        if a[c] != b[c]: bad += 1; print('khác cột', c, a['stt'])
    s1, _, o1 = a['de_bai'].partition('\n\nA.')
    s2, _, o2 = b['de_bai'].partition('\n\nA.')
    if o1 != o2: bad += 1; print('phương án khác', a['stt'])
    if b['de_bai_v1'] != a['de_bai']: bad += 1; print('de_bai_v1 sai', a['stt'])
    errs = B.check(a['ma_dang_bai_bao'], s1, s2, B.MATH.findall(s1), B.OPTIONAL.get(a['ma_dang_bai_bao'], set()))
    if errs: bad += 1; print('lỗi', a['stt'], errs)
print('số lỗi:', bad)
# đa dạng
MATH = B.MATH
tot_unique = 0
for code in sorted(set(r['ma_dang_bai_bao'] for r in v2)):
    rs = [r for r in v2 if r['ma_dang_bai_bao'] == code]
    skel = collections.Counter(MATH.sub('#', r['de_bai'].partition('\n\nA.')[0]) for r in rs)
    frames = len(set(r['khung_cau'] for r in rs))
    opening = len(set(' '.join(MATH.sub('#', r['de_bai']).split()[:4]) for r in rs))
    print(code, 'khung dùng:', frames, '| khung chữ khác nhau:', len(skel), '/90 | số cách mở đầu (4 từ đầu):', opening, '| lặp nhiều nhất:', skel.most_common(1)[0][1])
    tot_unique += len(skel)
print('tổng khung chữ khác nhau:', tot_unique, '/ 2160')
