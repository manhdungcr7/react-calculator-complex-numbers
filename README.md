# ReAct + Calculator cho Toán trắc nghiệm Số phức (SoICT 2026)

Repo đi kèm bài báo **"Improving Small Language Model Performance on
High-School Mathematics Using ReAct: A Case Study on Complex Numbers"**
(SoICT 2026): giúp một small language model (SLM) trả lời đúng toàn bộ câu
hỏi trắc nghiệm Toán trung học phổ thông, chuyên đề Số phức, bằng cách cho
model giải theo **ReAct** (xen kẽ lập luận và hành động) và giao phần tính
toán cho một **Calculator** ngoài thay vì để model tự tính bằng token.

## Appendix: 54 Problem Types (Complex Numbers)

Phụ lục của bài báo nộp SoICT 2026 (type codes D01–D54). Bản máy đọc được:
[`appendix/problem_types_54.csv`](appendix/problem_types_54.csv).

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

Repo gồm 4 phần, mỗi phần có README riêng giải thích chi tiết:

| Thư mục | Nội dung |
|---|---|
| [`appendix/`](appendix/) | **Phụ lục của bài báo**: 54 dạng bài Số phức (mã dạng D01–D54 + tên dạng, tiếng Anh và tiếng Việt) |
| [`data/`](data/) | **Dữ liệu**: bộ câu hỏi (gốc + biến thể) và kết quả giải chi tiết từng câu của các model, dùng để đối chiếu số liệu trong bài báo |
| [`scripts/`](scripts/) | **Script sinh dữ liệu**: chuyển đề bài từ PDF sang Markdown/LaTeX, và sinh thêm câu hỏi biến thể (đổi số liệu, giữ nguyên phương pháp giải) |
| [`experiments/`](experiments/) | **Notebook chạy thử nghiệm**: giải bằng ReAct+Calculator so với baseline zero-shot, trên 3 model (Qwen3-4B, DeepSeek-R1-Distill-Qwen-1.5B, Llama-3.2-3B-Instruct) |

## Tóm tắt quy trình

1. **Chọn bộ dữ liệu đánh giá** - trích câu hỏi Số phức từ một tài liệu ôn
   tập thật (`scripts/pdf_to_markdown/`), sinh thêm câu hỏi biến thể để mở
   rộng bộ dữ liệu (`scripts/generate_questions/`) → kết quả là bộ dữ liệu
   trong [`data/questions/`](data/questions/).
2. **Chọn loại prompt phù hợp** - thử từ prompt cơ sở (zero-shot) đến prompt
   có hướng dẫn giải, tìm ra những dạng bài mô hình còn giải sai.
3. **Cải tiến bằng ReAct-Calculator** - cho model giải theo ReAct, gọi
   Calculator để tính toán chính xác thay vì tự tính bằng token
   (`experiments/`) → kết quả chi tiết từng câu ở
   [`data/results/`](data/results/).
4. **Dùng lại prompt và quy trình trên 2 SLM khác** (DeepSeek-R1-Distill-
   Qwen-1.5B, Llama-3.2-3B-Instruct) để kiểm tra khả năng tái sử dụng.

Xem chi tiết từng bước trong README của thư mục tương ứng ở bảng trên.
