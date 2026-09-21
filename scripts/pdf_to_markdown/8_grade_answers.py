"""
Chấm điểm tự động: trích đáp án (A/B/C/D) mà mỗi mô hình kết luận trong lời
giải, so sánh với đáp án đúng (cột "Đáp án đúng"), rồi thêm các cột:

    - "ChatGPT chọn", "ChatGPT đúng/sai"
    - "Gemini chọn",  "Gemini đúng/sai"
    - "Qwen chọn",    "Qwen đúng/sai"

Chạy sau khi solve_with_models.py đã điền xong các cột lời giải:
    python grade_answers.py
"""

import re
import sys

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_XLSX = "So_phuc_60_mau.xlsx"
DATA_CSV = "So_phuc_60_mau.csv"

# Nhiều mẫu để bắt được đáp án model kết luận, phòng khi model không theo
# đúng 100% định dạng "Đáp án đúng: X" đã yêu cầu trong prompt.
PATTERNS = [
    r"[Đđ]áp\s*án\s*đúng\s*(?:là)?\s*[:\-]?\s*\**\s*\(?([A-D])\)?",
    r"[Cc]họn\s*đáp\s*án\s*\**\s*\(?([A-D])\)?",
    r"\\boxed\{\s*(?:\\text\{)?([A-D])",
    r"[Đđ]áp\s*án\s*(?:là)?\s*[:\-]?\s*\**\s*\(?([A-D])\)?",
]


def parse_choices(de_bai: str) -> dict:
    """Tách 4 lựa chọn A/B/C/D từ cột đề bài, trả về {'A': 'nội dung', ...}."""
    choices = {}
    for line in str(de_bai).split("\n"):
        line = line.strip()
        if len(line) > 2 and line[0] in "ABCD" and line[1] == ".":
            choices[line[0]] = line[2:].strip()
    return choices


def normalize(s: str) -> str:
    s = s.strip().rstrip(".").strip()
    s = s.replace("$", "").replace(" ", "")
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    return s


def extract_choice(text: str, choices: dict | None = None) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""
    for pat in PATTERNS:
        matches = re.findall(pat, text)
        if matches:
            return matches[-1].upper()

    # Fallback: model chỉ đóng khung giá trị cuối cùng (\boxed{...}) mà không
    # nêu rõ chữ cái — so khớp giá trị đó với nội dung 4 lựa chọn.
    if choices:
        boxed = re.findall(r"\\boxed\{([^}]*)\}", text)
        if boxed:
            val = normalize(boxed[-1])
            for letter, content in choices.items():
                if normalize(content) == val:
                    return letter
    return ""


def main():
    df = pd.read_excel(DATA_XLSX)

    correct_letter = df["Đáp án đúng"].astype(str).str.strip().str[0].str.upper()

    all_choices = df["Đề bài"].apply(parse_choices)

    for label, col in [
        ("ChatGPT", "Lời giải ChatGPT"),
        ("Gemini", "Lời giải Gemini"),
        ("Qwen", "Lời giải Qwen"),
    ]:
        is_error = df[col].astype(str).str.startswith("[LỖI:")
        chosen = [
            extract_choice(text, choices)
            for text, choices in zip(df[col], all_choices)
        ]
        df[f"{label} chọn"] = chosen
        status = []
        for c, g, err in zip(chosen, correct_letter, is_error):
            if err:
                status.append("Lỗi API")
            elif c == "":
                status.append("Không xác định")
            elif c == g:
                status.append("Đúng")
            else:
                status.append("Sai")
        df[f"{label} đúng/sai"] = status

    df.to_excel(DATA_XLSX, index=False)
    df.to_csv(DATA_CSV, index=False, encoding="utf-8-sig")

    print("Đã chấm điểm. Tóm tắt:")
    for label in ["ChatGPT", "Gemini", "Qwen"]:
        vc = df[f"{label} đúng/sai"].value_counts()
        print(f"  {label}: {vc.to_dict()}")


if __name__ == "__main__":
    main()
