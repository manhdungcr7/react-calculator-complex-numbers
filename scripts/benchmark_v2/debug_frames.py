import csv, re, random, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
import build_v2 as B
rows = list(csv.DictReader(open(B.V1, encoding='utf-8-sig')))
by = collections.OrderedDict()
for r in rows: by.setdefault(r['ma_dang_bai_bao'], []).append(r)
bad = 0
for code, rs in by.items():
    L = [list(x) for x in B.FRAMES[code]]
    if code == 'D45': L[2].append(B.F.D45_EXTRA_L3)
    pieces = B.PIECES.get(code, {})
    for lv in range(3):
        for fi, tpl in enumerate(L[lv]):
            fails = collections.Counter(); n = 0
            for r in rs[:30]:
                stem1 = r['de_bai'].partition('\n\nA.')[0]
                maths = B.MATH.findall(stem1)
                if code in B.PAD: maths = B.PAD[code](maths)
                rng = random.Random(n); n += 1
                try:
                    t = B.expand_choices(B.expand_tokens(tpl, pieces), rng)
                    body = B.normalize(t.format(*maths, **B.EXTRA_SYM))
                except Exception as e:
                    fails['EXC ' + repr(e)] += 1; continue
                errs = B.check(code, stem1, body, B.MATH.findall(stem1), B.OPTIONAL.get(code, set()))
                for e in errs: fails[e] += 1
            if fails:
                bad += 1
                print(code, 'M%d' % (lv + 1), 'K%02d' % (fi + 1), dict(fails), '|', tpl[:70])
print('khung lỗi:', bad)
