import html
import pandas as pd

DATA_XLSX = "So_phuc_60_mau.xlsx"

df = pd.read_excel(DATA_XLSX)
df = df.fillna("")

with open("scratch/katex/katex_inlined.css", encoding="utf-8") as f:
    katex_css = f.read()
with open("scratch/katex/katex.min.js", encoding="utf-8") as f:
    katex_js = f.read()
with open("scratch/katex/auto-render.min.js", encoding="utf-8") as f:
    auto_render_js = f.read()


def esc(s):
    return html.escape(str(s), quote=False)


def split_stem_choices(text):
    lines = [l.strip() for l in str(text).split("\n") if l.strip()]
    stem_lines, choice_lines = [], []
    for l in lines:
        if len(l) > 2 and l[0] in "ABCD" and l[1] == ".":
            choice_lines.append(l)
        else:
            stem_lines.append(l)
    stem_html = "<br>".join(esc(l) for l in stem_lines)
    choices_html = ""
    if choice_lines:
        choices_html = '<div class="choices">' + "".join(
            f'<div class="choice"><span class="choice-letter">{c[0]}</span><span>{esc(c[3:].strip())}</span></div>'
            for c in choice_lines
        ) + "</div>"
    return stem_html, choices_html


def paras(text):
    ps = [p.strip() for p in str(text).split("\n") if p.strip()]
    if not ps:
        return '<p class="empty">(chưa có)</p>'
    return "".join(f"<p>{esc(p)}</p>" for p in ps)


STATUS_CLASS = {
    "Đúng": "ok",
    "Sai": "bad",
    "Không xác định": "warn",
    "Lỗi API": "err",
    "Lụi": "luck",
    "Đúng ý tưởng nhưng chưa giải xong": "partial",
    "Sai hướng": "wrongdir",
}


def status_badge(status):
    cls = STATUS_CLASS.get(status, "warn")
    label = status if status else "Chưa chạy"
    return f'<span class="badge badge-{cls}">{esc(label)}</span>'


def model_block(model_key, label, row):
    solution = row[f"Lời giải {label}"]
    status = row[f"{label} đúng/sai"]
    chosen = row[f"{label} chọn"]
    comment = row[f"Nhận xét {label}"]
    cls = STATUS_CLASS.get(status, "warn")
    chosen_txt = f" (chọn {esc(chosen)})" if chosen else ""
    comment_html = (
        f'<div class="comment"><span class="comment-label">Nhận xét:</span> {esc(comment)}</div>'
        if str(comment).strip()
        else '<div class="comment comment-empty">Chưa có nhận xét</div>'
    )
    return f"""
    <details class="model-block model-{cls}" data-model="{model_key}" data-status="{esc(status)}">
      <summary>
        <span class="model-name">{label}</span>
        {status_badge(status)}
        <span class="chosen">{chosen_txt}</span>
      </summary>
      <div class="model-body">
        {paras(solution)}
        {comment_html}
      </div>
    </details>"""


rows_html = []
for _, row in df.iterrows():
    stt = int(row["STT"])
    stem_html, choices_html = split_stem_choices(row["Đề bài"])
    statuses = {
        m: row[f"{m} đúng/sai"] for m in ["ChatGPT", "Gemini", "Qwen"]
    }
    data_attrs = " ".join(
        f'data-{m.lower()}="{esc(statuses[m])}"' for m in statuses
    )
    rows_html.append(f"""
    <article class="card" id="q{stt}" data-stt="{stt}" {data_attrs}>
      <header class="card-head">
        <span class="stt">#{stt:02d}</span>
        <span class="loc">{esc(row['Bài (Trang - Câu)'])}</span>
        <span class="status-strip">
          {status_badge(statuses['ChatGPT'])}
          {status_badge(statuses['Gemini'])}
          {status_badge(statuses['Qwen'])}
        </span>
      </header>
      <div class="stem">{stem_html}</div>
      {choices_html}
      <div class="answer-line"><span class="answer-badge">Đáp án đúng: {esc(row['Đáp án đúng'])}</span></div>
      <details class="doc-solution">
        <summary>Lời giải theo tài liệu</summary>
        <div class="model-body">{paras(row['Lời giải (theo tài liệu)'])}</div>
      </details>
      <div class="model-grid">
        {model_block('chatgpt', 'ChatGPT', row)}
        {model_block('gemini', 'Gemini', row)}
        {model_block('qwen', 'Qwen', row)}
      </div>
    </article>""")

nav_items = "".join(
    f'<button class="nav-item" data-target="q{int(row["STT"])}" data-search="{int(row["STT"])}">'
    f'<span class="nav-idx">{int(row["STT"]):02d}</span></button>'
    for _, row in df.iterrows()
)

# Summary counts
summary_rows = ""
for m in ["ChatGPT", "Gemini", "Qwen"]:
    vc = df[f"{m} đúng/sai"].value_counts().to_dict()
    ok = vc.get("Đúng", 0)
    bad = vc.get("Sai", 0)
    warn = vc.get("Không xác định", 0)
    err = vc.get("Lỗi API", 0)
    luck = vc.get("Lụi", 0)
    partial = vc.get("Đúng ý tưởng nhưng chưa giải xong", 0)
    wrongdir = vc.get("Sai hướng", 0)
    total = len(df)
    summary_rows += f"""
    <div class="summary-row">
      <span class="summary-model">{m}</span>
      <div class="summary-bar">
        <div class="bar-seg bar-ok" style="flex:{ok}" title="Đúng: {ok}"></div>
        <div class="bar-seg bar-luck" style="flex:{luck}" title="Lụi: {luck}"></div>
        <div class="bar-seg bar-partial" style="flex:{partial}" title="Đúng ý tưởng nhưng chưa giải xong: {partial}"></div>
        <div class="bar-seg bar-bad" style="flex:{bad}" title="Sai: {bad}"></div>
        <div class="bar-seg bar-wrongdir" style="flex:{wrongdir}" title="Sai hướng: {wrongdir}"></div>
        <div class="bar-seg bar-warn" style="flex:{warn}" title="Không xác định: {warn}"></div>
        <div class="bar-seg bar-err" style="flex:{err}" title="Lỗi API: {err}"></div>
      </div>
      <span class="summary-count">{ok}/{total} đúng</span>
    </div>"""

html_doc = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Đối chiếu lời giải — Số phức 66 câu</title>
<style>
:root {{
  --bg: #f7f5f1; --surface: #ffffff; --surface-2: #f0eee8; --border: #e3ded3;
  --text: #21201d; --text-dim: #6f6a5f; --accent: #4a3fc4; --accent-soft: #ece9fb;
  --ok: #1f7a5c; --ok-soft: #e3f3ec;
  --bad: #b23a3a; --bad-soft: #fbe9e7;
  --warn: #9a6b12; --warn-soft: #fdf3df;
  --err: #7a1f5c; --err-soft: #f6e6f0;
  --luck: #b45309; --luck-soft: #fdedd3;
  --partial: #1d5f8a; --partial-soft: #e2eef6;
  --wrongdir: #8f2d3d; --wrongdir-soft: #f7e3e6;
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Noto Serif", serif;
  --sans: "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
  --mono: "Cascadia Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #15161b; --surface: #1d1f26; --surface-2: #23252d; --border: #2d303a;
    --text: #e9e7e0; --text-dim: #9b98a8; --accent: #9089ff; --accent-soft: #2a2660;
    --ok: #57d9a8; --ok-soft: #12332a;
    --bad: #ff8a80; --bad-soft: #3a1f1e;
    --warn: #e0b84d; --warn-soft: #3a3016;
    --err: #e588c2; --err-soft: #331f2c;
    --luck: #e5a04f; --luck-soft: #3d2c14;
    --partial: #6fb2e0; --partial-soft: #16293a;
    --wrongdir: #e28b98; --wrongdir-soft: #3a1c22;
  }}
}}
:root[data-theme="dark"] {{
  --bg: #15161b; --surface: #1d1f26; --surface-2: #23252d; --border: #2d303a;
  --text: #e9e7e0; --text-dim: #9b98a8; --accent: #9089ff; --accent-soft: #2a2660;
  --ok: #57d9a8; --ok-soft: #12332a; --bad: #ff8a80; --bad-soft: #3a1f1e;
  --warn: #e0b84d; --warn-soft: #3a3016; --err: #e588c2; --err-soft: #331f2c;
  --luck: #e5a04f; --luck-soft: #3d2c14; --partial: #6fb2e0; --partial-soft: #16293a;
  --wrongdir: #e28b98; --wrongdir-soft: #3a1c22;
}}
:root[data-theme="light"] {{
  --bg: #f7f5f1; --surface: #ffffff; --surface-2: #f0eee8; --border: #e3ded3;
  --text: #21201d; --text-dim: #6f6a5f; --accent: #4a3fc4; --accent-soft: #ece9fb;
  --ok: #1f7a5c; --ok-soft: #e3f3ec; --bad: #b23a3a; --bad-soft: #fbe9e7;
  --warn: #9a6b12; --warn-soft: #fdf3df; --err: #7a1f5c; --err-soft: #f6e6f0;
  --luck: #b45309; --luck-soft: #fdedd3; --partial: #1d5f8a; --partial-soft: #e2eef6;
  --wrongdir: #8f2d3d; --wrongdir-soft: #f7e3e6;
}}
{katex_css}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{ background: var(--bg); color: var(--text); font-family: var(--sans); line-height: 1.55; }}
.layout {{ display: grid; grid-template-columns: 220px minmax(0,1fr); min-height: 100vh; }}
.sidebar {{
  position: sticky; top: 0; height: 100vh; overflow-y: auto;
  border-right: 1px solid var(--border); background: var(--surface-2); padding: 1.25rem 1rem;
}}
.brand {{ font-family: var(--serif); font-size: 1.15rem; margin: 0 0 .15rem; text-wrap: balance; }}
.brand-sub {{ font-size: .76rem; color: var(--text-dim); margin: 0 0 1rem; }}
.search-box {{
  width: 100%; padding: .5rem .65rem; border-radius: 8px; border: 1px solid var(--border);
  background: var(--surface); color: var(--text); font-family: var(--sans); font-size: .85rem; margin-bottom: .6rem;
}}
.filter-select {{
  width: 100%; padding: .4rem .5rem; border-radius: 8px; border: 1px solid var(--border);
  background: var(--surface); color: var(--text); font-size: .78rem; margin-bottom: .4rem;
}}
.filter-label {{ font-size: .72rem; color: var(--text-dim); margin: .5rem 0 .15rem; text-transform: uppercase; letter-spacing: .04em; }}
.nav-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: .3rem; margin-top: .5rem; }}
.nav-item {{
  padding: .35rem 0; border-radius: 6px; border: 1px solid var(--border); background: var(--surface);
  color: var(--text-dim); font-family: var(--mono); cursor: pointer; font-size: .7rem; text-align: center;
}}
.nav-item:hover {{ border-color: var(--accent); color: var(--text); }}
.nav-item.active {{ background: var(--accent-soft); border-color: var(--accent); color: var(--accent); }}
.nav-item[hidden] {{ display: none; }}

main {{ padding: 2rem clamp(1rem, 3vw, 3rem); max-width: 980px; }}
.page-head h1 {{ font-family: var(--serif); font-size: clamp(1.4rem, 3vw, 1.9rem); margin: 0 0 .3rem; text-wrap: balance; }}
.page-head p {{ color: var(--text-dim); max-width: 68ch; font-size: .92rem; margin: 0 0 1.2rem; }}

.summary {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1.5rem; }}
.summary-row {{ display: grid; grid-template-columns: 80px 1fr 90px; align-items: center; gap: .75rem; margin-bottom: .55rem; }}
.summary-row:last-child {{ margin-bottom: 0; }}
.summary-model {{ font-family: var(--mono); font-size: .82rem; color: var(--text-dim); }}
.summary-bar {{ display: flex; height: 10px; border-radius: 5px; overflow: hidden; background: var(--surface-2); }}
.bar-seg {{ height: 100%; }}
.bar-ok {{ background: var(--ok); }}
.bar-bad {{ background: var(--bad); }}
.bar-warn {{ background: var(--warn); }}
.bar-err {{ background: var(--err); }}
.bar-luck {{ background: var(--luck); }}
.bar-partial {{ background: var(--partial); }}
.bar-wrongdir {{ background: var(--wrongdir); }}
.summary-count {{ font-family: var(--mono); font-size: .78rem; color: var(--text-dim); text-align: right; }}

.card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem 1.4rem; margin-bottom: 1.1rem; scroll-margin-top: 1.25rem; }}
.card-head {{ display: flex; align-items: baseline; gap: .6rem; margin-bottom: .6rem; flex-wrap: wrap; }}
.stt {{ font-family: var(--mono); color: var(--accent); font-size: .8rem; font-weight: 600; }}
.loc {{ font-family: var(--mono); color: var(--text-dim); font-size: .78rem; }}
.status-strip {{ margin-left: auto; display: flex; gap: .3rem; }}
.stem {{ font-size: 1rem; margin-bottom: .5rem; }}
.choices {{ display: grid; grid-template-columns: 1fr 1fr; gap: .35rem .9rem; margin: .6rem 0 .8rem; }}
.choice {{ display: flex; gap: .45rem; font-size: .92rem; align-items: baseline; }}
.choice-letter {{ font-family: var(--mono); color: var(--accent); font-weight: 700; min-width: 1.1em; }}
.answer-line {{ margin: .5rem 0 .7rem; }}
.answer-badge {{ display: inline-block; background: var(--ok-soft); color: var(--ok); font-family: var(--mono); font-size: .82rem; padding: .3rem .6rem; border-radius: 6px; font-weight: 600; }}

.doc-solution {{ margin-bottom: .8rem; border: 1px solid var(--border); border-radius: 8px; padding: .5rem .8rem; }}
.doc-solution summary {{ cursor: pointer; font-size: .85rem; color: var(--text-dim); }}

.model-grid {{ display: grid; gap: .6rem; }}
.model-block {{ border: 1px solid var(--border); border-radius: 8px; padding: .1rem .8rem; }}
.model-block summary {{
  cursor: pointer; padding: .6rem 0; display: flex; align-items: center; gap: .6rem; list-style: none;
}}
.model-block summary::-webkit-details-marker {{ display: none; }}
.model-name {{ font-weight: 600; font-size: .88rem; min-width: 5.5em; }}
.chosen {{ font-size: .78rem; color: var(--text-dim); font-family: var(--mono); }}
.badge {{ font-family: var(--mono); font-size: .74rem; padding: .18rem .5rem; border-radius: 999px; font-weight: 600; }}
.badge-ok {{ background: var(--ok-soft); color: var(--ok); }}
.badge-bad {{ background: var(--bad-soft); color: var(--bad); }}
.badge-warn {{ background: var(--warn-soft); color: var(--warn); }}
.badge-err {{ background: var(--err-soft); color: var(--err); }}
.badge-luck {{ background: var(--luck-soft); color: var(--luck); }}
.badge-partial {{ background: var(--partial-soft); color: var(--partial); }}
.badge-wrongdir {{ background: var(--wrongdir-soft); color: var(--wrongdir); }}
.model-body {{ padding: 0 0 .8rem; font-size: .9rem; }}
.model-body p {{ margin: 0 0 .5rem; }}
.model-body p:last-child {{ margin-bottom: 0; }}
.model-body p.empty {{ color: var(--text-dim); font-style: italic; }}
.comment {{ margin-top: .6rem; padding: .5rem .7rem; background: var(--surface-2); border-radius: 6px; font-size: .85rem; }}
.comment-label {{ font-weight: 600; color: var(--text-dim); }}
.comment-empty {{ color: var(--text-dim); font-style: italic; }}
.katex {{ font-size: 1.02em; }}

@media (max-width: 760px) {{
  .layout {{ grid-template-columns: 1fr; }}
  .sidebar {{ position: static; height: auto; }}
  .choices {{ grid-template-columns: 1fr; }}
  .summary-row {{ grid-template-columns: 70px 1fr 70px; }}
}}
</style>
</head>
<body>

<div class="layout">
  <nav class="sidebar">
    <p class="brand">Đối chiếu 3 model</p>
    <p class="brand-sub">66 câu số phức &middot; ChatGPT / Gemini / Qwen</p>
    <input class="search-box" id="searchBox" type="text" placeholder="Tìm theo số câu…">
    <div class="filter-label">Lọc theo trạng thái</div>
    <select class="filter-select" id="chatgptFilter">
      <option value="">ChatGPT: tất cả</option>
      <option value="Đúng">ChatGPT: Đúng</option>
      <option value="Lụi">ChatGPT: Lụi</option>
      <option value="Đúng ý tưởng nhưng chưa giải xong">ChatGPT: Đúng ý tưởng, chưa xong</option>
      <option value="Sai hướng">ChatGPT: Sai hướng</option>
      <option value="Sai">ChatGPT: Sai</option>
      <option value="Không xác định">ChatGPT: Không xác định</option>
      <option value="Lỗi API">ChatGPT: Lỗi API</option>
    </select>
    <select class="filter-select" id="geminiFilter">
      <option value="">Gemini: tất cả</option>
      <option value="Đúng">Gemini: Đúng</option>
      <option value="Lụi">Gemini: Lụi</option>
      <option value="Đúng ý tưởng nhưng chưa giải xong">Gemini: Đúng ý tưởng, chưa xong</option>
      <option value="Sai hướng">Gemini: Sai hướng</option>
      <option value="Sai">Gemini: Sai</option>
      <option value="Không xác định">Gemini: Không xác định</option>
      <option value="Lỗi API">Gemini: Lỗi API</option>
    </select>
    <select class="filter-select" id="qwenFilter">
      <option value="">Qwen: tất cả</option>
      <option value="Đúng">Qwen: Đúng</option>
      <option value="Lụi">Qwen: Lụi</option>
      <option value="Đúng ý tưởng nhưng chưa giải xong">Qwen: Đúng ý tưởng, chưa xong</option>
      <option value="Sai hướng">Qwen: Sai hướng</option>
      <option value="Sai">Qwen: Sai</option>
      <option value="Không xác định">Qwen: Không xác định</option>
      <option value="Lỗi API">Qwen: Lỗi API</option>
    </select>
    <div class="nav-grid" id="navGrid">
      {nav_items}
    </div>
  </nav>
  <main>
    <div class="page-head">
      <h1>Đối chiếu lời giải 3 mô hình</h1>
      <p>66 câu số phức, kèm lời giải &amp; đánh giá Đúng/Sai của ChatGPT (gpt-4o), Gemini (2.5 flash) và Qwen (3:4b, chạy local). Bấm vào từng model để mở lời giải chi tiết.</p>
    </div>
    <div class="summary">
      {summary_rows}
    </div>
    {''.join(rows_html)}
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
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));

  navItems.forEach(function(btn) {{
    btn.addEventListener('click', function() {{
      var target = document.getElementById(btn.dataset.target);
      if (target) {{
        target.scrollIntoView({{behavior: 'smooth', block: 'start'}});
      }}
    }});
  }});

  var searchBox = document.getElementById('searchBox');
  var chatgptFilter = document.getElementById('chatgptFilter');
  var geminiFilter = document.getElementById('geminiFilter');
  var qwenFilter = document.getElementById('qwenFilter');

  function applyFilters() {{
    var q = searchBox.value.trim();
    var cg = chatgptFilter.value;
    var ge = geminiFilter.value;
    var qw = qwenFilter.value;

    cards.forEach(function(card) {{
      var stt = card.dataset.stt;
      var matchSearch = !q || stt.indexOf(q) !== -1;
      var matchCg = !cg || card.dataset.chatgpt === cg;
      var matchGe = !ge || card.dataset.gemini === ge;
      var matchQw = !qw || card.dataset.qwen === qw;
      card.hidden = !(matchSearch && matchCg && matchGe && matchQw);
    }});

    navItems.forEach(function(btn) {{
      var card = document.getElementById(btn.dataset.target);
      btn.hidden = card ? card.hidden : false;
    }});
  }}

  searchBox.addEventListener('input', applyFilters);
  chatgptFilter.addEventListener('change', applyFilters);
  geminiFilter.addEventListener('change', applyFilters);
  qwenFilter.addEventListener('change', applyFilters);

  var observer = new IntersectionObserver(function(entries) {{
    entries.forEach(function(entry) {{
      if (entry.isIntersecting) {{
        var stt = entry.target.dataset.stt;
        navItems.forEach(function(b) {{ b.classList.toggle('active', b.dataset.target === 'q' + stt); }});
      }}
    }});
  }}, {{ rootMargin: '-10% 0px -80% 0px' }});
  cards.forEach(function(c) {{ observer.observe(c); }});
}});
</script>
</body>
</html>
"""

with open("Doi_chieu_66_cau_so_phuc.html", "w", encoding="utf-8") as f:
    f.write(html_doc)

# Bản fragment cho Artifact (Artifact tool tự bọc <!doctype>/<head>/<body>,
# nên không được để file này tự có các thẻ đó, kẻo bị lồng đôi).
fragment = html_doc
fragment = fragment.replace('<!DOCTYPE html>\n<html lang="vi">\n<head>\n', '')
fragment = fragment.replace('<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n', '')
fragment = fragment.replace('</head>\n<body>\n\n', '')
fragment = fragment.replace('\n</body>\n</html>\n', '')

with open("scratch/review_view_artifact.html", "w", encoding="utf-8") as f:
    f.write(fragment)

print("written standalone:", len(html_doc), "chars; fragment:", len(fragment), "chars")
