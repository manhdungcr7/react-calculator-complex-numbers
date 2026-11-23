import csv, re, random, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
import build_v2 as B
import quality_v2 as Q  # chạy lint trên file hiện có (in kết quả), chỉ để lấy LOW/UP
LOW, UP = Q.LOW, Q.UP
rows = list(csv.DictReader(open(B.V1, encoding='utf-8-sig')))
by = collections.OrderedDict()
for r in rows: by.setdefault(r['ma_dang_bai_bao'], []).append(r)
def lint(p):
    e = []
    if re.search(r'\b(\w+) \1\b', p, re.I): e.append('từ lặp')
    if re.search(r'[.?!] [%s]' % LOW, p): e.append('chữ thường sau dấu chấm')
    if re.search(r'[,;] [%s][%s]' % (UP, LOW), p.replace('§', '')): e.append('chữ hoa sau phẩy')
    if len(re.findall(r'[Cc]họn', p)) >= 2: e.append('chọn lặp')
    if len(re.findall(r'[Hh]ãy', p)) >= 3: e.append('hãy>=3')
    if re.search(r'\s[,.;?:]', p) or '  ' in p: e.append('khoảng trắng')
    if re.search(r'[.?]\s*[.?]', p): e.append('dấu câu kép')
    if re.search(r'(Đề bài|Bài toán|Câu hỏi)[^:]{0,40}: (Đề bài|Bài toán|Câu hỏi)', p): e.append('nhãn kép')
    if re.search(r'(Đề bài|Bài toán|Câu hỏi): (Hãy giải|Hãy đọc)', p): e.append('nhãn+câu dẫn')
    return e
N = 40; total = 0; bad = collections.Counter(); ex = {}
for code, rs in by.items():
    L = [list(x) for x in B.FRAMES[code]]
    if code == 'D45': L[2].append(B.F.D45_EXTRA_L3)
    pieces = B.PIECES.get(code, {})
    for lv in range(3):
        for fi, tpl in enumerate(L[lv]):
            for k in range(N):
                r = rs[(k * 7 + fi) % 90]
                stem1 = r['de_bai'].partition('\n\nA.')[0]
                maths = B.MATH.findall(stem1)
                if code in B.PAD: maths = B.PAD[code](maths)
                rng = random.Random(1000 * fi + k)
                t = B.expand_choices(B.expand_tokens(tpl, pieces), rng)
                body = B.normalize(t.format(*maths, **B.EXTRA_SYM))
                pre = rng.choice(B.PREFIXES)
                if body.startswith('Đề bài'): pre = ''
                suf = rng.choice(B.SUFFIXES) if body.endswith(('.', '?')) else ''
                if re.search(r'[Cc]họn', body) or len(re.findall(r'[Hh]ãy', pre + body)) >= 2: suf = ''
                elif 'Hãy' in pre and 'Hãy' in suf: suf = suf.replace('Hãy chọn', 'Chọn')
                s2 = B.normalize(pre + body + suf); s2 = s2[0].upper() + s2[1:]
                total += 1
                errs = B.check(code, stem1, s2, B.MATH.findall(stem1), B.OPTIONAL.get(code, set()))
                errs = [e for e in errs if e not in ('trùng đề v1', 'quá giống đề v1')] + lint(B.MATH.sub('§', s2))
                for e in errs:
                    bad[(code, e)] += 1; ex.setdefault((code, e), s2)
print('đã thử', total, 'câu | lỗi:', sum(bad.values()))
for k, v in bad.items(): print(k, v, '|', ex[k][:200])
