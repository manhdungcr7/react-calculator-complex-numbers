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

## Appendix: 54 Problem Types (Complex Numbers)

Referenced as the Appendix in the paper submitted to SoICT 2026 (type codes D01–D54).

| Code | Type name (English) | Tên dạng (Tiếng Việt) |
|---|---|---|
| D01 | Given z = a+bi, find both the real part and the imaginary part of z | Cho số phức z = a+bi, tìm đồng thời phần thực và phần ảo của z |
| D02 | Given z = a+bi, find the real part of z | Cho số phức z = a+bi, tìm phần thực của z |
| D03 | Given z = a+bi, find the imaginary part of z | Cho số phức z = a+bi, tìm phần ảo của z |
| D04 | Given z = a+bi, find the real part and the imaginary part of its conjugate z-bar | Cho số phức z = a+bi, tìm phần thực và phần ảo của số phức liên hợp z̄ |
| D05 | Given two complex numbers z1, z2, find the real part of z1+z2 | Cho hai số phức z1, z2, tìm phần thực của tổng z1+z2 |
| D06 | Given two complex numbers z1, z2, find the imaginary part of z1 + conj(z2) | Cho hai số phức z1, z2, tìm phần ảo của z1 + z̄2 |
| D07 | Given two complex numbers, find the real part or the imaginary part of their product | Cho hai số phức, tìm phần thực hoặc phần ảo của tích của chúng |
| D08 | Given z, find the real part or the imaginary part of z^2 | Cho số phức z, tìm phần thực hoặc phần ảo của bình phương z² |
| D09 | Given the real part and the imaginary part, write the corresponding complex number | Cho phần thực và phần ảo, viết số phức tương ứng |
| D10 | Given several complex numbers, identify which ones are purely imaginary | Cho một số số phức, nhận biết số nào là số thuần ảo |
| D11 | Given z = a+bi, find its conjugate z-bar | Cho số phức z = a+bi, tìm số phức liên hợp z̄ |
| D12 | Given a complex number as an expression, find its conjugate z-bar | Cho số phức dưới dạng biểu thức, tìm số phức liên hợp z̄ |
| D13 | Given z = a+bi, compute the modulus |z| | Cho số phức z = a+bi, tính môđun |z| |
| D14 | Given two complex numbers, compute the modulus of their sum / difference | Cho hai số phức, tính môđun của tổng / hiệu của chúng |
| D15 | Compute the modulus of z given that z-bar equals the product of two complex numbers | Tính môđun của z khi biết z̄ bằng tích hai số phức |
| D16 | Compute the modulus of the product of a complex number with the conjugate of another (z * conj(w)) | Tính môđun của tích một số phức với liên hợp của số phức khác (z·w̄) |
| D17 | Compute the modulus of the product of two given complex numbers | Tính môđun của tích hai số phức cho trước |
| D18 | Given z = a+bi, find the coordinates of the point representing z | Cho số phức z = a+bi, tìm tọa độ điểm biểu diễn của z |
| D19 | Find the point representing z^2 | Tìm điểm biểu diễn của z² |
| D20 | Find the point representing w = iz | Tìm điểm biểu diễn của w = iz |
| D21 | Find the point representing a linear combination of two complex numbers (e.g., 2z1+z2) | Tìm điểm biểu diễn của một tổ hợp tuyến tính hai số phức (vd 2z₁+z₂) |
| D22 | Given the representing point M(p;q), find z | Cho điểm biểu diễn M(p;q), tìm số phức z |
| D23 | Given the representing point M(p;q), find the real part of z | Cho điểm biểu diễn M(p;q), tìm phần thực của z |
| D24 | Given two complex numbers, find their sum | Cho hai số phức, tìm tổng của chúng |
| D25 | Given two complex numbers, find their difference | Cho hai số phức, tìm hiệu của chúng |
| D26 | Given z and a real number k, compute the product k*z | Cho số phức z và số thực k, tính tích k·z |
| D27 | Given z, compute an expression combining several operations on z | Cho số phức z, tính một biểu thức phối hợp nhiều phép toán theo z |
| D28 | Solve a linear equation in z (containing only z or only z-bar), compute the modulus |z| | Giải phương trình bậc nhất ẩn z (chỉ chứa z hoặc z̄), tính môđun |z| |
| D29 | Solve a linear equation in z (containing only z or only z-bar), find the real part or the imaginary part of z | Giải phương trình bậc nhất ẩn z (chỉ chứa z hoặc z̄), tìm phần thực hoặc phần ảo của z |
| D30 | Solve a linear equation in z (containing only z or only z-bar), find the conjugate z-bar | Giải phương trình bậc nhất ẩn z (chỉ chứa z hoặc z̄), tìm số phức liên hợp z̄ |
| D31 | Given an equation containing both z and z-bar, solve for z then compute the sum of its real part and imaginary part | Cho phương trình chứa cả z và z̄, giải tìm z rồi tính tổng phần thực và phần ảo |
| D32 | Given an equation containing both z and z-bar, solve for z then compute the modulus |z| | Cho phương trình chứa cả z và z̄, giải tìm z rồi tính môđun |z| |
| D33 | Given an equation containing |z|, find z by matching real and imaginary parts | Cho phương trình chứa |z|, tìm z bằng cách đồng nhất phần thực, phần ảo |
| D34 | Given a circle condition and the condition that z^2 is purely imaginary, count the number of z satisfying both | Cho điều kiện đường tròn và điều kiện z² thuần ảo, đếm số số phức z thỏa mãn |
| D35 | Given a circle condition and the condition that z/(z-q) is purely imaginary, count the number of z satisfying both | Cho điều kiện đường tròn và điều kiện z/(z−q) thuần ảo, đếm số số phức z thỏa mãn |
| D36 | Given the condition |z|^2 = k|z+z-bar|+c and a perpendicular-bisector condition, count the number of z satisfying both | Cho điều kiện |z|²=k|z+z̄|+c và điều kiện đường trung trực, đếm số số phức z thỏa mãn |
| D37 | Given an equation with |z| in several places, set t=|z| and take the modulus of both sides to determine the interval containing |z| | Cho phương trình chứa |z| ở nhiều vị trí, đặt t=|z| và lấy môđun hai vế để xác định khoảng chứa |z| |
| D38 | Given an equation with |z| in several places, set t=|z| and take the modulus of both sides to count the number of z | Cho phương trình chứa |z| ở nhiều vị trí, đặt t=|z| và lấy môđun hai vế để đếm số số phức z |
| D39 | Given two conditions on the modulus and the conjugate, count the number of z satisfying both | Cho hai điều kiện về môđun và liên hợp, đếm số số phức z thỏa mãn |
| D40 | Given the condition |z-z0|=R, find the set of points representing z (a circle) | Cho điều kiện |z−z₀|=R, tìm tập hợp điểm biểu diễn z (đường tròn) |
| D41 | Given that a product is purely imaginary, find the center of the circle formed by the points representing z | Cho một tích là số thuần ảo, tìm tâm của đường tròn tập hợp điểm biểu diễn z |
| D42 | Given that a product is purely imaginary, find the radius of the circle formed by the points representing z | Cho một tích là số thuần ảo, tìm bán kính của đường tròn tập hợp điểm biểu diễn z |
| D43 | Given w = az+b with |z| fixed, find the set of points representing w (a circle) | Cho w = az+b và |z| không đổi, tìm tập hợp điểm biểu diễn của w (đường tròn) |
| D44 | Given w = (az+b)/(cz+d) with |z| fixed, find the set of points representing w (a circle) | Cho w = (az+b)/(cz+d) và |z| không đổi, tìm tập hợp điểm biểu diễn của w (đường tròn) |
| D45 | Given a quadratic equation with parameter m, count the values of m for which the two roots have equal modulus | Cho phương trình bậc hai một tham số m, đếm số giá trị m để hai nghiệm có môđun bằng nhau |
| D46 | Given a quadratic equation with parameter m, count the values of m for which the sum of the moduli of the two roots equals S | Cho phương trình bậc hai một tham số m, đếm số giá trị m để tổng môđun hai nghiệm bằng S |
| D47 | Given a quadratic equation with parameter m, count the values of m for which a root z0 with modulus R exists | Cho phương trình bậc hai một tham số m, đếm số giá trị m để tồn tại nghiệm z₀ có môđun R |
| D48 | Given a quadratic equation with two parameters, count the pairs of parameters satisfying a condition on the roots | Cho phương trình bậc hai hai tham số, đếm số cặp tham số thỏa điều kiện về nghiệm |
| D49 | Given two roots that are conjugate complex numbers, write the quadratic equation having them as roots | Cho hai nghiệm là hai số phức liên hợp, viết phương trình bậc hai nhận chúng làm nghiệm |
| D50 | Given that the point representing z lies on a line segment, find the maximum and minimum of a modulus | Cho z có điểm biểu diễn thuộc một đoạn thẳng, tìm GTLN, GTNN của một môđun |
| D51 | Given that z lies on a circle, find the maximum of the difference between two squared distances | Cho z thuộc một đường tròn, tìm GTLN của hiệu bình phương hai khoảng cách |
| D52 | Given the condition |z^2-C|=k*|z|, find the maximum and minimum of |z| | Cho điều kiện |z²−C|=k·|z|, tìm GTLN, GTNN của |z| |
| D53 | Given two complex numbers with fixed moduli, find the minimum of a modulus expression and use it to derive the requested quantity | Cho hai số phức có môđun cố định, tìm GTNN của một biểu thức môđun rồi suy ra đại lượng hỏi |
| D54 | Given three complex numbers satisfying a relation, compute the area of the triangle formed by the three representing points | Cho ba số phức thỏa một hệ thức, tính diện tích tam giác tạo bởi ba điểm biểu diễn |

Machine-readable version: [`problem_types_54.csv`](problem_types_54.csv).


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
