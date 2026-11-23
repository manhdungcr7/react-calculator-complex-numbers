import random, sys, re
sys.stdout.reconfigure(encoding='utf-8')
import build_v2 as B
codes = sys.argv[1].split(',')
for code in codes:
    L = [list(x) for x in B.FRAMES[code]]
    if code == 'D45': L[2].append(B.F.D45_EXTRA_L3)
    pieces = B.PIECES.get(code, {})
    print('==', code)
    for lv in range(3):
        for fi, tpl in enumerate(L[lv]):
            rng = random.Random(fi * 31 + lv)
            t = B.expand_choices(B.expand_tokens(tpl, pieces), rng)
            ph = ['⟦%d⟧' % i for i in range(8)]
            s = B.normalize(t.format(*ph, **{'z': '⟦z⟧', 'm': '⟦m⟧', 'M': '⟦M⟧', 'w': '⟦w⟧'}))
            print('M%d.%02d %s' % (lv + 1, fi + 1, s))
