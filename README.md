# Script xử lý dữ liệu Số phức & thử nghiệm LLM Tool Calling

Repo này chứa **script/notebook** dùng để (1) chuyển đổi đề bài/lời giải Số
phức từ PDF sang Markdown/LaTeX, (2) sinh thêm câu hỏi nhân bản (thay số,
giữ nguyên phương pháp giải) để mở rộng bộ dữ liệu đánh giá, và (3) thử
nghiệm phương pháp **ReAct + Calculator tool-calling** so với baseline
zero-shot trên nhiều LLM (Qwen3-4B, DeepSeek-R1-Distill-Qwen-1.5B,
Llama-3.2-3B-Instruct) trên toàn bộ 24 dạng bài số phức.

Repo chủ yếu chứa **code**, không chứa dữ liệu/kết quả đầy đủ: tài liệu PDF
gốc có bản quyền, và các file Excel/CSV/JSON kết quả chạy thử nghiệm là sản
phẩm chạy ra từ các script này — được lưu, quản lý riêng, không đưa lên đây.
Ngoại lệ duy nhất là [`problem_types_54.csv`](problem_types_54.csv): danh
sách 54 dạng bài Số phức (mã dạng + tên dạng, tiếng Anh và tiếng Việt) dùng
trong bài báo — nội dung này do nhóm tự viết mô tả, không sao chép nguyên
văn từ tài liệu gốc, nên không vướng bản quyền.

## 1. Chuyển đổi PDF → Markdown/LaTeX

Thư mục `Danh_gia_chuyen_doi_markdown/scripts/`, chạy theo thứ tự số đứng đầu
tên file:

| Script | Việc làm |
|---|---|
| `1_find_questions.py` | Quét toàn bộ text PDF (đã trích qua PyMuPDF) tìm các câu có từ khóa "số phức", ghi lại số trang + số câu |
| `2_render_pages.py` | Render các trang đã chọn thành ảnh PNG (dùng PyMuPDF) |
| `3_build_katex_css.py` | Đóng gói CSS/font KaTeX (inline base64) để dựng trang xem trước offline |
| `4_build_html_66cau.py`, `5_merge_batches.py` | Gộp các batch câu đã transcribe thành 1 bảng, dựng trang HTML đối chiếu |
| `6_build_review_html.py` | Dựng trang HTML review kết quả các model giải 66 câu |
| `7_solve_with_models.py` | Gọi ChatGPT/Gemini/Qwen giải 66 câu bằng 1 prompt chuẩn hóa chung |
| `8_grade_answers.py` | Tự động chấm đáp án (A/B/C/D) mỗi model chọn so với đáp án đúng |
| `9_find_other_topics.py`, `10_select_other_topics.py`, `11_render_other_pages.py`, `15_select_13_more.py` | Tìm & chọn thêm câu hỏi thuộc 6 chủ đề khác (ngoài số phức), đủ >100 mẫu cho bảng đánh giá chuyển đổi |
| `12_prompt_transcribe.txt` | Prompt dùng để transcribe ảnh trang PDF sang Markdown/LaTeX |
| `13_transcribe_via_claude_api.py` | Gọi Claude API (đọc ảnh trực tiếp — vision) để transcribe từng câu theo prompt trên |
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

## 2. Sinh câu hỏi nhân bản

Thư mục `Sinh_them_cau_hoi/scripts/`:

| Script | Việc làm |
|---|---|
| `10_common_utils.py` | Hàm dùng chung: định dạng LaTeX (rút gọn căn thức, phân số), sinh số ngẫu nhiên theo 3 loại (nguyên / hữu tỉ / vô tỉ), kiểm tra 4 phương án trắc nghiệm không trùng nhau |
| `11_generate_dang1_full.py` .. `17_generate_dang7_full.py` | Với mỗi câu gốc thuộc dạng tương ứng (1-7), sinh N câu nhân bản/loại số bằng cách giải lại thật sự (sympy) theo đúng phương pháp lời giải gốc |
| `20_export_all.py` | Gộp câu gốc + toàn bộ câu nhân bản thành 1 file Excel/CSV, có cột "Nhận xét" |
| `21_verify_all.py` | Với mỗi câu nhân bản, tính lại đáp án bằng một cách suy luận **độc lập** (không tái sử dụng logic đã sinh ra câu hỏi), so khớp với đáp án đã lưu |

**Quy trình tóm tắt:**
1. Với mỗi câu gốc, viết 1 hàm Python (dùng thư viện sympy) nhận số ngẫu
   nhiên làm đầu vào.
2. Hàm này giải lại theo đúng phương pháp của lời giải gốc (không phải chỉ
   thay số vào công thức có sẵn) — kể cả câu phải biện luận nhiều trường
   hợp, đếm nghiệm, hay giải hệ phương trình.
3. Từ đó sinh ra đề bài, 4 phương án, đáp án đúng và lời giải tương ứng với
   bộ số mới.
4. Sau khi sinh, kiểm tra lại bằng script sympy giải lại từ đầu để xác nhận
   đáp án đúng (`21_verify_all.py`), sau đó tự rà soát lại một lượt xem đã
   ổn chưa rồi điền vào cột "Nhận xét".

### Cách chạy lại

```bash
cd Sinh_them_cau_hoi/scripts
python 11_generate_dang1_full.py   # ... đến 17_generate_dang7_full.py
python 20_export_all.py            # gộp + kiểm tra + xuất Excel/CSV cuối cùng
```

`20_export_all.py` sẽ tự dừng và báo lỗi (không xuất file) nếu có bất kỳ câu
nhân bản nào không vượt qua kiểm tra độc lập ở `21_verify_all.py`.

## 3. Thử nghiệm ReAct + Calculator tool-calling trên nhiều LLM

Thư mục `Sinh_them_cau_hoi/`: các notebook Kaggle (`.ipynb`) dùng để thử
nghiệm phương pháp **ReAct + Calculator** — model tự sinh `Thought` →
`Action: Calculator` → `Action Input: <biểu thức>`, một harness bên
ngoài thực thi biểu thức bằng backend sympy (chính xác tuyệt đối) rồi
chèn `Observation: <kết quả thật>` ngược lại để model tiếp tục, thay vì
để model tự tính bằng token — trên 24 dạng bài số phức, đối chiếu với
baseline **zero-shot** (không hướng dẫn, không tool), trên 3 model:
**Qwen3-4B**, **DeepSeek-R1-Distill-Qwen-1.5B**, **Llama-3.2-3B-
Instruct**. Repo chỉ up các notebook **thực sự dùng để chạy thử
nghiệm** (không up log/kết quả CSV, không up các notebook nháp/debug
1-câu dùng trong lúc phát triển prompt).

### Qwen3-4B (model gốc, 18 notebook — dùng làm chuẩn tham chiếu)

| File | Dạng bao gồm |
|---|---|
| `KLTN_D<NN>_ReAct_Calculator_full90.ipynb` (16 file: D04, D35–D39, D44–D48, D50–D53, D55) | Mỗi file 1 dạng, 90 câu |
| `KLTN_Nhom1_D04_D14_D28_D32_D33_full90.ipynb` | D04, D14, D28, D32, D33 (1 backend + 1 lần nạp model dùng chung cho cả 5 dạng) |
| `KLTN_Nhom2_D34_D40_D42_D45_D46_D49_full90.ipynb` | D34, D40, D42, D45, D46, D49 (dùng chung backend/model như Nhóm 1) |

Gộp lại, 2 file Nhóm phủ đủ 8 dạng còn thiếu (D14, D28, D32, D33, D34,
D40, D42, D49) mà 16 file lẻ ở trên không có — tổng cộng đủ **24/24
dạng**.

### DeepSeek-R1-Distill-Qwen-1.5B và Llama-3.2-3B-Instruct (test chéo model)

Mỗi model có 6 notebook, gộp theo lô 3 nhóm dạng (để chỉ cần nạp model
1 lần cho nhiều dạng, tránh nạp lại nhiều lần gây lỗi hết bộ nhớ GPU) ×
2 chế độ (ReAct có Calculator / zero-shot không tool):

| Lô dạng | ReAct + Calculator | Zero-shot |
|---|---|---|
| D04, D38, D46, D51, D53 | `KLTN_5dang_ReAct_Calculator_full90_<model>.ipynb` | `KLTN_5dang_zeroshot_full90_<model>.ipynb` |
| D35, D36, D37, D39, D44, D45, D47, D48, D50, D52, D55 | `KLTN_11dang_ReAct_Calculator_full90_<model>.ipynb` | `KLTN_11dang_zeroshot_full90_<model>.ipynb` |
| D14, D28, D32, D33, D34, D40, D42, D49 | `KLTN_8dangMoi_ReAct_Calculator_full90_<model>.ipynb` | `KLTN_8dangMoi_zeroshot_full90_<model>.ipynb` |

(`<model>` = `DeepSeek-R1-Distill-Qwen-1.5B` hoặc `Llama-3.2-3B-Instruct`)

Prompt/phương pháp trong các file này **copy y hệt** bản Qwen3-4B đã
kiểm chứng — chỉ đổi tên model và tham số sinh (`temperature`/`top_p`
theo đúng khuyến nghị chính thức của từng nhà phát hành model), không
chỉnh sửa gì khác, để đảm bảo so sánh công bằng giữa các model.

**Yêu cầu khi chạy:** mỗi notebook cần 1 Kaggle Dataset chứa file JSON
đề bài tương ứng (đường dẫn khai báo ở đầu mỗi notebook, tên biến
`DATA_PATH`/`DATA_DIR`/`MERGED_DATA_PATH` — sửa lại cho khớp dataset
bạn tự upload).
