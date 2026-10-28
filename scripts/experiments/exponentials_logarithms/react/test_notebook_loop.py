# -*- coding: utf-8 -*-
"""
Dry run of the notebook's batched ReAct loop, tool backend and grading with a
scripted stand-in for vLLM (no GPU, no real model). The stand-in "model"
follows the method of PART_NHIEMVU exactly, so every question must end up
graded correct; any bug in the loop, the stop handling, the Observation
feeding, the forced prefix or the answer extraction shows up here.

    python scripts/experiments/react/test_notebook_loop.py D79
"""
import glob
import json
import re
import sys
import time
from types import SimpleNamespace

import pandas as pd

sys.path.insert(0, "scripts/experiments/react")
import build_react_notebook as builder  # noqa: E402

MA_DANG = sys.argv[1] if len(sys.argv) > 1 else "D79"
N_QUESTIONS = int(sys.argv[2]) if len(sys.argv) > 2 else 6

nb = json.load(open(f"experiments/ReAct-Calculator/KLTN_{MA_DANG}_ReAct_Calculator_full90.ipynb", encoding="utf-8"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
prompt_cell, backend_loop_cell = cells[2], cells[4]   # cells[0] is pip, [1] config, [2] prompts, [3] model, [4] backend+loop
assert "PROMPT_TEMPLATE" in prompt_cell and "STOP_STR" in backend_loop_cell

records_all = json.load(open(builder.DATA_JSON, encoding="utf-8"))[MA_DANG][:N_QUESTIONS]


class FakeTok:
    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=True, enable_thinking=True):
        return "<|im_start|>user\n" + messages[0]["content"] + "<|im_end|>\n<|im_start|>assistant\n"

    def __call__(self, text):
        return SimpleNamespace(input_ids=list(range(len(text) // 3)))


class FakeSamplingParams:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def scripted_program(question):
    m = re.search(r"không quá (\d+) số nguyên \$y\$ thỏa mãn \$\\log_\{?(\d+)\}?\(x\^2\+y\)\\ge \\log_\{?(\d+)\}?\(x\+y\)\$", question)
    bound, a, b = map(int, m.groups())
    options = dict(re.findall(r"(?m)^([A-D])\.\s*\$?(-?\d+)\$?\.?\s*$", question))
    cmds = [
        f"n_plus_1 = {bound} + 1", f"exponent = log({a})/log({b})",
        "threshold = N(n_plus_1**exponent - n_plus_1, 20)", "x_roots = solve(x**2 - x - threshold, x)",
        "x_low = Min(x_roots[0], x_roots[1])", "x_high = Max(x_roots[0], x_roots[1])",
        "first_x = floor(x_low) + 1", "last_x = ceiling(x_high) - 1", "count = last_x - first_x + 1",
    ] + [f"test_{k} = Eq(count, {options[k]})" for k in "ABCD"]
    return cmds


class FakeLLM:
    """Stands in for vLLM: answers one ReAct step per call, following the method."""

    def generate(self, prompts, sampling_params, use_tqdm=False):
        if not isinstance(sampling_params, list):
            sampling_params = [sampling_params] * len(prompts)
        outs = []
        for prompt, sp_ in zip(prompts, sampling_params):
            question = prompt.rsplit("Đề bài:", 1)[1]
            program = scripted_program(question)
            tail = prompt.rsplit("<think>\nThought:", 1)[1]        # only what THIS question has generated
            done_calls = tail.count("Observation:")
            if done_calls < len(program):
                text = f" step {done_calls + 1}.\nAction: Calculator\nAction Input: {program[done_calls]}\n"
                o = SimpleNamespace(text=text, token_ids=list(range(len(text) // 4)), stop_reason="Observation:", finish_reason="stop")
            else:
                # read the stored test results from the Observations already appended to the text
                letter = re.findall(r"test_([A-D]) = True", tail)[-1]
                text = f" all four tested.\n</think>\nFinal Answer: \\boxed{{{letter}}}\n"
                o = SimpleNamespace(text=text, token_ids=list(range(len(text) // 4)), stop_reason=None, finish_reason="stop")
            outs.append(SimpleNamespace(outputs=[o]))
        return outs


ns = {
    "re": re, "time": time, "pd": pd, "json": json, "glob": glob,
    "records": records_all, "tok": FakeTok(), "llm": FakeLLM(),
    "SamplingParams": FakeSamplingParams,
    "MAX_MODEL_LEN": 20480, "MAX_NEW_TOKENS": 9216,
    "TEMPERATURE": 0.3, "TOP_P": 0.95, "TOP_K": 20, "SEED": 42, "PRESENCE_PENALTY": 1.2,
    "FREE_UNKNOWNS": {"x"}, "MA_DANG": MA_DANG,
    "OUT_PATH": f"experiments/ReAct-Calculator/.tmp_dryrun_{MA_DANG}.csv",
}
exec(prompt_cell, ns)
exec(backend_loop_cell, ns)

df = ns["df"]
print()
assert len(df) == len(records_all)
assert df["DUNG"].all(), df[~df["DUNG"]][["STT", "dap_an_dung", "model_chon", "stop_reason"]]
assert (df["syntax_errors"] == 0).all()
assert (df["tool_calls"] == 13).all(), df["tool_calls"].tolist()
print(f"[ok] dry run: {len(df)} questions graded correct through the notebook's own loop, "
      f"{int(df['tool_calls'].iloc[0])} tool calls each, 0 syntax errors")


# ---------------------------------------------------------------------------
# the single question notebook (Cell 4 reruns with the default question)
# ---------------------------------------------------------------------------
import io
import contextlib

nb1 = json.load(open(f"experiments/ReAct-Calculator/KLTN_{MA_DANG}_ReAct_Calculator_1cau.ipynb", encoding="utf-8"))
code1 = ["".join(c["source"]) for c in nb1["cells"] if c["cell_type"] == "code"]
assert len(code1) == 3, len(code1)           # pip, model load, Cell 4
cell4 = code1[2]
assert "DE_BAI = r'''" in cell4 and "DAP_AN_DUNG" in cell4

ns1 = {"re": re, "time": time, "tok": FakeTok(), "llm": FakeLLM(), "SamplingParams": FakeSamplingParams,
       "MAX_MODEL_LEN": 18432, "MAX_NEW_TOKENS": 9216, "TEMPERATURE": 0.3, "TOP_P": 0.95, "TOP_K": 20,
       "SEED": 42, "PRESENCE_PENALTY": 1.2}
# the single question notebook writes /kaggle/working/full_response.txt: redirect it for the local dry run
cell4 = cell4.replace("/kaggle/working/full_response.txt", "experiments/ReAct-Calculator/.tmp_full_response.txt")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(cell4, ns1)
report = buf.getvalue()
assert ns1["dung"] is True, report[-1500:]
assert ns1["n_calls"] == 13 and ns1["n_loi"] == 0, (ns1["n_calls"], ns1["n_loi"])
assert "Dap an dung: D" in report and "DUNG" in report
print(f"[ok] 1cau notebook: default question graded correct, {ns1['n_calls']} tool calls, 0 syntax errors")
print("     printed sections:", [t for t in ("NHAT KY GOI TOOL", "DA GHI FILE", "TOAN BO LOI GIAI") if t in report])
