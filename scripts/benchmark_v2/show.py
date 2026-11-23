import csv, sys, collections, random
sys.stdout.reconfigure(encoding='utf-8')
rows = list(csv.DictReader(open('F:/Math/data/questions/benchmark_so_phuc_v2_24dang_2160cau.csv', encoding='utf-8-sig')))
codes = sys.argv[1].split(',')
n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
for c in codes:
    rs = [r for r in rows if r['ma_dang_bai_bao'] == c]
    print('=====', c, '| v1:', rs[0]['de_bai_v1'].split('\n\nA.')[0].replace('\n', ' '))
    random.Random(7).shuffle(rs)
    for r in rs[:n]:
        print(' [M%s] %s' % (r['muc_dien_dat'], r['de_bai'].split('\n\nA.')[0].replace('\n', ' ')))
