# -*- coding: utf-8 -*-
"""
Builds ONE Kaggle notebook that runs Qwen3-4B zero-shot over the
Mu-Logarit evaluation set (91 problem types, 90 variants each, 8,190
questions total). The same notebook file is uploaded to all 10 Kaggle
accounts; each account only changes GROUP_ID (1-10) near the top before
"Run All" so the 10 accounts split the work between them.

Prompt, decoding settings, and grading regex are copied unchanged from
the Complex Numbers (so_phuc) Qwen3 zero-shot full-90 experiments (see
so_phuc/experiments/*/KLTN_*_zeroshot_full90_*.ipynb) - only the model
name, dataset path, and the per-group loop differ.

Run scripts/experiments/10_prepare_zeroshot_data.py first to produce
plan_solve_prompts_mulogarit_merged.json and mulogarit_group_split.json.
"""
import json

SPLIT_INFO = "scripts/experiments/mulogarit_group_split.json"
OUT_PATH = "experiments/Qwen3-4B/KLTN_mulogarit_zeroshot_full90_Qwen3-4B.ipynb"
MODEL = "Qwen/Qwen3-4B"

MAX_MODEL_LEN = 11264
MAX_NEW_TOKENS = 9216
TEMPERATURE, TOP_P, TOP_K, SEED = 0.6, 0.95, 20, 42
PRESENCE_PENALTY = 1.2

PROMPT_TEMPLATE = r'''Bạn hãy giải bài toán trắc nghiệm sau đây.

Yêu cầu trình bày:
- Giải chi tiết từng bước bằng tiếng Việt.
- Viết dưới dạng Markdown, dùng LaTeX cho công thức toán (đặt công thức trong dấu $...$).
- Không xuống dòng quá nhiều lần trong một biểu thức (ví dụ ngoặc vuông, phân số) vì sẽ khó đọc.
- Sau khi giải xong, kết luận rõ ràng ở dòng cuối cùng: "Đáp án đúng: X" (X là A, B, C hoặc D).

Đề bài:
{de_bai}
'''


def md_cell(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}


def code_cell(src):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": src.splitlines(keepends=True)}


def build_notebook(split_info):
    groups_literal = json.dumps(
        {int(k.replace("group", "")): v for k, v in split_info.items()},
        ensure_ascii=False, indent=4,
    )

    cells = [md_cell(
        "# Mu-Logarit (91 dạng, 8.190 biến thể) - FULL90 - ZERO-SHOT - Qwen3-4B\n\n"
        "**Dùng chung 1 notebook cho cả 10 tài khoản Kaggle.** Trước khi "
        "\"Run All\", chỉ cần đổi `GROUP_ID` (1-10) ở ô cấu hình bên dưới cho "
        "đúng tài khoản đang chạy - không cần sửa gì khác.\n\n"
        "Prompt, tham số sinh "
        "(`temperature=0.6, top_p=0.95, top_k=20, seed=42, presence_penalty=1.2, "
        "max_new_tokens=9216, enable_thinking=True`) và cách chấm điểm giữ "
        "nguyên y hệt bản Qwen3-4B zero-shot đã dùng cho bộ Số phục.\n\n"
        "**CẦN UPLOAD** `plan_solve_prompts_mulogarit_merged.json` lên Kaggle làm "
        "1 Dataset rồi \"Add Data\" vào notebook (tên dataset tuỳ ý) - notebook tự "
        "dò đường dẫn thật dưới `/kaggle/input/` bằng `glob`, không cần gõ cứng "
        "đường dẫn.\n"
    )]

    cells.append(code_cell(
        "!pip install -q -U vllm\n"
        "!pip uninstall -y -q torchcodec torchaudio\n"
        "import vllm; print('vLLM:', vllm.__version__)\n"
    ))

    cells.append(md_cell(
        "## Cấu hình - ĐỔI `GROUP_ID` CHO ĐÚNG TÀI KHOẢN (1-10), KHÔNG SỬA GÌ KHÁC Ở Ô NÀY"
    ))
    cells.append(code_cell(
        "import os, json, re, time, glob\n"
        "import pandas as pd\n"
        "import torch\n"
        "from transformers import AutoTokenizer\n"
        "from vllm import LLM, SamplingParams\n"
        "\n"
        "GROUP_ID = 1  # <-- SUA SO NAY (1-10) THEO TUNG TAI KHOAN, roi Run All\n"
        "\n"
        "DATA_FILENAME = 'plan_solve_prompts_mulogarit_merged.json'\n"
        "# Duong dan /kaggle/input/<ten-dataset>/... khac nhau tuy ten dataset ban\n"
        "# dat khi upload; thay vi go cung duong dan, tu do tim file nay o bat ky\n"
        "# dataset nao da duoc gan (Add Data) vao notebook.\n"
        "_matches = glob.glob(f'/kaggle/input/**/{DATA_FILENAME}', recursive=True)\n"
        "assert _matches, (f'Khong tim thay {DATA_FILENAME} duoi /kaggle/input/ - '\n"
        "                  'kiem tra da \"Add Data\" dataset chua chuoi file nay chua.')\n"
        "MERGED_DATA_PATH = _matches[0]\n"
        "print('Dung file du lieu:', MERGED_DATA_PATH)\n"
        "\n"
        "# Danh sach ma dang theo tung group (1-10), nhung 10 tai khoan deu dung\n"
        "# chung notebook nay - chi GROUP_ID doi.\n"
        f"GROUPS = {groups_literal}\n"
        "\n"
        "TYPES = GROUPS[str(GROUP_ID)]\n"
        f"MODEL = '{MODEL}'\n"
        f"MAX_MODEL_LEN, MAX_NEW_TOKENS = {MAX_MODEL_LEN}, {MAX_NEW_TOKENS}\n"
        f"TEMPERATURE, TOP_P, TOP_K, SEED = {TEMPERATURE}, {TOP_P}, {TOP_K}, {SEED}\n"
        f"PRESENCE_PENALTY = {PRESENCE_PENALTY}\n"
        "os.environ['TOKENIZERS_PARALLELISM'] = 'false'\n"
        "\n"
        "with open(MERGED_DATA_PATH, encoding='utf-8') as f:\n"
        "    ALL_RECORDS = json.load(f)\n"
        "\n"
        "print(f'GROUP_ID={GROUP_ID}: {len(TYPES)} dang, {sum(len(ALL_RECORDS[t]) for t in TYPES)} cau')\n"
        "print('Danh sach dang:', TYPES)\n"
    ))

    cells.append(md_cell("## Nạp model (1 lần cho cả nhóm dạng)"))
    cells.append(code_cell(
        "tok = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)\n"
        "N_GPU = torch.cuda.device_count()\n"
        "TENSOR_PARALLEL = 2 if N_GPU >= 2 else 1\n"
        "llm = LLM(model=MODEL, tensor_parallel_size=TENSOR_PARALLEL, dtype='float16',\n"
        "          max_model_len=MAX_MODEL_LEN, gpu_memory_utilization=0.90,\n"
        "          trust_remote_code=True, enforce_eager=True, seed=SEED)\n"
        "print('San sang.')\n"
        "sampling = SamplingParams(temperature=TEMPERATURE, top_p=TOP_P, top_k=TOP_K,\n"
        "                          presence_penalty=PRESENCE_PENALTY,\n"
        "                          max_tokens=MAX_NEW_TOKENS, seed=SEED)\n"
    ))

    cells.append(md_cell("## Sinh lời giải + chấm điểm cho từng dạng trong nhóm"))
    cells.append(code_cell(f"PROMPT_TEMPLATE = r'''{PROMPT_TEMPLATE}'''\n"))
    cells.append(code_cell(
        "def get_letter(t):\n"
        "    m = re.findall(r'[Đđ]áp\\s*án[^A-D]{0,15}([A-D])\\b', t)\n"
        "    if m:\n"
        "        return m[-1]\n"
        "    m = re.findall(r'\\\\boxed\\{([A-D])\\}', t)\n"
        "    return m[-1] if m else ''\n"
        "\n"
        "summary = []\n"
        "for ma_dang in TYPES:\n"
        "    records = ALL_RECORDS[ma_dang]\n"
        "    out_path = f'/kaggle/working/{ma_dang.lower()}_zeroshot_full90_Qwen3-4B.csv'\n"
        "\n"
        "    prompts = []\n"
        "    for r in records:\n"
        "        txt = PROMPT_TEMPLATE.replace('{de_bai}', r['de_bai_mcq'])\n"
        "        prompts.append(tok.apply_chat_template(\n"
        "            [{'role': 'user', 'content': txt}],\n"
        "            tokenize=False, add_generation_prompt=True, enable_thinking=True))\n"
        "\n"
        "    t0 = time.time()\n"
        "    outputs = llm.generate(prompts, sampling)\n"
        "    print(f'{ma_dang}: sinh xong {len(outputs)} cau, mat {(time.time()-t0)/60:.1f} phut.')\n"
        "\n"
        "    rows = []\n"
        "    for r, out in zip(records, outputs):\n"
        "        txt = out.outputs[0].text\n"
        "        ntok = len(out.outputs[0].token_ids)\n"
        "        think = txt.split('</think>')[0] if '</think>' in txt else txt\n"
        "        after = txt.split('</think>')[-1] if '</think>' in txt else ''\n"
        "        het_ngan_sach = ntok >= MAX_NEW_TOKENS - 1\n"
        "        chon = get_letter(after)\n"
        "        rows.append({\n"
        "            'STT': r['STT'], 'ma_dang': r['ma_dang'],\n"
        "            'dap_an_dung': r['dap_an_letter'], 'model_chon': chon,\n"
        "            'DUNG': chon == r['dap_an_letter'],\n"
        "            'token': ntok, 'het_ngan_sach': het_ngan_sach,\n"
        "            'think': think, 'after': after,\n"
        "        })\n"
        "\n"
        "    df = pd.DataFrame(rows)\n"
        "    df.to_csv(out_path, index=False, encoding='utf-8-sig')\n"
        "    summary.append({'ma_dang': ma_dang, 'dung': int(df['DUNG'].sum()), 'tong': len(df)})\n"
        "    print(f\"  -> {ma_dang}: {df['DUNG'].sum()}/{len(df)} dung ({df['DUNG'].mean()*100:.1f}%)\")\n"
    ))

    cells.append(md_cell("## Tổng kết nhóm dạng vừa chạy"))
    cells.append(code_cell(
        "df_summary = pd.DataFrame(summary)\n"
        "print('='*70)\n"
        "print(f'KET QUA NHOM GROUP_ID={GROUP_ID} ({len(TYPES)} dang):')\n"
        "print(df_summary)\n"
        "print('-'*70)\n"
        "print(f\"TONG: {df_summary['dung'].sum()}/{df_summary['tong'].sum()} dung \"\n"
        "      f\"({df_summary['dung'].sum()/df_summary['tong'].sum()*100:.1f}%)\")\n"
        "print('='*70)\n"
    ))

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main():
    split_info = json.load(open(SPLIT_INFO, encoding="utf-8"))
    nb = build_notebook(split_info)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
