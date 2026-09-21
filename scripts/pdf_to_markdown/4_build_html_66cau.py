import json, html

with open('scratch/batch1.json', encoding='utf-8') as f:
    b1 = json.load(f)
with open('scratch/batch2.json', encoding='utf-8') as f:
    b2 = json.load(f)
with open('scratch/batch3.json', encoding='utf-8') as f:
    b3 = json.load(f)

items = b1 + b2 + b3
for it in items:
    if it['trang'] == 40 and it['cau'] == 39:
        it['dap_an'] = 'C. 4.'
items.sort(key=lambda x: (x['trang'], x['cau']))

with open('scratch/katex/katex_inlined.css', encoding='utf-8') as f:
    katex_css = f.read()
with open('scratch/katex/katex.min.js', encoding='utf-8') as f:
    katex_js = f.read()
with open('scratch/katex/auto-render.min.js', encoding='utf-8') as f:
    auto_render_js = f.read()

def esc(s):
    return html.escape(s, quote=False)

def md_lines_to_html(text):
    # split question into stem + choices A./B./C./D. on their own lines
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    stem_lines = []
    choice_lines = []
    for l in lines:
        if len(l) > 2 and l[0] in 'ABCD' and l[1] == '.':
            choice_lines.append(l)
        else:
            stem_lines.append(l)
    stem_html = '<br>'.join(esc(l) for l in stem_lines)
    choices_html = ''
    if choice_lines:
        choices_html = '<div class="choices">' + ''.join(
            f'<div class="choice"><span class="choice-letter">{c[0]}</span><span>{esc(c[3:].strip())}</span></div>'
            for c in choice_lines
        ) + '</div>'
    return stem_html, choices_html

def solution_to_html(text):
    paras = [p.strip() for p in text.split('\n') if p.strip()]
    return ''.join(f'<p>{esc(p)}</p>' for p in paras)

cards = []
for i, it in enumerate(items, start=1):
    stem_html, choices_html = md_lines_to_html(it['de_bai'])
    sol_html = solution_to_html(it['loi_giai'])
    dap_an = esc(it['dap_an'])
    cards.append(f'''
    <article class="card" id="q{i}" data-trang="{it['trang']}" data-cau="{it['cau']}" data-idx="{i}">
      <header class="card-head">
        <span class="stt">#{i:02d}</span>
        <span class="loc">Trang {it['trang']} &middot; Câu {it['cau']}</span>
      </header>
      <div class="stem">{stem_html}</div>
      {choices_html}
      <details class="answer-block">
        <summary class="answer-summary">
          <span class="answer-badge">Đáp án đúng: {dap_an}</span>
          <span class="toggle-hint">Xem lời giải</span>
        </summary>
        <div class="solution">{sol_html}</div>
      </details>
    </article>''')

nav_items = ''.join(
    f'<button class="nav-item" data-target="q{i}" data-search="{it["trang"]} {it["cau"]}">'
    f'<span class="nav-idx">{i:02d}</span><span class="nav-loc">Tr.{it["trang"]} C.{it["cau"]}</span></button>'
    for i, it in enumerate(items, start=1)
)

html_doc = f'''<title>Ngân hàng số phức — 66 câu</title>
<style>
:root {{
  --bg: #f7f5f1;
  --surface: #ffffff;
  --surface-2: #f0eee8;
  --border: #e3ded3;
  --text: #21201d;
  --text-dim: #6f6a5f;
  --accent: #4a3fc4;
  --accent-soft: #ece9fb;
  --good: #1f7a5c;
  --good-soft: #e3f3ec;
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Noto Serif", serif;
  --sans: "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
  --mono: "Cascadia Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #15161b;
    --surface: #1d1f26;
    --surface-2: #23252d;
    --border: #2d303a;
    --text: #e9e7e0;
    --text-dim: #9b98a8;
    --accent: #9089ff;
    --accent-soft: #2a2660;
    --good: #57d9a8;
    --good-soft: #12332a;
  }}
}}
:root[data-theme="dark"] {{
  --bg: #15161b; --surface: #1d1f26; --surface-2: #23252d; --border: #2d303a;
  --text: #e9e7e0; --text-dim: #9b98a8; --accent: #9089ff; --accent-soft: #2a2660;
  --good: #57d9a8; --good-soft: #12332a;
}}
:root[data-theme="light"] {{
  --bg: #f7f5f1; --surface: #ffffff; --surface-2: #f0eee8; --border: #e3ded3;
  --text: #21201d; --text-dim: #6f6a5f; --accent: #4a3fc4; --accent-soft: #ece9fb;
  --good: #1f7a5c; --good-soft: #e3f3ec;
}}
{katex_css}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  line-height: 1.55;
  min-height: 100vh;
}}
.layout {{
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  min-height: 100vh;
}}
.sidebar {{
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  border-right: 1px solid var(--border);
  background: var(--surface-2);
  padding: 1.25rem 1rem;
}}
.brand {{
  font-family: var(--serif);
  font-size: 1.25rem;
  margin: 0 0 .15rem;
  text-wrap: balance;
}}
.brand-sub {{
  font-size: .78rem;
  color: var(--text-dim);
  margin: 0 0 1rem;
}}
.search-box {{
  width: 100%;
  padding: .5rem .65rem;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  font-family: var(--sans);
  font-size: .85rem;
  margin-bottom: .75rem;
}}
.search-box:focus {{ outline: 2px solid var(--accent); outline-offset: 1px; }}
.nav-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: .35rem;
}}
.nav-item {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: .1rem;
  padding: .35rem .2rem;
  border-radius: 7px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-dim);
  font-family: var(--mono);
  cursor: pointer;
  font-size: .68rem;
}}
.nav-item:hover {{ border-color: var(--accent); color: var(--text); }}
.nav-item.active {{ background: var(--accent-soft); border-color: var(--accent); color: var(--accent); }}
.nav-idx {{ font-weight: 600; }}
.nav-item[hidden] {{ display: none; }}

main {{
  padding: 2.5rem clamp(1rem, 4vw, 3.5rem);
  max-width: 900px;
}}
.page-head {{ margin-bottom: 2rem; }}
.page-head h1 {{
  font-family: var(--serif);
  font-size: clamp(1.6rem, 3vw, 2.1rem);
  margin: 0 0 .4rem;
  text-wrap: balance;
}}
.page-head p {{
  color: var(--text-dim);
  max-width: 62ch;
  font-size: .95rem;
  margin: 0;
}}
.card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem 1.4rem;
  margin-bottom: 1.1rem;
  scroll-margin-top: 1.25rem;
}}
.card-head {{
  display: flex;
  align-items: baseline;
  gap: .6rem;
  margin-bottom: .6rem;
}}
.stt {{
  font-family: var(--mono);
  color: var(--accent);
  font-size: .8rem;
  font-weight: 600;
}}
.loc {{
  font-family: var(--mono);
  color: var(--text-dim);
  font-size: .78rem;
  letter-spacing: .02em;
}}
.stem {{ font-size: 1rem; margin-bottom: .5rem; }}
.stem p, .stem br {{ margin: 0; }}
.choices {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: .35rem .9rem;
  margin: .6rem 0 .8rem;
}}
.choice {{
  display: flex;
  gap: .45rem;
  font-size: .92rem;
  align-items: baseline;
}}
.choice-letter {{
  font-family: var(--mono);
  color: var(--accent);
  font-weight: 700;
  min-width: 1.1em;
}}
.answer-block {{ margin-top: .4rem; border-top: 1px dashed var(--border); padding-top: .6rem; }}
.answer-summary {{
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: .5rem;
  list-style: none;
}}
.answer-summary::-webkit-details-marker {{ display: none; }}
.answer-badge {{
  display: inline-block;
  background: var(--good-soft);
  color: var(--good);
  font-family: var(--mono);
  font-size: .82rem;
  padding: .3rem .6rem;
  border-radius: 6px;
  font-weight: 600;
}}
.toggle-hint {{
  font-size: .78rem;
  color: var(--text-dim);
}}
.answer-block[open] .toggle-hint::before {{ content: "▲ "; }}
.answer-block:not([open]) .toggle-hint::before {{ content: "▼ "; }}
.solution {{
  margin-top: .75rem;
  padding: .8rem .9rem;
  background: var(--surface-2);
  border-radius: 8px;
  font-size: .93rem;
}}
.solution p {{ margin: 0 0 .5rem; }}
.solution p:last-child {{ margin-bottom: 0; }}
.katex {{ font-size: 1.02em; }}

@media (max-width: 760px) {{
  .layout {{ grid-template-columns: 1fr; }}
  .sidebar {{ position: static; height: auto; }}
  .choices {{ grid-template-columns: 1fr; }}
}}
</style>

<div class="layout">
  <nav class="sidebar">
    <p class="brand">Ngân hàng số phức</p>
    <p class="brand-sub">66 câu &middot; TN THPT &middot; trích từ DAP AN.pdf</p>
    <input class="search-box" id="searchBox" type="text" placeholder="Tìm theo trang hoặc câu…">
    <div class="nav-grid" id="navGrid">
      {nav_items}
    </div>
  </nav>
  <main>
    <div class="page-head">
      <h1>Ngân hàng câu hỏi số phức</h1>
      <p>66 câu trắc nghiệm về số phức, trích nguyên văn đề &amp; lời giải từ tài liệu ôn thi TN THPT 2023 (đã loại các câu cần nhìn hình vẽ). Bấm vào "Xem lời giải" để mở lời giải gốc.</p>
    </div>
    {''.join(cards)}
  </main>
</div>

<script>{katex_js}</script>
<script>{auto_render_js}</script>
<script>
document.addEventListener('DOMContentLoaded', function() {{
  renderMathInElement(document.body, {{
    delimiters: [
      {{left: "$$", right: "$$", display: true}},
      {{left: "$", right: "$", display: false}}
    ],
    throwOnError: false
  }});

  var navItems = Array.prototype.slice.call(document.querySelectorAll('.nav-item'));
  navItems.forEach(function(btn) {{
    btn.addEventListener('click', function() {{
      var target = document.getElementById(btn.dataset.target);
      if (target) {{
        target.scrollIntoView({{behavior: 'smooth', block: 'start'}});
        navItems.forEach(function(b) {{ b.classList.remove('active'); }});
        btn.classList.add('active');
      }}
    }});
  }});

  var searchBox = document.getElementById('searchBox');
  searchBox.addEventListener('input', function() {{
    var q = searchBox.value.trim().toLowerCase();
    navItems.forEach(function(btn) {{
      var hay = btn.dataset.search.toLowerCase();
      btn.hidden = q.length > 0 && hay.indexOf(q) === -1;
    }});
  }});

  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var observer = new IntersectionObserver(function(entries) {{
    entries.forEach(function(entry) {{
      if (entry.isIntersecting) {{
        var idx = entry.target.dataset.idx;
        navItems.forEach(function(b) {{ b.classList.toggle('active', b.dataset.target === 'q' + idx); }});
      }}
    }});
  }}, {{ rootMargin: '-10% 0px -80% 0px' }});
  cards.forEach(function(c) {{ observer.observe(c); }});
}});
</script>
'''

with open('scratch/so_phuc_view.html', 'w', encoding='utf-8') as f:
    f.write(html_doc)

print('written, total chars', len(html_doc))
