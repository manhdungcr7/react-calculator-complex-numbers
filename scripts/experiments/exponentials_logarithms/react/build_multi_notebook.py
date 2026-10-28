# -*- coding: utf-8 -*-
"""
Builds ONE Kaggle notebook that runs ReAct + Calculator (Qwen3-4B) on several
problem types of the Exponential and Logarithm chapter, one after the other,
with the model loaded once.

    python scripts/experiments/react/build_multi_notebook.py G01 D89 D84 D47

Checks done before a notebook is written (it refuses to continue if any fails):
  1. backend self check (reserved names, unknown functions, working spellings);
  2. the worked example of each type is run through the REAL Calculator, so every
     Observation printed in PART_FEWSHOT is genuine, and it must pick EXAMPLE_ANSWER;
  3. the commands of the method (dang.program + the four option tests) are replayed
     on all 90 questions AND on the source question, without any language model,
     and the matched letter must be the stored key, with no error;
  4. the commands of the worked example equal the commands of the method, and every
     variable name of the method appears in PART_NHIEMVU;
  5. lint of the model facing text (no dash used as punctuation).
"""
import importlib
import inspect
import json
import re
import sys

import pandas as pd

sys.path.insert(0, "scripts/experiments/react")
import calculator_backend as backend  # noqa: E402
import framework as fw  # noqa: E402
from build_react_notebook import backend_self_check, default_source_question, lint, md, code  # noqa: E402
from part_kienthuc import PART_KIENTHUC  # noqa: E402
from part_tool import PART_TOOL  # noqa: E402

DATA_JSON = "scripts/experiments/plan_solve_prompts_mulogarit_merged.json"
STATS_CSV = "data/results/qwen3_4b_zeroshot/full_dataset/thong_ke_theo_dang_regraded.csv"
OUT_DIR = "experiments/ReAct-Calculator"
MODEL = "Qwen/Qwen3-4B"
NAME_OK = re.compile(r"^[a-z][a-z0-9_]*$")


# ----------------------------------------------------------------------------
# worked example with real observations
# ----------------------------------------------------------------------------
def option_block(dang, question_text):
    """The standard closing steps: copy the four options side by side, test each, line them up."""
    shown = fw.display_options(dang, question_text)
    style = getattr(dang, "OPTION_STYLE", "exact")
    side = ", ".join(f"{k}: ${raw}$" for k, raw, _ in shown)
    steps = [(f"The computation is done and its results are stored. Before testing anything, I copy all four options exactly as they "
              f"are written in the problem, side by side: {side}. I will write each one in Calculator syntax, "
              f"test them one call per option, and read each result next to the option I copied here.", None)]
    for k, raw, calc in shown:
        reason = dang.option_reason(question_text, k) if hasattr(dang, "option_reason") else None
        if reason:
            steps.append((f"Option {k} is ${raw}$. {reason}", fw.test_command(k, calc, style)))
        elif raw.replace(" ", "") == calc.replace(" ", ""):
            steps.append((f"Option {k} is ${raw}$.", fw.test_command(k, calc, style)))
        else:
            steps.append((f"Option {k} is ${raw}$; in Calculator syntax this is `{calc}`.", fw.test_command(k, calc, style)))
    return steps


def option_store_steps(dang, question_text, stores):
    """OPTION_VARIABLES: the four options are stored first, one command each, before anything is computed."""
    shown = fw.display_options(dang, question_text)
    steps = []
    for (k, raw, calc), command in zip(shown, stores):
        if k == "A":
            lead = ("Before computing anything, I store the four options exactly as they are written in the problem, "
                    "in the order A, B, C, D, one command each, so that no option can be mixed up later. ")
        else:
            lead = ""
        if hasattr(dang, "option_store_thought"):
            steps.append((lead + dang.option_store_thought(k, raw, calc), command))
        elif raw.replace(" ", "") == calc.replace(" ", ""):
            steps.append((f"{lead}Option {k} is ${raw}$.", command))
        else:
            steps.append((f"{lead}Option {k} is ${raw}$; in Calculator syntax this is `{calc}`.", command))
    return steps


def option_test_steps(dang, question_text, tests):
    steps = [("The four options are stored and the result is computed. I test the result against each stored option, "
              "one call per option, in the order A, B, C, D.", None)]
    for k, command in zip("ABCD", tests):
        steps.append((f"Test option {k}, stored as `option_{k.lower()}`.", command))
    return steps


def build_fewshot(dang):
    cmds = fw.full_program(dang, dang.EXAMPLE_QUESTION)
    ov = getattr(dang, "OPTION_VARIABLES", False)
    if ov:
        stores, program, tests = cmds[:4], cmds[4:-4], cmds[-4:]
    else:
        stores, program, tests = [], cmds[:-4], cmds[-4:]
    assert len(dang.EXAMPLE_THOUGHTS) == len(program), (
        f"{dang.MA_DANG}: EXAMPLE_THOUGHTS has {len(dang.EXAMPLE_THOUGHTS)} entries, program has {len(program)}")
    thoughts = list(dang.EXAMPLE_THOUGHTS)
    reading = [(dang.EXAMPLE_READING, None)] if hasattr(dang, "EXAMPLE_READING") else []
    if ov:
        if not reading:
            # the options were already read first, so the first method Thought continues from there
            thoughts[0] = thoughts[0].replace("I read the problem. ", "The options are stored. Now the data of the problem: ", 1)
        store_steps = option_store_steps(dang, dang.EXAMPLE_QUESTION, stores)
        if reading and getattr(dang, "MERGE_READING", False):
            # the options are stored FIRST (before the model has looked at any data); the digit by digit reading
            # opens the Thought of the first command of the method, so no Thought is left without an Action
            thoughts[0] = reading[0][0] + " " + thoughts[0]
            reading = []
        test_steps = option_test_steps(dang, dang.EXAMPLE_QUESTION, tests)
        if getattr(dang, "MERGE_READING", False):
            # no Thought without an Action anywhere in the trace: the opening sentence joins the first test
            test_steps[1] = (test_steps[0][0] + " " + test_steps[1][0], test_steps[1][1])
            test_steps = test_steps[1:]
        steps = reading + store_steps + list(zip(thoughts, program)) + test_steps
    else:
        steps = reading + list(zip(thoughts, program)) + option_block(dang, dang.EXAMPLE_QUESTION)
    calc = backend.Calculator(free_unknowns=dang.FREE_UNKNOWNS)
    lines = ["\n**PART 3: WORKED EXAMPLE (STUDY THIS TRACE CAREFULLY)**\n", dang.EXAMPLE_QUESTION + "\n", "<think>"]
    for thought, action_input in steps:
        if action_input is None:
            lines.append(f"Thought: {thought}\n")
            continue
        result, error = calc.evaluate(action_input)
        assert error is None, f"{dang.MA_DANG} example step failed: {action_input} -> {error}"
        lines.append(f"Thought: {thought}\nAction: Calculator\nAction Input: {action_input}\nObservation: {result}\n")
    truths = {k: bool(calc.ns[f"test_{k}"]) for k in "ABCD"}
    assert [k for k, v in truths.items() if v] == [dang.EXAMPLE_ANSWER], (dang.MA_DANG, truths)
    shown = fw.display_options(dang, dang.EXAMPLE_QUESTION)
    if ov:
        lines.append(f"Thought: Only `test_{dang.EXAMPLE_ANSWER}` is True and the other three are False, "
                     f"so the answer is {dang.EXAMPLE_ANSWER}.\n")
    else:
        lineup = ", ".join(f"{k}: ${raw}$ gives {truths[k]}" for k, raw, _ in shown)
        lines.append(f"Thought: Lining up what I copied with the stored results: {lineup}. "
                     f"Exactly one option matches, and it is {dang.EXAMPLE_ANSWER}.\n")
    if hasattr(dang, "example_check"):
        dang.example_check(calc, dang.EXAMPLE_QUESTION)
    elif hasattr(dang, "brute_force"):
        independent = dang.brute_force(dang.EXAMPLE_QUESTION)
        assert abs(float(calc.ns["answer"]) - float(independent)) < getattr(dang, "BRUTE_TOLERANCE", 1e-9), (dang.MA_DANG, calc.ns["answer"], independent)
    lines.append("</think>")
    lines.append(f"Final Answer: \\boxed{{{dang.EXAMPLE_ANSWER}}}\n")
    return "\n".join(lines), [c for _, c in steps if c]


# ----------------------------------------------------------------------------
# regression without a language model
# ----------------------------------------------------------------------------
def replay(dang, question_text):
    calc = backend.Calculator(free_unknowns=dang.FREE_UNKNOWNS)
    cmds = fw.full_program(dang, question_text)
    for cmd in cmds:
        _, err = calc.evaluate(cmd)
        assert err is None, (cmd, err)
    return [k for k in "ABCD" if bool(calc.ns[f"test_{k}"])], len(cmds)


def regression(dang):
    records = json.load(open(DATA_JSON, encoding="utf-8"))[dang.MA_DANG]
    wrong, longest = [], 0
    for r in records:
        matched, n = replay(dang, r["de_bai_mcq"])
        longest = max(longest, n)
        if matched != [r["dap_an_letter"]]:
            wrong.append((r["STT"], matched, r["dap_an_letter"]))
    assert not wrong, f"{dang.MA_DANG}: replay disagrees with the key on {len(wrong)} questions: {wrong[:6]}"
    if getattr(dang, "SOURCE_REPLAY", True):
        _, source_text, source_letter = default_source_question(dang.MA_DANG)
        matched, n = replay(dang, source_text)
        longest = max(longest, n)
        assert matched == [source_letter], f"{dang.MA_DANG}: replay fails on the source question: {matched} vs {source_letter}"
    else:
        print(f"[note] {dang.MA_DANG}: the source question is written with other numbers/bases and is not replayed")
    return len(records), longest


def check_consistency(dang, example_cmds):
    assigned = []
    for c in example_cmds:
        m = re.match(r"^([A-Za-z_]\w*)\s*=", c)
        if m:
            assigned.append(m.group(1))
    problems = []
    for name in assigned:
        if not NAME_OK.match(name) and not name.startswith("test_"):
            problems.append(f"{dang.MA_DANG}: bad variable name {name!r}")
        if name in backend.RESERVED_NAMES or name in dang.FREE_UNKNOWNS:
            problems.append(f"{dang.MA_DANG}: variable name {name!r} clashes with a Calculator name")
        if f"`{name}" not in dang.PART_NHIEMVU and name not in ("test_A", "test_B", "test_C", "test_D"):
            problems.append(f"{dang.MA_DANG}: variable {name!r} is not mentioned in PART_NHIEMVU")
    return problems


# ----------------------------------------------------------------------------
# notebook
# ----------------------------------------------------------------------------
LOOP_SOURCE = r'''
# =====================================================================
# BATCHED ReAct LOOP (one function call = one problem type, all its questions):
# one vLLM call per round for every active question, then the Calculator
# runs separately for each question.
# =====================================================================
STOP_STR = 'Observation:'
ACTION_INPUT_RE = re.compile(r'Action Input:[ \t]*(.*)')


class QuestionState:
    """ReAct state of ONE question (own variable memory, own token budget)."""

    def __init__(self, rec, chat_prompt, free_unknowns):
        self.rec = rec
        self.chat_prompt = chat_prompt
        self.calculator = Calculator(free_unknowns=free_unknowns)
        # Forced prefix: the model must continue from "Thought:" right after
        # <think>, it cannot start with free prose.
        self.full_text = '<think>\nThought:'
        self.total_tokens = 0
        self.n_calls = 0
        self.tool_log = []
        self.done = False
        self.stop_reason = ''
        self.final_round = False          # tool limit reached: force the Final Answer


def extract_letter(t):
    for pat in (r'Final\s+Answer[^A-D]{0,20}([A-D])\b',
                r'\\boxed\{\s*(?:\\text\{\s*)?([A-D])\b',
                r'[Đđ]áp\s*án[^A-D]{0,15}([A-D])\b'):
        m = re.findall(pat, t)
        if m:
            return m[-1]
    return ''


def run_type(ma_dang):
    spec = TYPE_PROMPTS[ma_dang]
    free_unknowns = set(spec['free_unknowns'])
    max_tool_calls = spec['max_tool_calls']
    records = ALL_RECORDS[ma_dang]
    if RUN_STT is not None:
        records = [r for r in records if r['STT'] in RUN_STT]
    out_path = f'/kaggle/working/{ma_dang.lower()}_react_calculator_full90.csv'
    print('=' * 72)
    print(f'{ma_dang}: {len(records)} questions')
    print('=' * 72)

    states = []
    for r in records:
        prompt_text = spec['template'].replace('{de_bai}', r['de_bai_mcq'])
        chat = tok.apply_chat_template([{'role': 'user', 'content': prompt_text}],
                                       tokenize=False, add_generation_prompt=True, enable_thinking=True)
        states.append(QuestionState(r, chat, free_unknowns))

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
                repeated = bool(s.tool_log) and s.tool_log[-1][0] == expression \
                    and str(s.tool_log[-1][1]).startswith('ERROR')
                result, error = s.calculator.evaluate(expression)
                if error:
                    observation = (f'ERROR: {error}. Fix the syntax and try again '
                                   '(sqrt() for roots, ** for powers, log() for logarithms, '
                                   'Eq(a, b) to compare).')
                    if repeated:
                        observation += (' You just sent exactly this expression and it failed in the same way. '
                                        'Do not send it again unchanged: change it, or first store the values it uses.')
                    s.tool_log.append((expression, f'ERROR: {error}'))
                else:
                    observation = result
                    s.tool_log.append((expression, result))

            s.full_text += f'{STOP_STR} {observation}\n'

            if s.n_calls >= max_tool_calls:
                s.full_text += ('\n[SYSTEM: tool-call limit reached, give your Final '
                                'Answer now, with no further Action.]\n')
                s.final_round = True

        print(f'  Round {round_no:2d}: {len(batch):2d} questions generating, '
              f'{calls_this_round:2d} tool calls, '
              f'{sum(1 for s in states if not s.done):2d} still active '
              f'({time.time()-t0:.0f}s)')

    print(f'Finished after {round_no} rounds, {(time.time()-t0)/60:.1f} minutes.')

    rows = []
    for s in states:
        chosen = extract_letter(s.full_text)
        n_err = sum(1 for _, obs in s.tool_log if str(obs).startswith('ERROR'))
        rows.append({
            'STT': s.rec['STT'],
            'ma_dang': s.rec.get('ma_dang', ma_dang),
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
    df.to_csv(out_path, index=False, encoding='utf-8-sig')

    n_right = int(df['DUNG'].sum())
    n_none = int((df['model_chon'] == '').sum())
    print(f"RESULT {ma_dang}: {n_right} / {len(df)} correct ({df['DUNG'].mean()*100:.1f}%)   "
          f"wrong={len(df) - n_right - n_none}   undetermined={n_none}")
    print(f"Average tool calls per question : {df['tool_calls'].mean():.1f}   "
          f"Total syntax errors: {df['syntax_errors'].sum()} "
          f"({df['syntax_errors'].sum() / max(1, df['tool_calls'].sum()) * 100:.1f}%)   "
          f"Questions with NO tool call: {(df['tool_calls'] == 0).sum()}   "
          f"Average tokens: {df['token'].mean():.0f}")
    print(df['stop_reason'].value_counts().to_string())
    if (~df['DUNG']).any():
        print('--- WRONG OR UNDETERMINED QUESTIONS ---')
        print(df[~df['DUNG']][['STT', 'dap_an_dung', 'model_chon', 'token',
                               'tool_calls', 'syntax_errors', 'stop_reason']].to_string(index=False))
    else:
        print(f'*** ALL {len(df)} QUESTIONS CORRECT ***')
    print('Saved:', out_path)
    return df
'''

RUN_SOURCE = r'''
# =====================================================================
# RUN EVERY TYPE OF THIS NOTEBOOK, ONE AFTER THE OTHER
# =====================================================================
summary_rows = []
for ma in RUN_TYPES:
    d_ = run_type(ma)
    summary_rows.append({'ma_dang': ma, 'tong': len(d_), 'dung': int(d_['DUNG'].sum()),
                         'ti_le_dung': round(float(d_['DUNG'].mean()) * 100, 1),
                         'tool_calls_tb': round(float(d_['tool_calls'].mean()), 1),
                         'syntax_errors': int(d_['syntax_errors'].sum()),
                         'token_tb': round(float(d_['token'].mean()))})
    pd.DataFrame(summary_rows).to_csv(f'/kaggle/working/summary_{GROUP}.csv', index=False, encoding='utf-8-sig')

print()
print('=' * 72)
print('SUMMARY')
print('=' * 72)
print(pd.DataFrame(summary_rows).to_string(index=False))
'''


def zero_shot_rates():
    d = pd.read_csv(STATS_CSV)
    return {r["ma_dang"]: (int(r["dung"]), int(r["tong"])) for _, r in d.iterrows()}


def build_group(group, codes):
    rates = zero_shot_rates()
    specs, intro_rows = {}, []
    for ma in codes:
        dang = importlib.import_module(f"dang_{ma}")
        assert dang.MA_DANG == ma
        backend_self_check(dang.FREE_UNKNOWNS)
        all_texts = {r["de_bai_mcq"].strip() for r in json.load(open(DATA_JSON, encoding="utf-8"))[ma]}
        assert dang.EXAMPLE_QUESTION.strip() not in all_texts, f"{ma}: the worked example is one of the 90 questions"
        fewshot, example_cmds = build_fewshot(dang)
        n, longest = regression(dang)
        problems = lint({"PART_TOOL": PART_TOOL, "PART_KIENTHUC": PART_KIENTHUC, "PART_HUONGGIAI": dang.PART_HUONGGIAI,
                         "PART_FEWSHOT": fewshot, "PART_NHIEMVU": dang.PART_NHIEMVU})
        problems += check_consistency(dang, example_cmds)
        assert not problems, "\n".join(problems)
        template = PART_TOOL + PART_KIENTHUC + dang.PART_HUONGGIAI + fewshot + dang.PART_NHIEMVU
        specs[ma] = {"template": template, "free_unknowns": sorted(dang.FREE_UNKNOWNS),
                     "max_tool_calls": max(25, longest + 10)}
        z = rates[ma]
        intro_rows.append(f"| {ma} | {dang.TITLE_VI} | {z[0]}/{z[1]} | {longest} | {len(template):,} |")
        print(f"[ok] {ma}: example real; replay matches the key on {n}/{n} questions and the source question; "
              f"{longest} commands at most; prompt {len(template):,} characters")
        suffix = "_v2" if group.startswith("H") else (f"_v{int(group[1:]) + 2}" if group.startswith("R") else "")
        with open(f"{OUT_DIR}/prompt_{ma}{suffix}.txt", "w", encoding="utf-8") as f:
            f.write(template.replace("{de_bai}", "<DE_BAI_HERE>"))

    backend_src = inspect.getsource(backend)
    cells = [
        md(f"""# {group}: ReAct + Calculator (Qwen3-4B), chuyên đề Mũ-Logarit, {len(codes)} dạng: {', '.join(codes)}

Notebook chạy **lần lượt {len(codes)} dạng** mà Qwen3-4B zero-shot chưa đạt 100%, nạp model **một lần**. Mỗi dạng chạy đủ
90 câu và ghi một file `<mã dạng>_react_calculator_full90.csv` trong `/kaggle/working`, cuối cùng ghi `summary_{group}.csv`.

| Dạng | Nội dung | Zero-shot đúng | Số lệnh Calculator tối đa | Độ dài prompt (ký tự) |
|---|---|---|---|---|
""" + "\n".join(intro_rows) + """

Model **không tự tính tay bất kỳ phép nào**: mọi phép tính đều gọi tool `Calculator` (sympy, chính xác tuyệt đối, có bộ nhớ biến)
theo vòng lặp ReAct thật: `Thought → Action → Action Input → Observation → ...`

Prompt mỗi dạng gồm 5 phần giống bộ Số phức và dạng D79: `PART_TOOL` + `PART_KIENTHUC` (dùng chung) + `PART_HUONGGIAI`
(hướng giải theo lời giải mẫu của câu gốc) + `PART_FEWSHOT` (các `Observation` là kết quả chạy thật bằng chính backend) + `PART_NHIEMVU`.
Tham số sinh: `temperature=0.3, top_p=0.95, top_k=20, seed=42, presence_penalty=1.2, max_new_tokens=9216`, ép mở đầu `<think>\\nThought:`.

## Trước khi chạy

1. Gắn Kaggle Dataset chứa `plan_solve_prompts_mulogarit_merged.json` (đã dùng cho zero-shot). Notebook tự dò đường dẫn bằng `glob`.
2. Bật GPU (khuyến nghị 2×T4), chọn **Save & Run All**.
3. Muốn thử nhanh vài câu: đặt `RUN_STT = [1, 2, 3]` và/hoặc `RUN_TYPES` ở ô cấu hình.
"""),
        code("!pip install -q -U vllm\n!pip uninstall -y -q torchcodec torchaudio\nimport vllm; print('vLLM:', vllm.__version__)\n"),
        code(f"""import os, re, json, time, glob
import pandas as pd
import torch
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

GROUP = '{group}'
RUN_TYPES = {codes!r}      # the types of this notebook, in running order
DATA_FILENAME = 'plan_solve_prompts_mulogarit_merged.json'
# The dataset folder name under /kaggle/input differs between accounts, so
# search for the file instead of hardcoding a path.
_matches = glob.glob(f'/kaggle/input/**/{{DATA_FILENAME}}', recursive=True)
assert _matches, f'{{DATA_FILENAME}} not found under /kaggle/input. Add the dataset to the notebook first.'
DATA_PATH = _matches[0]

RUN_STT = None            # None = all 90 questions; for a quick test use e.g. [1, 2, 3]

MODEL = '{MODEL}'
# Same decoding settings as the Complex Numbers ReAct + Calculator runs.
TEMPERATURE, TOP_P, TOP_K, SEED = 0.3, 0.95, 20, 42
PRESENCE_PENALTY = 1.2
MAX_NEW_TOKENS = 9216

os.environ['TOKENIZERS_PARALLELISM'] = 'false'

with open(DATA_PATH, encoding='utf-8') as f:
    _all = json.load(f)
ALL_RECORDS = {{ma: _all[ma] for ma in RUN_TYPES}}
print({{ma: len(v) for ma, v in ALL_RECORDS.items()}})

tok = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
"""),
        code("# =====================================================================\n"
             "# PROMPTS. PART_TOOL and PART_KIENTHUC are shared by every problem type of the\n"
             "# chapter; PART_HUONGGIAI, PART_FEWSHOT and PART_NHIEMVU are specific to each type.\n"
             "# TYPE_PROMPTS[type]['template'] is the five parts joined; {de_bai} is the question.\n"
             "# =====================================================================\n\n"
             + f"PART_TOOL = r'''{PART_TOOL}'''\n\n"
             + f"PART_KIENTHUC = r'''{PART_KIENTHUC}'''\n\n"
             + "TYPE_PROMPTS = {}\n\n"
             + "\n\n".join(_type_cell(ma, specs[ma], importlib.import_module(f"dang_{ma}")) for ma in codes)),
        code("""# The context window must hold the longest prompt plus the whole generation budget.
PROMPT_TOKENS = 0
for ma, spec in TYPE_PROMPTS.items():
    longest = max(ALL_RECORDS[ma], key=lambda r: len(r['de_bai_mcq']))
    n_tok = len(tok(spec['template'].replace('{de_bai}', longest['de_bai_mcq'])).input_ids)
    print(f'{ma}: prompt {n_tok} tokens')
    PROMPT_TOKENS = max(PROMPT_TOKENS, n_tok)
MAX_MODEL_LEN = ((PROMPT_TOKENS + MAX_NEW_TOKENS + 1500) // 1024 + 1) * 1024
print(f'Longest prompt: {PROMPT_TOKENS} tokens -> MAX_MODEL_LEN={MAX_MODEL_LEN}')

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
             + "\n" + LOOP_SOURCE + "\n" + RUN_SOURCE),
    ]
    nb = {"cells": cells,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python", "version": "3.11"}},
          "nbformat": 4, "nbformat_minor": 5}
    out = f"{OUT_DIR}/KLTN_{group}_ReAct_Calculator.ipynb"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("wrote", out)


def _type_cell(ma, spec, dang):
    """Source text defining the five parts of one type and its TYPE_PROMPTS entry."""
    fewshot, _ = build_fewshot(dang)
    return (f"# ---------------------------------------------------------------- {ma}\n"
            f"{ma}_HUONGGIAI = r'''{dang.PART_HUONGGIAI}'''\n\n"
            f"{ma}_FEWSHOT = r'''{fewshot}'''\n\n"
            f"{ma}_NHIEMVU = r'''{dang.PART_NHIEMVU}'''\n\n"
            f"TYPE_PROMPTS['{ma}'] = {{\n"
            f"    'template': PART_TOOL + PART_KIENTHUC + {ma}_HUONGGIAI + {ma}_FEWSHOT + {ma}_NHIEMVU,\n"
            f"    'free_unknowns': {spec['free_unknowns']!r},\n"
            f"    'max_tool_calls': {spec['max_tool_calls']},\n"
            f"}}\n")


if __name__ == "__main__":
    build_group(sys.argv[1], sys.argv[2:])
