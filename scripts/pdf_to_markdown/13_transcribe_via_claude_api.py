"""
Script chuyển đổi (transcribe) đề bài/đáp án/lời giải từ ẢNH trang PDF sang
Markdown/LaTeX bằng Claude API (có khả năng đọc ảnh - vision).

Đây là bản SCRIPT HÓA, tái lập được của bước transcribe đã thực hiện (trước đó
được giao trực tiếp cho Claude qua cơ chế Agent/Task trong phiên làm việc).
Prompt dùng đúng như trong file 12_prompt_transcribe.txt.

Cách chạy:
    1. Điền ANTHROPIC_API_KEY vào file .env ở thư mục gốc F:\\Math.
    2. Chỉnh danh sách CAU_CAN_CHUYEN bên dưới (trang, câu, đường dẫn ảnh).
    3. Chạy: python 13_transcribe_via_claude_api.py
    4. Kết quả JSON lưu vào Danh_gia_chuyen_doi_markdown/data/transcribe_api_output.json
"""

import base64
import json
import os

from dotenv import load_dotenv

load_dotenv()

import anthropic

MODEL = "claude-sonnet-4-5"

PROMPT_TEMPLATE = """Đọc ảnh trang PDF đính kèm. Mỗi trang có nhiều câu hỏi ("Câu N:") kèm 4 phương án A/B/C/D, tiếp theo là "Lời giải" và kết thúc bằng "Chọn đáp án X" (chữ khoanh tròn trong ảnh).

Với câu hỏi số {cau} trên trang này, transcribe thành 1 object JSON gồm:

- "trang": {trang}
- "cau": {cau}
- "de_bai": TOÀN BỘ đề bài kèm 4 phương án A/B/C/D, viết dưới dạng Markdown, công thức toán đặt trong dấu $...$. Giữ mỗi phương án trên 1 dòng, không xuống dòng quá nhiều lần bên trong 1 biểu thức.
- "dap_an": đáp án đúng, dạng "X. <nội dung phương án X>" — lấy từ dòng "Chọn đáp án X" trong lời giải rồi khớp với nội dung phương án X tương ứng.
- "loi_giai": TOÀN BỘ lời giải gốc trong tài liệu, transcribe trung thực, KHÔNG diễn giải lại, KHÔNG tự sửa nội dung dù thấy có vẻ sai.

Yêu cầu bắt buộc:
1. Transcribe đúng y hệt những gì thấy trong ảnh — đây là nguồn xác thực duy nhất, không suy diễn hay "sửa hộ" công thức trông lạ.
2. Nếu lời giải bị cắt (không thấy dòng "Chọn đáp án"), ghi chú rõ ở cuối "loi_giai", không tự bịa đoạn kết luận.
3. Giữ nguyên cấu trúc phân số, căn thức, chỉ số dưới bằng LaTeX chuẩn.

CHỈ trả về đúng 1 object JSON, không thêm giải thích gì khác ngoài JSON."""


def transcribe_one(client, image_path: str, trang: int, cau: int) -> dict:
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    resp = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": PROMPT_TEMPLATE.format(trang=trang, cau=cau),
                    },
                ],
            }
        ],
    )
    text = resp.content[0].text.strip()
    # Loại bỏ code fence nếu Claude trả về dạng ```json ... ```
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


# Ví dụ danh sách câu cần chuyển (điền theo nhu cầu thực tế khi chạy lại)
CAU_CAN_CHUYEN = [
    # (trang, cau, duong_dan_anh)
    (2, 3, "Danh_gia_chuyen_doi_markdown/pages/page_002.png"),
]


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("CẢNH BÁO: chưa có ANTHROPIC_API_KEY trong .env — không thể chạy.")
        return

    client = anthropic.Anthropic(api_key=api_key)
    results = []
    for trang, cau, img_path in CAU_CAN_CHUYEN:
        print(f"Đang transcribe trang {trang} câu {cau}...")
        try:
            results.append(transcribe_one(client, img_path, trang, cau))
        except Exception as e:
            print(f"  Lỗi: {e}")

    out_path = "Danh_gia_chuyen_doi_markdown/data/transcribe_api_output.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Đã lưu", out_path)


if __name__ == "__main__":
    main()
