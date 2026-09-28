# Scripts

The scripts in this directory produce the data under [`../data/`](../data/).
They cover two stages: converting source PDF pages to Markdown/LaTeX and
generating numerical variants of the extracted questions.

## `pdf_to_markdown/`

Run the scripts in the order indicated by their numeric prefixes.

| Script | Purpose |
|---|---|
| `1_find_questions.py` | Search extracted PDF text for Complex Numbers questions and record their pages and question numbers |
| `2_render_pages.py` | Render selected PDF pages as PNG images with PyMuPDF |
| `3_build_katex_css.py` | Bundle KaTeX CSS and fonts for offline previews |
| `4_build_html_66cau.py`, `5_merge_batches.py` | Merge transcription batches and build an HTML comparison page |
| `6_build_review_html.py` | Build an HTML page for reviewing model answers to the source questions |
| `7_solve_with_models.py` | Ask ChatGPT, Gemini, and Qwen to solve the source questions with a shared prompt |
| `8_grade_answers.py` | Compare each selected option with the correct answer |
| `9_find_other_topics.py`, `10_select_other_topics.py`, `11_render_other_pages.py`, `15_select_13_more.py` | Select questions from six additional topics for conversion-quality evaluation |
| `12_prompt_transcribe.txt` | Prompt used to transcribe page images into Markdown/LaTeX |
| `13_transcribe_via_claude_api.py` | Send page images to the Claude API for transcription |
| `14_build_evaluation_table.py` | Combine transcribed questions into a conversion-quality evaluation table |
| `16_export_for_review.py`, `17_split_review_batches.py` | Export the data and split it for two independent reviewers |
| `18_merge_review_issues.py`, `19_apply_ghichu.py` | Merge reviewer findings and apply the recorded corrections |

The source review PDF is not included in this repository. Update the input
paths and provide the required API credentials before running scripts that
depend on the source document or an external API.

## `generate_questions/`

| Script | Purpose |
|---|---|
| `10_common_utils.py` | Shared LaTeX formatting, random-number generation, and answer-choice validation utilities |
| `11_generate_dang1_full.py` through `17_generate_dang7_full.py` | Generate variants for the corresponding source-question types using SymPy |
| `20_export_all.py` | Combine the source questions and generated variants, validate them, and export CSV/Excel files |
| `21_verify_all.py` | Recompute each generated answer with an independent verification path |

For each source question, the generator samples new integer, rational, or
irrational values, constructs the question and four answer choices, computes
the correct answer, and produces a corresponding solution. The verification
script then recomputes the answer independently.

### Example

```bash
cd scripts/generate_questions
python 11_generate_dang1_full.py
# Run the remaining generators through 17_generate_dang7_full.py.
python 20_export_all.py
```

`20_export_all.py` stops without exporting the final files if any generated
question fails the independent checks performed by `21_verify_all.py`.
