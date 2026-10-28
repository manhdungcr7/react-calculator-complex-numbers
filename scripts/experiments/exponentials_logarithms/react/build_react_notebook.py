# -*- coding: utf-8 -*-
"""
Builds the Kaggle notebook for ReAct + Calculator with Qwen3-4B on one
problem type of the Exponential and Logarithm chapter.

    python scripts/experiments/react/build_react_notebook.py D79

What it does (and refuses to continue if any of it fails):
  1. Runs the Action Inputs of the worked example through the REAL Calculator
     backend, so every Observation printed in PART_FEWSHOT is genuine.
  2. Regression check: replays the method of PART_NHIEMVU (the exact
     Calculator calls) on all 90 questions of the type, without any language
     model, and requires the matched letter to equal the stored key.
  3. Lints the model facing text (no dash used as punctuation, English
     identifiers only, the words of PART_TOOL not contradicted).
  4. Writes the notebook, with PART_TOOL / PART_KIENTHUC shared by all types.

Prompt, decoding settings and notebook structure follow the Complex Numbers
ReAct + Calculator notebooks (so_phuc/experiments/Qwen3-4B).
"""
import importlib
import inspect
import json
import re
import sys

sys.path.insert(0, "scripts/experiments/react")
import calculator_backend as backend  # noqa: E402
from part_kienthuc import PART_KIENTHUC  # noqa: E402
from part_tool import PART_TOOL  # noqa: E402

DATA_JSON = "scripts/experiments/plan_solve_prompts_mulogarit_merged.json"
OUT_DIR = "experiments/ReAct-Calculator"
MODEL = "Qwen/Qwen3-4B"


# ----------------------------------------------------------------------------
# 1. worked example with real observations
# ----------------------------------------------------------------------------
def build_fewshot(dang):
    calc = backend.Calculator(free_unknowns=dang.FREE_UNKNOWNS)
    lines = [
        "\n**PART 3: WORKED EXAMPLE (STUDY THIS TRACE CAREFULLY)**\n",
        dang.EXAMPLE_QUESTION + "\n",
        "<think>",
    ]
    last_count = None
    for thought, action_input in dang.EXAMPLE_STEPS:
        if action_input is None:
            lines.append(f"Thought: {thought}\n")
            continue
        result, error = calc.evaluate(action_input)
        assert error is None, f"example step failed: {action_input} -> {error}"
        if action_input.startswith("count ="):
            last_count = int(calc.ns["count"])
        lines.append(f"Thought: {thought}\nAction: Calculator\nAction Input: {action_input}\nObservation: {result}\n")
    assert last_count == dang.EXAMPLE_COUNT, (last_count, dang.EXAMPLE_COUNT)
    truths = {k: bool(calc.ns[k]) for k in ("test_A", "test_B", "test_C", "test_D")}
    assert [k[-1] for k, v in truths.items() if v] == [dang.EXAMPLE_ANSWER], truths
    lines.append("</think>")
    lines.append(f"Final Answer: \\boxed{{{dang.EXAMPLE_ANSWER}}}\n")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# 2. regression: replay PART_NHIEMVU on every question, no language model
# ----------------------------------------------------------------------------
def replay_method(question_text, free_unknowns):
    m = re.search(r"không quá (\d+) số nguyên \$y\$ thỏa mãn \$\\log_\{?(\d+)\}?\(x\^2\+y\)\\ge \\log_\{?(\d+)\}?\(x\+y\)\$", question_text)
    bound, a, b = map(int, m.groups())
    options = dict(re.findall(r"(?m)^([A-D])\.\s*\$?(-?\d+)\$?\.?\s*$", question_text))
    calc = backend.Calculator(free_unknowns=free_unknowns)
    program = [
        f"n_plus_1 = {bound} + 1",
        f"exponent = log({a})/log({b})",
        "threshold = N(n_plus_1**exponent - n_plus_1, 20)",
        "x_roots = solve(x**2 - x - threshold, x)",
        "x_low = Min(x_roots[0], x_roots[1])",
        "x_high = Max(x_roots[0], x_roots[1])",
        "first_x = floor(x_low) + 1",
        "last_x = ceiling(x_high) - 1",
        "count = last_x - first_x + 1",
    ] + [f"test_{k} = Eq(count, {options[k]})" for k in "ABCD"]
    for cmd in program:
        _, err = calc.evaluate(cmd)
        assert err is None, (cmd, err)
    matched = [k for k in "ABCD" if bool(calc.ns[f"test_{k}"])]
    return matched


def regression(dang):
    records = json.load(open(DATA_JSON, encoding="utf-8"))[dang.MA_DANG]
    wrong = []
    for r in records:
        matched = replay_method(r["de_bai_mcq"], dang.FREE_UNKNOWNS)
        if matched != [r["dap_an_letter"]]:
            wrong.append((r["STT"], matched, r["dap_an_letter"]))
    assert not wrong, f"method replay disagrees with the key on {len(wrong)} questions: {wrong[:5]}"
    # The original (source) question is written differently from the generated variants
    # (log base without braces, options without dollar signs): the method must work on it too.
    _, source_text, source_letter = default_source_question(dang.MA_DANG)
    assert replay_method(source_text, dang.FREE_UNKNOWNS) == [source_letter], "method replay fails on the source question"
    return len(records)


# ----------------------------------------------------------------------------
# 3. lint of the model facing text
# ----------------------------------------------------------------------------
def lint(prompt_parts):
    problems = []
    for name, text in prompt_parts.items():
        # Action Input / Observation lines are Calculator code, where "-" is a genuine minus sign.
        stripped = re.sub(r"(?m)^(Action Input|Observation):.*$", " ", text)
        stripped = re.sub(r"```.*?```", " ", stripped, flags=re.S)
        stripped = re.sub(r"\$\$.*?\$\$", " ", stripped, flags=re.S)
        stripped = re.sub(r"\$[^$]*\$", " ", stripped)
        stripped = re.sub(r"`[^`]*`", " ", stripped)
        for pat, label in ((r"[\u2014\u2013]", "em/en dash"), (r"(?<=\S) - (?=\S)", "spaced hyphen used as dash")):
            for mm in re.finditer(pat, stripped):
                problems.append(f"{name}: {label} near {stripped[max(0, mm.start()-30):mm.end()+30]!r}")
    return problems


def lint_identifiers(dang):
    allowed = {"n_plus_1", "exponent", "threshold", "x_roots", "x_low", "x_high", "first_x",
               "last_x", "count", "test_A", "test_B", "test_C", "test_D"}
    problems = []
    for _, ai in dang.EXAMPLE_STEPS:
        if ai:
            name = ai.split("=")[0].strip()
            if name not in allowed:
                problems.append(f"unexpected identifier {name!r} in the example")
    return problems


# ----------------------------------------------------------------------------
# 4. notebook
# ----------------------------------------------------------------------------
def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}


def code(src):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": src.splitlines(keepends=True)}


LOOP_SOURCE = r'''
# =====================================================================
# BATCHED ReAct LOOP: one vLLM call per round for every active question,
# then the Calculator runs separately for each question.
# =====================================================================
STOP_STR = 'Observation:'
MAX_TOOL_CALLS = 25
ACTION_INPUT_RE = re.compile(r'Action Input:[ \t]*(.*)')


class QuestionState:
    """ReAct state of ONE question (own variable memory, own token budget)."""

    def __init__(self, rec, chat_prompt):
        self.rec = rec
        self.chat_prompt = chat_prompt
        self.calculator = Calculator(free_unknowns=FREE_UNKNOWNS)
        # Forced prefix: the model must continue from "Thought:" right after
        # <think>, it cannot start with free prose.
        self.full_text = '<think>\nThought:'
        self.total_tokens = 0
        self.n_calls = 0
        self.tool_log = []
        self.done = False
        self.stop_reason = ''
        self.final_round = False          # tool limit reached: force the Final Answer


initial_prompts = []
for r in records:
    prompt_text = PROMPT_TEMPLATE.replace('{de_bai}', r['de_bai_mcq'])
    initial_prompts.append(tok.apply_chat_template(
        [{'role': 'user', 'content': prompt_text}],
        tokenize=False, add_generation_prompt=True, enable_thinking=True))

states = [QuestionState(r, p) for r, p in zip(records, initial_prompts)]

t0 = time.time()
round_no = 0
while True:
    active = [s for s in states if not s.done]
    if not active:
        break
    round_no += 1

    batch = []
    for s in active:
        model_input = s.chat_prompt + s.full_text
        room = MAX_MODEL_LEN - len(tok(model_input).input_ids) - 8
        n_new = min(MAX_NEW_TOKENS - s.total_tokens, room)
        if n_new <= 0:
            s.done = True
            s.stop_reason = 'out_of_context' if room <= 0 else 'out_of_token_budget'
            continue
        stop = None if s.final_round else [STOP_STR]
        batch.append((s, model_input, SamplingParams(
            temperature=TEMPERATURE, top_p=TOP_P, top_k=TOP_K,
            presence_penalty=PRESENCE_PENALTY, max_tokens=n_new,
            seed=SEED, stop=stop)))

    if not batch:
        break

    outs = llm.generate([p for _, p, _ in batch],
                        [sp_ for _, _, sp_ in batch], use_tqdm=False)

    calls_this_round = 0
    for (s, _, _), out in zip(batch, outs):
        o = out.outputs[0]
        s.full_text += o.text
        s.total_tokens += len(o.token_ids)

        if s.final_round:
            s.done = True
            s.stop_reason = 'tool_limit_reached'
            continue

        if o.stop_reason != STOP_STR:
            s.done = True
            s.stop_reason = ('model_finished' if o.finish_reason == 'stop'
                             else 'out_of_tokens')
            continue

        s.n_calls += 1
        calls_this_round += 1
        match = None
        for mm in ACTION_INPUT_RE.finditer(o.text):
            match = mm
        expression = match.group(1).strip() if match else ''

        if not expression:
            observation = ('ERROR: no "Action Input:" line found. Write a Thought, '
                           'then "Action: Calculator", then "Action Input: <expression>".')
            s.tool_log.append(('(no Action Input)', observation))
        else:
            result, error = s.calculator.evaluate(expression)
            if error:
                observation = (f'ERROR: {error}. Fix the syntax and try again '
                               '(sqrt() for roots, ** for powers, log() for logarithms, '
                               'Eq(a, b) to compare).')
                s.tool_log.append((expression, f'ERROR: {error}'))
            else:
                observation = result
                s.tool_log.append((expression, result))

        s.full_text += f'{STOP_STR} {observation}\n'

        if s.n_calls >= MAX_TOOL_CALLS:
            s.full_text += ('\n[SYSTEM: tool-call limit reached, give your Final '
                            'Answer now, with no further Action.]\n')
            s.final_round = True

    print(f'  Round {round_no:2d}: {len(batch):2d} questions generating, '
          f'{calls_this_round:2d} tool calls, '
          f'{sum(1 for s in states if not s.done):2d} still active '
          f'({time.time()-t0:.0f}s)')

print(f'Finished after {round_no} rounds, {(time.time()-t0)/60:.1f} minutes.')


# =====================================================================
# GRADING + SAVING
# =====================================================================
def extract_letter(t):
    for pat in (r'Final\s+Answer[^A-D]{0,20}([A-D])\b',
                r'\\boxed\{\s*(?:\\text\{\s*)?([A-D])\b',
                r'[Đđ]áp\s*án[^A-D]{0,15}([A-D])\b'):
        m = re.findall(pat, t)
        if m:
            return m[-1]
    return ''


rows = []
for s in states:
    chosen = extract_letter(s.full_text)
    n_err = sum(1 for _, obs in s.tool_log if str(obs).startswith('ERROR'))
    rows.append({
        'STT': s.rec['STT'],
        'ma_dang': s.rec.get('ma_dang', MA_DANG),
        'dap_an_dung': s.rec['dap_an_letter'],
        'model_chon': chosen,
        'DUNG': chosen == s.rec['dap_an_letter'],
        'token': s.total_tokens,
        'tool_calls': s.n_calls,
        'syntax_errors': n_err,
        'stop_reason': s.stop_reason,
        'tool_log': ' | '.join(f'{ex} -> {obs}' for ex, obs in s.tool_log),
        'full_text': s.full_text,
    })

df = pd.DataFrame(rows)
df.to_csv(OUT_PATH, index=False, encoding='utf-8-sig')

n_right = int(df['DUNG'].sum())
n_none = int((df['model_chon'] == '').sum())
print('=' * 72)
print(f"RESULT: {n_right} / {len(df)} correct ({df['DUNG'].mean()*100:.1f}%)   "
      f"wrong={len(df) - n_right - n_none}   undetermined={n_none}")
print('=' * 72)
print()
print('--- Tool usage quality ---')
print(f"Average tool calls per question : {df['tool_calls'].mean():.1f}")
print(f"Total tool calls                : {df['tool_calls'].sum()}")
print(f"Total syntax errors             : {df['syntax_errors'].sum()} "
      f"({df['syntax_errors'].sum() / max(1, df['tool_calls'].sum()) * 100:.1f}%)")
print(f"Questions with NO tool call     : {(df['tool_calls'] == 0).sum()}")
print(f"Average tokens per question     : {df['token'].mean():.0f}")
print()
print('--- Stop reason ---')
print(df['stop_reason'].value_counts())
print()
if (~df['DUNG']).any():
    print('--- WRONG OR UNDETERMINED QUESTIONS ---')
    print(df[~df['DUNG']][['STT', 'dap_an_dung', 'model_chon', 'token',
                           'tool_calls', 'syntax_errors', 'stop_reason']].to_string(index=False))
else:
    print(f"*** ALL {len(df)} QUESTIONS CORRECT ***")
print()
print('Saved:', OUT_PATH)
'''


def build_notebook(dang, prompt_template, intro_stats):
    backend_src = inspect.getsource(backend)
    cells = [
        md(f"""# {dang.MA_DANG}: FULL 90 câu bằng **ReAct + Calculator tool** (Qwen3-4B), chuyên đề Mũ-Logarit

Dạng {dang.MA_DANG}: *đếm số nguyên $x$ sao cho ứng với mỗi $x$ có không quá $N$ số nguyên $y$ thỏa mãn
$\\log_a(x^2+y)\\ge\\log_b(x+y)$ (với $a>b>1$)*. Qwen3-4B zero-shot đúng **0/90** ở dạng này (cả 90 câu đều
hết 9.216 token giữa chừng suy luận).

Model **không tự tính tay bất kỳ phép nào**: mọi phép tính đều gọi tool `Calculator` (sympy, chính xác tuyệt đối,
**có bộ nhớ biến**, hỗ trợ `log`, `exp`, `floor`, `ceiling`, `N(...)`, `solve`, `Eq`, so sánh `<`, `>`...) theo vòng
lặp ReAct thật: `Thought → Action → Action Input → Observation → ...`

Prompt gồm 5 phần giống bộ Số phức: `PART_TOOL` (dùng chung) + `PART_KIENTHUC` (kiến thức nền Mũ-Logarit, dùng chung
cho cả chuyên đề) + `PART_HUONGGIAI` (hướng giải riêng của dạng) + `PART_FEWSHOT` (vết ReAct mẫu, các `Observation`
là kết quả chạy thật bằng chính backend ở cell cuối) + `PART_NHIEMVU` (danh sách bước riêng của dạng).

Prompt được **ép mở đầu bằng `<think>\\nThought:`** (forced prefix), tham số sinh giữ nguyên bản Số phức
(`temperature=0.3, top_p=0.95, top_k=20, seed=42, presence_penalty=1.2, max_new_tokens=9216`).

**Khác bản Số phức:** `MAX_MODEL_LEN` được tính theo độ dài prompt (prompt dài hơn vì `PART_KIENTHUC` của Mũ-Logarit
lớn hơn; bản Số phức đặt cố định 14336).

## Trước khi chạy

1. Dùng lại Kaggle Dataset chứa `plan_solve_prompts_mulogarit_merged.json` (đã dùng cho zero-shot) và gắn vào notebook
   ("Add Data"). Notebook tự dò đường dẫn bằng `glob`, không cần gõ cứng.
2. Bật GPU (khuyến nghị 2×T4).
3. Để thử vài câu trước khi chạy cả 90 câu, đặt `RUN_STT = [1, 2, 3]` ở ô cấu hình.

Kết quả: `/kaggle/working/{dang.MA_DANG.lower()}_react_calculator_full90.csv`
(prompt: {intro_stats['chars']:,} ký tự, ước lượng khoảng {intro_stats['approx_tokens']:,} token)
"""),
        code("!pip install -q -U vllm\n!pip uninstall -y -q torchcodec torchaudio\nimport vllm; print('vLLM:', vllm.__version__)\n"),
        code(f"""import os, re, json, time, glob
import pandas as pd
import torch
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

MA_DANG = '{dang.MA_DANG}'
DATA_FILENAME = 'plan_solve_prompts_mulogarit_merged.json'
# The dataset folder name under /kaggle/input differs between accounts, so
# search for the file instead of hardcoding a path.
_matches = glob.glob(f'/kaggle/input/**/{{DATA_FILENAME}}', recursive=True)
assert _matches, f'{{DATA_FILENAME}} not found under /kaggle/input. Add the dataset to the notebook first.'
DATA_PATH = _matches[0]
OUT_PATH = f'/kaggle/working/{{MA_DANG.lower()}}_react_calculator_full90.csv'

RUN_STT = None            # None = all questions; for a quick test use e.g. [1, 2, 3]

MODEL = '{MODEL}'
# Same decoding settings as the Complex Numbers ReAct + Calculator runs.
TEMPERATURE, TOP_P, TOP_K, SEED = 0.3, 0.95, 20, 42
PRESENCE_PENALTY = 1.2
MAX_NEW_TOKENS = 9216

FREE_UNKNOWNS = {sorted(dang.FREE_UNKNOWNS)!r}
FREE_UNKNOWNS = set(FREE_UNKNOWNS)

os.environ['TOKENIZERS_PARALLELISM'] = 'false'

with open(DATA_PATH, encoding='utf-8') as f:
    records = json.load(f)[MA_DANG]
if RUN_STT is not None:
    records = [r for r in records if r['STT'] in RUN_STT]
print('Questions:', len(records))

tok = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
"""),
        code("# =====================================================================\n"
             "# PROMPT: five parts. PART_TOOL and PART_KIENTHUC are shared by every\n"
             "# problem type of the chapter; PART_HUONGGIAI, PART_FEWSHOT and\n"
             "# PART_NHIEMVU are specific to this one.\n"
             "# =====================================================================\n\n"
             + f"PART_TOOL = r'''{PART_TOOL}'''\n\n"
             + f"PART_KIENTHUC = r'''{PART_KIENTHUC}'''\n\n"
             + f"PART_HUONGGIAI = r'''{dang.PART_HUONGGIAI}'''\n\n"
             + f"PART_FEWSHOT = r'''{intro_stats['fewshot']}'''\n\n"
             + f"PART_NHIEMVU = r'''{dang.PART_NHIEMVU}'''\n\n"
             + "PROMPT_TEMPLATE = (PART_TOOL + PART_KIENTHUC + PART_HUONGGIAI\n"
             + "                   + PART_FEWSHOT + PART_NHIEMVU)\n"),
        code("""# The context window must hold the prompt plus the whole generation budget.
longest = max(records, key=lambda r: len(r['de_bai_mcq']))
PROMPT_TOKENS = len(tok(PROMPT_TEMPLATE.replace('{de_bai}', longest['de_bai_mcq'])).input_ids)
MAX_MODEL_LEN = ((PROMPT_TOKENS + MAX_NEW_TOKENS + 1500) // 1024 + 1) * 1024
print(f'Prompt: {PROMPT_TOKENS} tokens -> MAX_MODEL_LEN={MAX_MODEL_LEN}')

N_GPU = torch.cuda.device_count()
TENSOR_PARALLEL = 2 if N_GPU >= 2 else 1
print(f'GPUs: {N_GPU} -> tensor_parallel_size={TENSOR_PARALLEL}')

llm = LLM(model=MODEL, tensor_parallel_size=TENSOR_PARALLEL, dtype='float16',
          max_model_len=MAX_MODEL_LEN, gpu_memory_utilization=0.90,
          trust_remote_code=True, enforce_eager=True, seed=SEED)
print('Ready.')
"""),
        code("# =====================================================================\n"
             "# BACKEND: the Calculator tool (SymPy with variable memory)\n"
             "# =====================================================================\n"
             + backend_src[backend_src.index("import re"):]
             + "\n" + LOOP_SOURCE),
    ]
    return {
        "cells": cells,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python", "version": "3.11"}},
        "nbformat": 4, "nbformat_minor": 5,
    }


def default_source_question(ma_dang):
    """The original (source) question of the type, used as the default test question."""
    base = "data/questions/mu_logarit_extraction"
    ids = [json.loads(l)["id"] for l in open(f"{base}/Mu_Logarit_107_cau_phan_dang.jsonl", encoding="utf-8")
           if l.strip() and json.loads(l)["Ma dang"] == ma_dang]
    assert len(ids) >= 1, ma_dang
    for line in open(f"{base}/Mu_Logarit_107_cau_goc.jsonl", encoding="utf-8"):
        row = json.loads(line)
        if row["id"] == ids[0]:
            return ids[0], row["de_bai"], row["dap_an"].strip()[0]
    raise AssertionError("source question not found")


def build_notebook_1cau(dang, intro_stats):
    """One question notebook: same four cells and printed report as the
    Complex Numbers 1cau notebooks. Load the model once (Cell 3), then edit
    DE_BAI / DAP_AN_DUNG in Cell 4 and rerun only Cell 4."""
    source_id, question, letter = default_source_question(dang.MA_DANG)
    backend_src = inspect.getsource(backend)
    loop_src = open("scripts/experiments/react/loop_single_question.py", encoding="utf-8").read()
    loop_src = loop_src[loop_src.index("# ====="):]       # drop the explanatory header comment of that file

    cell_intro = md(f"""# {dang.MA_DANG}: Thử nghiệm ReAct + Calculator tool (1 câu, load model 1 lần), chuyên đề Mũ-Logarit

Dạng {dang.MA_DANG}: *đếm số nguyên $x$ sao cho ứng với mỗi $x$ có không quá $N$ số nguyên $y$ thỏa mãn
$\\log_a(x^2+y)\\ge\\log_b(x+y)$ (với $a>b>1$)*. Dạng đầu tiên của chuyên đề Mũ-Logarit thử nghiệm phương pháp
ReAct + Calculator. Chọn vì Qwen3-4B zero-shot đúng **0/90** ở dạng này (cả 90 câu đều hết 9.216 token giữa chừng suy luận).

## Hướng giải (đặt ẩn phụ + khảo sát hàm số)

1. Điều kiện $x+y>0$, $x^2+y>0$; $x,y$ nguyên nên $x+y\\ge1$.
2. Đặt $t=x+y\\ge1$, khi đó $x^2+y=x^2-x+t$.
3. Đưa $a$ lên hai vế rồi dùng $a^{{\\log_b t}}=t^{{\\log_b a}}$ được $x^2-x\\ge t^{{\\log_b a}}-t$.
4. $f(t)=t^{{\\log_b a}}-t$ đồng biến trên $[1;+\\infty)$ vì $a>b>1$ nên $\\log_b a>1$.
5. "Không quá $N$ số nguyên $y$" $\\Leftrightarrow$ "không quá $N$ số nguyên $t$" $\\Leftrightarrow$ $x^2-x<f(N+1)$.
6. Tính số thực $C=f(N+1)$, giải $x^2-x-C<0$ được $x_1<x<x_2$, đếm số nguyên $x$ trong khoảng đó.

## Đã kiểm chứng trước khi chạy

- Làm đúng 6 bước trên cho ra đáp án đúng **90/90 câu D79** (đã chạy lại bằng đúng các lệnh Calculator của `PART_NHIEMVU`,
  đối chiếu đáp án lưu, không có nghiệm nào sát số nguyên).
- Ví dụ trong `PART_FEWSHOT` ($a=7$, $b=5$, $N=120$, đáp án 28) không nằm trong 90 câu đánh giá, đáp án kiểm chứng độc lập
  bằng vét cạn, và mọi `Observation` đều là kết quả chạy thật bằng chính backend ở cell cuối.
- Vòng lặp ReAct, backend và chấm điểm đã chạy thử với mô hình giả làm đúng hướng dẫn: đúng, 13 lượt gọi tool, 0 lỗi cú pháp.
- Prompt dài khoảng {intro_stats['approx_tokens']:,} token (ước lượng), nên `MAX_MODEL_LEN` ở Cell 3 đặt 18432
  (bản Số phức là 14336). Cell 4 tự kiểm tra và báo lỗi nếu prompt không còn đủ chỗ cho 9.216 token sinh.

## Cách dùng

Giống hệt các bản trước: chạy Cell 1 → 3 (nạp model, 1 lần), sửa `DE_BAI`/`DAP_AN_DUNG` ở Cell 4 rồi chạy lại Cell 4.
Câu mặc định là câu gốc ({source_id}, đáp án {letter}).
""")
    cell_pip = code("!pip install -q -U vllm\n!pip uninstall -y -q torchcodec torchaudio\nimport vllm; print('vLLM:', vllm.__version__)\n")
    cell_model = code(f"""import re, time
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

MODEL = '{MODEL}'
MAX_MODEL_LEN, MAX_NEW_TOKENS = 18432, 9216
TEMPERATURE, TOP_P, TOP_K, SEED = 0.3, 0.95, 20, 42
PRESENCE_PENALTY = 1.2

tok = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
llm = LLM(model=MODEL, tensor_parallel_size=1, dtype='float16',
          max_model_len=MAX_MODEL_LEN, gpu_memory_utilization=0.90,
          trust_remote_code=True, enforce_eager=True, seed=SEED)
print('San sang - CHI CAN CHAY 1 LAN.')
""")
    free_unknowns = "{" + ", ".join(repr(u) for u in sorted(dang.FREE_UNKNOWNS)) + "}"
    cell_main = code(
        "# =====================================================================\n"
        "# CELL 4 - SUA O DAY ROI CHAY LAI CELL NAY (khong can load lai model)\n"
        "# =====================================================================\n"
        "# MODULAR PROMPT ARCHITECTURE (to generalize to other types):\n"
        "#   [A] PART_TOOL      - how to use the ReAct tool        -> SHARED BY EVERY TYPE\n"
        "#   [B] PART_KIENTHUC  - foundational knowledge of the chapter -> SHARED BY THE WHOLE CHAPTER\n"
        "#   [C] PART_HUONGGIAI - solution method of this type     -> CHANGES PER TYPE\n"
        "#   [D] PART_FEWSHOT   - worked example of this type      -> CHANGES PER TYPE\n"
        "#   [E] PART_NHIEMVU   - the task steps + the question    -> CHANGES PER TYPE\n"
        "# Switching to another type => rewrite [C], [D], [E]; keep [A] and [B].\n\n"
        f"DE_BAI = r'''{question}'''\n"
        f"DAP_AN_DUNG = '{letter}'\n\n"
        "# Free unknowns: letters the Calculator accepts without an earlier assignment.\n"
        "# In this type x is the unknown of solve(...).\n"
        f"AN_SO_TU_DO = {free_unknowns}\n\n\n"
        "# =====================================================================\n"
        "# [A] PART_TOOL (SHARED BY EVERY TYPE)\n"
        "# =====================================================================\n"
        f"PART_TOOL = r'''{PART_TOOL}'''\n\n\n"
        "# =====================================================================\n"
        "# [B] PART_KIENTHUC (SHARED BY THE WHOLE EXPONENTIAL AND LOGARITHM CHAPTER)\n"
        "# =====================================================================\n"
        f"PART_KIENTHUC = r'''{PART_KIENTHUC}'''\n\n\n"
        "# =====================================================================\n"
        f"# [C] PART_HUONGGIAI ({dang.MA_DANG})\n"
        "# =====================================================================\n"
        f"PART_HUONGGIAI = r'''{dang.PART_HUONGGIAI}'''\n\n\n"
        "# =====================================================================\n"
        f"# [D] PART_FEWSHOT ({dang.MA_DANG}); the Observation lines are REAL results of\n"
        "# the Calculator class below, not made up numbers.\n"
        "# =====================================================================\n"
        f"PART_FEWSHOT = r'''{intro_stats['fewshot']}'''\n\n\n"
        "# =====================================================================\n"
        f"# [E] PART_NHIEMVU ({dang.MA_DANG})\n"
        "# =====================================================================\n"
        f"PART_NHIEMVU = r'''{dang.PART_NHIEMVU}'''\n\n"
        "PROMPT_TEMPLATE = (PART_TOOL + PART_KIENTHUC + PART_HUONGGIAI\n"
        "                   + PART_FEWSHOT + PART_NHIEMVU)\n\n\n"
        "# =====================================================================\n"
        "# BACKEND: the Calculator tool (SymPy with variable memory)\n"
        "# =====================================================================\n"
        + backend_src[backend_src.index("import re"):]
        + "\n\n" + loop_src
    )
    return {
        "cells": [cell_intro, cell_pip, cell_model, cell_main],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python", "version": "3.11"}},
        "nbformat": 4, "nbformat_minor": 5,
    }


def backend_self_check(free_unknowns):
    """The failure seen on Kaggle: "N = 94" silently replaced the function N(...)."""
    calc = backend.Calculator(free_unknowns=free_unknowns)
    for bad in ("N = 94", "E = 3", "I = 2") + tuple(f"{u} = 5" for u in sorted(free_unknowns)):
        result, error = calc.evaluate(bad)
        assert result is None and error and "cannot be" in error, (bad, result, error)
    # Unknown function names must never be stored as if they were results.
    calc.evaluate("big = 115.36")
    for bad in ("ceil(big)", "log10(100)", "log2(8)", "int(big)", "Floor(big)", "count = ceil(big) - 1"):
        result, error = calc.evaluate(bad)
        assert result is None and error and "unknown function" in error, (bad, result, error)
    assert "count" not in calc.ns, "a refused assignment must not be stored"
    # Common spellings that DO work and must keep working.
    for ok, expected in (("ln(5)", "log(5)"), ("2^3", "8"), ("log(8, 2)", "3"), ("floor(big)", "115"),
                         ("ceiling(big)", "116"), ("Max(1, 2)", "2")):
        result, error = calc.evaluate(ok)
        assert error is None and result == expected, (ok, result, error)
    for good in ("bound = 94", "n_plus_1 = bound + 1", "exponent = log(18)/log(4)",
                 "threshold = N(n_plus_1**exponent - n_plus_1, 20)"):
        result, error = calc.evaluate(good)
        assert error is None, (good, error)
    return True


def main():
    ma_dang = sys.argv[1] if len(sys.argv) > 1 else "D79"
    dang = importlib.import_module(f"dang_{ma_dang}")

    backend_self_check(dang.FREE_UNKNOWNS)
    print("[ok] backend refuses names that would replace a Calculator function (N, E, I, ...) or an unknown")
    fewshot = build_fewshot(dang)
    n_checked = regression(dang)
    print(f"[ok] worked example replayed with the real Calculator; "
          f"method replay matches the key on {n_checked}/{n_checked} questions")

    parts = {"PART_TOOL": PART_TOOL, "PART_KIENTHUC": PART_KIENTHUC, "PART_HUONGGIAI": dang.PART_HUONGGIAI,
             "PART_FEWSHOT": fewshot, "PART_NHIEMVU": dang.PART_NHIEMVU}
    problems = lint(parts) + lint_identifiers(dang)
    assert not problems, "lint problems:\n" + "\n".join(problems)
    print("[ok] lint: no dash used as punctuation, identifiers are English")

    prompt_template = "".join(parts.values())
    chars = len(prompt_template)
    stats = {"chars": chars, "approx_tokens": int(chars / 3.3), "fewshot": fewshot}
    print(f"[ok] prompt is {chars:,} characters (about {stats['approx_tokens']:,} tokens)")

    nb = build_notebook(dang, prompt_template, stats)
    out = f"{OUT_DIR}/KLTN_{ma_dang}_ReAct_Calculator_full90.ipynb"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    with open(f"{OUT_DIR}/prompt_{ma_dang}.txt", "w", encoding="utf-8") as f:
        f.write(prompt_template.replace("{de_bai}", "<DE_BAI_HERE>"))
    print("wrote", out)

    nb1 = build_notebook_1cau(dang, stats)
    out1 = f"{OUT_DIR}/KLTN_{ma_dang}_ReAct_Calculator_1cau.ipynb"
    with open(out1, "w", encoding="utf-8") as f:
        json.dump(nb1, f, ensure_ascii=False, indent=1)
    print("wrote", out1)


if __name__ == "__main__":
    main()
