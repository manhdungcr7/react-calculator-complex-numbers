# Complex Numbers benchmark v2 (reworded questions)

Benchmark v2 rewrites the wording of the Complex Numbers benchmark v1 to test whether the
current methods still work when the same problems are phrased differently.

- Scope: the 24 problem types that Qwen3-4B does not fully solve with the baseline prompt, 90 variants each, 2160 questions.
- Output: `data/questions/benchmark_so_phuc_v2_24dang_2160cau.csv` (column `de_bai` is the v2 question, `de_bai_v1` is the original).
- Only the Vietnamese text around the formulas is rewritten. Every `$...$` formula, number, the four answer choices and the correct answer are identical to v1.

## How the questions are produced

Each problem type has hand-written sentence frames in `frames.py`, split into three levels:

| Level | Kind of change |
|---|---|
| 1 | synonyms and sentence type (Tính / Tìm / Xác định, thỏa mãn / thỏa, direct question) |
| 2 | word order (question first, swap conditions of equal role, merge or split sentences) |
| 3 | stronger restructuring (renaming, "Đề bài ... Yêu cầu ...", describing a relation in words) |

Each question fills the formulas of its v1 counterpart into a randomly chosen frame, with random synonym choices and optional short lead-in or closing sentences.

## Files

| File | Purpose |
|---|---|
| `frames.py` | hand-written frames and macros for each type |
| `build_v2.py` | generates the CSV and rejects any question that fails a check |
| `verify_v2.py` | independent check of the CSV against v1 |
| `quality_v2.py` | language lint (repeated words, capitalization, punctuation, duplicated labels) |
| `stress_v2.py` | expands every frame 40 times and runs all checks |
| `difficulty_v2.py` | measures text difference from v1 and tests a simple type classifier trained on v1 |
| `dump_frames.py`, `debug_frames.py`, `show.py`, `make_docs.py` | review helpers |

Run `py -3.12 build_v2.py` and then `py -3.12 verify_v2.py` to regenerate and check.

## Checks (all passing)

- Formulas: the multiset of complex `$...$` segments equals v1, no new formula or symbol appears. Only three formulas may be described in words (D04 conjugate, D14 sum, D45 equal moduli).
- Answer choices and answer columns are byte-identical to v1.
- No v2 question equals its v1 question, and each differs from v1 by at least 0.15 (token level, formula order included).
- Keyword rules per type, for example D45 keeps "nguyên" and "phân biệt", D46 has no "nguyên", D50 and D52 keep the min/max order.
- 15320 stress-test expansions produce no error.

## Known limitation

Formulas are unchanged, so a simple classifier trained on v1 still recognizes the type of 96.7% of v2 questions when it sees the formulas, and 68.9% when formulas are masked. v2 therefore mainly measures sensitivity to wording.
