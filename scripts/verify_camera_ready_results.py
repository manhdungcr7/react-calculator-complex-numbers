#!/usr/bin/env python3
"""Verify the per-question Experiment 5 and 6 data packaged with the paper."""
import collections
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def require(condition, message):
    if not condition:
        raise AssertionError(message)

q = read("data/questions/exponentials_logarithms/questions_original_and_variants.csv")
require(len(q) == 8117, "Expected 107 original questions and 8,010 variants")
origin = collections.Counter(row[list(q[0])[2]] for row in q)
require(sorted(origin.values()) == [107, 8010], f"Unexpected origins: {origin}")
require(len({row[list(q[0])[1]] for row in q}) == 89, "Expected 89 types")

baseline = read("data/results/experiment5_exponentials_logarithms/baseline_regraded_index.csv")
require(len(baseline) == 8010, "Expected 8,010 baseline results")
totals = collections.Counter(row["outcome"] for row in baseline)
require(totals == {"Correct": 7118, "Incorrect": 36, "Undetermined": 856}, f"Unexpected baseline outcomes: {totals}")
by_type = collections.Counter(row["ma_dang"] for row in baseline)
require(len(by_type) == 89 and all(n == 90 for n in by_type.values()), "Expected 90 results per type")

files = sorted((ROOT / "data/results/experiment5_exponentials_logarithms/react_final").glob("d*_react_calculator_full90.csv"))
require(len(files) == 32, "Expected 32 final ReAct files")
selected = {"D" + p.name[1:3] for p in files}
for path in files:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 90 and all(row["DUNG"] == "True" for row in rows), f"Unexpected ReAct results: {path.name}")
chosen = [row for row in baseline if row["ma_dang"] in selected]
require(len(chosen) == 2880 and sum(row["outcome"] == "Correct" for row in chosen) == 1988, "Unexpected selected baseline count")
require(all(any(row["ma_dang"] == code and row["outcome"] != "Correct" for row in baseline) for code in selected), "Selected types must have baseline errors")

web = read("data/results/experiment6_internet_questions/selected_77_questions_and_results.csv")
require(len(web) == 77 and len({row["id"] for row in web}) == 77, "Expected 77 distinct question IDs")
require(len({row["type_id"] for row in web}) == 41, "Expected 41 known types")
require(sorted(collections.Counter(row["topic"] for row in web).values()) == [22, 55], "Unexpected topics")
counts = collections.Counter((row["setting"], row["outcome"] == "Sai") for row in web)
require(counts == {("Baseline", False): 43, ("ReAct-Calculator", False): 30, ("ReAct-Calculator", True): 4}, f"Unexpected Internet results: {counts}")
print("Experiment 5: 107 originals, 8,010 variants; baseline 7,118/8,010; selected baseline 1,988/2,880; ReAct 2,880/2,880.")
print("Experiment 6: 77 questions across 41 types; baseline 43/43, ReAct 30/34, total 73/77.")
