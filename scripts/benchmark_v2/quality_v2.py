import csv, re, collections, sys, statistics
sys.stdout.reconfigure(encoding='utf-8')
MATH = re.compile(r'\$[^$]+\$')
LOW = 'a-zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ'
UP = 'A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ'
rows = list(csv.DictReader(open('F:/Math/data/questions/benchmark_so_phuc_v2_24dang_2160cau.csv', encoding='utf-8-sig')))
def stem(r): return r['de_bai'].partition('\n\nA.')[0]
def plain(s): return MATH.sub('§', s)

issues = collections.defaultdict(list)
for r in rows:
    s = stem(r); p = plain(s); c = r['ma_dang_bai_bao']
    ref = '%s#%s' % (c, r['bien_the'])
    if re.search(r'\b(\w+) \1\b', p, re.I): issues['từ lặp liền kề'].append((ref, s))
    if re.search(r'[.?!] [%s]' % LOW, p): issues['chữ thường sau dấu chấm'].append((ref, s))
    if re.search(r'[,;] [%s][%s]' % (UP, LOW), re.sub(r'§', '', p)) : issues['chữ hoa sau dấu phẩy'].append((ref, s))
    if len(re.findall(r'[Cc]họn', p)) >= 2: issues['"chọn" lặp'].append((ref, s))
    if len(re.findall(r'[Hh]ãy', p)) >= 3: issues['"hãy" ≥3'].append((ref, s))
    if re.search(r'\s[,.;?:]', p) or '  ' in p: issues['khoảng trắng/dấu câu'].append((ref, s))
    if not p.rstrip().endswith(('.', '?')): issues['không kết thúc bằng . hoặc ?'].append((ref, s))
    if re.search(r'[.?]\s*[.?]', p): issues['dấu câu kép'].append((ref, s))
    if re.search(r'(Đề bài|Bài toán|Câu hỏi)[^:]{0,40}: (Đề bài|Bài toán|Câu hỏi)', p): issues['nhãn kép'].append((ref, s))
    if len(re.findall(r'Cho |Xét |Giả sử ', p)) >= 3: issues['"Cho/Xét/Giả sử" ≥3'].append((ref, s))
    if re.search(r'(?i)\b(tính|tìm|xác định)\b.*\b(tính|tìm|xác định)\b.*\b(tính|tìm|xác định)\b', p): issues['động từ yêu cầu ≥3'].append((ref, s))
    if len(s) > 520: issues['quá dài'].append((ref, s))
print('Tổng câu:', len(rows))
for k, v in issues.items():
    print('\n[%s] %d câu' % (k, len(v)))
    for ref, s in v[:4]: print('   ', ref, '|', s[:230])
if not issues: print('Không phát hiện lỗi ngôn ngữ theo các luật trên')
