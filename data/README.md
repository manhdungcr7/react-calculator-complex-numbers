# Data

Dữ liệu dùng để đối chiếu số liệu trong bài báo: bộ câu hỏi ở
[`questions/`](questions/), kết quả giải chi tiết từng câu ở
[`results/`](results/) (tách theo từng thí nghiệm trong bài báo). Bộ câu hỏi
do [`../scripts/`](../scripts/) sinh ra; kết quả do notebook trong
[`../experiments/`](../experiments/) chạy ra.

## `questions/So_phuc_day_du.csv`

Toàn bộ bộ câu hỏi chuyên đề Số phức dùng trong nghiên cứu: 65 câu gốc trích
từ tài liệu ôn tập (cột `nguon` = "Câu gốc") và 4860 câu biến thể do nhóm
sinh thêm bằng cách đổi số liệu, giữ nguyên phương pháp giải (cột `nguon` =
"Nhân bản"), thuộc đúng 54 dạng (D01–D54) như trong bài báo (xem
[`../appendix/`](../appendix/)). Mỗi câu có đề bài đầy đủ (kèm 4 phương án
trắc nghiệm), đáp án đúng, và lời giải.

> **Ghi chú mã dạng:** dữ liệu gốc của nhóm có 55 dạng (D01–D55); dạng
> `D54` gốc (1 câu gốc + 90 câu biến thể) bị loại khỏi phạm vi nghiên cứu ở
> bước chọn dữ liệu, và `D55` được đánh số lại thành `D54` để khớp với bài
> báo. File này đã áp dụng đúng phép đổi số đó.

## `results/` - kết quả giải chi tiết từng câu, theo từng thí nghiệm

| Thư mục | Thí nghiệm trong bài báo | Nội dung |
|---|---|---|
| [`experiment1_65cau_khao_sat/`](results/experiment1_65cau_khao_sat/) | TN1 - Đánh giá tính thách thức của bộ dữ liệu | 65 câu gốc, giải bởi GPT-4o, Gemini-2.5-Flash, Qwen3-4B |
| [`experiment2_810cau_huong_dan_giai/`](results/experiment2_810cau_huong_dan_giai/) | TN2 - Đánh giá zero-shot có hướng dẫn giải | 810 câu (9 dạng khó nhất), Qwen3-4B, đối chiếu thiết lập cơ sở với có hướng dẫn giải |
| [`experiment3_4_react_calculator/`](results/experiment3_4_react_calculator/) | TN3 & TN4 - ReAct-Calculator trên Qwen3-4B và trên 2 SLM khác | 2160 câu (24 dạng khó nhất), 3 model, đối chiếu thiết lập cơ sở với ReAct-Calculator |

### `experiment1_65cau_khao_sat/65cau_khao_sat_GPT4o_Gemini_Qwen3-4B.csv`

Đề bài, đáp án đúng, lời giải và nhận xét của từng model, cùng cột
`*_ket_qua` (C/I/U = Correct/Incorrect/Undetermined) tổng hợp - khớp đúng số
liệu Bảng 4 của bài báo (GPT-4o 56/9/0, Gemini-2.5-Flash 65/0/0, Qwen3-4B
62/2/1).

### `experiment2_810cau_huong_dan_giai/810cau_zero_shot_vs_huong_dan_giai_Qwen3-4B.csv`

Qwen3-4B trên 810 câu thuộc 9 dạng khó nhất, đối chiếu thiết lập cơ sở
(`baseline_*`) với thiết lập có hướng dẫn giải (`guided_*`, kèm lời giải đầy
đủ) - khớp đúng Bảng 5 của bài báo (thiết lập cơ sở 234/21/555, có hướng dẫn
giải 665/11/134).

### `experiment3_4_react_calculator/<model>/`

Tách theo 3 model (`Qwen3-4B/`, `DeepSeek-R1-Distill-Qwen-1.5B/`,
`Llama-3.2-3B-Instruct/`); trong mỗi thư mục model, file đặt tên
`d<NN>_<thiet_lap>_full90.csv` - `<thiet_lap>` là `zeroshot` (thiết lập cơ
sở) hoặc `react_calculator` (ReAct-Calculator). Mỗi file gồm 90 câu (1
dạng), có cột đáp án model chọn, kết quả Đúng/Sai/KXĐ, và lời giải đầy đủ do
model sinh ra. Thư mục `Qwen3-4B/` chỉ có `react_calculator` (thiết lập cơ
sở của Qwen3-4B trên 24 dạng này đã có sẵn trong Bảng 4 của bài báo, không
lặp lại ở đây).
