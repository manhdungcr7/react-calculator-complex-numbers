# Experiments

Notebook Kaggle (`.ipynb`) dùng để thử nghiệm phương pháp **ReAct +
Calculator** — model tự sinh `Thought` → `Action: Calculator` →
`Action Input: <biểu thức>`, một harness bên ngoài thực thi biểu thức bằng
backend sympy (chính xác tuyệt đối) rồi chèn `Observation: <kết quả thật>`
ngược lại để model tiếp tục, thay vì để model tự tính bằng token — trên 24
dạng bài số phức, đối chiếu với baseline **zero-shot** (không hướng dẫn,
không tool). Kết quả chi tiết từng câu nằm ở
[`../data/results/experiment3_4_react_calculator/`](../data/results/experiment3_4_react_calculator/),
tách theo cùng cấu trúc model bên dưới.

Repo chỉ up các notebook **thực sự dùng để chạy thử nghiệm** (không up
log/kết quả CSV trong notebook, không up các notebook nháp/debug 1-câu dùng
trong lúc phát triển prompt).

## `Qwen3-4B/` — model chính, 18 notebook (dùng làm chuẩn tham chiếu)

| File | Dạng bao gồm |
|---|---|
| `KLTN_D<NN>_ReAct_Calculator_full90.ipynb` (16 file: D04, D35–D39, D44–D48, D50–D53, D55) | Mỗi file 1 dạng, 90 câu |
| `KLTN_Nhom1_D04_D14_D28_D32_D33_full90.ipynb` | D04, D14, D28, D32, D33 (1 backend + 1 lần nạp model dùng chung cho cả 5 dạng) |
| `KLTN_Nhom2_D34_D40_D42_D45_D46_D49_full90.ipynb` | D34, D40, D42, D45, D46, D49 (dùng chung backend/model như Nhóm 1) |

Gộp lại, 2 file Nhóm phủ đủ 8 dạng còn thiếu (D14, D28, D32, D33, D34, D40,
D42, D49) mà 16 file lẻ ở trên không có — tổng cộng đủ **24/24 dạng**.
(Mã dạng `D55` trong notebook và dữ liệu tương ứng với `D54` trong bài báo —
xem ghi chú ở [`../data/README.md`](../data/README.md).)

## `DeepSeek-R1-Distill-Qwen-1.5B/` và `Llama-3.2-3B-Instruct/` — test chéo model

Mỗi model có 6 notebook, gộp theo lô 3 nhóm dạng (để chỉ cần nạp model 1 lần
cho nhiều dạng, tránh nạp lại nhiều lần gây lỗi hết bộ nhớ GPU) × 2 chế độ
(ReAct có Calculator / zero-shot không tool):

| Lô dạng | ReAct + Calculator | Zero-shot |
|---|---|---|
| D04, D38, D46, D51, D53 | `KLTN_5dang_ReAct_Calculator_full90_<model>.ipynb` | `KLTN_5dang_zeroshot_full90_<model>.ipynb` |
| D35, D36, D37, D39, D44, D45, D47, D48, D50, D52, D55 | `KLTN_11dang_ReAct_Calculator_full90_<model>.ipynb` | `KLTN_11dang_zeroshot_full90_<model>.ipynb` |
| D14, D28, D32, D33, D34, D40, D42, D49 | `KLTN_8dangMoi_ReAct_Calculator_full90_<model>.ipynb` | `KLTN_8dangMoi_zeroshot_full90_<model>.ipynb` |

(`<model>` = `DeepSeek-R1-Distill-Qwen-1.5B` hoặc `Llama-3.2-3B-Instruct`)

Prompt/phương pháp trong các file này **copy y hệt** bản Qwen3-4B đã kiểm
chứng — chỉ đổi tên model và tham số sinh (`temperature`/`top_p` theo đúng
khuyến nghị chính thức của từng nhà phát hành model), không chỉnh sửa gì
khác, để đảm bảo so sánh công bằng giữa các model.

## Yêu cầu khi chạy lại

Mỗi notebook cần 1 Kaggle Dataset chứa file JSON đề bài tương ứng (đường dẫn
khai báo ở đầu mỗi notebook, tên biến `DATA_PATH`/`DATA_DIR`/
`MERGED_DATA_PATH` — sửa lại cho khớp dataset bạn tự upload từ
[`../data/questions/`](../data/questions/)).
