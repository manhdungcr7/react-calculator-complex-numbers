# `generate_questions/` (Exponential and Logarithm)

Generates numerical variants of the Exponential and Logarithm source questions.
Each generator computes the answer and then verifies it independently with a
different method. A repository-wide scan also checks that every generated
question has exactly four distinct answer choices labeled A-D.

**Current coverage: all 89 retained problem types, 90 variants each**
(8,010 generated variants; 107 retained source questions + 8,010 variants =
8,117 rows in the combined CSV/XLSX). D09 and D11 are excluded because they
have no numeric inputs to vary. D31 and D32 are excluded too: a Qwen3-4B zero-shot
audit found D31 variants with two answer options that are the same set (9 of 90)
and D32 variants whose options are numerically equal (2 of 90). Their generators
stay in `16_`/`17_` untouched (so the random seeds of the other types do not
shift), but `22_export_all.py` skips them and `23b_exclude_types.py` removed them
from every batch file and derived result. Type grouping requires the same given-data
form, requested task, and solution method. A manual audit split D36 into
proposition selection (D36a) and direct evaluation (D36b), and split D50 into
the logarithm quotient-rule case (D50a) and product-rule case (D50b).

**Note on a data-integrity bug found and fixed after the initial expansion
to 90/type**: several batches (`batch_round2.json`, `batch_round8.json`,
`D01_bien_the.json`) picked up a Windows console/tool encoding bug where
UTF-8 text got mis-decoded as Windows-1252 (mojibake), corrupting Vietnamese
diacritics in thousands of rows while the Vietnamese-looking garbled text
still passed the answer-choice and duplicate-question scans (those scans
check structure, not spelling). Caught by a manual spot-check of the actual
rendered question text, not by the automated checks. Fixed by restoring the
two files with clean git history (`23_generate_round2.py`, `11_generate_D01.py`)
from the commit before the bug was introduced and regenerating from those,
and by a byte-level Windows-1252 reversal for `batch_round8.json` (which had
no clean baseline to restore). Every row across all batches was re-scanned
afterward and confirmed to contain no mojibake or lost characters. The
lesson: structural checks (duplicate options, unique questions) do not catch
character-encoding corruption — spelling/rendering needs a direct look.

An initial pass treated many types as unsafe to vary. Later rounds recovered
types by deriving only the final answer independently, designing parameters
backwards from an equality point, using exact endpoint/continuity arguments,
or finding a general symbolic relation that does not depend on particular
numbers.

| Script | Coverage and independent check |
|---|---|
| `10_common_utils.py` | Shared LaTeX formatting and answer-choice utilities (`render_mc`, `bump_until_distinct`, etc.) |
| `11_generate_D01.py`-`14_generate_D53.py` | Pilot batch: D01, D12, D18, D53 |
| `15_generate_identities_A.py` | D06, D13, D30, D36a, D36b, D54, D59, D60, D66, D76, D81, D90 |
| `16_generate_identities_B.py` | D32, D37, D44, D50a, D50b, D64, D72, D77, D87 |
| `17_generate_basic_eq.py` | D02, D04, D07, D14, D19, D21, D27, D28, D31, D33, D34, D38, D42, D43, D48, D55, D58, D61, D62, D63, D71, D73, D80, D82, D85, D86, D91 |
| `18_generate_counting.py` | D25, D41, D74, D92; brute-force verified |
| `19_generate_identities_C.py` | D49, D20 |
| `22_export_all.py` | Combines source questions and every listed variant batch into CSV/XLSX |
| `23_generate_round2.py` | D05, D15, D16, D35, D40, D45, D51, D67, D69; Vieta/counting checks |
| `31_fix_and_expand.py` | Fixed the encoding bug in D01/round2, and expanded D01/round2/D51/D67 to (near-)90 variants using fast algebraic re-implementations of the slow sympy verifiers |
| `24_generate_round3.py` | D10, D46, D68, D94; parameters designed from equality/critical points |
| `25_generate_round4.py` | D29, D56, D83, D88; algebraic and direct-count verifiers |
| `26_generate_round5.py` | D22, D24, D39, D75, D93; symbolic and brute-force checks |
| `27_generate_round6.py` | D79, D89; endpoint signs and continuity (IVT), checked against direct evaluations |
| `28_generate_round7.py` | D17, D65; numeric minimization checks independent of the derived formulas |
| `29_generate_round8.py` | D08 (direct change-of-base evaluation), D23 (numerical root bracketing), D47 (continuous-variable search), D52 (high-precision log comparison), D57 (direct integer-pair enumeration), D78 (dense grid in the original feasible region) |
| `30_generate_round9.py` | D84; independent endpoint-sign enumeration at 80-digit precision |
| `32_generate_round10_shortfalls.py` | Completes D43 with exact rational thresholds and D51 with factored quadratic coefficients; checks D43 symbolically and D51 by direct enumeration |

### Example

```bash
python scripts/generate_questions/30_generate_round9.py
python scripts/generate_questions/22_export_all.py
```

D09, D11, D31 and D32 are excluded from the retained source set (see above). All 89 retained types have 90
variants. D43 uses exact integer and rational threshold values. D51 varies the
quadratic coefficients while preserving its exponential-quadratic inequality
form; the selected coefficients make the quadratic factor at integer powers
of 2, and direct enumeration checks every generated answer against the original
inequality. For each type, generation changes only numerical values in the
original question form; an independent verifier checks the resulting answer.
A final repository-wide audit checks for repeated question statements and
duplicate answer choices. D84's 90 variants vary endpoint parameter U over the
verified range, with the linked exponent coefficient 3U; an independent
80-digit endpoint-sign verifier checks the count.
