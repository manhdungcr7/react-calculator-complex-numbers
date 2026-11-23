# -*- coding: utf-8 -*-
"""Sinh benchmark Số phức v2 (24 dạng x 90 = 2160 câu) bằng cách viết lại câu chữ của đề v1.

Nguyên tắc: chỉ đổi phần chữ tiếng Việt quanh công thức. Mọi công thức $...$, bốn phương án A-D
và đáp án giữ nguyên từ v1. Việc "không sai đề" được bảo đảm bằng (1) khung câu viết tay và
(2) bộ kiểm tra tự động ở hàm check().
"""
import csv, re, random, collections, sys, os, difflib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
import frames as F

V1 = 'F:/Math/data/questions/benchmark_so_phuc_v1_24dang_2160cau.csv'
OUT = 'F:/Math/data/questions/benchmark_so_phuc_v2_24dang_2160cau.csv'
MATH = re.compile(r'\$[^$]+\$')

# ------------------------------------------------------------------ cấu hình từng dạng
MAC = dict(F.MAC); MAC['ASKS'] = F.ASKS
EXTRA_SYM = {'z': '$z$', 'm': '$m$', 'M': '$M$', 'w': '$w$'}

def count_pieces(second_is_thuan_ao):
    b = '{2} là [số|một số] thuần ảo' if second_is_thuan_ao else '{2}'
    return {'A': '{1}', 'B': b}

QPAR = '[{1} là tham số thực|{1} là một tham số thực]'
PIECES = {
    'D34': count_pieces(True), 'D35': count_pieces(True),
    'D36': count_pieces(False), 'D39': count_pieces(False),
    'D45': {'OBJ': 'giá trị nguyên của {2}', 'PAR': QPAR,
            'ROOT': '[có hai nghiệm phân biệt|có hai nghiệm phức phân biệt] {3} <TM> {4}'},
    'D46': {'OBJ': '[giá trị|giá trị thực] của {2}', 'PAR': QPAR,
            'ROOT': '[có hai nghiệm phân biệt|có hai nghiệm phức phân biệt] {3} <TM> {4}'},
    'D47': {'OBJ': '[giá trị|giá trị thực] của {2}', 'PAR': QPAR,
            'ROOT': '[có nghiệm|có nghiệm phức|có ít nhất một nghiệm] {3} <TM> {4}'},
    'D48': {'OBJ': 'cặp số thực {2}', 'PAR': '{1} là các tham số thực',
            'ROOT': '[có hai nghiệm|có hai nghiệm phức] {3} <TM> {4}'},
}
FRAMES = {
    'D04': F.D04, 'D14': F.D14, 'D28': F.MOD, 'D32': F.MOD, 'D37': F.D37, 'D38': F.D38,
    'D34': F.COUNT2, 'D35': F.COUNT2, 'D36': F.COUNT2, 'D39': F.COUNT2,
    'D45': F.QUAD, 'D46': F.QUAD, 'D47': F.QUAD, 'D48': F.QUAD,
    'D49': F.D49, 'D33': F.D33, 'D40': F.D40, 'D42': F.D42, 'D44': F.D44,
    'D53': F.D53, 'D50': F.D50, 'D52': F.D52, 'D51': F.D51, 'D54': F.D54,
}
# chỉ số công thức được phép vắng mặt (đã diễn đạt bằng lời, vẫn đúng nghĩa)
OPTIONAL = {'D04': {1}, 'D14': {2}, 'D45': {4}}
# D28 chỉ có 2 công thức; khung dùng chung với D32 cần {2} = z
PAD = {'D28': lambda m: [m[0], m[1], m[0]]}

# kiểm tra ngữ nghĩa theo từ khóa: (phải có, không được có)
SEM = {
    'D04': ([r'phần thực', r'phần ảo'], []),
    'D14': ([r'[Mm]ô-?đun'], []), 'D28': ([r'[Mm]ô-?đun'], []), 'D32': ([r'[Mm]ô-?đun'], []),
    'D37': ([r'đúng'], []),
    'D38': ([r'bao nhiêu|Đếm|số lượng|số các|số nghiệm|tìm số'], []),
    'D34': ([r'thuần ảo', r'bao nhiêu|Đếm|số lượng|số các|số nghiệm|tìm số'], []), 'D35': ([r'thuần ảo', r'bao nhiêu|Đếm|số lượng|số các|số nghiệm|tìm số'], []),
    'D36': ([r'bao nhiêu|Đếm|số lượng|số các|số nghiệm|tìm số'], []), 'D39': ([r'bao nhiêu|Đếm|số lượng|số các|số nghiệm|tìm số'], []),
    'D45': ([r'nguyên', r'phân biệt'], []), 'D46': ([r'phân biệt'], [r'nguyên']),
    'D47': ([r'nghiệm'], [r'phân biệt', r'hai nghiệm']), 'D48': ([r'cặp'], [r'phân biệt', r'nguyên']),
    'D49': ([r'nghiệm'], []), 'D33': ([], []),
    'D40': ([r'tâm', r'đường tròn'], []), 'D42': ([r'bán kính', r'thuần ảo'], []), 'D44': ([r'bán kính'], []),
    'D50': ([r'nhỏ nhất', r'lớn nhất'], []), 'D52': ([r'nhỏ nhất', r'lớn nhất'], []),
    'D53': ([r'nhỏ nhất'], []), 'D51': ([r'lớn nhất', r'phần thực'], []), 'D54': ([r'[Dd]iện tích'], []),
}

PREFIXES = ['', '', '', '', '', '', 'Đề bài: ', 'Bài toán: ', 'Câu hỏi: ', 'Hãy giải bài toán sau. ', 'Hãy đọc kỹ đề bài sau. ']
SUFFIXES = ['', '', '', '', '', ' Hãy chọn đáp án đúng.', ' Chọn đáp án đúng nhất.', ' Chọn một đáp án.']

PURE = re.compile(r'^\$[A-Za-z]{1,3}(?:_\d)?(?:,\s*[A-Za-z]{1,3}(?:_\d)?)*\$$')
ATOM = re.compile(r'[A-Za-z](?:_\d)?')


# ------------------------------------------------------------------ biểu thức khung -> văn bản
def expand_tokens(t, pieces):
    for k, v in pieces.items():
        t = t.replace('<%s>' % k, v)
    for _ in range(6):
        changed = False
        for k, v in MAC.items():
            if '<%s>' % k in t:
                t = t.replace('<%s>' % k, v); changed = True
        if not changed:
            break
    return t

CHOICE = re.compile(r'\[([^\[\]]*)\]')
def expand_choices(t, rng):
    return CHOICE.sub(lambda m: rng.choice(m.group(1).split('|')), t)

def normalize(s):
    maths = []
    def keep(m):
        maths.append(m.group(0)); return '\x00%d\x00' % (len(maths) - 1)
    s = MATH.sub(keep, s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+([,.;:?])', r'\1', s)
    s = re.sub(r'([.?])\.+', r'\1', s)
    s = re.sub(r'\x00(\d+)\x00', lambda m: maths[int(m.group(1))], s)
    return s


# ------------------------------------------------------------------ độ khác biệt so với v1
MIN_DIFF = 0.15
SPELL = [('thoả', 'thỏa'), ('mô-đun', 'môđun'), ('kí hiệu', 'ký hiệu'), ('đề bài', 'đề')]
def tokens(stem):
    out = []
    for part in re.split(r'(\$[^$]+\$)', stem):
        if part.startswith('$'): out.append(part)
        else:
            s = part.lower()
            for a, b in SPELL: s = s.replace(a, b)
            out += re.findall(r'\w+', s)
    return out
def diff_from_v1(s1, s2):
    return 1 - difflib.SequenceMatcher(None, tokens(s1), tokens(s2), autojunk=False).ratio()


# ------------------------------------------------------------------ kiểm tra
def atoms_of(seg):
    return set(ATOM.findall(re.sub(r'\\[a-zA-Z]+', ' ', seg)))

def check(code, v1_stem, v2_stem, v1_maths, opt_idx):
    errs = []
    m2 = MATH.findall(v2_stem)
    c1 = collections.Counter(x for x in v1_maths if not PURE.match(x))
    c2 = collections.Counter(x for x in m2 if not PURE.match(x))
    extra = c2 - c1
    if extra: errs.append('công thức lạ: %s' % list(extra))
    missing = c1 - c2
    allowed = collections.Counter(v1_maths[i] for i in opt_idx)
    if missing - allowed: errs.append('thiếu công thức: %s' % list(missing - allowed))
    v1_atoms = set().union(*[atoms_of(x) for x in v1_maths]) if v1_maths else set()
    v1_pure_atoms = set().union(*[atoms_of(x) for x in v1_maths if PURE.match(x)] or [set()])
    v2_pure_atoms = set().union(*[atoms_of(x) for x in m2 if PURE.match(x)] or [set()])
    if v2_pure_atoms - v1_atoms: errs.append('ký hiệu lạ: %s' % (v2_pure_atoms - v1_atoms))
    if v1_pure_atoms - v2_pure_atoms - atoms_of(' '.join(m2)): errs.append('mất ký hiệu: %s' % (v1_pure_atoms - v2_pure_atoms))
    plain = MATH.sub(' ', v2_stem)
    if re.search(r'[<>\[\]{}|\x00]', plain): errs.append('còn ký tự khung')
    need, ban = SEM[code]
    for p in need:
        if not re.search(p, plain, re.I): errs.append('thiếu từ khóa %s' % p)
    for p in ban:
        if re.search(p, plain, re.I): errs.append('có từ cấm %s' % p)
    if code == 'D04' and plain.lower().find('phần ảo') < plain.lower().find('phần thực'): errs.append('đảo thứ tự thực/ảo')
    if code == 'D50' and '$m, M$' in m2:
        if plain.find('nhỏ nhất') > plain.find('lớn nhất'): errs.append('thứ tự m,M sai')
    if v2_stem == v1_stem: errs.append('trùng đề v1')
    elif diff_from_v1(v1_stem, v2_stem) < MIN_DIFF: errs.append('quá giống đề v1')
    return errs


# ------------------------------------------------------------------ sinh
def generate_type(code, rows):
    rng = random.Random(20261123 + int(code[1:]))
    L = FRAMES[code]
    levels = [list(L[0]), list(L[1]), list(L[2])]
    if code == 'D45':
        levels[2].append(F.D45_EXTRA_L3)
    pieces = PIECES.get(code, {})
    order = [rng.sample(range(len(lv)), len(lv)) for lv in levels]
    pos = [0, 0, 0]
    used = set(); out = []
    stats = collections.Counter()
    for i, r in enumerate(rows):
        stem1, _, opts = r['de_bai'].partition('\n\nA.')
        maths = MATH.findall(stem1)
        if code in PAD: maths = PAD[code](maths)
        ok = None
        for attempt in range(400):
            lvl = i % 3 if attempt < 200 else rng.randrange(3)
            if attempt < 3:
                fi = order[lvl][pos[lvl] % len(levels[lvl])]
            else:
                fi = rng.randrange(len(levels[lvl]))
            tpl = levels[lvl][fi]
            t = expand_choices(expand_tokens(tpl, pieces), rng)
            body = normalize(t.format(*maths, **EXTRA_SYM))
            pre = rng.choice(PREFIXES)
            if body.startswith('Đề bài'): pre = ''
            suf = rng.choice(SUFFIXES) if body.endswith(('.', '?')) else ''
            # tránh lặp yêu cầu "chọn"/"hãy": không thêm câu kết nếu đề đã có "chọn", hoặc đã có từ 2 "hãy" trở lên
            if re.search(r'[Cc]họn', body) or len(re.findall(r'[Hh]ãy', pre + body)) >= 2: suf = ''
            elif 'Hãy' in pre and 'Hãy' in suf: suf = suf.replace('Hãy chọn', 'Chọn')
            stem2 = normalize(pre + body + suf)
            stem2 = stem2[0].upper() + stem2[1:]
            if stem2 in used: continue
            errs = check(code, stem1, stem2, MATH.findall(stem1), OPTIONAL.get(code, set()))
            if errs:
                if attempt > 395: raise SystemExit('LỖI %s #%d khung L%d/%d: %s\n  %s' % (code, i, lvl + 1, fi, errs, stem2))
                if attempt > 50 and attempt % 50 == 0: print('  cảnh báo', code, i, errs, stem2)
                continue
            used.add(stem2)
            pos[lvl] += 1
            ok = (stem2, lvl + 1, fi)
            break
        if ok is None: raise SystemExit('không sinh được %s #%d' % (code, i))
        out.append((r, ok[0] + '\n\nA.' + opts, ok[1], '%s-M%d-K%02d' % (code, ok[1], ok[2] + 1)))
    return out


def main():
    rows = list(csv.DictReader(open(V1, encoding='utf-8-sig')))
    by = collections.OrderedDict()
    for r in rows: by.setdefault(r['ma_dang_bai_bao'], []).append(r)
    result = []
    for code, rs in by.items():
        rs.sort(key=lambda r: int(r['bien_the']))
        result += generate_type(code, rs)
    cols = list(rows[0].keys()) + ['de_bai_v1', 'muc_dien_dat', 'khung_cau']
    with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r, new, lvl, fr in result:
            d = dict(r); d['de_bai_v1'] = r['de_bai']; d['de_bai'] = new; d['muc_dien_dat'] = lvl; d['khung_cau'] = fr
            w.writerow(d)
    print('đã ghi', len(result), 'câu ->', OUT)

if __name__ == '__main__':
    main()
