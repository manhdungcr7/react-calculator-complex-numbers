# -*- coding: utf-8 -*-
"""Static checks of the ten multi type notebooks: every code cell compiles (lines starting with '!' are shell
commands and are skipped), the prompts of all types are present, and no notebook has leftover outputs."""
import glob
import json
import re

total_types = []
for path in sorted(glob.glob("experiments/ReAct-Calculator/KLTN_H*_ReAct_Calculator.ipynb")):
    nb = json.load(open(path, encoding="utf-8"))
    for i, c in enumerate([c for c in nb["cells"] if c["cell_type"] == "code"]):
        src = "\n".join(line for line in "".join(c["source"]).splitlines() if not line.startswith("!"))
        compile(src, f"{path}#cell{i}", "exec")
    print(path.split("/")[-1], "(corrected run) compiles")
for path in sorted(glob.glob("experiments/ReAct-Calculator/KLTN_G*_ReAct_Calculator.ipynb")):
    nb = json.load(open(path, encoding="utf-8"))
    codes = [c for c in nb["cells"] if c["cell_type"] == "code"]
    assert len(codes) == 5, (path, len(codes))
    for i, c in enumerate(codes):
        src = "".join(c["source"])
        src = "\n".join(line for line in src.splitlines() if not line.startswith("!"))
        compile(src, f"{path}#cell{i}", "exec")
        assert not c["outputs"]
    config = "".join(codes[1]["source"])
    types = eval(re.search(r"RUN_TYPES = (\[.*?\])", config).group(1))
    prompts = "".join(codes[2]["source"])
    for t in types:
        assert f"TYPE_PROMPTS['{t}']" in prompts, (path, t)
        assert f"{t}_HUONGGIAI" in prompts and f"{t}_FEWSHOT" in prompts and f"{t}_NHIEMVU" in prompts
    total_types += types
    print(path.split("/")[-1], types, "ok")
assert len(total_types) == len(set(total_types)) == 31, (len(total_types), sorted(total_types))
print("31 distinct types in 10 notebooks, all code cells compile")
