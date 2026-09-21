# Data

## `questions/So_phuc_day_du.csv`

Toàn bộ bộ câu hỏi chuyên đề Số phức dùng trong nghiên cứu: 65 câu gốc trích
từ tài liệu ôn tập (cột `nguon` = "Câu gốc") và 4860 câu biến thể do nhóm
sinh thêm bằng cách đổi số liệu, giữ nguyên phương pháp giải (cột `nguon` =
"Nhân bản"), thuộc đúng 54 dạng (D01–D54) như trong bài báo. Mỗi câu có đề
bài đầy đủ (kèm 4 phương án trắc nghiệm), đáp án đúng, và lời giải. (Dữ liệu
gốc của nhóm có thêm 1 dạng — đánh số D54 trong dữ liệu gốc, chứa 1 câu gốc +
90 câu biến thể — bị loại khỏi phạm vi nghiên cứu ở bước chọn dữ liệu; file
này đã lược bỏ dạng đó và đổi số dạng kế tiếp từ D55 thành D54 để khớp với
bài báo.)

## `results/`

Kết quả giải từng câu, tách theo dạng bài (mã `d<NN>`, D01–D54 khớp với bài
báo), thiết lập (`zeroshot` = thiết lập cơ sở, `react_calculator` =
ReAct-Calculator), và mô hình (không có hậu tố tên model = Qwen3-4B; có hậu
tố `DeepSeek-R1-Distill-Qwen-1.5B` hoặc `Llama-3.2-3B-Instruct`). Mỗi file
gồm 90 câu (1 dạng), có cột đáp án model chọn, kết quả Đúng/Sai/KXĐ, và lời
giải đầy đủ do model sinh ra.

File [`65cau_khao_sat_GPT4o_Gemini_Qwen3-4B.csv`](results/65cau_khao_sat_GPT4o_Gemini_Qwen3-4B.csv)
là kết quả khảo sát 65 câu gốc trên GPT-4o, Gemini-2.5-Flash và Qwen3-4B
(Thí nghiệm 1), gồm đề bài, đáp án đúng, lời giải và nhận xét của từng model,
cùng cột `*_ket_qua` (C/I/U) tổng hợp — khớp đúng số liệu Bảng 4 của bài báo
(GPT-4o 56/9/0, Gemini-2.5-Flash 65/0/0, Qwen3-4B 62/2/1).

File [`810cau_zero_shot_vs_huong_dan_giai_Qwen3-4B.csv`](results/810cau_zero_shot_vs_huong_dan_giai_Qwen3-4B.csv)
là kết quả Qwen3-4B trên 810 câu thuộc 9 dạng khó nhất (Thí nghiệm 2), đối
chiếu thiết lập cơ sở (`baseline_*`) với thiết lập có hướng dẫn giải
(`guided_*`, kèm lời giải đầy đủ) — khớp đúng Bảng 5 của bài báo (thiết lập
cơ sở 234/21/555, có hướng dẫn giải 665/11/134).
