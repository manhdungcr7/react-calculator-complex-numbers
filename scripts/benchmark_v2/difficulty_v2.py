import csv, re, sys, collections, statistics, difflib
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
MATH = re.compile(r'\$[^$]+\$')
rows = list(csv.DictReader(open('F:/Math/data/questions/benchmark_so_phuc_v2_24dang_2160cau.csv', encoding='utf-8-sig')))
def stem(s): return s.partition('\n\nA.')[0]
def words(s): return re.findall(r'\w+', MATH.sub(' ', stem(s)).lower())

# 1) khác biệt câu chữ v1 -> v2 (chỉ phần chữ, bỏ công thức)
print('== 1. Mức khác biệt chữ giữa v1 và v2 (1 - tỉ lệ giống theo từ; càng cao càng khác)')
byl = collections.defaultdict(list)
for r in rows:
    a, b = words(r['de_bai_v1']), words(r['de_bai'])
    byl[r['muc_dien_dat']].append(1 - difflib.SequenceMatcher(None, a, b).ratio())
for k in sorted(byl): print('  mức', k, 'trung bình %.2f | nhỏ nhất %.2f | lớn nhất %.2f' % (statistics.mean(byl[k]), min(byl[k]), max(byl[k])))
ratio = [len(stem(r['de_bai'])) / len(stem(r['de_bai_v1'])) for r in rows]
print('  độ dài đề v2 / v1: trung bình %.2f, nhỏ nhất %.2f, lớn nhất %.2f' % (statistics.mean(ratio), min(ratio), max(ratio)))

# 2) đáp án và phân bố
print('== 2. Phân bố')
print('  mức:', dict(collections.Counter(r['muc_dien_dat'] for r in rows)))
print('  đáp án đúng:', dict(sorted(collections.Counter(r['dap_an_dung'] for r in rows).items())))

# 3) bộ phân loại dạng đơn giản huấn luyện trên v1 (24 dạng x 72 biến thể), thử trên v2
print('== 3. Bộ phân loại dạng (TF-IDF ký tự + hồi quy logistic) học trên v1')
tr = [r for r in rows if int(r['bien_the']) <= 60]      # 60 câu v1 mỗi dạng để học
te_ids = [r for r in rows if int(r['bien_the']) > 60]   # 30 câu còn lại để thử
for name, mask in (('giữ công thức', lambda s: s), ('che công thức (chỉ xét chữ)', lambda s: MATH.sub(' M ', s))):
    vec = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 5), sublinear_tf=True)
    Xtr = vec.fit_transform([mask(stem(r['de_bai_v1'])) for r in tr]); ytr = [r['ma_dang_bai_bao'] for r in tr]
    clf = LogisticRegression(max_iter=2000, C=20).fit(Xtr, ytr)
    def acc(rs, key):
        p = clf.predict(vec.transform([mask(stem(r[key])) for r in rs])); return np.mean([a == r['ma_dang_bai_bao'] for a, r in zip(p, rs)])
    print('  [%s] v1 (câu chưa học): %.1f%% | v2 chung: %.1f%%' % (name, 100 * acc(te_ids, 'de_bai_v1'), 100 * acc(te_ids, 'de_bai')))
    for lv in '123':
        sub = [r for r in te_ids if r['muc_dien_dat'] == lv]
        print('       v2 mức %s: %.1f%% (%d câu)' % (lv, 100 * acc(sub, 'de_bai'), len(sub)))
    # dạng sai nhiều nhất
    p = clf.predict(vec.transform([mask(stem(r['de_bai'])) for r in te_ids]))
    wrong = collections.Counter(r['ma_dang_bai_bao'] for a, r in zip(p, te_ids) if a != r['ma_dang_bai_bao'])
    print('       dạng nhận sai nhiều nhất:', wrong.most_common(6))
