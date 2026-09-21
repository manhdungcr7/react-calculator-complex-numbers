# Scripts

Script dùng để **sinh ra** bộ dữ liệu ở [`../data/`](../data/), gồm 2 bước
nối tiếp nhau: chuyển đề bài từ PDF sang Markdown/LaTeX, rồi sinh thêm câu
hỏi biến thể.

## `pdf_to_markdown/` - Chuyển đổi PDF → Markdown/LaTeX

Chạy theo thứ tự số đứng đầu tên file:

| Script | Việc làm |
|---|---|
| `1_find_questions.py` | Quét toàn bộ text PDF (đã trích qua PyMuPDF) tìm các câu có từ khóa "số phức", ghi lại số trang + số câu |
| `2_render_pages.py` | Render các trang đã chọn thành ảnh PNG (dùng PyMuPDF) |
| `3_build_katex_css.py` | Đóng gói CSS/font KaTeX (inline base64) để dựng trang xem trước offline |
| `4_build_html_66cau.py`, `5_merge_batches.py` | Gộp các batch câu đã transcribe thành 1 bảng, dựng trang HTML đối chiếu |
| `6_build_review_html.py` | Dựng trang HTML review kết quả các model giải 66 câu |
| `7_solve_with_models.py` | Gọi ChatGPT/Gemini/Qwen giải 66 câu bằng 1 prompt chuẩn hóa chung (kết quả → [`data/results/experiment1_65cau_khao_sat/`](../data/results/experiment1_65cau_khao_sat/)) |
| `8_grade_answers.py` | Tự động chấm đáp án (A/B/C/D) mỗi model chọn so với đáp án đúng |
| `9_find_other_topics.py`, `10_select_other_topics.py`, `11_render_other_pages.py`, `15_select_13_more.py` | Tìm & chọn thêm câu hỏi thuộc 6 chủ đề khác (ngoài số phức), đủ >100 mẫu cho bảng đánh giá chuyển đổi |
| `12_prompt_transcribe.txt` | Prompt dùng để transcribe ảnh trang PDF sang Markdown/LaTeX |
| `13_transcribe_via_claude_api.py` | Gọi Claude API (đọc ảnh trực tiếp - vision) để transcribe từng câu theo prompt trên |
| `14_build_evaluation_table.py` | Gộp toàn bộ câu đã transcribe thành bảng đánh giá chất lượng chuyển đổi |
| `16_export_for_review.py`, `17_split_review_batches.py` | Xuất dữ liệu + chia batch để 2 người review độc lập đối chiếu với ảnh gốc |
| `18_merge_review_issues.py`, `19_apply_ghichu.py` | Gộp các lỗi 2 người tìm được, ghi chú vào bảng đánh giá |

**Quy trình tóm tắt:**
1. Quét toàn bộ text PDF bằng PyMuPDF, tìm các câu có từ khóa chủ đề (số
   phức, sau đó mở rộng sang 6 chủ đề khác), chọn ra danh sách trang chứa
   câu hỏi + lời giải liên quan.
2. Render các trang đó thành ảnh PNG.
3. Đưa ảnh kèm prompt (`12_prompt_transcribe.txt`) cho Claude API để
   transcribe từ ảnh về định dạng Markdown/LaTeX và lưu lại.
4. Hai người review độc lập, đối chiếu bản transcribe với ảnh gốc, ghi lại
   lỗi chuyển đổi (nếu có) vào bảng đánh giá.

## `generate_questions/` - Sinh câu hỏi biến thể

| Script | Việc làm |
|---|---|
| `10_common_utils.py` | Hàm dùng chung: định dạng LaTeX (rút gọn căn thức, phân số), sinh số ngẫu nhiên theo 3 loại (nguyên / hữu tỉ / vô tỉ), kiểm tra 4 phương án trắc nghiệm không trùng nhau |
| `11_generate_dang1_full.py` .. `17_generate_dang7_full.py` | Với mỗi câu gốc thuộc dạng tương ứng (1-7), sinh N câu biến thể/loại số bằng cách giải lại thật sự (sympy) theo đúng phương pháp lời giải gốc |
| `20_export_all.py` | Gộp câu gốc + toàn bộ câu biến thể thành 1 file Excel/CSV, có cột "Nhận xét" - kết quả tương ứng [`data/questions/So_phuc_day_du.csv`](../data/questions/So_phuc_day_du.csv) |
| `21_verify_all.py` | Với mỗi câu biến thể, tính lại đáp án bằng một cách suy luận **độc lập** (không tái sử dụng logic đã sinh ra câu hỏi), so khớp với đáp án đã lưu |

**Quy trình tóm tắt:**
1. Với mỗi câu gốc, viết 1 hàm Python (dùng thư viện sympy) nhận số ngẫu
   nhiên làm đầu vào.
2. Hàm này giải lại theo đúng phương pháp của lời giải gốc (không phải chỉ
   thay số vào công thức có sẵn) - kể cả câu phải biện luận nhiều trường
   hợp, đếm nghiệm, hay giải hệ phương trình.
3. Từ đó sinh ra đề bài, 4 phương án, đáp án đúng và lời giải tương ứng với
   bộ số mới.
4. Sau khi sinh, kiểm tra lại bằng script sympy giải lại từ đầu để xác nhận
   đáp án đúng (`21_verify_all.py`), sau đó tự rà soát lại một lượt xem đã
   ổn chưa rồi điền vào cột "Nhận xét".

### Cách chạy lại

```bash
cd generate_questions
python 11_generate_dang1_full.py   # ... đến 17_generate_dang7_full.py
python 20_export_all.py            # gộp + kiểm tra + xuất Excel/CSV cuối cùng
```

`20_export_all.py` sẽ tự dừng và báo lỗi (không xuất file) nếu có bất kỳ câu
biến thể nào không vượt qua kiểm tra độc lập ở `21_verify_all.py`.
