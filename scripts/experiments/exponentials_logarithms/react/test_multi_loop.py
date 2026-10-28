# -*- coding: utf-8 -*-
"""
Dry run of a multi type notebook's batched ReAct loop with a scripted stand-in
for vLLM (no GPU, no real model). The stand-in "model" follows the commands of
each type's method exactly, so every question must be graded correct; any bug in
the loop, stop handling, Observation feeding, forced prefix or answer
extraction shows up here.

    python scripts/experiments/react/test_multi_loop.py G01 [N_QUESTIONS_PER_TYPE]
"""
import glob
import importlib
import json
import re
import sys
import time
from types import SimpleNamespace

import pandas as pd

sys.path.insert(0, "scripts/experiments/react")
import build_multi_notebook as builder  # noqa: E402
import framework as fw  # noqa: E402

GROUP = sys.argv[1]
N_Q = int(sys.argv[2]) if len(sys.argv) > 2 else 90

nb = json.load(open(f"experiments/ReAct-Calculator/KLTN_{GROUP}_ReAct_Calculator.ipynb", encoding="utf-8"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
# cells: 0 pip, 1 config, 2 prompts, 3 model, 4 backend + loop
config_cell, prompt_cell, backend_loop_cell = cells[1], cells[2], cells[4]
codes = re.search(r"RUN_TYPES = (\[.*?\])", config_cell).group(1)
codes = eval(codes)
data = json.load(open(builder.DATA_JSON, encoding="utf-8"))
ALL = {ma: data[ma][:N_Q] for ma in codes}
dangs = {ma: importlib.import_module(f"dang_{ma}") for ma in codes}
question_to_type = {r["de_bai_mcq"]: ma for ma in codes for r in ALL[ma]}


class FakeTok:
    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=True, enable_thinking=True):
        return "<|im_start|>user\n" + messages[0]["content"] + "<|im_end|>\n<|im_start|>assistant\n"

    def __call__(self, text):
        return SimpleNamespace(input_ids=list(range(len(text) // 3)))


class FakeSamplingParams:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class FakeLLM:
    """Answers one ReAct step per call, following the method of the question's type."""

    def generate(self, prompts, sampling_params, use_tqdm=False):
        outs = []
        for prompt in prompts:
            question = prompt.rsplit("Đề bài:\n", 1)[1].split("<|im_end|>")[0].rstrip("\n")
            question = next(q for q in question_to_type if q.strip() == question.strip())
            ma = question_to_type[question]
            program = fw.full_program(dangs[ma], question)
            tail = prompt.rsplit("<think>\nThought:", 1)[1]
            done_calls = tail.count("Observation:")
            if done_calls < len(program):
                text = f" step {done_calls + 1}.\nAction: Calculator\nAction Input: {program[done_calls]}\n"
                o = SimpleNamespace(text=text, token_ids=list(range(len(text) // 4)), stop_reason="Observation:", finish_reason="stop")
            else:
                letter = re.findall(r"test_([A-D]) = True", tail)[-1]
                text = f" all four tested.\n</think>\nFinal Answer: \\boxed{{{letter}}}\n"
                o = SimpleNamespace(text=text, token_ids=list(range(len(text) // 4)), stop_reason=None, finish_reason="stop")
            outs.append(SimpleNamespace(outputs=[o]))
        return outs


ns = {
    "re": re, "time": time, "pd": pd, "json": json, "glob": glob,
    "ALL_RECORDS": ALL, "RUN_TYPES": codes, "GROUP": GROUP, "RUN_STT": None,
    "tok": FakeTok(), "llm": FakeLLM(), "SamplingParams": FakeSamplingParams,
    "MAX_MODEL_LEN": 40000, "MAX_NEW_TOKENS": 9216,
    "TEMPERATURE": 0.3, "TOP_P": 0.95, "TOP_K": 20, "SEED": 42, "PRESENCE_PENALTY": 1.2,
}
exec(prompt_cell, ns)

# run the loop with output redirected to a temp folder
code = backend_loop_cell.replace("/kaggle/working/", "experiments/ReAct-Calculator/.tmp_dry_")
exec(code, ns)

import os  # noqa: E402

for ma in codes:
    path = f"experiments/ReAct-Calculator/.tmp_dry_{ma.lower()}_react_calculator_full90.csv"
    df = pd.read_csv(path, encoding="utf-8-sig")
    assert len(df) == len(ALL[ma]), (ma, len(df))
    assert df["DUNG"].all(), (ma, df[~df["DUNG"]][["STT", "dap_an_dung", "model_chon", "stop_reason"]])
    assert (df["syntax_errors"] == 0).all(), ma
    expected = [len(fw.full_program(dangs[ma], r["de_bai_mcq"])) for r in ALL[ma]]
    assert df["tool_calls"].tolist() == expected, (ma, df["tool_calls"].tolist()[:5], expected[:5])
    print(f"[ok] {ma}: {len(df)} questions graded correct through the notebook's own loop, "
          f"{df['tool_calls'].min()}-{df['tool_calls'].max()} tool calls each, 0 syntax errors")
    os.remove(path)
os.remove(f"experiments/ReAct-Calculator/.tmp_dry_summary_{GROUP}.csv")
