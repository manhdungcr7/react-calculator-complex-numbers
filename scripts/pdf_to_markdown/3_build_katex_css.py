import re, base64, os

base = 'scratch/katex'
with open(f'{base}/katex.min.css', encoding='utf-8') as f:
    css = f.read()

def repl(m):
    path = m.group(1)
    fname = os.path.basename(path)
    with open(f'{base}/fonts/{fname}', 'rb') as fh:
        b64 = base64.b64encode(fh.read()).decode('ascii')
    ext = 'woff2'
    return f'url(data:font/{ext};base64,{b64}) format("woff2")'

# match url(fonts/XXX.woff2) format("woff2")  possibly with other formats too; katex css has multiple url() per rule (woff2, woff, ttf) - we only keep woff2 one and strip others
# Simplify: for each font-face block, replace entire src list with just the woff2 data url
def repl_src(m):
    block = m.group(0)
    wf2 = re.search(r'url\((fonts/[^)]+\.woff2)\)', block)
    if not wf2:
        return block
    path = wf2.group(1)
    fname = os.path.basename(path)
    with open(f'{base}/fonts/{fname}', 'rb') as fh:
        b64 = base64.b64encode(fh.read()).decode('ascii')
    return f'src:url(data:font/woff2;base64,{b64}) format("woff2");'

css2 = re.sub(r'src:[^;]+;', repl_src, css)

with open(f'{base}/katex_inlined.css', 'w', encoding='utf-8') as f:
    f.write(css2)

print('done, size', len(css2))
