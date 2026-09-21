"""
Gọi 3 mô hình ngôn ngữ (ChatGPT qua API OpenAI, Gemini qua API Google,
Qwen3:4b chạy local qua Ollama) để giải 66 câu số phức, dùng CHUNG một
prompt chuẩn hóa (xem PROMPT_TEMPLATE bên dưới) để đảm bảo tính nhất
quán, minh bạch cho báo cáo KLTN.

Cách chạy:
    1. Điền OPENAI_API_KEY và GEMINI_API_KEY vào file .env (cùng thư mục).
    2. Đảm bảo Ollama đang chạy và đã có model qwen3:4b (`ollama list`).
    3. Chạy: python solve_with_models.py
       (mặc định chạy cả 3 model, tuần tự từng câu — sẽ bị Qwen kéo chậm)

       Hoặc chạy riêng từng nhóm model (khuyên dùng, vì Qwen local rất chậm
       so với ChatGPT/Gemini qua API):
         python solve_with_models.py --models chatgpt,gemini   (nhanh, vài phút)
         python solve_with_models.py --models qwen             (chậm, để chạy nền lâu)

    4. Kết quả được ghi vào So_phuc_60_mau.xlsx / .csv (các cột
       "Lời giải ChatGPT", "Lời giải Gemini", "Lời giải Qwen"), đồng thời
       lưu bản thô (raw) vào scratch/model_answers.json để đối chiếu.

Mỗi model resume độc lập: đã xong model nào cho câu nào thì không giải lại,
kể cả khi tắt máy/dừng giữa chừng (kết quả lưu ngay sau mỗi lần gọi).

Cột "Nhận xét ..." được để trống, do người (Chỉnh/Minh/bạn) tự đọc và
nhận xét sau khi xem lời giải mỗi mô hình.
"""

import argparse
import json
import os
import sys
import time

import pandas as pd
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

load_dotenv()

OPENAI_MODEL = "gpt-4o"
GEMINI_MODEL = "gemini-2.5-flash"
OLLAMA_MODEL = "qwen3:4b"
OLLAMA_URL = "http://localhost:11434/api/chat"

DATA_XLSX = "So_phuc_60_mau.xlsx"
DATA_CSV = "So_phuc_60_mau.csv"
RAW_OUT = "scratch/model_answers.json"

# ---------------------------------------------------------------------------
# PROMPT CHUẨN HÓA — dùng chung, giống hệt nhau cho cả 3 model.
# Không thay đổi nội dung đề bài, chỉ yêu cầu cách trình bày lời giải.
# ---------------------------------------------------------------------------
PROMPT_TEMPLATE = """Bạn hãy giải bài toán trắc nghiệm sau đây.

Yêu cầu trình bày:
- Giải chi tiết từng bước bằng tiếng Việt.
- Viết dưới dạng Markdown, dùng LaTeX cho công thức toán (đặt công thức trong dấu $...$).
- Không xuống dòng quá nhiều lần trong một biểu thức (ví dụ ngoặc vuông, phân số) vì sẽ khó đọc.
- Sau khi giải xong, kết luận rõ ràng ở dòng cuối cùng: "Đáp án đúng: X" (X là A, B, C hoặc D).

Đề bài:
{de_bai}
"""


def build_prompt(de_bai: str) -> str:
    return PROMPT_TEMPLATE.format(de_bai=de_bai.strip())


def call_openai(prompt: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()


def call_gemini(prompt: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(GEMINI_MODEL)
    resp = model.generate_content(prompt)
    return resp.text.strip()


def call_qwen(prompt: str) -> dict:
    import requests

    r = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.2},
        },
        timeout=1200,
    )
    r.raise_for_status()
    msg = r.json()["message"]
    return {
        "content": msg.get("content", "").strip(),
        "thinking": msg.get("thinking", "").strip(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--models",
        default="chatgpt,gemini,qwen",
        help="Danh sách model cần chạy, phân tách bởi dấu phẩy, ví dụ: chatgpt,gemini",
    )
    args = parser.parse_args()
    wanted = {m.strip().lower() for m in args.models.split(",") if m.strip()}

    df = pd.read_excel(DATA_XLSX)

    for col in [
        "Lời giải ChatGPT",
        "Nhận xét ChatGPT",
        "Lời giải Gemini",
        "Nhận xét Gemini",
        "Lời giải Qwen",
        "Nhận xét Qwen",
    ]:
        if col not in df.columns:
            df[col] = ""

    raw_results = []
    if os.path.exists(RAW_OUT):
        with open(RAW_OUT, encoding="utf-8") as f:
            raw_results = json.load(f)

    have_openai = "chatgpt" in wanted and bool(os.environ.get("OPENAI_API_KEY"))
    have_gemini = "gemini" in wanted and bool(os.environ.get("GEMINI_API_KEY"))
    have_qwen = "qwen" in wanted
    if "chatgpt" in wanted and not have_openai:
        print("CẢNH BÁO: chưa có OPENAI_API_KEY trong .env, sẽ bỏ qua ChatGPT.")
    if "gemini" in wanted and not have_gemini:
        print("CẢNH BÁO: chưa có GEMINI_API_KEY trong .env, sẽ bỏ qua Gemini.")

    by_stt = {r["STT"]: r for r in raw_results}

    # Các trường mà lượt chạy này có quyền ghi. Dùng để save() một cách an
    # toàn khi nhiều tiến trình (vd: qwen chạy nền + chatgpt/gemini chạy
    # riêng) cùng ghi vào chung RAW_OUT — mỗi lượt chỉ đè đúng phần của
    # mình, không được ghi đè phần của model khác đang được tiến trình kia
    # cập nhật đồng thời.
    owned_fields = {"prompt"}
    if "chatgpt" in wanted:
        owned_fields.add("chatgpt")
    if "gemini" in wanted:
        owned_fields.add("gemini")
    if "qwen" in wanted:
        owned_fields.update({"qwen", "qwen_thinking"})

    def is_ok(entry, key):
        return key in entry and not str(entry[key]).startswith("[LỖI:")

    def save():
        # Đọc lại trạng thái mới nhất trên đĩa (có thể đã bị tiến trình khác
        # cập nhật) rồi chỉ ghi đè các trường mình sở hữu, để không xóa mất
        # tiến độ của tiến trình khác.
        if os.path.exists(RAW_OUT):
            with open(RAW_OUT, encoding="utf-8") as f:
                disk_by_stt = {r["STT"]: r for r in json.load(f)}
        else:
            disk_by_stt = {}
        for stt, entry in by_stt.items():
            target = disk_by_stt.setdefault(stt, {"STT": stt})
            for key in owned_fields:
                if key in entry:
                    target[key] = entry[key]
        with open(RAW_OUT, "w", encoding="utf-8") as f:
            json.dump(
                [disk_by_stt[s] for s in sorted(disk_by_stt)],
                f,
                ensure_ascii=False,
                indent=2,
            )

    for i, row in df.iterrows():
        stt = int(row["STT"])
        entry = by_stt.setdefault(stt, {"STT": stt})
        prompt = build_prompt(row["Đề bài"])
        entry["prompt"] = prompt

        if have_openai and not is_ok(entry, "chatgpt"):
            print(f"[{stt}/{len(df)}] ChatGPT...")
            try:
                entry["chatgpt"] = call_openai(prompt)
            except Exception as e:
                entry["chatgpt"] = f"[LỖI: {e}]"
            save()
            time.sleep(1)

        if have_gemini and not is_ok(entry, "gemini"):
            print(f"[{stt}/{len(df)}] Gemini...")
            try:
                entry["gemini"] = call_gemini(prompt)
            except Exception as e:
                entry["gemini"] = f"[LỖI: {e}]"
            save()
            time.sleep(1)

        if have_qwen and not is_ok(entry, "qwen"):
            print(f"[{stt}/{len(df)}] Qwen (local, chậm)...")
            try:
                qwen_out = call_qwen(prompt)
                entry["qwen"] = qwen_out["content"]
                entry["qwen_thinking"] = qwen_out["thinking"]
            except Exception as e:
                entry["qwen"] = f"[LỖI: {e}]"
            save()

    # Đọc lại JSON mới nhất trên đĩa (thay vì dùng by_stt trong bộ nhớ) để
    # không vô tình ghi đè lên tiến độ của tiến trình khác (vd: qwen chạy
    # nền) khi xuất ra xlsx/csv cuối cùng.
    with open(RAW_OUT, encoding="utf-8") as f:
        final_by_stt = {r["STT"]: r for r in json.load(f)}

    for i, row in df.iterrows():
        r = final_by_stt.get(int(row["STT"]))
        if not r:
            continue
        if "chatgpt" in r:
            df.at[i, "Lời giải ChatGPT"] = r["chatgpt"]
        if "gemini" in r:
            df.at[i, "Lời giải Gemini"] = r["gemini"]
        if "qwen" in r:
            df.at[i, "Lời giải Qwen"] = r["qwen"]

    df.to_excel(DATA_XLSX, index=False)
    df.to_csv(DATA_CSV, index=False, encoding="utf-8-sig")
    print("Hoàn tất. Đã ghi vào", DATA_XLSX, "và", DATA_CSV)


if __name__ == "__main__":
    main()
